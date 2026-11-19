"""Auto-run: one open request PR, picked by the Experimentation Wizard on Station House (CONTRIBUTING.md, "Auto-run").

Only data comes from the PR: the `requests/<id>.yaml` files it adds or changes, read as text at the given head
commit through the GitHub API and parsed with yaml.safe_load. Nothing from the PR is checked out, imported or run.
The PR is refused when its head moved, it isn't open, it changes anything but requests/<id>.yaml, a request fails
the schema, has a type other than the four templates, already has a result on main, or breaks the cost rule.
"""

import base64
import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from runner import cost, pick

REQUEST_PATH = re.compile(r"^requests/(L\d+-N\d+-\d{3})\.yaml$")


class Refused(Exception):
    pass


def request_validator(root=None):
    root = root or pick.ROOT
    schemas = {name: json.loads((root / "schema" / f"{name}.schema.json").read_text())
               for name in ("explanation", "request", "result")}
    registry = Registry().with_resources(
        (f"{name}.schema.json", Resource.from_contents(schema)) for name, schema in schemas.items())
    return Draft202012Validator(schemas["request"], registry=registry)


def gh_json(gh, *args):
    return json.loads(gh("gh", "api", *args))


def changed_files(gh, repo, pr):
    pages = gh_json(gh, "--paginate", "--slurp", f"repos/{repo}/pulls/{pr}/files?per_page=100")
    return [f for page in pages for f in page]


def load(gh, repo, pr, sha, cap_usd, root=None):
    """The PR's requests as pick.Pending items (commit = the PR head), or Refused naming every reason."""
    root = root or pick.ROOT
    info = gh_json(gh, f"repos/{repo}/pulls/{pr}")
    if info.get("state") != "open":
        raise Refused(f"PR #{pr} is {info.get('state')}, not open")
    head = info["head"]["sha"]
    if head != sha:
        raise Refused(f"PR #{pr} head moved: {head[:12]} is not {sha[:12]}")
    head_repo = (info["head"].get("repo") or {}).get("full_name") or repo

    files = changed_files(gh, repo, pr)
    if not files:
        raise Refused("the PR changes no files")
    bad = [f"{f['filename']} ({f['status']})" for f in files
           if not REQUEST_PATH.match(f["filename"]) or f["status"] not in ("added", "modified")]
    if bad:
        raise Refused("only added or modified requests/<id>.yaml files may change; the PR also changes "
                      + ", ".join(bad))

    check = request_validator(root)
    reasons, items = [], []
    for f in files:
        rid = REQUEST_PATH.match(f["filename"]).group(1)
        blob = gh_json(gh, f"repos/{head_repo}/contents/{f['filename']}?ref={sha}")
        try:
            req = yaml.safe_load(base64.b64decode(blob["content"]).decode())
        except (yaml.YAMLError, UnicodeDecodeError, ValueError) as e:
            reasons.append(f"{rid}: not readable YAML ({str(e)[:120]})")
            continue
        if not isinstance(req, dict):
            reasons.append(f"{rid}: not a mapping")
            continue
        if req.get("type") not in cost.AUTO_RUN_TYPES:
            reasons.append(f"{rid}: type {req.get('type')!r} is not auto-run (only {', '.join(cost.AUTO_RUN_TYPES)})")
            continue
        errors = sorted(check.iter_errors(req), key=lambda e: list(e.path))
        if errors:
            reasons.append(f"{rid}: schema: " + "; ".join(e.message[:120] for e in errors[:3]))
            continue
        if (root / "results" / f"{rid}.yaml").exists():
            reasons.append(f"{rid}: already has results/{rid}.yaml on main")
            continue
        items.append(pick.Pending(rid, Path(f["filename"]), req, 0, sha))
    if not reasons:
        reasons += cost.over_cap([i.request for i in items], cap_usd)
    if reasons:
        raise Refused("; ".join(reasons))
    return items


def note(auto_run_id):
    return f"Auto-run before review (Experimentation Wizard auto-run {auto_run_id})."


def timeout_s(cap_usd):
    """Modal function timeout for an auto-run: the time the cap buys, so a wrong estimate can't spend past it."""
    return max(cost.STARTUP_S + 60, int(cap_usd / cost.USD_PER_S))
