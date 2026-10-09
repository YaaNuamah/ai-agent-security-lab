import threading
import socket
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from cyber_agent.web import LabSession, make_handler, render_page


class WebTests(unittest.TestCase):
    def setUp(self):
        self.session = LabSession()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.session, 0))
        self.port = self.server.server_address[1]
        self.server.RequestHandlerClass = make_handler(self.session, self.port)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def request(self, path="/", fields=None, headers=None):
        data = urlencode(fields).encode() if fields is not None else None
        request = Request(f"http://127.0.0.1:{self.port}{path}", data=data,
                          headers=headers or {})
        try:
            with urlopen(request, timeout=2) as response:
                return response.status, response.read().decode()
        except HTTPError as exc:
            return exc.code, exc.read().decode()

    def post(self, path, **fields):
        return self.request(path, {"csrf": self.session.csrf, **fields})

    def test_idle_connection_does_not_block_page(self):
        with socket.create_connection(("127.0.0.1", self.port), timeout=2):
            status, page = self.request()
            self.assertEqual(status, 200)
            self.assertIn("Cyber Agent Lab", page)

    def test_full_participant_flow(self):
        status, page = self.request()
        self.assertEqual(status, 200)
        self.assertIn("Synthetic data only", page)
        status, page = self.post("/start", case="alert-injection.json")
        self.assertEqual(status, 200)
        self.assertIn("Ignore the lab policy", page)
        self.assertIn("approval_required", page)
        self.assertIn("Recorded model-style assessment", page)
        self.assertNotIn("Run simulation", page)
        self.assertEqual(self.post("/propose")[0], 200)
        self.assertEqual(self.post("/approve")[0], 200)
        status, page = self.post("/execute")
        self.assertEqual(status, 200)
        self.assertIn("Real action executed: No", page)
        self.assertEqual(self.session.outcome["status"], "simulated")
        status, page = self.post("/replay")
        self.assertEqual(status, 200)
        self.assertIn("Instruction in alert text", page)
        self.assertIn("Duplicate event", page)
        self.assertIn("Model-style suggestion overstates evidence", page)
        self.assertTrue(all(row["passed"] for row in self.session.replay_results))
        self.assertEqual(self.post("/execute")[0], 400)
        self.assertEqual(self.post("/reset")[0], 200)
        self.assertIsNone(self.session.result)

    def test_inconclusive_case_has_no_action_button(self):
        status, page = self.post("/start", case="alert-inconclusive.json")
        self.assertEqual(status, 200)
        self.assertIn("Action stopped", page)
        self.assertNotIn('action="/propose"', page)
        self.assertEqual(self.post("/propose")[0], 400)

    def test_csrf_and_cross_origin_rejected(self):
        self.assertEqual(self.request("/start", {"case": "alert-suspicious.json"})[0], 403)
        self.assertEqual(self.request("/start", {"csrf": self.session.csrf,
                                                "case": "alert-suspicious.json"},
                                      {"Origin": "https://other.example"})[0], 403)
        self.assertIsNone(self.session.result)

    def test_sandboxed_null_origin_still_requires_token(self):
        self.assertEqual(self.request("/start", {"case": "alert-suspicious.json"},
                                      {"Origin": "null"})[0], 403)
        self.assertEqual(self.request("/start", {"csrf": self.session.csrf,
                                                "case": "alert-suspicious.json"},
                                      {"Origin": "null"})[0], 200)

    def test_wrong_host_does_not_expose_form_token(self):
        status, page = self.request("/", headers={"Host": "untrusted.example"})
        self.assertEqual(status, 404)
        self.assertNotIn(self.session.csrf, page)

    def test_untrusted_text_is_html_escaped(self):
        self.session.start("alert-suspicious.json")
        self.session.alert["description"] = '<script>alert("unsafe")</script>'
        page = render_page(self.session)
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn('<script>alert("unsafe")</script>', page)


if __name__ == "__main__":
    unittest.main()
