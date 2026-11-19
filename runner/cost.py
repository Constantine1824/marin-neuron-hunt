"""Modal cost estimate for the daily batch (pick.py). Station House's shared experiment runner, which
auto-runs eligible request PRs, uses the same numbers in its template registry
(station-house-platform experiments/templates.json); change both together.

    est seconds(req) = passes(req) * S_PER_PASS;   batch cost = (STARTUP_S + sum of est seconds) * USD_PER_S
"""

# Modal H200 + 8 CPU + 128 GiB, USD per second (list price, Oct 2026), and rough timings for Marin 32B.
USD_PER_S = 0.00160
STARTUP_S = 240  # container start + loading 64 GB of weights
S_PER_PASS = 0.06  # one prompt of <= 512 tokens through all 64 layers, batched
BASELINE_PASSES = 101  # steering/ablation: the target plus 100 random neurons or sets


def passes(req):
    t = req["type"]
    if t == "activation-test":
        return len(req["should_fire"]) + len(req["should_not_fire"])
    if t == "contrast":
        return 2 * len(req["pairs"])
    if t in ("steering", "ablation"):
        return (BASELINE_PASSES + 1) * len(req["prompts"])
    return 0


def est_seconds(req):
    return passes(req) * S_PER_PASS
