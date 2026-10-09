# Cyber Agent Learning Backlog

This backlog is ordered to produce a working, testable agent increment before adding AI. Each item has a tangible result you can inspect and explain.

## Milestone 1 Synthetic case and data contracts

**B01 Define the legitimate task.** The agent triages a synthetic suspicious-IP alert and recommends an analyst's next step. Learn the difference between a security event, evidence, recommendation, authorization, and action. Done when three cases have expected outcomes: suspicious, benign or inconclusive, and unknown.

**B02 Model the alert and evidence.** Validate event IDs, source, IP indicator, bounded description, evidence IDs, labels, and provenance. Learn typed data and input validation. Done when malformed addresses and unsupported sources are rejected by tests.

**B03 Create synthetic fixtures.** Use documentation-only IP ranges and fictional evidence. Learn reproducible test data and provenance. Done when fixtures contain no credentials, personal data, or live targets.

## Milestone 2 Deterministic prototype

**B04 Implement evidence retrieval.** Query local fixture records by exact IP. Learn separation of storage from decision logic. Done when unknown indicators return no evidence rather than guessed facts.

**B05 Implement explainable triage.** Apply documented rules and return evidence IDs with the recommendation. Learn pure functions and testable decision logic. Done when changing untrusted description text alone cannot change the decision.

**B06 Add independent policy.** Label the next step `recommend_only`, `approval_required`, or `deny_action`; execute nothing. Learn the difference between a recommendation and permission. Done when the suspicious case proposes review but no tool action occurs.

**B07 Add audit and replay safety.** Record one event-to-decision trace per event ID in a process. Learn correlation IDs and idempotency. Done when a duplicate event returns the original result without a second audit entry.

**B08 Add offline CLI and tests.** Make each fixture runnable with one command and run the test suite without an API key. Learn packaging, automated testing, and failure diagnosis. Done when all tests pass from a fresh checkout with a supported Python interpreter.

## Milestone 3 Secure interactive lab

**B09 Add a simulation-only gateway — implemented.** Allow only narrow, typed mock actions. Learn tool contracts and least privilege. Tests reject unknown tools; the gateway has no external connector.

**B10 Add exact-action approval — lab demonstration implemented.** Bind a local approval token to tool name, parameters, event ID, and expiry. Tests deny changed or expired requests and replay. Authentication, role checks, and durable approval are not implemented; the demo approver name is a label only.

**B11 Build the participant interface.** Show alert, evidence, recommendation, policy decision, and audit timeline. Learn usable security explanations. Done when a beginner can identify why an action was allowed or denied.

**B12 Add attack-and-defend replay.** Test injected instructions, malformed indicators, duplicate events, missing evidence, and tool misuse. Learn threat modelling and regression tests. Done when the legitimate task still works while unsafe actions stay blocked.

## Milestone 4 Optional AI layer and pilot

**B13 Add a replaceable model adapter.** Limit the model to structured assessment and summary; keep policy and tools independent. Learn LLM integration and structured output validation. Done when malformed, timed-out, or unavailable model responses fail safely and offline replay remains usable.

**B14 Run a small pilot.** Measure completion, understanding, reset time, and facilitator load. Learn evaluation and operations. Done when observed results are recorded separately from design assumptions and reviewed before scaling.

## Learning routine

For each backlog item: explain the trust boundary in your own words; run the normal case; run one failure or abuse case; inspect the audit/output; record one lesson in the learning journal. Do not publish team-only schedules, private correspondence, credentials, or unreviewed event operations.
