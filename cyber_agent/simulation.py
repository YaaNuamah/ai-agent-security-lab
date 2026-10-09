"""In-memory, simulation-only approval and tool gateway for the lab."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hmac import compare_digest
from secrets import token_urlsafe
from typing import Callable

from .core import Agent, ValidationError, _lab_ip, _text


class AuthorizationError(ValueError):
    """A simulated action is not authorized."""


@dataclass(frozen=True)
class ProposedAction:
    request_id: str
    event_id: str
    tool: str
    indicator: str
    duration_minutes: int
    expires_at: datetime


class SimulationGateway:
    """A narrow mock tool; it cannot connect to or modify a firewall.

    The approver name is a lab label, not an authenticated identity. This class
    demonstrates action binding, expiry, and one-time use; it is not production
    authorization or a durable audit store.
    """

    TOOL = "simulate_block_ip"

    def __init__(self, agent: Agent, clock: Callable[[], datetime] | None = None):
        self._agent = agent
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._requests: dict[str, ProposedAction] = {}
        self._approvals: dict[str, tuple[str, str]] = {}
        self._used: set[str] = set()
        self._audit: list[dict[str, object]] = []

    @property
    def audit(self) -> tuple[dict[str, object], ...]:
        return tuple(entry.copy() for entry in self._audit)

    def propose(self, event_id: str, indicator: str, duration_minutes: int, *, tool: str = TOOL) -> ProposedAction:
        if tool != self.TOOL:
            raise AuthorizationError("tool is not on the simulation allowlist")
        if type(duration_minutes) is not int or not 1 <= duration_minutes <= 1440:
            raise ValidationError("duration_minutes must be an integer from 1 to 1440")
        indicator = _lab_ip(indicator)
        result = self._agent.result_for(event_id)
        if result is None or result["policy_decision"] != "approval_required":
            raise AuthorizationError("event is not eligible for a containment simulation")
        if indicator != result["indicator"]:
            raise AuthorizationError("indicator differs from the triaged event")
        request_id = token_urlsafe(18)
        proposed = ProposedAction(request_id, event_id, tool, indicator, duration_minutes,
                                  self._clock() + timedelta(minutes=5))
        self._requests[request_id] = proposed
        self._audit.append({"event_id": event_id, "request_id": request_id,
                            "event": "proposed", "tool": tool, "indicator": indicator,
                            "duration_minutes": duration_minutes})
        return proposed

    def approve(self, request_id: str, approver: str) -> str:
        proposed = self._valid_request(request_id)
        approver = _text(approver, "approver", 80)
        if request_id in self._approvals:
            raise AuthorizationError("request already approved")
        token = token_urlsafe(32)
        self._approvals[request_id] = (token, approver)
        self._audit.append({"event_id": proposed.event_id, "request_id": request_id,
                            "event": "approved", "approver": approver})
        return token

    def execute(self, request_id: str, token: str, *, indicator: str,
                duration_minutes: int, tool: str = TOOL) -> dict[str, object]:
        proposed = self._valid_request(request_id)
        approval = self._approvals.get(request_id)
        if approval is None or not isinstance(token, str) or not compare_digest(token, approval[0]):
            raise AuthorizationError("valid approval token required")
        if (tool, indicator, duration_minutes) != (
            proposed.tool, proposed.indicator, proposed.duration_minutes
        ):
            raise AuthorizationError("action parameters differ from approved request")
        current = self._agent.result_for(proposed.event_id)
        if current is None or current["policy_decision"] != "approval_required":
            raise AuthorizationError("event policy no longer permits simulation")
        self._used.add(request_id)
        outcome = {"request_id": request_id, "event_id": proposed.event_id,
                   "tool": self.TOOL, "indicator": proposed.indicator,
                   "duration_minutes": proposed.duration_minutes,
                   "status": "simulated", "real_action_executed": False}
        self._audit.append({"event_id": proposed.event_id, "request_id": request_id,
                            "event": "simulated", "real_action_executed": False})
        return outcome

    def _valid_request(self, request_id: str) -> ProposedAction:
        proposed = self._requests.get(request_id)
        if proposed is None:
            raise AuthorizationError("unknown request")
        if request_id in self._used:
            raise AuthorizationError("request already used")
        if self._clock() >= proposed.expires_at:
            raise AuthorizationError("request expired")
        return proposed
