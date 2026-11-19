"""Picks today's batch: requests on main with no result yet, oldest merge first, up to the compute cap."""

import subprocess
from dataclasses import dataclass
from pathlib import Path

import yaml

from runner.cost import BASELINE_PASSES, S_PER_PASS, STARTUP_S, USD_PER_S, est_seconds, passes  # noqa: F401

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Pending:
    id: str
    path: Path
    request: dict
    added_at: int  # unix time of the commit that added the file
    commit: str


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True).stdout


def first_added(path):
    lines = git("log", "--diff-filter=A", "--format=%ct %H", "--", str(path.relative_to(ROOT))).split()
    return (int(lines[-2]), lines[-1]) if lines else (0, "")


def pending(exclude=(), rerun=()):
    """Requests with no result yet, plus any in `rerun` (whose result a new results PR will replace)."""
    done = {p.stem for p in (ROOT / "results").glob("*.yaml")} - set(rerun)
    out = []
    for path in sorted((ROOT / "requests").glob("*.yaml")):
        if path.stem in done or path.stem in exclude:
            continue
        added_at, commit = first_added(path)
        out.append(Pending(path.stem, path, yaml.safe_load(path.read_text()), added_at, commit))
    return sorted(out, key=lambda p: (p.added_at, p.id))


def batch(items, cap_usd):
    """Split into (run today, custom for a maintainer, over the cap and left for tomorrow)."""
    run, custom, later = [], [], []
    budget = cap_usd / USD_PER_S - STARTUP_S
    for item in items:
        if item.request.get("type") == "custom":
            custom.append(item)
        elif est_seconds(item.request) <= budget and not later:
            run.append(item)
            budget -= est_seconds(item.request)
        else:
            later.append(item)
    return run, custom, later


def est_cost(items):
    return (STARTUP_S + sum(est_seconds(i.request) for i in items)) * USD_PER_S if items else 0.0
