"""Show triage, approval, and a mock action in one offline run."""

import json
from pathlib import Path

from .core import Agent
from .simulation import SimulationGateway


def main() -> None:
    fixtures = Path(__file__).resolve().parent.parent / "fixtures"
    evidence = json.loads((fixtures / "evidence.json").read_text(encoding="utf-8"))
    alert = json.loads((fixtures / "alert-injection.json").read_text(encoding="utf-8"))
    agent = Agent(evidence)
    decision = agent.process(alert)
    gateway = SimulationGateway(agent)
    proposed = gateway.propose(decision["event_id"], decision["indicator"], 60)
    # This label is deliberately not an authenticated user identity.
    token = gateway.approve(proposed.request_id, "demo_analyst")
    outcome = gateway.execute(proposed.request_id, token,
                              indicator=proposed.indicator,
                              duration_minutes=proposed.duration_minutes)
    print(json.dumps({"triage": decision, "simulated_outcome": outcome,
                      "gateway_audit": gateway.audit}, indent=2))


if __name__ == "__main__":
    main()
