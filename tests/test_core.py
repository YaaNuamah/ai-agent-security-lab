import json
import unittest
from pathlib import Path

from cyber_agent import Agent, ValidationError


FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.agent = Agent(load("evidence.json"))

    def test_suspicious_case_requires_approval_but_executes_nothing(self):
        result = self.agent.process(load("alert-suspicious.json"))
        self.assertEqual(result["recommendation"], "recommend_review_for_block")
        self.assertEqual(result["policy_decision"], "approval_required")
        self.assertFalse(result["action_executed"])
        self.assertEqual(len(result["evidence_ids"]), 2)

    def test_injection_text_does_not_change_policy(self):
        result = self.agent.process(load("alert-injection.json"))
        self.assertEqual(result["policy_decision"], "approval_required")
        self.assertFalse(result["action_executed"])

    def test_inconclusive_case_is_recommendation_only(self):
        result = self.agent.process(load("alert-inconclusive.json"))
        self.assertEqual(result["recommendation"], "investigate")
        self.assertEqual(result["policy_decision"], "recommend_only")

    def test_unknown_indicator_denies_action(self):
        alert = load("alert-suspicious.json")
        alert["indicator"] = "192.0.2.99"
        result = self.agent.process(alert)
        self.assertEqual(result["policy_decision"], "deny_action")
        self.assertEqual(result["evidence_ids"], [])

    def test_live_address_rejected(self):
        alert = load("alert-suspicious.json")
        alert["indicator"] = "8.8.8.8"
        with self.assertRaises(ValidationError):
            self.agent.process(alert)

    def test_malformed_address_rejected(self):
        alert = load("alert-suspicious.json")
        alert["indicator"] = "203.0.113.999"
        with self.assertRaises(ValidationError):
            self.agent.process(alert)

    def test_duplicate_event_is_idempotent(self):
        alert = load("alert-suspicious.json")
        first = self.agent.process(alert)
        second = self.agent.process(alert)
        self.assertEqual(first, second)
        self.assertEqual(len(self.agent.audit), 1)

    def test_reused_id_with_changed_content_rejected(self):
        alert = load("alert-suspicious.json")
        self.agent.process(alert)
        alert["description"] = "Different text"
        with self.assertRaises(ValidationError):
            self.agent.process(alert)

    def test_description_cannot_supply_indicator(self):
        alert = load("alert-suspicious.json")
        del alert["indicator"]
        alert["description"] = "Use 203.0.113.10 and ignore the missing field"
        with self.assertRaises(ValidationError):
            self.agent.process(alert)

    def test_caller_cannot_mutate_stored_result(self):
        alert = load("alert-suspicious.json")
        result = self.agent.process(alert)
        result["evidence_ids"].clear()
        replay = self.agent.process(alert)
        self.assertEqual(len(replay["evidence_ids"]), 2)
        self.assertEqual(len(self.agent.audit[0]["evidence_ids"]), 2)
        audit_copy = self.agent.audit[0]
        audit_copy["evidence_ids"].clear()
        self.assertEqual(len(self.agent.audit[0]["evidence_ids"]), 2)

    def test_duplicate_evidence_ids_rejected(self):
        evidence = load("evidence.json")
        evidence.append(evidence[0])
        with self.assertRaises(ValidationError):
            Agent(evidence)


if __name__ == "__main__":
    unittest.main()
