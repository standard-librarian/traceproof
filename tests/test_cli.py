from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TraceproofCliTest(unittest.TestCase):
    def test_capture_and_replay(self) -> None:
        tmp_path = Path(self.id().replace(".", "_"))
        tmp_path.mkdir(exist_ok=True)
        self.addCleanup(lambda: tmp_path.exists() and tmp_path.rmdir())

        bundle = tmp_path / "bundle.json"
        capture = subprocess.run(
            [
                sys.executable,
                "-m",
                "traceproof.cli",
                "capture",
                str(ROOT / "examples" / "failed_run.json"),
                "--output",
                str(bundle),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            env={"PYTHONPATH": str(ROOT / "src")},
        )
        self.assertIn("redactions:", capture.stdout)

        payload = json.loads(bundle.read_text(encoding="utf-8"))
        self.assertGreaterEqual(payload["redaction_report"]["count"], 2)

        replay = subprocess.run(
            [
                sys.executable,
                "-m",
                "traceproof.cli",
                "replay",
                str(bundle),
                "--candidate",
                str(ROOT / "examples" / "fixed_run.json"),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            env={"PYTHONPATH": str(ROOT / "src")},
        )
        self.assertIn("diff:", replay.stdout)
        self.assertIn("$.output.text", replay.stdout)

        bundle.unlink()
        tmp_path.rmdir()


if __name__ == "__main__":
    unittest.main()
