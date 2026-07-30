import tempfile
import unittest
from pathlib import Path

import pause_score
import tracker


class SovereigntyEquationTests(unittest.TestCase):
    def test_authentic_delta_uses_cost_and_presence(self):
        self.assertAlmostEqual(tracker.calculate_delta(True, 0.5, 0.8), 0.008)

    def test_degraded_delta_is_asymmetric(self):
        self.assertAlmostEqual(tracker.calculate_delta(False, 0.5, 0.8), -0.02)

    def test_sigma_is_bounded(self):
        _, upper = tracker.calculate_sigma(0.999, True, 1, 1)
        _, lower = tracker.calculate_sigma(0.001, False, 1, 1)
        self.assertEqual(upper, 1.0)
        self.assertEqual(lower, 0.0)

    def test_scores_outside_unit_interval_are_rejected(self):
        for value in (-0.01, 1.01):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    tracker.calculate_delta(True, value)

    def test_sovereignty_entry_round_trip(self):
        entry = tracker.SovereigntyEntry(
            date="2026-07-29",
            thread="A loose thread",
            knot="One honest action",
            authentic=True,
            cost=0.4,
            presence=1.0,
            sigma_before=0.1,
            delta=0.008,
            sigma_after=0.108,
            human_witnessed=False,
            witness_note="",
            shadow="The next question",
            audit_note="Held steady",
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sovereignty.jsonl"
            tracker.append_entry(entry, path)
            self.assertEqual(tracker.load_entries(path), [entry])

    def test_degraded_entry_cannot_be_human_witnessed(self):
        with self.assertRaises(ValueError):
            tracker.SovereigntyEntry(
                date="2026-07-29",
                thread="A loose thread",
                knot="A degraded action",
                authentic=False,
                cost=0.4,
                presence=1.0,
                sigma_before=0.1,
                delta=-0.02,
                sigma_after=0.08,
                human_witnessed=True,
                witness_note="Recognition",
                shadow="The next question",
                audit_note="",
            )


class PauseScoreTests(unittest.TestCase):
    def test_pause_score_percentage(self):
        self.assertEqual(pause_score.calculate_pause_score(4, 3), 75.0)
        self.assertEqual(pause_score.calculate_pause_score(0, 0), 0.0)

    def test_invalid_counts_are_rejected(self):
        for hooks, pauses in [(-1, 0), (1, -1), (2, 3), (True, False), (2.5, 1)]:
            with self.subTest(hooks=hooks, pauses=pauses):
                with self.assertRaises(ValueError):
                    pause_score.calculate_pause_score(hooks, pauses)

    def test_pause_entry_round_trip(self):
        entry = pause_score.PauseEntry("2026-07-29", 5, 4, 80.0, "Caught the hook")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pause.jsonl"
            pause_score.append_entry(entry, path)
            self.assertEqual(pause_score.load_entries(path), [entry])

    def test_pause_entry_rejects_inconsistent_score(self):
        with self.assertRaises(ValueError):
            pause_score.PauseEntry("2026-07-29", 5, 4, 70.0, "")


if __name__ == "__main__":
    unittest.main()
