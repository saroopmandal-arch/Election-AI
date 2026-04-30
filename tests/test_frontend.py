import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path


class InlineScriptParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self._in_script = False
        self._current = []

    def handle_starttag(self, tag, attrs):
        if tag == "script" and not dict(attrs).get("src"):
            self._in_script = True
            self._current = []

    def handle_data(self, data):
        if self._in_script:
            self._current.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._in_script:
            self.scripts.append("".join(self._current))
            self._in_script = False
            self._current = []


class FrontendTests(unittest.TestCase):
    def test_inline_scripts_are_valid_javascript(self):
        parser = InlineScriptParser()
        parser.feed(Path("index.html").read_text(encoding="utf-8"))

        self.assertGreater(len(parser.scripts), 0)
        for index, script in enumerate(parser.scripts, start=1):
            with self.subTest(script=index):
                with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as file:
                    file.write(script)
                    file_path = file.name

                result = subprocess.run(
                    ["node", "--check", file_path],
                    capture_output=True,
                    text=True,
                )

                self.assertEqual(result.returncode, 0, result.stderr)

    def test_chat_request_has_timeout_recovery(self):
        html = Path("index.html").read_text(encoding="utf-8")

        self.assertIn("AbortController", html)
        self.assertIn("timed out", html)

    def test_inactive_pages_stay_hidden_when_tailwind_display_classes_apply(self):
        html = Path("index.html").read_text(encoding="utf-8")
        compact_html = "".join(html.split())

        self.assertIn(".page:not(.active){display:none!important}", compact_html)


if __name__ == "__main__":
    unittest.main()
