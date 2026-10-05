"""Run an offline lab fixture: python -m cyber_agent path/to/alert.json."""

import argparse
import json
from pathlib import Path

from .core import Agent, ValidationError


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the simulation-only IP triage prototype")
    parser.add_argument("alert", type=Path, help="path to a synthetic alert JSON file")
    args = parser.parse_args()
    fixtures = Path(__file__).resolve().parent.parent / "fixtures" / "evidence.json"
    try:
        evidence = json.loads(fixtures.read_text(encoding="utf-8"))
        alert = json.loads(args.alert.read_text(encoding="utf-8"))
        agent = Agent(evidence)
        print(json.dumps({"result": agent.process(alert), "audit": agent.audit}, indent=2))
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        parser.exit(2, f"Lab input error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
