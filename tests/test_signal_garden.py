import json
import unittest

from signal_garden import build_brief, main


class SignalGardenTests(unittest.TestCase):
    def test_build_brief_normalizes_goal_and_detects_risk(self):
        brief = build_brief("  ship   an auth   service ")

        self.assertEqual(brief.goal, "ship an auth service")
        self.assertEqual(brief.effort, "focused")
        self.assertTrue(any("Authentication" in risk for risk in brief.risks))
        self.assertEqual(len(brief.milestones), 4)

    def test_long_goals_are_marked_expanded(self):
        brief = build_brief(" ".join(["word"] * 13))

        self.assertEqual(brief.effort, "expanded")

    def test_empty_goal_is_rejected(self):
        with self.assertRaises(ValueError):
            build_brief("   ")

    def test_json_mode_is_machine_readable(self):
        from io import StringIO
        from contextlib import redirect_stdout

        output = StringIO()
        with redirect_stdout(output):
            exit_code = main(["make", "a", "demo", "--json"])

        self.assertEqual(exit_code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["goal"], "make a demo")
        self.assertEqual(len(payload["milestones"]), 4)


if __name__ == "__main__":
    unittest.main()
