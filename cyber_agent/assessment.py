"""Replaceable assessment boundary; recorded responses are not live AI."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Any, Mapping, Protocol


class ModelUnavailable(Exception):
    """The optional assessment provider cannot return a response."""


class ModelOutputError(ValueError):
    """A provider response violates the structured assessment contract."""


class ModelAdapter(Protocol):
    def assess(self, *, event_id: str, indicator: str, description: str,
               evidence: list[dict[str, Any]]) -> Mapping[str, Any]: ...


@dataclass(frozen=True)
class Assessment:
    indicator: str
    classification: str
    summary: str
    suggested_action: str
    evidence_ids: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["evidence_ids"] = list(self.evidence_ids)
        return result


def validate_assessment(raw: Mapping[str, Any], *, indicator: str,
                        available_evidence_ids: set[str]) -> Assessment:
    """Validate syntax and citations, not the factual truth of model prose."""
    if not isinstance(raw, Mapping):
        raise ModelOutputError("assessment must be an object")
    required = {"indicator", "classification", "summary", "suggested_action", "evidence_ids"}
    if set(raw) != required:
        raise ModelOutputError("assessment fields do not match the contract")
    if raw["indicator"] != indicator:
        raise ModelOutputError("assessment indicator differs from the alert")
    if (not isinstance(raw["classification"], str)
            or raw["classification"] not in {"suspicious", "inconclusive", "unknown"}):
        raise ModelOutputError("classification is invalid")
    summary = raw["summary"]
    if not isinstance(summary, str) or not summary.strip() or len(summary) > 500:
        raise ModelOutputError("summary must be non-empty text of at most 500 characters")
    if (not isinstance(raw["suggested_action"], str)
            or raw["suggested_action"] not in {"review_block", "investigate", "none"}):
        raise ModelOutputError("suggested action is invalid")
    ids = raw["evidence_ids"]
    if (not isinstance(ids, list) or any(not isinstance(item, str) for item in ids)
            or len(ids) != len(set(ids)) or not set(ids).issubset(available_evidence_ids)):
        raise ModelOutputError("evidence IDs must be unique references to supplied records")
    return Assessment(indicator, raw["classification"], summary.strip(),
                      raw["suggested_action"], tuple(ids))


class RecordedAdapter:
    """Return checked-in fixture responses for offline exercises."""

    def __init__(self, responses: Mapping[str, Mapping[str, Any]]):
        self._responses = deepcopy(dict(responses))

    def assess(self, *, event_id: str, indicator: str, description: str,
               evidence: list[dict[str, Any]]) -> Mapping[str, Any]:
        # The signature matches future adapters; no inference occurs here.
        if event_id not in self._responses:
            raise ModelUnavailable("no recorded response for event")
        return deepcopy(self._responses[event_id])
