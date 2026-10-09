import json
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cyber_agent import Agent, ValidationError
from cyber_agent.simulation import AuthorizationError, SimulationGateway


FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class SimulationTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.agent = Agent(load("evidence.json"))
        self.agent.process(load("alert-suspicious.json"))
        self.gateway = SimulationGateway(self.agent, clock=lambda: self.now)

    def propose(self):
        return self.gateway.propose("lab-alert-001", "203.0.113.10", 60)

    def test_approved_exact_action_is_only_simulated(self):
        request = self.propose()
        token = self.gateway.approve(request.request_id, "lab_analyst")
        result = self.gateway.execute(request.request_id, token,
                                      indicator="203.0.113.10", duration_minutes=60)
        self.assertEqual(result["status"], "simulated")
        self.assertFalse(result["real_action_executed"])
        self.assertEqual([row["event"] for row in self.gateway.audit],
                         ["proposed", "approved", "simulated"])

    def test_unapproved_action_denied(self):
        request = self.propose()
        with self.assertRaises(AuthorizationError):
            self.gateway.execute(request.request_id, "bad-token",
                                 indicator="203.0.113.10", duration_minutes=60)

    def test_changed_parameters_denied(self):
        request = self.propose()
        token = self.gateway.approve(request.request_id, "lab_analyst")
        with self.assertRaises(AuthorizationError):
            self.gateway.execute(request.request_id, token,
                                 indicator="203.0.113.11", duration_minutes=60)
        with self.assertRaises(AuthorizationError):
            self.gateway.execute(request.request_id, token,
                                 indicator="203.0.113.10", duration_minutes=120)

    def test_expiry_denies_action(self):
        request = self.propose()
        token = self.gateway.approve(request.request_id, "lab_analyst")
        self.now += timedelta(minutes=5)
        with self.assertRaises(AuthorizationError):
            self.gateway.execute(request.request_id, token,
                                 indicator="203.0.113.10", duration_minutes=60)

    def test_replay_denied(self):
        request = self.propose()
        token = self.gateway.approve(request.request_id, "lab_analyst")
        self.gateway.execute(request.request_id, token,
                             indicator="203.0.113.10", duration_minutes=60)
        with self.assertRaises(AuthorizationError):
            self.gateway.execute(request.request_id, token,
                                 indicator="203.0.113.10", duration_minutes=60)

    def test_unknown_tool_and_other_event_denied(self):
        with self.assertRaises(AuthorizationError):
            self.gateway.propose("lab-alert-001", "203.0.113.10", 60, tool="shell")
        with self.assertRaises(AuthorizationError):
            self.gateway.propose("unknown", "203.0.113.10", 60)
        self.agent.process(load("alert-inconclusive.json"))
        with self.assertRaises(AuthorizationError):
            self.gateway.propose("lab-alert-003", "198.51.100.20", 60)

    def test_wrong_indicator_and_invalid_duration_denied(self):
        with self.assertRaises(AuthorizationError):
            self.gateway.propose("lab-alert-001", "203.0.113.11", 60)
        with self.assertRaises(ValidationError):
            self.gateway.propose("lab-alert-001", "203.0.113.10", True)
        with self.assertRaises(ValidationError):
            self.gateway.propose("lab-alert-001", "203.0.113.10", 1441)


if __name__ == "__main__":
    unittest.main()
