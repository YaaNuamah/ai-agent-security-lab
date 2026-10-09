import json
import unittest
from pathlib import Path

from cyber_agent import Agent
from cyber_agent.assessment import ModelOutputError, RecordedAdapter, validate_assessment


FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class BrokenAdapter:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error

    def assess(self, **kwargs):
        if self.error:
            raise self.error
        return self.response


class AssessmentTests(unittest.TestCase):
    def test_recorded_output_is_visible_but_not_authority(self):
        agent = Agent(load("evidence.json"), RecordedAdapter(load("recorded-assessments.json")))
        result = agent.process(load("alert-inconclusive.json"))
        self.assertEqual(result["model_status"], "validated_assessment")
        self.assertEqual(result["model_assessment"]["suggested_action"], "review_block")
        self.assertEqual(result["policy_decision"], "recommend_only")
        self.assertFalse(result["action_executed"])

    def test_invalid_and_unavailable_outputs_fail_safely(self):
        alert = load("alert-suspicious.json")
        for adapter in (BrokenAdapter(response={"suggested_action": "review_block"}),
                        BrokenAdapter(error=TimeoutError("offline"))):
            with self.subTest(adapter=adapter):
                result = Agent(load("evidence.json"), adapter).process(alert)
                self.assertEqual(result["model_status"], "unavailable_or_invalid")
                self.assertIsNone(result["model_assessment"])
                self.assertEqual(result["policy_decision"], "approval_required")
                self.assertFalse(result["action_executed"])

    def test_response_cannot_cite_unknown_evidence(self):
        response = load("recorded-assessments.json")["lab-alert-001"]
        response["evidence_ids"] = ["invented-record"]
        with self.assertRaises(ModelOutputError):
            validate_assessment(response, indicator="203.0.113.10",
                                available_evidence_ids={"ev-siem-001", "ev-intel-001"})

    def test_response_cannot_change_indicator(self):
        response = load("recorded-assessments.json")["lab-alert-001"]
        response["indicator"] = "203.0.113.11"
        with self.assertRaises(ModelOutputError):
            validate_assessment(response, indicator="203.0.113.10",
                                available_evidence_ids={"ev-siem-001", "ev-intel-001"})


if __name__ == "__main__":
    unittest.main()
