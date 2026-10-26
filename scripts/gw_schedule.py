"""FPL gameweek helpers for the auto-run workflow.

  python scripts/gw_schedule.py generate   # rewrite .github/gw_schedule.json + print cron lines
  python scripts/gw_schedule.py latest     # print the latest gameweek FPL has finished AND data-checked
"""
import json, sys, urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = "https://fantasy.premierleague.com/api"
SCHEDULE = Path(__file__).resolve().parent.parent / ".github" / "gw_schedule.json"
RUN_HOURS_UTC = (9, 21)   # two attempts, next day after the last kickoff (FPL data_checked lags the final whistle)


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def generate():
    last_kickoff = defaultdict(list)
    for f in get_json(f"{API}/fixtures/"):
        if f["event"] and f["kickoff_time"]:
            last_kickoff[f["event"]].append(f["kickoff_time"])
    out = []
    for gw in sorted(last_kickoff):
        last = datetime.fromisoformat(max(last_kickoff[gw]).replace("Z", "+00:00"))
        day = (last + timedelta(days=1)).date()
        out.append({"gw": gw, "last_kickoff": last.isoformat(),
                    "runs": [datetime(day.year, day.month, day.day, h, tzinfo=timezone.utc).isoformat()
                             for h in RUN_HOURS_UTC]})
    SCHEDULE.write_text(json.dumps(out, indent=2) + "\n")
    for e in out:
        d = datetime.fromisoformat(e["runs"][0])
        print(f"    - cron: '0 {','.join(map(str, RUN_HOURS_UTC))} {d.day} {d.month} *'  # GW{e['gw']}")


def latest():
    done = [e["id"] for e in get_json(f"{API}/bootstrap-static/")["events"]
            if e["finished"] and e["data_checked"]]
    print(max(done) if done else "")


if __name__ == "__main__":
    {"generate": generate, "latest": latest}[sys.argv[1]]()
