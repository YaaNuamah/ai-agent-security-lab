"""Offline suspicious-IP triage with no LLM or external integrations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from copy import deepcopy
from ipaddress import ip_address, ip_network
from typing import Any, Mapping

from .assessment import ModelAdapter, validate_assessment


class ValidationError(ValueError):
    """An alert or evidence fixture does not meet the lab contract."""


LAB_RANGES = (
    ip_network("192.0.2.0/24"),
    ip_network("198.51.100.0/24"),
    ip_network("203.0.113.0/24"),
)
ALLOWED_SOURCES = frozenset({"synthetic_siem", "synthetic_email", "manual_lab"})
ALLOWED_LABELS = frozenset({"malicious", "benign", "inconclusive"})


def _text(value: Any, field: str, maximum: int) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValidationError(f"{field} must be non-empty text of at most {maximum} characters")
    return value.strip()


def _lab_ip(value: Any) -> str:
    raw = _text(value, "indicator", 45)
    try:
        address = ip_address(raw)
    except ValueError as exc:
        raise ValidationError("indicator must be an IP address") from exc
    if not any(address in network for network in LAB_RANGES):
        raise ValidationError("indicator must be in a documentation-only lab range")
    return str(address)


@dataclass(frozen=True)
class Alert:
    event_id: str
    source: str
    indicator: str
    description: str

    @classmethod
    def parse(cls, raw: Mapping[str, Any]) -> "Alert":
        if not isinstance(raw, Mapping):
            raise ValidationError("alert must be an object")
        event_id = _text(raw.get("event_id"), "event_id", 80)
        source = _text(raw.get("source"), "source", 40)
        if source not in ALLOWED_SOURCES:
            raise ValidationError("source is not an allowed lab source")
        indicator = _lab_ip(raw.get("indicator"))
        description = _text(raw.get("description"), "description", 2000)
        return cls(event_id, source, indicator, description)


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    indicator: str
    source: str
    observed_at: str
    label: str
    summary: str

    @classmethod
    def parse(cls, raw: Mapping[str, Any]) -> "Evidence":
        if not isinstance(raw, Mapping):
            raise ValidationError("evidence must be an object")
        evidence_id = _text(raw.get("evidence_id"), "evidence_id", 80)
        indicator = _lab_ip(raw.get("indicator"))
        source = _text(raw.get("source"), "evidence source", 80)
        observed_at = _text(raw.get("observed_at"), "observed_at", 40)
        try:
            datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValidationError("observed_at must be ISO 8601") from exc
        label = _text(raw.get("label"), "label", 20)
        if label not in ALLOWED_LABELS:
            raise ValidationError("evidence label is invalid")
        summary = _text(raw.get("summary"), "summary", 500)
        return cls(evidence_id, indicator, source, observed_at, label, summary)


class Agent:
    """A one-process lab agent; repeated event IDs return the first result."""

    def __init__(self, evidence_rows: list[Mapping[str, Any]],
                 model_adapter: ModelAdapter | None = None):
        evidence = [Evidence.parse(row) for row in evidence_rows]
        ids = [row.evidence_id for row in evidence]
        if len(ids) != len(set(ids)):
            raise ValidationError("evidence IDs must be unique")
        evidence_by_indicator: dict[str, list[Evidence]] = {}
        for row in evidence:
            evidence_by_indicator.setdefault(row.indicator, []).append(row)
        self._evidence_by_indicator = {
            indicator: tuple(rows) for indicator, rows in evidence_by_indicator.items()
        }
        self._results: dict[str, dict[str, Any]] = {}
        self._fingerprints: dict[str, tuple[str, str, str]] = {}
        self._audit: list[dict[str, Any]] = []
        self._model_adapter = model_adapter

    @property
    def audit(self) -> tuple[dict[str, Any], ...]:
        return tuple(deepcopy(entry) for entry in self._audit)

    def result_for(self, event_id: str) -> dict[str, Any] | None:
        """Return a copy of a prior decision for the local simulation gateway."""
        result = self._results.get(event_id)
        return deepcopy(result) if result is not None else None

    def process(self, raw_alert: Mapping[str, Any]) -> dict[str, Any]:
        alert = Alert.parse(raw_alert)
        if alert.event_id in self._results:
            previous = self._results[alert.event_id]
            if (alert.source, alert.indicator, alert.description) != self._fingerprints[alert.event_id]:
                raise ValidationError("event_id was already used for different alert content")
            return deepcopy(previous)

        evidence = self._evidence_by_indicator.get(alert.indicator, ())
        malicious = [row for row in evidence if row.label == "malicious"]
        if not evidence:
            recommendation, policy = "insufficient_evidence", "deny_action"
            reason = "No local evidence exists for this indicator. Do not infer a verdict."
        elif len(malicious) >= 2:
            recommendation, policy = "recommend_review_for_block", "approval_required"
            reason = "At least two distinct synthetic evidence records are labelled malicious."
        else:
            recommendation, policy = "investigate", "recommend_only"
            reason = "Evidence does not meet the lab threshold for containment review."

        model_status = "not_configured"
        model_assessment = None
        if self._model_adapter is not None:
            try:
                raw_assessment = self._model_adapter.assess(
                    event_id=alert.event_id,
                    indicator=alert.indicator,
                    description=alert.description,
                    evidence=[{
                        "evidence_id": row.evidence_id,
                        "source": row.source,
                        "observed_at": row.observed_at,
                        "label": row.label,
                        "summary": row.summary,
                    } for row in evidence],
                )
                model_assessment = validate_assessment(
                    raw_assessment, indicator=alert.indicator,
                    available_evidence_ids={row.evidence_id for row in evidence},
                ).as_dict()
                model_status = "validated_assessment"
            except Exception:
                # Optional provider failure cannot change or authorize the policy decision.
                model_status = "unavailable_or_invalid"

        result = {
            "event_id": alert.event_id,
            "indicator": alert.indicator,
            "evidence_ids": [row.evidence_id for row in evidence],
            "recommendation": recommendation,
            "policy_decision": policy,
            "reason": reason,
            "model_status": model_status,
            "model_assessment": model_assessment,
            "action_executed": False,
        }
        self._results[alert.event_id] = result
        self._fingerprints[alert.event_id] = (alert.source, alert.indicator, alert.description)
        self._audit.append({
            "event_id": alert.event_id,
            "source": alert.source,
            "indicator": alert.indicator,
            "evidence_ids": result["evidence_ids"].copy(),
            "recommendation": recommendation,
            "policy_decision": policy,
            "model_status": model_status,
            "action_executed": False,
        })
        return deepcopy(result)
