from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.extract_screenshot_evidence import write_screenshot_outputs


class ExtractScreenshotEvidenceTests(unittest.TestCase):
    def test_write_screenshot_outputs_builds_ocr_and_component_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            screenshots = workspace / "inputs" / "screenshots"
            working = workspace / "working"
            screenshots.mkdir(parents=True)
            working.mkdir(parents=True)

            (screenshots / "login-screen.png").write_bytes(b"fake-image")
            (screenshots / "login-screen.ocr.txt").write_text("登录页\n手机号\n验证码\n登录\n注册", encoding="utf-8")

            write_screenshot_outputs(workspace)

            ocr_payload = json.loads((working / "screenshot-ocr.json").read_text(encoding="utf-8"))
            classification_payload = json.loads((working / "page-classification.json").read_text(encoding="utf-8"))
            evidence_doc = (working / "screenshot-evidence.md").read_text(encoding="utf-8")

            self.assertEqual(1, len(ocr_payload["screenshots"]))
            self.assertIn("登录页", ocr_payload["screenshots"][0]["ocr_text"])
            self.assertEqual("登录页", classification_payload["pages"][0]["page_name"])
            self.assertIn("手机号", classification_payload["pages"][0]["components"]["fields"])
            self.assertIn("登录", classification_payload["pages"][0]["components"]["buttons"])
            self.assertIn("# Screenshot Evidence", evidence_doc)
            self.assertIn("登录页", evidence_doc)


if __name__ == "__main__":
    unittest.main()
