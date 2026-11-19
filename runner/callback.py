"""Reports an auto-run's progress back to Station House (POST /api/agent/design/auto-runs/<id>).

Never fatal: a failed callback is logged and the run carries on. Skipped without an id or token.
"""

import json
import os
import urllib.request

UA = "marin-hunt-runner/1.0"  # Cloudflare answers 403 (error 1010) to Python's default User-Agent


def run_url(env=os.environ):
    if env.get("GITHUB_RUN_ID") and env.get("GITHUB_REPOSITORY"):
        server = env.get("GITHUB_SERVER_URL", "https://github.com")
        return f"{server}/{env['GITHUB_REPOSITORY']}/actions/runs/{env['GITHUB_RUN_ID']}"
    return None


def payload(state, detail="", actual_seconds=None, actual_usd=None, results=(), env=os.environ):
    return {
        "state": state,
        "ghRunUrl": run_url(env),
        "actualSeconds": actual_seconds,
        "actualUsd": actual_usd,
        "results": [dict(id=r["id"], outcome=r.get("outcome"), resultsPr=r.get("resultsPr")) for r in results],
        "detail": detail[:2000],
    }


def send(auto_run_id, body, env=os.environ, opener=urllib.request.urlopen):
    token = env.get("AUTO_RUN_CALLBACK_TOKEN")
    if not auto_run_id or not token:
        return False
    base = (env.get("PLATFORM_URL") or "https://app.station-house.net").rstrip("/")
    req = urllib.request.Request(
        f"{base}/api/agent/design/auto-runs/{auto_run_id}", data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "User-Agent": UA})
    try:
        with opener(req, timeout=20) as r:
            r.read()
        return True
    except Exception as e:  # noqa: BLE001 - a callback must never stop the run
        print(f"callback {body['state']} failed: {e}")
        return False
