#!/usr/bin/env python3
"""SLA risk for a ticket: how close is it to breaching its resolution target?

usage:
    python3 sla_risk.py --priority P2 --opened 2026-10-01T07:15:00Z [--now 2026-10-01T13:30:00Z]
    python3 sla_risk.py --json < request.json      # {"priority", "opened", "now" (optional)}

Prints one JSON object. --now defaults to the current time (UTC).
Time is calendar time: every minute between opened and now counts.
"""
import argparse
import json
import sys
from datetime import datetime, timezone

# resolution targets in minutes, calendar time
TARGETS = {"P1": 240, "P2": 480, "P3": 1440, "P4": 4320}


def _parse(ts):
    ts = ts.strip()
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def assess(priority, opened, now=None):
    priority = priority.upper()
    if priority not in TARGETS:
        raise ValueError("unknown priority %r, expected one of %s" % (priority, ", ".join(sorted(TARGETS))))
    opened_at = _parse(opened)
    now_at = _parse(now) if now else datetime.now(timezone.utc)
    target = TARGETS[priority]
    elapsed = int((now_at - opened_at).total_seconds() // 60)
    left = target - elapsed
    if left < 0:
        risk = "breached"
    elif left <= target * 0.25:
        risk = "high"
    elif left <= target * 0.5:
        risk = "medium"
    else:
        risk = "low"
    return {
        "priority": priority,
        "target_minutes": target,
        "elapsed_minutes": elapsed,
        "minutes_left": left,
        "risk": risk,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="SLA breach risk for one ticket")
    p.add_argument("--json", action="store_true", help="read {priority, opened, now} as JSON on standard input")
    p.add_argument("--priority", help="P1..P4")
    p.add_argument("--opened", help="when the ticket was opened, ISO 8601")
    p.add_argument("--now", help="evaluation time, ISO 8601 (default: current time)")
    a = p.parse_args(argv)
    try:
        if a.json:
            request = json.load(sys.stdin)
            if not isinstance(request, dict) or not request.get("priority") or not request.get("opened"):
                raise ValueError("the JSON request needs 'priority' and 'opened'")
            out = assess(request["priority"], request["opened"], request.get("now"))
        else:
            if not (a.priority and a.opened):
                raise ValueError("--priority and --opened are required (or use --json)")
            out = assess(a.priority, a.opened, a.now)
    except ValueError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
