# Research Log

Use this log to separate sourced evidence from interpretation and design decisions.

| Date | Source and link | Source type | What it says | Relevance to the lab | Limitation / follow-up |
| --- | --- | --- | --- | --- | --- |
| 2026-09-19 | [AI Village](https://aivillage.org/) | Official program site | AI Village combines hands-on education, red-team exercises, workshops, events, and open resources. | Supports a mixed, practical format for Z2. | High-level description; activity operations still require research. |
| 2026-09-19 | [AI Village 2023 Generative Red Team](https://aivillage.org/blog/generative-red-team/) | Official event announcement | The event used supplied laptops, timed access to models, a CTF-style points system, and participation rules. | Provides operational patterns for access, scoring, safety, and scale. | A large sponsored event is not directly comparable to NESTCON resources. |
| 2026-09-19 | [AI Village at DEF CON 34](https://aivillage.org/events/defcon-34/) | Official event page | The program included a sandboxed agentic-security CTF and a novice-friendly local-agent demonstration. | Supports isolation and distinct beginner/advanced pathways. | Need activity runbooks or retrospective evidence to assess staffing and throughput. |
| 2026-09-19 | [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Official security guidance | Identifies critical risks in autonomous and agentic AI systems, including goal hijacking, tool misuse, and identity or privilege abuse. | Provides the threat categories for Agent Under Attack. | The lab should select only risks that can be demonstrated safely and clearly. |
| 2026-09-19 | [OWASP LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) | Official security guidance | Excessive functionality, permissions, or autonomy can turn manipulated or erroneous model output into harmful action. | Supports least privilege, tool allowlisting, approval, and restricted autonomy. | Controls must be translated into participant-friendly exercises. |
| 2026-09-19 | [MITRE ATLAS SAFE AI](https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf) | Official framework report | Describes indirect prompt injection through external data sources and agent/plugin risks. | Supports the synthetic-email or alert attack scenario. | Select precise ATLAS techniques during threat-model development. |
| 2026-09-19 | [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | Official risk-management framework | Organizes continuous AI risk management into Govern, Map, Measure, and Manage. | Provides a framework for context, evaluation, controls, and improvement. | The framework is voluntary and broader than one event lab; tailor it proportionately. |
| 2026-09-19 | [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | Official NIST publication | Extends the AI RMF with considerations specific to generative AI across its lifecycle. | Supports safety, evaluation, documentation, and governance decisions. | Extract only controls relevant to the prototype and event setting. |
| 2026-09-19 | [Ghana Cyber Security Authority resources](https://www.csa.gov.gh/resources.php) | Official government regulator resource | Lists the Cybersecurity Act 2020, Data Protection Act 2012, Electronic Transactions Act 2008, and other national cybersecurity materials. | Identifies legal and policy sources for organizer review. | Applicability to NESTCON requires qualified local advice. |
| 2026-09-19 | [CSA licensing and accreditation FAQ](https://www.csa.gov.gh/licensing-and-accreditation-faq) | Official regulatory guidance | Describes Ghana's licensing/accreditation regime and includes cybersecurity training among covered services. | Flags a compliance question for organizers before delivery. | The project cannot determine whether or how the rules apply to this event. |

## Source Quality Rules

- Prefer official event pages, workshop repositories, standards, research papers, and vendor documentation.
- Record the publication or last-updated date when available.
- Use direct quotations sparingly; paraphrase accurately and retain the link.
- Label personal observations and design hypotheses as such.
- Cross-check important safety, cost, and feasibility claims.

## Search Queue

- DEF CON AI Village activities and published resources
- OWASP guidance for LLM and generative-AI applications
- MITRE ATLAS techniques relevant to agent systems
- NIST AI Risk Management Framework and Generative AI Profile
- Public agent-security labs, CTFs, and workshop repositories
- Local/offline model deployment requirements
- Event connectivity, power, equipment, and accessibility considerations in Ghana
