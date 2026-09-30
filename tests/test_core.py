import unittest
from pilot_planner.core import build_raw_baseline_message, build_structured_messages, score_plan, validate_input

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.payload = {"industry":"retail","use_case":"draft replies","target_user":"3 staff","duration_weeks":2,"pain_point":"slow replies","constraint":"no PII","start_date":"2026-10-12"}

    def test_valid_payload(self):
        self.assertEqual(validate_input(self.payload), [])
        self.assertEqual(len(build_structured_messages(self.payload)), 2)

    def test_score_complete_plan(self):
        plan = {"test_group":"3 staff","stages":[{"date_or_deadline":"2026-10-12","task":"start"}],"success_metric":"80%","feedback_instrument":"weekly survey","human_approval_checkpoint":"manager signs off"}
        self.assertEqual(score_plan(plan)["total"], 5)

    def test_raw_baseline_has_no_system_message(self):
        messages = build_raw_baseline_message(self.payload)
        self.assertEqual([m["role"] for m in messages], ["user"])

if __name__ == "__main__":
    unittest.main()
