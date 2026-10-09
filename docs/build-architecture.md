# Suspicious IP Triage Agent Build Architecture

## Purpose and boundary

This is a learning prototype for the NESTCON Agent Lab, not a production SOC product. It processes synthetic alerts about documentation-only IP addresses. It never connects to a SIEM, firewall, EDR, email account, or live threat-intelligence service. The first milestone is deterministic so we can prove the workflow and safety boundaries before adding an LLM.

## First vertical slice

```text
Structured synthetic alert
    |
    v
Schema and indicator validation
    |
    v
Local evidence lookup with provenance
    |
    v
Deterministic triage recommendation
    |
    v
Policy decision: recommend only or deny
    |
    v
Structured result and audit event
```

The `description` field is untrusted context. It may contain natural language, including attacker-controlled instructions. It cannot change the indicator, rules, permissions, or policy. The prototype reads only the structured `indicator` field for an IP address. This is an intentional design constraint, not a complete prompt-injection defence for a future LLM-enabled system.

## Components and contracts

| Component | Responsibility | Initial implementation |
| --- | --- | --- |
| Alert validator | Validate event ID, IP address, text length, and allowed event source | Python standard library |
| Evidence store | Return synthetic records by exact IP, including source and observed time | Version-controlled JSON fixture |
| Triage engine | Apply transparent rules to evidence | Pure Python function |
| Policy gate | Prevent execution; classify proposed next step | Pure Python function |
| Audit recorder | Record input reference, evidence IDs, recommendation, policy decision, and result | In-memory append-only sequence for a single run |
| CLI | Replay a fixture and display structured output | `python -m cyber_agent` |

An audit event in this milestone is a development trace, **not** tamper-resistant evidence. Persistent storage, access control, and integrity protection are later work.

## Trust boundaries

1. Alert `description` and source metadata are untrusted data. They do not become platform instructions, even when they claim to be from an administrator.
2. Evidence fixtures are test data. Provenance is displayed so a participant can see why a recommendation was made.
3. The triage engine makes a recommendation only. It has no access to a state-changing tool.
4. The policy gate is code outside the triage engine. Unknown or insufficient evidence cannot produce a containment recommendation.
5. If an LLM is added later, its output must be schema-validated and sent through this independent policy gate. A model confidence score must not authorize an action.

## Rules for the baseline

- Two or more distinct synthetic evidence records labelled `malicious` produce `recommend_review_for_block` with `approval_required`. This is a proposal, not a block.
- Any other known indicator produces `investigate` with `recommend_only`.
- An indicator missing from the local evidence store produces `insufficient_evidence` with `deny_action`.
- A malformed alert fails validation before analysis.
- Replaying the same event ID in one process returns the earlier result and does not add another audit event.

These are demonstration rules, not incident-response thresholds. The team should adjust them only after specifying the learning objective and expected outcomes for each case.

## Second milestone simulation gateway

The gateway accepts only `simulate_block_ip` for a previously triaged, eligible event. It binds a request to event ID, tool, indicator, and duration; a local demo approval yields a one-time token valid for five minutes. Execution rechecks the request and current policy, then returns `status: simulated` without calling any real system. Tests cover changed parameters, expiry, replay, unknown tools, and ineligible events.

The demo approver is a text label, **not** an authenticated person. Tokens and audit entries exist only in process memory. A real multi-user deployment would need authenticated identities, role checks, durable transactions, audit integrity, and an approval service that cannot be bypassed by the same operator.

## Next boundary before an LLM

A single-user localhost participant interface now shows alert, evidence, decision, local approval, simulated result, and audit timeline. It can reset its in-memory session. This is a teaching interface, not authenticated multi-user software. Next add persistent audit storage only if needed for the pilot, and a full attack-and-defend replay. Test unavailable evidence. Only then add a model adapter that can be replaced with a recorded-response adapter for offline use. No live security integration is part of the event prototype.

## Definition of done for this milestone

- A benign fixture and an adversarial-text fixture both complete the legitimate triage flow.
- Invalid IPs and unknown indicators fail safely.
- No code path can invoke a live or state-changing security tool.
- Replayed event IDs do not create duplicate audit events.
- Unit tests run offline using only the Python standard library.
