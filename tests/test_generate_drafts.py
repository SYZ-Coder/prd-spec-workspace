from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.extract_initial_dsl import write_initial_outputs
from scripts.generate_drafts import write_draft_outputs


SAMPLE_PRD = """\u8ba2\u5355\u652f\u4ed8\u9700\u6c42\u3002

\u4e1a\u52a1\u89c4\u5219
- \u63d0\u4ea4\u652f\u4ed8\u524d\u5fc5\u987b\u5b8c\u6210\u5b9e\u540d\u6821\u9a8c\uff1b
- \u652f\u4ed8\u6210\u529f\u540e\u8df3\u8f6c\u652f\u4ed8\u7ed3\u679c\u9875\uff1b
- \u652f\u4ed8\u5931\u8d25\u65f6\u9700\u63d0\u793a\u539f\u56e0\uff1b

\u9875\u9762
- \u652f\u4ed8\u9875\uff1a\u5c55\u793a\u8ba2\u5355\u4fe1\u606f\u5e76\u63d0\u4ea4\u652f\u4ed8\uff1b
- \u652f\u4ed8\u7ed3\u679c\u9875\uff1a\u5c55\u793a\u652f\u4ed8\u6210\u529f\u6216\u5931\u8d25\u72b6\u6001\uff1b
"""

SAMPLE_CONTEXT = """API \u5305\u542b create-payment \u548c query-payment-result\u3002"""


class GenerateDraftsTests(unittest.TestCase):
    def test_generate_prd_and_openspec_drafts_from_generic_dsl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            (workspace / "inputs" / "prd").mkdir(parents=True)
            (workspace / "inputs" / "notes").mkdir(parents=True)
            (workspace / "inputs" / "context").mkdir(parents=True)
            (workspace / "inputs" / "screenshots").mkdir(parents=True)
            (workspace / "working").mkdir(parents=True)
            (workspace / "openspec" / "changes" / "payment-flow" / "specs" / "order").mkdir(parents=True)
            (workspace / "inputs" / "prd" / "sample.md").write_text(SAMPLE_PRD, encoding="utf-8")
            (workspace / "inputs" / "context" / "api.md").write_text(SAMPLE_CONTEXT, encoding="utf-8")

            write_initial_outputs(workspace)
            write_draft_outputs(workspace, "payment-flow", "order", "\u8ba2\u5355\u652f\u4ed8\u9700\u6c42\u9a8c\u6536")

            generated_prd = (workspace / "working" / "generated-prd.md").read_text(encoding="utf-8")
            spec = (workspace / "openspec" / "changes" / "payment-flow" / "specs" / "order" / "spec.md").read_text(encoding="utf-8")

            self.assertIn("\u8ba2\u5355\u652f\u4ed8\u9700\u6c42\u9a8c\u6536", generated_prd)
            self.assertIn("\u652f\u4ed8\u9875", generated_prd)
            self.assertIn("\u652f\u4ed8\u7ed3\u679c\u9875", generated_prd)
            self.assertIn("\u901a\u7528\u4ea7\u54c1\u9700\u6c42", generated_prd)
            self.assertIn("\u8ba2\u5355\u652f\u4ed8\u9700\u6c42", spec)


if __name__ == "__main__":
    unittest.main()
