# Attack and Defend Replay Learning Guide

## What this exercise demonstrates

The replay runs five fictional inputs against the protected, deterministic workflow. It displays a **counterfactual risk** (what a poorly designed agent might do), the **observed result** from this prototype, and the **control** responsible. It does not create or run an agent with unsafe permissions, and a PASS does not prove general prompt-injection resistance. No LLM or real security tool is involved.

## Read each case

| Case | Trust boundary to notice | Expected result |
| --- | --- | --- |
| Instruction in alert text | Untrusted description must not authorize a block | Injected and normal alerts produce the same policy decision; no action executes |
| Malformed IP address | Input must be valid before investigation or tool use | Parser rejects it before triage |
| Missing evidence | A recommendation needs actual local evidence | Action is denied rather than invented |
| Tool outside allowlist | A recommendation cannot create a new capability | Gateway rejects the unknown tool |
| Duplicate event | A replay should not repeat work or actions | Prior result is returned and only one audit event exists |

## Try it

1. Start `python3 -m cyber_agent.web` from the repository and open `http://127.0.0.1:8765`.
2. Load **Alert with untrusted instruction** and read the description. Identify which sentence is data masquerading as an instruction.
3. Check the recommendation and policy. The agent may recommend analyst review, but it cannot skip approval.
4. Select **Run safety replay**. For each case, state the input, expected safe result, observed result, and enforcing control in your own words.
5. Reset and try the inconclusive case. Notice that the interface does not offer a containment proposal.

## What this does not prove

The description does not enter an LLM today, so this replay demonstrates a **software trust boundary**, not measured resistance of a model to prompt injection. The approval is a local label, not authenticated identity. State and audit are in memory. Before a public pilot, the team should test the learning activity with participants and record real completion and reset times.
