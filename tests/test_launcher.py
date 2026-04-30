import unittest
from pathlib import Path


class LauncherTests(unittest.TestCase):
    def test_windows_launcher_reuses_existing_electioniq_server(self):
        launcher = Path("start_electioniq.bat").read_text(encoding="utf-8")

        self.assertIn("EXISTING", launcher)
        self.assertIn("ElectionIQ is already running", launcher)

    def test_windows_launcher_uses_single_server_process(self):
        launcher = Path("start_electioniq.bat").read_text(encoding="utf-8")

        self.assertIn("python -m uvicorn main:app --host 127.0.0.1 --port %PORT%", launcher)
        self.assertNotIn("--reload", launcher)


if __name__ == "__main__":
    unittest.main()
