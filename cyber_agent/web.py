"""Single-user, localhost-only web walkthrough for the offline Agent Lab."""

from __future__ import annotations

import argparse
import json
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from secrets import token_urlsafe
from urllib.parse import parse_qs

from .core import Agent, ValidationError
from .assessment import RecordedAdapter
from .replay import run_replay
from .simulation import AuthorizationError, ProposedAction, SimulationGateway


FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
CASES = {
    "alert-suspicious.json": "Suspicious alert",
    "alert-inconclusive.json": "Inconclusive alert",
    "alert-injection.json": "Alert with untrusted instruction",
}


def _load(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class LabSession:
    """One disposable session for a local facilitator or learner."""

    def __init__(self):
        self.csrf = token_urlsafe(32)
        self.reset()

    def reset(self):
        self.case_name: str | None = None
        self.alert: dict | None = None
        self.agent: Agent | None = None
        self.gateway: SimulationGateway | None = None
        self.result: dict | None = None
        self.proposal: ProposedAction | None = None
        self.approval_token: str | None = None
        self.outcome: dict | None = None
        self.replay_results: list[dict] | None = None

    def start(self, case_name: str):
        if case_name not in CASES:
            raise ValidationError("choose one of the three synthetic cases")
        self.reset()
        self.case_name = case_name
        self.alert = _load(case_name)
        self.agent = Agent(_load("evidence.json"), RecordedAdapter(_load("recorded-assessments.json")))
        self.result = self.agent.process(self.alert)
        self.gateway = SimulationGateway(self.agent)

    def propose(self):
        if self.gateway is None or self.result is None:
            raise AuthorizationError("start a case first")
        if self.proposal is not None:
            raise AuthorizationError("a simulation has already been proposed")
        self.proposal = self.gateway.propose(
            self.result["event_id"], self.result["indicator"], 60
        )

    def approve(self):
        if self.gateway is None or self.proposal is None:
            raise AuthorizationError("propose a simulation first")
        if self.approval_token is not None:
            raise AuthorizationError("this request is already approved")
        self.approval_token = self.gateway.approve(self.proposal.request_id, "demo_analyst")

    def execute(self):
        if self.gateway is None or self.proposal is None or self.approval_token is None:
            raise AuthorizationError("a local demo approval is required")
        if self.outcome is not None:
            raise AuthorizationError("simulation already completed")
        self.outcome = self.gateway.execute(
            self.proposal.request_id, self.approval_token,
            indicator=self.proposal.indicator,
            duration_minutes=self.proposal.duration_minutes,
        )

    def replay(self):
        if self.result is None:
            raise AuthorizationError("start a case first")
        self.replay_results = run_replay()


def _form(action: str, label: str, csrf: str, extra: str = "") -> str:
    return (f'<form method="post" action="{action}">'
            f'<input type="hidden" name="csrf" value="{escape(csrf)}">'
            f'{extra}<button type="submit">{escape(label)}</button></form>')


def render_page(session: LabSession, notice: str = "", error: bool = False) -> str:
    case_options = "".join(
        f'<option value="{escape(name)}">{escape(label)}</option>'
        for name, label in CASES.items()
    )
    choose = _form(
        "/start", "Load synthetic case", session.csrf,
        f'<label for="case">Choose a case</label><select id="case" name="case">{case_options}</select>',
    )
    status = (f'<p class="notice{" error" if error else ""}" role="status">'
              f'{escape(notice)}</p>') if notice else ""
    content = '<p>Choose a case to see how the agent handles evidence, policy, and a proposed action.</p>'
    if session.alert is not None and session.result is not None:
        result = session.result
        evidence = _load("evidence.json")
        matched = [row for row in evidence if row["evidence_id"] in result["evidence_ids"]]
        evidence_html = "".join(
            f'<li><strong>{escape(row["source"])}</strong> — {escape(row["summary"])} '
            f'<span class="muted">({escape(row["evidence_id"])})</span></li>'
            for row in matched
        ) or "<li>No local evidence found.</li>"
        content = (
            f'<section><h2>1. Untrusted alert</h2><p><strong>Case:</strong> {escape(CASES[session.case_name])}</p>'
            f'<p><strong>Indicator:</strong> <code>{escape(session.alert["indicator"])}</code></p>'
            f'<p class="alert-text">{escape(session.alert["description"])}</p>'
            '<p class="muted">The description is data. It cannot change the policy or authorize a tool.</p></section>'
            f'<section><h2>2. Evidence</h2><ul>{evidence_html}</ul></section>'
            f'<section><h2>3. Decision</h2><p><strong>Recommendation:</strong> {escape(result["recommendation"])}</p>'
            f'<p><strong>Policy:</strong> {escape(result["policy_decision"])}</p>'
            f'<p>{escape(result["reason"])}</p>'
            '<p class="safe">Real action executed: No</p></section>'
        )
        assessment = result["model_assessment"]
        if assessment is not None:
            content += (
                '<section><h2>Recorded model-style assessment</h2>'
                '<p class="muted">This is a saved example response, not a live AI model. It may be wrong and cannot authorize an action.</p>'
                f'<p><strong>Classification:</strong> {escape(assessment["classification"])}</p>'
                f'<p><strong>Summary:</strong> {escape(assessment["summary"])}</p>'
                f'<p><strong>Suggested action:</strong> {escape(assessment["suggested_action"])}</p>'
                f'<p><strong>Cited evidence:</strong> {escape(", ".join(assessment["evidence_ids"]))}</p>'
                '</section>'
            )
        elif result["model_status"] != "not_configured":
            content += '<section><h2>Recorded model-style assessment</h2><p>Response unavailable or invalid. The independent policy still applies.</p></section>'
        if result["policy_decision"] == "approval_required":
            if session.proposal is None:
                content += '<section><h2>4. Propose mock action</h2><p>A 60-minute IP block is proposed in simulation only.</p>'
                content += _form("/propose", "Propose simulation", session.csrf) + '</section>'
            elif session.approval_token is None:
                content += (f'<section><h2>4. Review mock action</h2>'
                            f'<p><code>{escape(session.proposal.tool)}</code> for '
                            f'<code>{escape(session.proposal.indicator)}</code>, '
                            f'{session.proposal.duration_minutes} minutes.</p>'
                            '<p class="muted">Approval is a local demo click, not an authenticated user decision.</p>')
                content += _form("/approve", "Approve demo request", session.csrf) + '</section>'
            elif session.outcome is None:
                content += '<section><h2>5. Approved mock action</h2><p>The gateway will recheck the exact parameters and expiry.</p>'
                content += _form("/execute", "Run simulation", session.csrf) + '</section>'
            else:
                content += ('<section><h2>5. Simulation result</h2>'
                            '<p class="safe">Status: simulated. Real action executed: No.</p></section>')
        else:
            content += '<section><h2>4. Action stopped</h2><p>Policy does not permit a containment proposal for this case.</p></section>'
        trail = list(session.agent.audit) + list(session.gateway.audit)
        trail_html = "".join(
            f'<li>{escape(str(entry.get("event", "triage")))} — '
            f'{escape(str(entry.get("policy_decision", entry.get("tool", "local record"))))}</li>'
            for entry in trail
        )
        content += f'<section><h2>Audit timeline</h2><ol>{trail_html}</ol></section>'
        content += '<section><h2>Attack and defend replay</h2>'
        content += '<p>Run six fictional checks against the protected workflow. The risk statements are counterfactual teaching examples, not observed compromises.</p>'
        content += _form("/replay", "Run safety replay", session.csrf)
        if session.replay_results is not None:
            replay_html = "".join(
                f'<li><strong>{escape(str(row["case"]))}: '
                f'{"PASS" if row["passed"] else "FAIL"}</strong><br>'
                f'Risk: {escape(str(row["risk"]))}<br>'
                f'Observed: {escape(str(row["observed"]))}<br>'
                f'Control: {escape(str(row["control"]))}</li>'
                for row in session.replay_results
            )
            content += f'<ol>{replay_html}</ol>'
        content += '</section>'
        content += _form("/reset", "Reset lab", session.csrf)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cyber Agent Lab</title><style>
body{{font:16px/1.5 system-ui,sans-serif;color:#14222b;background:#f5f7f8;margin:0}}
main{{max-width:760px;margin:0 auto;padding:2rem 1rem 4rem}}
h1{{font-size:2rem;margin-bottom:.3rem}}h2{{font-size:1.25rem;margin-top:0}}
section{{background:#fff;border:1px solid #d9e2e6;border-radius:10px;padding:1.25rem;margin:1rem 0}}
.banner{{background:#12394c;color:white;padding:.8rem 1rem;border-radius:8px;font-weight:700}}
.muted{{color:#4c626c}}.safe{{color:#126546;font-weight:700}}.alert-text{{padding:1rem;background:#f2f5f7;border-left:4px solid #7a99a9;white-space:pre-wrap}}
.notice{{padding:.8rem;background:#e7f4ed;border-radius:8px}}.error{{background:#fbe9e7;color:#7d2118}}
form{{margin:1rem 0;display:flex;gap:.7rem;align-items:center;flex-wrap:wrap}}
button,select{{font:inherit;padding:.55rem .8rem}}button{{background:#12394c;color:white;border:0;border-radius:6px;cursor:pointer}}button:hover{{background:#205b74}}
code{{word-break:break-all}}li{{margin:.4rem 0}}
</style></head><body><main><h1>Cyber Agent Lab</h1>
<p class="banner">Offline simulation • Synthetic data only • No real security actions</p>
<p>Explore how an alert moves through evidence, policy, approval, and a mock tool.</p>
{status}<section><h2>Choose a case</h2>{choose}</section>{content}
<p class="muted">Single-user local learning prototype. The demo approval is not authentication; state and audit disappear when the server stops.</p>
</main></body></html>'''


def make_handler(session: LabSession, port: int):
    class Handler(BaseHTTPRequestHandler):
        def _allowed_host(self) -> bool:
            return self.headers.get("Host") in {f"127.0.0.1:{port}", f"localhost:{port}"}

        def _send(self, html: str, status: int = 200):
            body = html.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if not self._allowed_host() or self.path != "/":
                self._send("<!doctype html><title>Not found</title><p>Page not found.</p>", 404)
                return
            self._send(render_page(session))

        def do_POST(self):
            if not self._allowed_host() or self.path not in {"/start", "/propose", "/approve", "/execute", "/replay", "/reset"}:
                self._send("<!doctype html><title>Not found</title><p>Request not allowed.</p>", 404)
                return
            origin = self.headers.get("Origin")
            # Some sandboxed in-app browsers send Origin: null for localhost forms.
            # The loopback Host check and unpredictable CSRF token remain required.
            if origin and origin not in {f"http://127.0.0.1:{port}", f"http://localhost:{port}", "null"}:
                self._send(render_page(session, "Request origin rejected.", True), 403)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length < 1 or length > 4096:
                    raise ValidationError("invalid form length")
                fields = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)
                if fields.get("csrf") != [session.csrf]:
                    self._send(render_page(session, "Form token rejected.", True), 403)
                    return
                if self.path == "/start":
                    session.start(fields.get("case", [""])[0])
                    notice = "Synthetic case loaded."
                elif self.path == "/propose":
                    session.propose()
                    notice = "Mock action proposed; review it before approval."
                elif self.path == "/approve":
                    session.approve()
                    notice = "Demo approval recorded. No real action has occurred."
                elif self.path == "/execute":
                    session.execute()
                    notice = "Simulation complete. No real action occurred."
                elif self.path == "/replay":
                    session.replay()
                    notice = "Safety replay complete. Review each observed control."
                else:
                    session.reset()
                    notice = "Lab reset."
                self._send(render_page(session, notice))
            except (ValueError, UnicodeDecodeError, OSError) as exc:
                self._send(render_page(session, str(exc), True), 400)

    return Handler


def main():
    parser = argparse.ArgumentParser(description="Start the localhost-only Agent Lab interface")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("port must be between 1024 and 65535")
    session = LabSession()
    with HTTPServer(("127.0.0.1", args.port), make_handler(session, args.port)) as server:
        print(f"Open http://127.0.0.1:{args.port} in your browser. Press Ctrl+C to stop.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nLab stopped.")


if __name__ == "__main__":
    main()
