# SLA Risk Agent

Dummy asset for the marketplace composition demonstrator. Listed as **AMS-003** in the (fictional) AMS Asset Exchange.

Tells you how close a ticket is to breaching its resolution target. Time is **calendar time**: every minute between opened and now counts, nights and weekends included.

    python3 sla_risk.py --priority P2 --opened 2026-10-01T07:15:00Z
    python3 sla_risk.py --json < examples/input.json

- **Manifest (since 1.0.0):** `asset.manifest.json`.
- **Check:** `python3 -m unittest test_sla_risk`

Questions: priya.nair@firm.example

Everything here is fictional: the people, the marketplace and the data.
