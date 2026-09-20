# AI Agent Security Lab

An implementation-focused research project for designing a safe, practical cyber AI agent village. The project combines **Build-a-Bot** activities with **Agent Under Attack** exercises so participants can learn how agents are built, how they fail, and how to secure them.

> Status: Research and design in progress  
> Assignment: Z2 — Agent Lab  
> Focus: AI agent development and security

## Project Question

How can a cybersecurity event deliver an accessible, hands-on AI agent lab that is technically useful, safe to operate, realistic for Ghana, and resilient when internet or paid API access is limited?

## Intended Outcomes

- Define a progressive participant journey from basic agent concepts to adversarial testing.
- Design four practical activities with clear learning objectives and difficulty levels.
- Recommend an isolated technical architecture, hardware, software, models, and APIs.
- Document realistic attack scenarios, safety controls, and facilitator procedures.
- Estimate capacity, setup time, staffing, cost, and fallback options.
- Translate the research into an actionable implementation report for organizers.

## Proposed Lab Journey

| Stage | Activity | Participant outcome |
| --- | --- | --- |
| 1 | Agent Foundations | Understand an agent's model, tools, memory, instructions, and permissions. |
| 2 | Build-a-Bot | Create a small defensive cyber agent using constrained tools and test data. |
| 3 | Agent Under Attack | Test prompt injection, unsafe tool use, data leakage, and excessive agency. |
| 4 | Defend and Retest | Add guardrails, monitoring, and least privilege; then verify the improvements. |

The activity names and design are working proposals and will be refined through research.

## Research Tracks

1. Comparable AI villages, workshops, CTFs, and security labs.
2. Participant personas, prerequisites, accessibility, and learning progression.
3. Agent architecture, model choices, tools, memory, APIs, and observability.
4. Threat scenarios, including prompt injection, data leakage, tool abuse, and over-permissioning.
5. Isolation, safety controls, reset procedures, and facilitator escalation paths.
6. Ghana feasibility: connectivity, power, hardware, cost, local relevance, and offline fallbacks.
7. Operations: staffing, throughput, timing, evidence collection, and success metrics.

## Source Documents

- **NESTCON Research Template:** the controlling structure for the final research and implementation report.
- **Build-a-Bot Cyber Agent BRD/SRS:** a product-level reference for use cases, architecture, controls, testing ideas, and acceptance criteria. It is broader than the proposed event lab and will be reduced to a safe simulation.

See [Source Context and Project Interpretation](docs/source-context.md) for the detailed scope decision and proposed activity mapping.

## Repository Map

```text
ai-agent-security-lab/
├── README.md
├── docs/
│   ├── implementation-report.md
│   ├── project-scope.md
│   ├── research-log.md
│   └── source-context.md
├── findings/
│   └── findings-register.md
├── journal/
│   └── learning-journal.md
└── evidence/
    └── README.md
```

## Research Method

1. Review primary sources and comparable public programs.
2. Record each source, claim, relevance, and limitation in the research log.
3. Convert evidence into design decisions in the implementation report.
4. Record risks, constraints, and recommendations in the findings register.
5. Prototype activities only in isolated environments with synthetic data.
6. Validate activities for safety, timing, clarity, and resetability.
7. Publish sanitized results and clearly label assumptions or unverified claims.

## Ethical and Safety Boundaries

- Use only authorized systems, purpose-built labs, and synthetic data.
- Do not publish secrets, personal data, working credentials, or harmful payloads.
- Apply least privilege and explicit allowlists to agent tools.
- Keep attack demonstrations reproducible but non-deployable against real targets.
- Add human approval before consequential actions.
- Log important agent actions and maintain a rapid reset path.

## Current Deliverables

- [x] Create the public project structure.
- [x] Define the research question and reporting method.
- [ ] Confirm the organizers' research template and required format.
- [ ] Research comparable implementations and primary guidance.
- [x] Draft the four activities and participant journey.
- [ ] Validate activity timing, difficulty, scoring, and resets through a pilot.
- [ ] Produce architecture, bill of materials, cost, and fallback options.
- [x] Draft the architecture, equipment baseline, and fallback modes.
- [x] Draft risk, safety, staffing, capacity, and Ghana compliance considerations.
- [ ] Validate the design with venue, budget, legal, and organizer inputs.
- [ ] Build and test a minimal prototype.
- [ ] Finalize the implementation report and executive recommendations.

## Publication Note

This repository documents an evolving learning and research process. Early entries are hypotheses, not final recommendations. Findings will be updated when stronger evidence or prototype results become available.
