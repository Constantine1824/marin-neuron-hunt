"""Modal cost estimate for requests, shared by the daily batch and auto-run (and mirrored by the platform,
which reads runner/cost_fixtures.json to stay in step).

    est_usd(req)    = (STARTUP_S + passes(req) * S_PER_PASS) * USD_PER_S       one request on its own
    total_usd(reqs) = (STARTUP_S + sum(passes) * S_PER_PASS) * USD_PER_S       one container for all of them
"""

# Modal H200 + 8 CPU + 128 GiB, USD per second (list price, Oct 2026), and rough timings for Marin 32B.
USD_PER_S = 0.00160
STARTUP_S = 240  # container start + loading 64 GB of weights
S_PER_PASS = 0.06  # one prompt of <= 512 tokens through all 64 layers, batched
BASELINE_PASSES = 101  # steering/ablation: the target plus 100 random neurons or sets

AUTO_RUN_TYPES = ("activation-test", "contrast", "steering", "ablation")


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


def est_usd(req):
    return (STARTUP_S + est_seconds(req)) * USD_PER_S


def total_usd(reqs):
    reqs = list(reqs)
    return (STARTUP_S + sum(est_seconds(r) for r in reqs)) * USD_PER_S if reqs else 0.0


def over_cap(reqs, cap_usd):
    """Reasons the requests break the auto-run cost rule (each one, and all together, under the cap)."""
    reqs = list(reqs)
    out = [f"request {i + 1} est ${est_usd(r):.2f} >= ${cap_usd:.2f}" for i, r in enumerate(reqs) if est_usd(r) >= cap_usd]
    if total_usd(reqs) >= cap_usd:
        out.append(f"total est ${total_usd(reqs):.2f} >= ${cap_usd:.2f}")
    return out
