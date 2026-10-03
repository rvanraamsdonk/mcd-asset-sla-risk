import unittest

from sla_risk import assess


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


if __name__ == "__main__":
    unittest.main()
