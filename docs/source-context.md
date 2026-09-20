# Source Context and Project Interpretation

## What the Research Template Requires

The NESTCON deliverable is not a general research paper about AI agents. It is a **zone content research and implementation report** that must answer four practical questions:

1. What is the content and why does it belong in the Agent Lab zone?
2. What will participants actually do?
3. What people, equipment, software, infrastructure, safety controls, and budget are required?
4. Is the activity feasible and recommended for NESTCON?

The report must cover content-to-zone fit, the participant journey, progressive activity levels, physical and technical implementation, staffing, safety, learning outcomes, cost, feasibility, recommendation, future development, references, and a one-page executive summary.

## What the Build a Bot BRD and SRS Contributes

The BRD/SRS describes a proposed production-grade cybersecurity agent platform. Its central use case is a governed agent that receives security events, extracts intent and indicators, gathers evidence, recommends a response, applies deterministic authorization policy, requests human approval when required, and uses only controlled tools.

Its most useful design principle for the NESTCON lab is:

> The AI may analyze untrusted content and recommend an action, but a separate deterministic policy and authorization layer decides whether the action is allowed.

Relevant controls for the lab include:

- Treat email, logs, tickets, attachments, and retrieved text as untrusted data.
- Separate prompts and data from system policy, credentials, and tool definitions.
- Give each bot and integration least-privilege permissions.
- Expose only narrow, typed, allowlisted tools.
- Validate structured model output before using it.
- Require human approval for consequential actions.
- Bind approval to exact action parameters and an expiry time.
- Fail closed when identity, authorization, evidence, or policy cannot be established.
- Record an end-to-end audit trail.
- Provide a simulation mode that cannot change real systems.

## Scope Decision

The enterprise platform in the BRD/SRS is too large to build as a conference activity. The NESTCON implementation should therefore use a **small, isolated simulation** of the core workflow rather than attempt the full product.

Recommended prototype flow:

```text
Synthetic alert or email
    → extract indicator and intent
    → label content as untrusted
    → query local or simulated evidence
    → produce a structured recommendation
    → apply a deterministic policy decision
    → request participant approval where required
    → simulate an allowlisted action
    → record the result in an audit log
```

No real SIEM, EDR, firewall, mailbox, production credential, or destructive action is required for the first implementation.

## Proposed Progressive Experience

| Layer | Working activity | Participant experience |
| --- | --- | --- |
| Five-minute first win | Spot the Unsafe Instruction | Identify prompt injection hidden inside a synthetic security alert and prevent an unsafe action. |
| Guided hands-on lab | Build a Suspicious IP Triage Bot | Configure a bot to extract an IP, check simulated evidence, and generate an explainable recommendation. |
| Clinic or demonstration | Agent Under Attack | Observe attacks involving prompt injection, tool abuse, excessive permission, and data leakage; then inspect the controls. |
| Advanced challenge | Defend and Retest | Add policy gates, least privilege, structured output, approval, and logging, then pass an adversarial test set. |

These are working proposals. Research and prototype testing must validate their duration, difficulty, equipment needs, and participant capacity.

## Decisions Still Needed

- Whether NESTCON expects one combined activity or four separately staffed stations.
- Expected participant skill levels and daily attendance.
- Available workstations, network, power, displays, and physical space.
- Internet reliability and whether cloud-model APIs are permitted.
- Budget range and access to sponsors or borrowed equipment.
- Required submission deadline, review milestones, and researcher status fields.
- Whether the provided BRD/SRS is an approved baseline, a concept document, or only a reference.
- Whether a Road to NESTCON pilot can be scheduled before the main event.

