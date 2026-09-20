# Findings Register

Record evidence-backed observations and track how each one changes the proposed lab.

| ID | Finding | Evidence | Impact | Recommendation | Confidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | Practical AI security events use multiple participation formats rather than relying on lectures alone. | AI Village official program and DEF CON event pages | A layered experience can serve beginners and advanced participants in the same zone. | Use a first win, guided lab, demonstration, and optional challenge. | High | Adopted for design |
| F-002 | An agentic challenge should run against sandboxed targets and controlled inference or tooling. | AI Village DEF CON 34 event page | Isolation reduces risk and makes challenge behavior more consistent. | Use synthetic data, a simulation-only tool gateway, and resettable containers or local services. | Medium | Validate in prototype |
| F-003 | Untrusted external content can manipulate an agent through indirect prompt injection. | MITRE ATLAS SAFE AI and OWASP guidance | A realistic security agent may ingest malicious instructions from the material it analyzes. | Make untrusted-alert handling the central attack scenario. | High | Adopted for design |
| F-004 | Excessive functionality, permissions, or autonomy can convert model error or manipulation into harmful action. | OWASP LLM06 Excessive Agency and Agentic Top 10 | The lab must teach authorization and least privilege, not prompt wording alone. | Separate AI recommendations from deterministic policy and allowlisted execution. | High | Adopted for design |
| F-005 | AI risk should be mapped, measured, managed, and governed throughout the lifecycle. | NIST AI RMF | The lab needs explicit objectives, tests, metrics, controls, and improvement steps. | Evaluate attack success, blocked unsafe actions, audit completeness, participant learning, and reset time. | High | Open |
| F-006 | A single scenario can support progressive learning when each layer reuses the same system and adds complexity. | NESTCON research template and proposed activity mapping | Reuse can reduce setup burden and make the relationship between building, attacking, and defending clear. | Use the suspicious-IP triage scenario for the first win, guided lab, demonstration, and advanced challenge. | Medium | Validate in pilot |
| F-007 | The activity design depends on unconfirmed operational assumptions. | Current project inputs | Duration, capacity, cost, and staffing cannot be finalized without venue and participant information. | Record working assumptions now and replace them with measured or organizer-confirmed values. | High | Open |
| F-008 | The full hands-on design is feasible but not ready for festival-floor deployment without a pilot. | Preliminary feasibility assessment across technical, cost, staffing, safety, accessibility, engagement, setup, and scalability factors | Unvalidated reset, timing, staffing, offline, and compliance assumptions could undermine safety or throughput. | Run a two-station Road to NESTCON pilot and apply explicit go/no-go criteria. | High | Open |
| F-009 | Reusing or borrowing equipment is the main lever for reducing cash cost. | Draft resource assessment | New hardware purchases could move the project from medium to high cost without necessarily improving the initial learning validation. | Validate the minimum pilot on borrowed or sponsored equipment before procurement. | Medium | Open |

## Finding Template

### F-XXX — Finding title

- **Observation:** What was found.
- **Evidence:** Source, experiment, screenshot, log, or measurement.
- **Why it matters:** Effect on participants, organizers, safety, cost, or delivery.
- **Recommendation:** Specific design or operational response.
- **Confidence:** Low, medium, or high, with the reason.
- **Validation needed:** Test or information required before finalizing.
