# Teammate Pilot Guide

This short pilot checks whether the **Cyber Agent Lab** is understandable to a first-time learner. It is not a test of a live AI model or a production security system. All alerts and IP addresses are synthetic, all actions are simulated, and no API key is required.

## Get the lab running

You need Git and Python 3.10 or newer. In Terminal, run:

```bash
git clone https://github.com/YaaNuamah/ai-agent-security-lab.git
cd ai-agent-security-lab
python3 -m cyber_agent.web
```

Open `http://127.0.0.1:8765` **on the same computer**. Leave Terminal open while testing. The address is local to your computer; it is not a public website. If port 8765 is already in use, stop the older lab process with `Ctrl+C`, or start this copy with `python3 -m cyber_agent.web --port 8766` and open `http://127.0.0.1:8766` instead. Press `Ctrl+C` in Terminal when finished.

If you already cloned the repository, update it from inside that directory with `git pull` before starting the lab. See [Run and Test](run-and-test.md) for command-line checks and troubleshooting.

## Try the walkthrough (about 10–15 minutes)

1. Load **Inconclusive alert**. Compare the recorded model-style suggestion with the independent policy decision. Can you explain why no containment proposal is available?
2. Select **Run safety replay**. Note whether all six checks say **PASS**. These are fixed regression checks, not proof that every attack is prevented.
3. Select **Reset lab**, then load **Suspicious alert**. Read the evidence and follow **Propose simulation → Approve demo request → Run simulation**. Confirm that the outcome says no real action was executed.
4. If time permits, reset and load **Alert with untrusted instruction**. Identify the instruction embedded in the alert description and check whether it changes the policy.

The recorded assessment is a saved example, **not a live model**. The demo approval is a local click, **not authenticated authorization**. Do not enter real IP addresses, customer alerts, credentials, or private data.

## Send feedback to Yaa

Please report observations, not just whether the buttons worked. You can copy this template into a message:

```text
Cyber Agent Lab pilot feedback
Device/OS and Python version (optional):
Could you start the lab? Yes / No — where did you get stuck?
Did all six safety replay checks show PASS? Yes / No — which failed?
Did the suspicious case end with no real action executed? Yes / No / Not reached
Why did the inconclusive case stop even though the saved assessment suggested review_block?
What was confusing or unclear?
What one change would help the next learner most?
Approximate time taken (optional):
```

If the page or a command fails, include the exact error text, but remove any personal paths or sensitive data before sharing. Feedback from one or two learners is useful for improving the next iteration; it should not be presented as a measured event-wide success rate.
