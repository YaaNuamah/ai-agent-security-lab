# AI Agent Security Lab — Implementation Report

> Working document. Claims should be linked to the research log or supported by prototype evidence.

## Executive Summary

Summarize the recommended lab, why it is valuable, what it requires, its key risks, and the decisions organizers need to make.

## 1. Research Information

- Researcher: Yaa Nuamah Kusi-Fordjour
- Zone: Z2 Agent Lab
- Content or topic: Build-a-Bot Cyber Agent and Agent Under Attack
- Date: To be confirmed
- Research status: In progress
- Research lead: Sesinam

## 2. Content Overview

### 2.1 What Is the Content

The proposed content is a hands-on **AI agent development and security experience**. An AI agent is a software system that uses an AI model to interpret a goal or event, make decisions, and interact with data or tools. Unlike a basic chatbot, an agent may retrieve information, call an API, create a ticket, send a notification, or recommend and initiate a security action.

The NESTCON activity combines two complementary perspectives:

- **Build-a-Bot:** participants assemble or configure a small cybersecurity agent that receives a synthetic alert, extracts an indicator, gathers approved evidence, and produces an explainable recommendation.
- **Agent Under Attack:** participants test how an agent can be manipulated through untrusted input, excessive permissions, unsafe tool use, or weak approval controls, then improve the design and retest it.

The content sits across AI security, application security, security automation, threat intelligence, security operations, and secure software development. It develops practical skills in agent workflow design, trust-boundary analysis, prompt-injection testing, least privilege, tool authorization, structured output validation, human approval, logging, and adversarial testing.

### 2.2 Key Concepts

**Agent components.** The activity introduces the model, instructions, tools, data or memory, identity and permissions, policy controls, and observability that together form an agent system. Participants learn that security depends on the whole system rather than on the language model alone.

**Untrusted content and prompt injection.** An alert, email, log entry, webpage, attachment, or tool response may contain text designed to change the agent's behavior. The agent must treat this content as data and must not allow it to override trusted policy. MITRE ATLAS describes indirect prompt injection as malicious input ingested from another data source during normal operation, while OWASP identifies prompt injection as a trigger for unsafe agent behavior ([MITRE ATLAS SAFE AI](https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf); [OWASP Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)).

**Agency and tool use.** Tools allow an agent to affect other systems. OWASP defines excessive agency as a condition in which unexpected, ambiguous, or manipulated model outputs can cause damaging actions. The 2026 OWASP agentic-security framework also highlights agent goal hijacking, tool misuse, and identity or privilege abuse as critical risk areas ([OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)).

**Deterministic authorization.** Model output is probabilistic and should be treated as a recommendation. A separate policy layer should decide whether an action is allowed, denied, simulated, or requires approval. The proposed lab demonstrates this separation through narrow allowlisted tools, exact parameters, participant approval, and a simulation-only action gateway.

**Human oversight and auditability.** A participant should be able to review the evidence, proposed action, risk, and expected effect before approval. The system should record the input, evidence, recommendation, policy decision, approval, and simulated result so the full decision path can be examined.

**Testing and continuous risk management.** NIST organizes AI risk management into Govern, Map, Measure, and Manage functions and emphasizes that risk management continues throughout the AI lifecycle. This provides a useful structure for explaining why the lab defines its context, tests failure modes, measures results, and improves controls rather than treating security as a one-time check ([NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)).

### 2.3 Real World Relevance

Security teams increasingly explore AI-enabled workflows for alert triage, indicator extraction, evidence gathering, incident summarization, ticket creation, and response recommendations. These workflows can reduce repetitive work, but connecting a model to tools and sensitive data increases the impact of errors or manipulation. A malicious instruction hidden in content can become an authorization problem if the agent is over-permissioned or if model output is executed without independent validation.

The content is relevant to SOC analysts, incident responders, application and product security engineers, detection engineers, security architects, AI red teamers, governance specialists, and software developers building AI-enabled systems. Participants practice both offensive reasoning—how an agent can be manipulated—and defensive engineering—how permissions, policy, approvals, isolation, validation, and logging reduce risk.

For Ghanaian and African participants, the proposed design emphasizes transferable skills and deployability under practical constraints. It will use synthetic data, open or low-cost components where feasible, a local simulation path, and activities that do not depend on access to enterprise SIEM, EDR, or firewall products. This is a design recommendation that must be validated against NESTCON's actual venue, equipment, connectivity, participant profile, and budget.

## 3. Content to Zone Fit

### 3.1 Why the Content Belongs in the Agent Lab Zone

The content belongs in Z2 because it allows participants to build, observe, attack, and defend an AI agent as one continuous experience. It moves beyond a presentation about AI by making the agent's decisions, tools, permissions, failures, and controls visible. Participants learn both what an agent can automate and why safe deployment requires engineering controls outside the model.

This approach is consistent with established AI security event formats. AI Village describes its program as hands-on AI security education combining red-team exercises, workshops, events, and open resources. At DEF CON, it has used beginner-friendly exercises, demonstrations, training workshops, competitions, and CTF-style scoring. Its 2023 public generative-AI red-team event supplied laptops and timed model access, while its 2026 program included a sandboxed agentic-security competition and a novice-friendly agent demonstration ([AI Village](https://aivillage.org/); [2023 Generative Red Team](https://aivillage.org/blog/generative-red-team/); [AI Village at DEF CON 34](https://aivillage.org/events/defcon-34/)). These examples support a progressive format rather than a single lecture or unrestricted open-ended test.

### 3.2 Contribution to the Zone

The activity contributes:

- A beginner-accessible explanation of models, tools, permissions, and trust boundaries.
- A visible first win in which participants detect an unsafe instruction.
- A guided building activity that connects AI with a recognizable defensive-security task.
- A controlled attack-and-defend experience covering prompt injection, tool misuse, excessive agency, and privilege.
- A blue-team perspective based on policy, validation, approval, logging, and retesting.
- An advanced challenge for experienced participants without making advanced knowledge a prerequisite for entering the zone.
- A reusable simulation that can be reset between participants and adapted for future workshops.

### 3.3 Relationship with Other Zone Activities

Build-a-Bot and Agent Under Attack should not be treated as unrelated stations. The bot created or introduced in the guided activity becomes the target in the adversarial activity. Participants first learn its intended workflow, then discover how untrusted content or excessive permissions change its behavior, and finally apply controls and retest it. This creates a clear build, attack, defend, and verify narrative.

The activity can also connect with other NESTCON content. Synthetic alerts can support threat-intelligence enrichment and SOC investigation; audit logs can support incident-response or detection exercises; API and authorization controls can connect to application-security content; and container isolation, secrets handling, and logging can connect to cloud or DevSecOps activities. These cross-zone connections should remain optional until the organizers confirm the final Village layout and ownership boundaries.

## 4. Proposed Implementation

### 4.1 Proposed Activity

**Activity name:** Build Secure Defend an AI Cyber Agent

**Description:** Participants investigate how a small cybersecurity agent processes a synthetic suspicious-IP alert. They identify untrusted content, configure or inspect the agent's workflow, observe an unsafe version fail, add security controls, and verify that the protected version blocks unauthorized behavior while still completing its intended task.

**Objective:** Teach participants how AI agents combine models, data, tools, permissions, and policy; demonstrate how prompt injection and excessive agency create risk; and provide hands-on practice with least privilege, deterministic authorization, approval, logging, and adversarial retesting.

**Target audience:** Students, early-career technologists, software developers, SOC or incident-response practitioners, and cybersecurity professionals curious about AI security. The first-win activity assumes no AI or programming experience. The guided lab benefits from basic familiarity with security alerts, IP addresses, or simple workflow logic. The advanced challenge is intended for participants comfortable with application security, scripting, or threat modeling.

**Difficulty:** Progressive, from beginner to advanced.

**Estimated duration:**

| Experience | Working duration | Participation mode |
| --- | ---: | --- |
| First win | 5–10 minutes | Walk-up |
| Guided lab | 25–35 minutes | Facilitated station or scheduled group |
| Clinic and demonstration | 20–30 minutes | Scheduled presentation with interaction |
| Advanced challenge | 30–45 minutes | Optional individual or team challenge |

Durations are initial design targets. A Road to NESTCON pilot should measure actual completion time and determine whether the guided and advanced activities need shorter variants.

### 4.2 Participant Journey

1. **Welcome and orientation.** A facilitator introduces the agent's legitimate task: assess a synthetic suspicious-IP alert and recommend an authorized response. The participant receives a short safety notice explaining that the environment is simulated and event-owned.
2. **Map the system.** The participant identifies the alert, AI analysis step, evidence source, policy gate, approval step, tool, and audit record on a simple workflow diagram.
3. **Establish normal behavior.** The participant runs or observes a benign alert. The agent extracts the IP address, checks simulated threat-intelligence evidence, produces a structured assessment, and recommends a response.
4. **Encounter the attack.** The participant receives an alert containing an embedded instruction that attempts to override policy or misuse a tool. In the intentionally unsafe version, the agent may propose an unauthorized action or disclose a planted synthetic value.
5. **Diagnose the control failure.** The participant decides whether the failure involves untrusted content, excessive permission, missing validation, weak approval, or incomplete logging.
6. **Secure the workflow.** Depending on the activity level, the participant selects or implements controls such as trust labels, structured output, a narrow tool allowlist, parameter validation, deterministic policy, human approval, or audit logging.
7. **Retest.** The same adversarial input is run again. Success requires the unsafe action to be denied or safely simulated while the legitimate investigation still completes.
8. **Review and takeaway.** The participant reviews the before-and-after audit trail, receives feedback, and records one control they would apply to a real system.

### 4.3 Implementation Format

The recommended format is a **hybrid station** combining four modes:

- An interactive five-minute first win for walk-up participants.
- A guided hands-on lab for the main learning experience.
- A scheduled clinic or demonstration for participants who cannot complete the lab or want a facilitator-led explanation.
- An optional scored challenge for experienced participants.

This hybrid format is appropriate because it accommodates different experience levels and available time without requiring every visitor to complete the longest activity. All modes reuse the same scenario, diagrams, synthetic data, and isolated technical environment, reducing setup and facilitator burden. The design should start as a pilot with one or two stations before capacity is increased.

## 5. Activity Structure

### 5.1 Beginner First Win Activity

**Activity:** Spot the Unsafe Instruction

**Objective:** Recognize that instructions embedded in security data are untrusted and should not be granted authority.

**Duration:** 5–10 minutes

**Difficulty:** Beginner

**What the participant does:**

1. Read a short synthetic suspicious-IP alert.
2. Highlight the factual security data, the legitimate user request, and a hidden instruction attempting to change the agent's behavior.
3. Choose the safest response from three options.
4. Place the content in the correct trust category: trusted policy, authorized user request, or untrusted evidence.
5. View a short explanation of why the unsafe instruction must not control tools or policy.

**Expected outcome:** The participant identifies the injected instruction and prevents the proposed unsafe action.

**What the participant learns:** Text processed by an AI system may be data rather than an authorized command. Identity, policy, and permission must be established independently of the wording interpreted by the model.

**Assessment:** One point each for identifying the malicious instruction, assigning the correct trust label, and choosing a safe response. A score of two out of three completes the first win; the facilitator explains any missed answer.

**Facilitator involvement:** Introduce the scenario, avoid giving away the answer, explain the trust boundary, and reset the card or screen.

**Reset procedure:** Reload the start screen or replace the laminated scenario card and response sheet. No participant data is retained.

### 5.2 Guided Hands On Lab

**Activity:** Build a Suspicious IP Triage Bot

**Objective:** Configure and test a bounded agent that extracts an indicator, gathers simulated evidence, produces an assessment, and submits any proposed action to policy and approval controls.

**Duration:** 25–35 minutes

**Difficulty:** Beginner to intermediate

**Participant instructions:**

1. Review the bot's purpose, allowed inputs, and permitted tools.
2. Arrange or configure the workflow: ingest alert, extract IP, validate IP, query local evidence, assess risk, check policy, request approval if required, simulate action, and write audit result.
3. Run a benign test case and confirm the structured output contains the indicator, evidence, confidence, recommendation, and reason.
4. Run an adversarial alert containing an indirect prompt injection.
5. Observe which control blocks the malicious instruction.
6. Review the audit timeline and confirm that no unapproved state-changing action occurred.

**Facilitator involvement:** Provide orientation, help participants distinguish the AI analysis layer from the policy and execution layers, assist with technical problems, and conduct a two-minute debrief.

**Expected outcome:** The configured bot completes the legitimate investigation, refuses or ignores the embedded malicious instruction, routes a containment recommendation for approval, and produces a complete simulated audit trail.

**Learning outcome:** Participants can describe why an AI recommendation is not authorization and identify at least three controls required before an agent can use security tools safely.

**Assessment:** A completion checklist verifies valid indicator extraction, evidence provenance, structured output, policy decision, approval behavior, safe tool result, and audit completeness. The target is six of seven controls, with the policy/approval control mandatory.

**Reset procedure:** End the participant session, delete the temporary session record, restore the known-good workflow configuration, reset simulated evidence and approvals, and run an automated health check before the next participant begins.

### 5.3 Clinic and Demonstration

**Topic:** Agent Under Attack From Prompt Injection to Tool Misuse

**Objective:** Show how a seemingly small trust-boundary failure can progress into unauthorized tool use or data exposure, and how layered controls interrupt the attack chain.

**Duration:** 20–30 minutes, including questions

**Difficulty:** Mixed audience

**Demonstration sequence:**

1. Explain the intended agent workflow and the trust boundaries.
2. Run a benign alert to establish expected behavior.
3. Introduce an indirect prompt injection in synthetic alert text.
4. Demonstrate the intentionally vulnerable configuration in simulation mode.
5. Trace the failure through input handling, model recommendation, permissions, and tool invocation.
6. Enable trust labels, structured output validation, policy, approval, and allowlisted tools.
7. Replay the attack and show the denial and audit evidence.
8. Discuss residual risk and why no single prompt or filter is a complete defense.

**Facilitator expertise:** The presenter should understand agent workflows, prompt injection, application-security trust boundaries, least privilege, authorization, and incident logging. A technical assistant should manage the environment and recovery.

**Equipment:** Facilitator laptop, large display, isolated demonstration environment, prepared benign and adversarial test cases, workflow diagram, and an offline recording or screenshots as a fallback.

**Expected learning outcome:** Participants can explain an agentic attack path and identify where preventive, detective, and recovery controls should be placed.

**Reset procedure:** Recreate the demonstration container or restore a clean snapshot. Confirm the planted synthetic secret, logs, policy, and test cases match the demonstration baseline.

### 5.4 Advanced Challenge

**Challenge:** Defend and Retest the Agent

**Objective:** Harden an intentionally vulnerable agent workflow against a small adversarial test set without breaking its legitimate security-triage function.

**Estimated duration:** 30–45 minutes

**Difficulty:** Intermediate to advanced

**Challenge task:** Participants receive a vulnerable workflow, a functional specification, and benign acceptance tests. They must identify weaknesses, select or implement controls, and submit the protected version to automated benign and adversarial tests.

**Proposed test categories:**

- Indirect prompt injection hidden in an alert.
- Attempted use of a tool outside the bot's allowlist.
- Malformed IP address or unexpected tool parameter.
- Containment request without valid approval.
- Expired approval or approval bound to different parameters.
- Attempt to retrieve or reveal a planted synthetic secret.
- Duplicate alert that could trigger a repeated action.
- Unavailable evidence service requiring safe failure.

**Assessment and scoring:**

| Category | Points | Condition |
| --- | ---: | --- |
| Legitimate functionality | 20 | Benign investigation completes with correct structured output. |
| Injection resistance | 20 | Malicious content cannot change policy or tool authority. |
| Tool and input controls | 20 | Disallowed tools and malformed parameters are rejected. |
| Authorization | 20 | Approval-required action cannot run without valid, matching approval. |
| Data protection | 10 | Synthetic secret is not disclosed through output or logs. |
| Auditability and safe failure | 10 | Decisions are traceable and dependency failure does not cause unsafe action. |

Participants must score at least 70 points, pass the legitimate-functionality test, and record no successful unauthorized action. Ties may be resolved by fewer control changes or faster completion, but safety must never be traded for speed.

**Facilitator involvement:** Provide the rules and environment, answer scope questions, monitor safety, verify results, and lead a short solution review. Facilitators must not encourage testing outside the supplied environment.

**Expected outcome:** The participant demonstrates that the secured workflow remains useful while blocking or containing the tested attacks.

**Reset procedure:** Destroy the per-team environment and recreate it from the signed baseline image or configuration. Rotate temporary session credentials, clear queues and logs that are not retained for scoring, and run benign and adversarial smoke tests.

### 5.5 Pilot Validation Requirements

Before final approval, the team should run a small pilot and record:

- Median and maximum completion time for each activity.
- Percentage of participants completing without facilitator intervention.
- Most common misunderstanding or failure point.
- Facilitator time required per participant or team.
- Technical failure and reset rates.
- Whether the scoring distinguishes beginner and advanced performance fairly.
- Whether the activity remains usable with limited or unavailable internet.
- Whether all test data, actions, secrets, and targets remain synthetic and isolated.

## 6. Zone Layout and Physical Implementation

### 6.1 Proposed Station

The recommended pilot layout uses two participant stations, one facilitator station, one shared display, and a small reset and equipment area. The layout should keep walk-up visitors outside the seated lab area so queues do not obstruct participants or expose screens and credentials.

```text
Entrance and queue
       ↓
First-win table → Orientation and safety briefing
                         ↓
              ┌──────────────────────┐
              │ Shared display       │
              │ workflow and timer   │
              └──────────────────────┘
              ┌──────────┐ ┌──────────┐
              │ Station A│ │ Station B│
              │ 1–2 users│ │ 1–2 users│
              └──────────┘ └──────────┘
                   ┌──────────────┐
                   │ Facilitator  │
                   │ and control  │
                   └──────────────┘
              Reset area and locked storage
```

Each participant station should display the activity instructions, trust-boundary diagram, progress state, and remaining time. The facilitator station should show service health, station status, reset controls, and safety events but should not expose reusable secrets on the shared display.

### 6.2 Space Requirements

The following is a planning baseline for a two-station pilot and must be confirmed with the venue team.

| Area | Working requirement | Rationale |
| --- | --- | --- |
| Space | Approximately 20–30 square metres | Allows two stations, facilitator access, queue separation, and safe cable routes. |
| Tables | Three standard tables plus one small reset/storage surface | Two participant tables, one facilitator table, and controlled equipment handling. |
| Seats | Six | Four participants and two facilitators; lead/technical support may stand or rotate. |
| Display | One 40-inch or larger display, or projector with readable resolution | Supports briefing, clinic, timer, and workflow visualization. |
| Power | At least eight grounded outlets through venue-approved protected distribution | Laptops, display, network device, facilitator equipment, and spare capacity. |
| Network | Dedicated isolated network segment; wired connections preferred | Makes access predictable and limits exposure to venue or participant networks. |
| Internet | Optional for the primary lab; controlled egress only for approved services | The activity should remain usable if internet or a model API is unavailable. |
| Storage | Lockable box or cabinet | Secures laptops, adapters, removable media, and printed administrative material. |
| Accessibility | Clear approach, seated participation option, readable text, keyboard navigation where feasible | Supports participants with different mobility and interaction needs. |

All cables should be secured with venue-approved covers or routed away from walkways. Power distribution, furniture placement, fire safety, and occupancy must follow venue rules.

### 6.3 Participant Capacity

For planning, each station supports one participant or a pair sharing defined roles. With two stations and a 30-minute guided session, the theoretical maximum is eight participants per hour. A more credible pilot target is **six participants per hour**, allowing briefing, transition, reset, and technical recovery.

| Mode | Participants | Cycle | Planning capacity |
| --- | ---: | ---: | ---: |
| First win | 1–4 concurrently | 5–10 minutes | 12–24 per hour, depending on facilitation |
| Guided lab | 2–4 per session | 30–40 minutes including reset | 6 per hour target |
| Clinic/demo | 10–25 viewers | 30 minutes plus transition | Venue-dependent |
| Advanced challenge | 2 teams of 1–2 | 45–60 minutes including reset | 4 participants per hour maximum |

Daily capacity must not be extrapolated until breaks, opening hours, facilitator rotations, failure rates, and the pilot completion-time distribution are known.

## 7. Technical Implementation

### 7.1 Architecture

The pilot should use a single-host or small local-server architecture with one isolated environment per station. The AI analysis component must not have direct authority to execute actions.

```text
Participant browser
        ↓
Local lab interface
        ↓
Scenario and input gateway
        ↓
Trust label and parser
        ↓
AI analysis adapter ─────→ approved local model or model gateway
        ↓
Schema validation
        ↓
Deterministic policy engine
        ↓
Human approval gate
        ↓
Simulation-only tool gateway
        ↓
Mock threat intelligence, ticketing and firewall services
        ↓
Append-only session audit log
```

The architecture enforces five boundaries:

1. External scenario content is always labeled untrusted.
2. The model produces a typed recommendation, not an executable command.
3. Deterministic policy evaluates the proposed action independently.
4. Approval is required for the simulated containment action and is bound to its exact parameters.
5. Only the mock tool gateway can perform an action, and it has no route to a real security system.

### 7.2 Hardware Baseline

| Equipment | Quantity | Minimum working specification | Purpose |
| --- | ---: | --- | --- |
| Participant laptops | 2 | Modern 4-core CPU, 8 GB RAM, current supported browser; 16 GB preferred for local containers | Run the guided lab and challenge. |
| Facilitator laptop | 1 | 16 GB RAM recommended | Monitor stations, present the clinic, and control resets. |
| Local lab server | 1 optional | 8 CPU cores, 32 GB RAM, 250 GB free SSD | Host station containers and an optional small local model. |
| Display/projector | 1 | HDMI or USB-C input, readable from the room | Briefing and demonstration. |
| Managed network device | 1 | VLAN or equivalent client isolation, local DHCP/DNS, egress rules | Separate the lab from venue and participant networks. |
| Power protection | As approved | Surge protection and, if available, UPS for server/network | Reduce interruption and unsafe shutdown. |
| Spare laptop and adapters | 1 set | Compatible with station image and display | Rapid recovery from device failure. |

The lab server is optional if each station can run its own containers. Local-model feasibility depends on the selected model and actual hardware tests; no performance claim should be made before benchmarking.

### 7.3 Software and Services

Recommended components should be replaceable rather than locked to one vendor:

- A browser-based local lab interface.
- Containerized station environments using Docker or a compatible runtime.
- A small application service for scenarios, workflow state, scoring, and resets.
- A model adapter supporting either an approved cloud API or a local model.
- JSON Schema or equivalent validation for model output.
- A deterministic policy module with allow, deny, approval-required, and simulation-only outcomes.
- Mock threat-intelligence, ticketing, and firewall APIs containing only synthetic records.
- Structured application and audit logs with session-specific correlation identifiers.
- Health checks, timeout handling, and idempotency protection for simulated actions.

No unrestricted shell, PowerShell, SQL, arbitrary URL fetch, participant-supplied plugin, or production connector should be exposed to the agent.

### 7.4 Network and Data Controls

- Place all lab systems on an event-controlled, isolated network.
- Deny inbound access from venue and public Wi-Fi networks.
- Deny internet egress by default; allow only explicitly required model endpoints through a controlled gateway.
- Do not accept participant devices into the lab network during the initial pilot.
- Use synthetic indicators, identities, incidents, credentials, secrets, and target systems.
- Do not collect names or contact information in the technical environment unless separately justified and consented to.
- Use temporary session identifiers and delete ordinary session data during reset.
- Retain only de-identified aggregate results required for evaluation.

### 7.5 Delivery Modes

**Preferred offline mode:** All scenarios, evidence, policy, tools, scoring, and audit functions run locally. AI responses may use a tested local model or precomputed deterministic response set. This mode provides the most predictable event operation.

**Controlled online mode:** The model adapter calls one approved provider through a gateway. The gateway enforces authentication, rate limits, timeouts, permitted model, data minimization, and logging that excludes secrets. The organizer must review provider data handling and cost before use.

**Degraded mode:** If model inference fails, the lab substitutes a prepared structured recommendation so participants can continue testing policy, approval, tool, and audit controls. The interface must disclose when a fallback response is being used.

### 7.6 Reset and Recovery

Each session should run in a disposable container or equivalent isolated instance. The reset process should:

1. Stop the session and revoke its temporary credentials.
2. Export only approved de-identified scoring metrics.
3. Destroy the session instance and writable storage.
4. Recreate the environment from a versioned read-only baseline.
5. Reset mock services, approval state, queues, and planted test values.
6. Run automated benign and adversarial smoke tests.
7. Mark the station ready only after all health checks pass.

The target reset time is under five minutes, but this is a pilot metric rather than a confirmed capability.

## 8. Staffing and Facilitation

### 8.1 Required Expertise

The team collectively needs knowledge of AI agent workflows, application-security trust boundaries, prompt injection, authorization and least privilege, basic SOC and threat-intelligence processes, container operations, network isolation, facilitation, and incident handling. Individual facilitators do not need to be experts in every area if escalation roles are clear.

### 8.2 Staffing Baseline

| Role | Number for two-station pilot | Responsibility |
| --- | ---: | --- |
| Zone or activity lead | 1 | Own scope, safety decision-making, facilitator briefing, scheduling, and organizer escalation. |
| Facilitator | 2 | Orient participants, support one station each, assess outcomes, and reset learning materials. |
| Technical support | 1 shared or on call | Maintain containers, network, model gateway, display, backups, and recovery. |

Three people may operate a small pilot if the lead also provides technical support, but four is safer during busy periods and demonstrations. Staffing must be validated through a timed pilot; the design should not assume that one facilitator can simultaneously teach, monitor two technical stations, manage a queue, and recover failures.

### 8.3 Responsibilities

**Before opening:** Verify the authorized scope, baseline image, software versions, network isolation, account expiry, test data, model/provider status, reset function, smoke tests, display, safety signage, and escalation contacts. Record readiness on an opening checklist.

**During a session:** Confirm the safety briefing, assign a session identifier, protect the answer path until needed, assist without taking over, monitor for out-of-scope behavior, verify scoring, and prevent participant access to administrative functions.

**Between sessions:** Export approved aggregate metrics, run the reset, inspect the health-check result, replace physical materials, and record technical or safety issues.

**After closing:** Revoke temporary access, shut down services safely, reconcile equipment, preserve approved incident and aggregate evaluation records, delete unnecessary session data, and document lessons for the next day.

### 8.4 Facilitator Preparation

Facilitators should complete the activity as both participant and operator before the event. Training should include the intended learning points, common misconceptions, hint ladder, scoring standard, accessibility adjustments, environment reset, stop conditions, and escalation procedure. A concise runbook and offline demonstration backup should be available at every station.

## 9. Safety Security and Legal Considerations

### 9.1 Primary Risks

| Risk | Potential consequence | Required treatment |
| --- | --- | --- |
| Agent reaches a real service | Unauthorized action, data exposure, or service disruption | Mock services only; deny external network paths; verify isolation before opening. |
| Prompt injection changes behavior | Unsafe recommendation, tool misuse, or misleading output | Trust labels, instruction/data separation, schema validation, policy, and approval. |
| Excessive permissions | A single failure has unnecessary impact | Per-session identity, least privilege, narrow allowlisted tools, simulation-only actions. |
| Secret or personal-data exposure | Privacy harm or credential compromise | Synthetic data, no production secrets, output/log redaction, session deletion. |
| Participant escapes the exercise scope | Harm to venue or third-party systems | Clear rules, event-owned targets, monitoring, network controls, and immediate stop procedure. |
| Container or station compromise | Cross-session contamination or persistence | Non-privileged containers, read-only baseline, resource limits, destruction and recreation. |
| Model/API outage or cost exhaustion | Lab interruption or unexpected expense | Local/precomputed fallback, quotas, rate limits, alerts, and cost cap. |
| Duplicate or replayed action | Inaccurate score or repeated simulated containment | Correlation identifiers, idempotency keys, and action-state checks. |
| Queue, cable, power, or heat issue | Physical injury or equipment damage | Venue-approved layout, cable covers, protected power, ventilation, and capacity limits. |

### 9.2 Rules of Engagement

- Participants may interact only with the supplied interface, accounts, scenarios, and targets.
- Scanning, testing, or accessing venue, public, sponsor, facilitator, or other participant systems is prohibited.
- No real credentials, personal data, malware, destructive payloads, or production indicators may be introduced.
- Challenge techniques must remain inside the assigned session environment.
- Facilitators may pause or end a session immediately if scope or safety is uncertain.
- Security issues in the lab platform should be reported privately to the activity lead rather than demonstrated against other sessions.

### 9.3 Control Layers

**Preventive controls:** isolated network; event-owned devices; synthetic data; least-privilege session identities; container isolation; no arbitrary execution; narrow tool contracts; schema and parameter validation; deterministic policy; exact-action approval; rate and resource limits.

**Detective controls:** structured audit events; correlation identifiers; tool and policy denial logs; service health monitoring; facilitator dashboard; alerts for repeated failures, out-of-scope requests, and resource exhaustion.

**Recovery controls:** stop switch; credential revocation; session destruction; known-good rebuild; offline fallback; incident recording; equipment isolation; and organizer escalation.

### 9.4 Data and Privacy

The preferred design collects no participant identity in the lab platform. If organizers need registration, certificates, prizes, photographs, or identifiable scores, those processes should be separated from the technical environment and covered by clear notice, purpose limitation, retention, access, and deletion rules. Logs should contain synthetic scenario values and opaque session identifiers only.

Ghana's Cyber Security Authority publishes the [Cybersecurity Act 2020](https://www.csa.gov.gh/resources/cybersecurity_Act_2020%28Act_1038%29.pdf), the Data Protection Act 2012, and the Electronic Transactions Act 2008 among its relevant acts and policies ([CSA resources](https://www.csa.gov.gh/resources.php)). The CSA also publishes current licensing and accreditation guidance that includes cybersecurity training within the services it regulates ([CSA licensing FAQ](https://www.csa.gov.gh/licensing-and-accreditation-faq)). NESTCON should obtain qualified Ghanaian legal and compliance advice on the event, organizers, instructors, data processing, and any applicable licensing or accreditation requirements. This report does not determine legal applicability.

### 9.5 Deployment Gate

The activity must not open to participants until the lead confirms:

- Written authorization and rules of engagement are approved.
- All targets and data are event-owned or synthetic.
- Network isolation and egress restrictions have been tested.
- No production credentials or connectors exist in the environment.
- State-changing operations are simulation-only.
- Reset, stop, and recovery procedures have passed testing.
- Staff know incident and medical/venue escalation routes.
- Participant notice and any consent process are ready.
- Required organizer, venue, legal, privacy, and regulatory reviews are complete.

## 10. Participant Experience and Learning Outcomes

- Target participant levels
- Measurable learning outcomes
- Participant takeaway beginning with “After completing this activity, I can…”

## 11. Cost and Resource Assessment

List hardware, software, infrastructure, consumables, specialist equipment, quantities, purpose, availability, and dated cost assumptions. Give an overall low, medium, or high cost rating.

## 12. Feasibility Assessment

- Score technical, cost, staffing, safety, beginner accessibility, engagement, setup complexity, and scalability from 1 to 5.
- Identify implementation challenges and proposed solutions.

## 13. Final Recommendation

Choose and justify one outcome: recommended, recommended with modifications, pilot first, clinic or demonstration only, flex-table activity, or not recommended. Describe the recommended NESTCON implementation concisely.

## 14. Future Development

Consider advanced challenges, additional equipment, industry involvement, sponsorship, a Road to NESTCON pilot, year-round community use, and future independent-village potential.

## 15. Sources and References

List every source, its type, link or reference, and the information used. Keep working notes in the research log.

## 16. Executive Summary

Limit this section to one page. State the content, what it is, why it belongs in the zone, proposed participant experience, major resources, staffing, complexity, cost, and final recommendation.

## Appendices

- Detailed bill of materials
- Activity runbooks
- Architecture and data-flow diagrams
- Findings register
- Research sources
- Prototype results
