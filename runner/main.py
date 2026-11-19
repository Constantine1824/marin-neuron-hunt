"""Daily runner entry point.

    python -m runner.main --dry-run                 # what would run today, cost estimate, prompt check (CPU)
    python -m runner.main                           # run today's batch on Modal, write results/ locally
    python -m runner.main --publish                 # ... then open one results PR per request and link it from
                                                    #     the request's PR and the explanation PR
    python -m runner.main --only L0-N10657-001      # just one pending request
    python -m runner.main --only L0-N10657-001 --rerun --publish   # rerun one; a new results PR replaces its file
    python -m runner.main --request-file x.yaml [y.yaml ...] --out dir/   # unmerged requests, results to dir/
    python -m runner.main --pr 170 --sha <head> --auto-run-id ar_x --publish   # auto-run one open request PR
                                                    #     (Station House picked it; see runner/autorun.py)
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import yaml

from runner import autorun, callback, pick, publish, report
from runner.prompts import check, load_tokenizer

REPO = os.environ.get("GITHUB_REPOSITORY", "Station-House/marin-neuron-hunt")


def sh(*args, **kw):
    return subprocess.run(args, check=True, capture_output=True, text=True, cwd=pick.ROOT, **kw).stdout


def in_open_results_prs():
    """Requests already answered in a results PR that hasn't merged yet."""
    prs = json.loads(sh("gh", "pr", "list", "-R", REPO, "--state", "open", "--limit", "100",
                        "--json", "headRefName,files"))
    return {Path(f["path"]).stem for pr in prs if pr["headRefName"].startswith("results-")
            for f in pr["files"] if f["path"].startswith("results/")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--rerun", action="store_true", help="with --only: run it again even if it has a result")
    ap.add_argument("--cap-usd", type=float, default=float(os.environ.get("RUNNER_CAP_USD", 10)))
    ap.add_argument("--request-file", type=Path, nargs="+")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--pr", type=int, help="auto-run: the open request PR")
    ap.add_argument("--sha", default="", help="with --pr: the head commit Station House checked")
    ap.add_argument("--auto-run-id", default="", help="with --pr: Station House's auto-run id, for callbacks")
    a = ap.parse_args()
    if a.rerun and not a.only:
        ap.error("--rerun needs --only <request id>")
    if a.pr and not a.sha:
        ap.error("--pr needs --sha <head commit>")

    def report_back(state, detail="", **kw):
        if a.pr:
            callback.send(a.auto_run_id, callback.payload(state, detail, **kw))

    if a.pr:
        try:
            items = autorun.load(sh, REPO, a.pr, a.sha, a.cap_usd)
        except autorun.Refused as e:
            print(f"refused: {e}")
            report_back("refused", str(e))
            return 0
        custom, later = [], []
        os.environ["RUNNER_TIMEOUT_S"] = str(autorun.timeout_s(a.cap_usd))
    elif a.request_file:
        items = [pick.Pending(f.stem, f, yaml.safe_load(f.read_text()), 0, "") for f in a.request_file]
        custom, later = [], []
        a.publish = False
    else:
        exclude = in_open_results_prs() if a.publish or os.environ.get("GITHUB_ACTIONS") else set()
        rerun = {a.only} if a.rerun else set()
        queue = [p for p in pick.pending(exclude - rerun, rerun) if not a.only or p.id == a.only]
        items, custom, later = pick.batch(queue, a.cap_usd)

    print(f"run: {len(items)}, custom (maintainer): {len(custom)}, over cap: {len(later)}, "
          f"est. ${pick.est_cost(items):.2f}")
    for label, group in (("run", items), ("custom", custom), ("later", later)):
        for p in group:
            print(f"  {label:6s} {p.id} {p.request['type']} ~{pick.est_seconds(p.request):.0f}s")
    if a.dry_run:
        tok = load_tokenizer()
        bad = 0
        for p in items:
            for problem in check(tok, p.request):
                bad += 1
                print(f"  {p.id}: {problem}")
        print("prompt check:", "OK" if not bad else f"{bad} problem(s); those requests will come back inconclusive")
        report_back("done", f"dry run, nothing ran on Modal; est ${pick.est_cost(items):.2f}; prompt problems: {bad}")
        return 0
    if not items:
        return 0

    import modal

    from runner.modal_app import app, run_batch

    payload = [dict(id=p.id, request=p.request, commit=p.commit) for p in items]
    report_back("running", f"{len(items)} request(s), est ${pick.est_cost(items):.2f}")
    t0 = time.time()
    try:
        with modal.enable_output(), app.run():
            results = run_batch.remote(payload)
    except Exception as e:
        wall = time.time() - t0
        report_back("failed", f"Modal run failed: {str(e)[:500]}", actual_seconds=wall, actual_usd=wall * pick.USD_PER_S)
        raise
    wall = time.time() - t0

    runner_commit = sh("git", "rev-parse", "HEAD").strip()
    date = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    out = a.out or pick.ROOT / "results"
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for item, res in zip(payload, results):
        rec = report.record(item, res, runner_commit, date, res.get("gpu", "?"))
        (out / f"{item['id']}.yaml").write_text(report.dump(rec))
        if a.request_file:
            (out / f"{item['id']}.comment.md").write_text(report.comment(rec))
        print(f"{item['id']}: {rec['outcome']}" + (f" ({rec['reason'][:200]})" if rec["reason"] else ""))
        records.append(rec)
    urls, failures = {}, []
    if a.publish:
        urls, failures = publish.publish(records, note=autorun.note(a.auto_run_id) if a.pr else None)
        if failures:
            print(f"{len(failures)} of {len(records)} results PRs failed:", *failures, sep="\n  ")
    report_back("failed" if failures else "done", "; ".join(failures) or f"{len(records)} result(s)",
                actual_seconds=wall, actual_usd=wall * pick.USD_PER_S,
                results=[dict(id=r["request"], outcome=r["outcome"], resultsPr=urls.get(r["request"])) for r in records])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
