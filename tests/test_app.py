import os
import tempfile
import time
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

import main


class ElectionIQAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)

    def test_health_endpoint_reports_ok(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_root_serves_frontend_html(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn("ElectionIQ", response.text)

    def test_root_serves_frontend_from_app_directory(self):
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)

                response = self.client.get("/")
            finally:
                os.chdir(original_cwd)

        self.assertEqual(response.status_code, 200)
        self.assertIn("ElectionIQ", response.text)

    def test_static_route_does_not_expose_project_files(self):
        for path in ("/static/.env", "/static/main.py", "/static/requirements.txt"):
            with self.subTest(path=path):
                response = self.client.get(path)

                self.assertEqual(response.status_code, 404)

    def test_chat_uses_configured_gemini_model(self):
        with patch.object(main, "GEMINI_API_KEY", "test-key"), patch.object(
            main, "GEMINI_MODEL", "gemini-3-flash-preview", create=True
        ), patch.object(main.genai, "GenerativeModel") as model_class:
            chat_session = model_class.return_value.start_chat.return_value
            chat_session.send_message.return_value.text = "Use Form 6 to register."

            response = self.client.post(
                "/chat",
                json={
                    "messages": [{"role": "user", "content": "hello"}],
                    "user_message": "How do I register?",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"response": "Use Form 6 to register."})
        model_class.assert_called_once_with(
            model_name="gemini-3-flash-preview",
            system_instruction=main.SYSTEM_PROMPT,
        )

    def test_chat_times_out_when_gemini_does_not_respond(self):
        with patch.object(main, "GEMINI_API_KEY", "test-key"), patch.object(
            main, "GEMINI_TIMEOUT_SECONDS", 0.001, create=True
        ), patch.object(main.genai, "GenerativeModel") as model_class:
            chat_session = model_class.return_value.start_chat.return_value
            chat_session.send_message.side_effect = lambda _message: time.sleep(0.05)

            response = self.client.post(
                "/chat",
                json={"messages": [], "user_message": "Why is it stuck?"},
            )

        self.assertEqual(response.status_code, 504)
        self.assertIn("timed out", response.json()["detail"].lower())


if __name__ == "__main__":
    unittest.main()
