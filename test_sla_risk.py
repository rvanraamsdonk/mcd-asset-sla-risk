import json
import subprocess
import sys
import unittest
from pathlib import Path

from sla_risk import assess

ROOT = Path(__file__).resolve().parent


class T(unittest.TestCase):
    def test_high(self):
        r = assess("P2", "2026-10-01T07:15:00Z", "2026-10-01T13:30:00Z")
        self.assertEqual((r["risk"], r["minutes_left"], r["target_minutes"]), ("high", 105, 480))

    def test_low(self):
        self.assertEqual(assess("p3", "2026-10-01T07:15:00Z", "2026-10-01T08:15:00Z")["risk"], "low")

    def test_medium(self):
        self.assertEqual(assess("P1", "2026-10-01T07:00:00Z", "2026-10-01T09:30:00Z")["risk"], "medium")

    def test_breached(self):
        self.assertEqual(assess("P1", "2026-10-01T07:00:00Z", "2026-10-01T12:00:00Z")["risk"], "breached")

    def test_bad_priority(self):
        with self.assertRaises(ValueError):
            assess("P9", "2026-10-01T07:00:00Z")

    def test_json_mode_matches_the_example(self):
        done = subprocess.run([sys.executable, "sla_risk.py", "--json"], cwd=str(ROOT), capture_output=True, text=True,
                              input=(ROOT / "examples" / "input.json").read_text(encoding="utf-8"))
        self.assertEqual(done.returncode, 0, done.stderr)
        expected = json.loads((ROOT / "examples" / "output.json").read_text(encoding="utf-8"))
        self.assertEqual(json.loads(done.stdout), expected)


if __name__ == "__main__":
    unittest.main()
