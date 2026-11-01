from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
import unittest
from unittest import mock

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
        output = StringIO()
        with redirect_stdout(output):
            exit_code = main(["make", "a", "demo", "--json"])

        self.assertEqual(exit_code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["goal"], "make a demo")
        self.assertEqual(len(payload["milestones"]), 4)

    def test_title_preserves_acronyms_and_special_casing(self):
        brief = build_brief("build a REST API with OAuth2 and PostgreSQL")
        self.assertEqual(brief.title, "Build a REST API with OAuth2 and PostgreSQL")

    def test_expanded_risk_taxonomy(self):
        brief = build_brief("create a parallel database sync with network retries and privacy checks")
        self.assertTrue(any("Network" in risk for risk in brief.risks))
        self.assertTrue(any("Concurrent" in risk for risk in brief.risks))
        self.assertTrue(any("persistence" in risk for risk in brief.risks))
        self.assertTrue(any("sensitive" in risk for risk in brief.risks))

    def test_domain_aware_milestone_tailoring(self):
        brief = build_brief("implement an auth and payment gateway")
        self.assertEqual(len(brief.milestones), 4)
        # Should incorporate domain-specific guidance
        self.assertTrue(any("auth" in m.lower() or "boundary" in m.lower() for m in brief.milestones))
        self.assertTrue(any("payment" in m.lower() or "idempotent" in m.lower() for m in brief.milestones))

    def test_markdown_mode_formatting(self):
        output = StringIO()
        with redirect_stdout(output):
            exit_code = main(["deploy", "auth", "service", "--markdown"])

        self.assertEqual(exit_code, 0)
        text = output.getvalue()
        self.assertIn("# Deploy auth service", text)
        self.assertIn("### 🎯 Milestones", text)
        self.assertIn("- [ ]", text)
        self.assertIn("### ⚠️ Identified Risks", text)

    def test_aikit_checkpoint_export(self):
        output = StringIO()
        with redirect_stdout(output):
            exit_code = main(["harden", "auth", "layer", "--aikit", "--task-id", "auth-task-1"])

        self.assertEqual(exit_code, 0)
        cmd = output.getvalue()
        self.assertIn("python aikit.py checkpoint", cmd)
        self.assertIn("--task auth-task-1", cmd)
        self.assertIn("--phase-num 2", cmd)
        self.assertIn("--risks", cmd)
        self.assertIn("--mitigation", cmd)

    def test_stdin_pipe_support(self):
        output = StringIO()
        with mock.patch("sys.stdin", StringIO("build offline analytics pipeline\n")):
            with redirect_stdout(output):
                exit_code = main(["-", "--json"])

        self.assertEqual(exit_code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["goal"], "build offline analytics pipeline")

    def test_goal_length_bound(self):
        huge_goal = "word " * 3000
        with self.assertRaises(ValueError) as ctx:
            build_brief(huge_goal)
        self.assertIn("exceeds maximum allowed length", str(ctx.exception))

    def test_error_triad_output_on_invalid_goal(self):
        stderr = StringIO()
        with redirect_stderr(stderr):
            exit_code = main(["   "])

        self.assertEqual(exit_code, 2)
        err_text = stderr.getvalue()
        self.assertIn("Error:", err_text)
        self.assertIn("Why:", err_text)
        self.assertIn("Fix:", err_text)


if __name__ == "__main__":
    unittest.main()
