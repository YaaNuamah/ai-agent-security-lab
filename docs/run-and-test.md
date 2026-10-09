# Run and Test the Cyber Agent Prototype

The prototype runs entirely offline with Python's standard library. It uses synthetic data and documentation-only IP addresses. It does not need an API key, paid model, Docker, or access to a security product.

## Start from the repository

If you already have the repository on your computer, open Terminal and change to its directory. On Yaa's Mac, the existing checkout is:

```bash
cd "/Users/yaa/Library/Mobile Documents/com~apple~CloudDocs/Documents/Documents - MacBook Pro (2)/ProdCyber Jobs/Github Profile/ai-agent-security-lab"
```

If you are on another computer, clone the public repository and enter it:

```bash
git clone https://github.com/YaaNuamah/ai-agent-security-lab.git
cd ai-agent-security-lab
```

Check that you are in the correct place and that Python is available:

```bash
pwd
python3 --version
```

Use Python 3.10 or newer. There is no `pip install` step for this milestone.

## Run the baseline triage

```bash
python3 -m cyber_agent fixtures/alert-suspicious.json
python3 -m cyber_agent fixtures/alert-inconclusive.json
python3 -m cyber_agent fixtures/alert-injection.json
```

The suspicious case should say `approval_required` and `action_executed: false`. The inconclusive case should say `recommend_only`. The injection case contains an instruction in the untrusted description; it should still require approval and execute nothing.

## Run the full mock approval demonstration

```bash
python3 -m cyber_agent.demo
```

Read the output in order: `triage`, `simulated_outcome`, then `gateway_audit`. The demo creates an approval token internally to show the control flow. The result must say `status: simulated` and `real_action_executed: false`. The displayed `demo_analyst` is a label, not a login or authenticated approver.

## Use the participant-facing interface

From the repository directory, start the local server:

```bash
python3 -m cyber_agent.web
```

Open `http://127.0.0.1:8765` in a browser on the same computer. Choose a synthetic case and select **Load synthetic case**. For the suspicious or injection case, continue through **Propose simulation**, **Approve demo request**, and **Run simulation**. Compare the evidence, policy decision, and audit timeline at each step. The inconclusive case stops before approval because its policy is `recommend_only`.

After loading a case, select **Run safety replay** to see six attack-and-defend checks. Each row shows a counterfactual risk, the observed protected result, and the control being exercised. The sixth check shows a saved model-style suggestion that recommends more than policy permits. See the [attack replay guide](attack-replay-guide.md) to interpret the results. The replay does not run an unsafe agent or a live LLM.

The server listens on your computer's loopback interface only. It has no external network calls or real security tools. It is a single-user teaching interface: the approver label is not authenticated and its state disappears when you stop the server. Press `Ctrl+C` in Terminal to stop it. If port 8765 is in use, run `python3 -m cyber_agent.web --port 8766` and open `http://127.0.0.1:8766` instead.

## Run all automated tests

```bash
python3 -m unittest discover -s tests -v
```

The tests should finish with `OK`. They cover input validation, untrusted description text, no-evidence handling, duplicate events, exact-parameter approval, expiry, replay, unknown tools, HTML escaping, cross-origin form rejection, and the web walkthrough. If Python says `No module named cyber_agent`, run `pwd` and return to the repository directory. If a test fails, keep the full failure output and inspect the named test before changing code.

## Learning exercise

Open `fixtures/alert-injection.json` and compare its `description` with the output. The sentence asking for an immediate block must not bypass the policy. Then read `cyber_agent/core.py` to find the independent triage decision and `cyber_agent/simulation.py` to find where the mock gateway checks approval again. Try changing `indicator` to a real public IP; validation should reject it because this lab permits only documentation-only ranges.

Do not enter real IPs, credentials, customer alerts, or private data into the fixtures. To reset the demo, simply run the command again; its state is in memory for that process only.
