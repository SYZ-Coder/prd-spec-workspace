from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.extract_initial_dsl import write_initial_outputs
from scripts.generate_derivatives import write_derivative_outputs


SAMPLE_PRD = """\u7528\u6237\u767b\u5f55\u6ce8\u518c\u9700\u6c42\u3002

\u4e1a\u52a1\u89c4\u5219
- \u6ce8\u518c\u65f6\u624b\u673a\u53f7\u5fc5\u987b\u552f\u4e00\uff1b
- \u9a8c\u8bc1\u7801\u6709\u6548\u671f\u4e3a5\u5206\u949f\uff1b
- \u767b\u5f55\u6210\u529f\u540e\u8fdb\u5165\u9996\u9875\uff1b

\u9875\u9762
- \u767b\u5f55\u9875\uff1a\u652f\u6301\u9a8c\u8bc1\u7801\u767b\u5f55\u548c\u5bc6\u7801\u767b\u5f55\uff1b
- \u6ce8\u518c\u9875\uff1a\u652f\u6301\u624b\u673a\u53f7\u9a8c\u8bc1\u7801\u6ce8\u518c\uff1b
- \u9996\u9875\uff1a\u627f\u63a5\u767b\u5f55\u6210\u529f\u540e\u7684\u9ed8\u8ba4\u843d\u70b9\uff1b
"""

SAMPLE_CONTEXT = """API \u5305\u542b send-code\u3001register\u3001login\u3002"""


class GenerateDerivativesTests(unittest.TestCase):
    def test_generate_derivative_outputs_from_generic_dsl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            (workspace / "inputs" / "prd").mkdir(parents=True)
            (workspace / "inputs" / "notes").mkdir(parents=True)
            (workspace / "inputs" / "context").mkdir(parents=True)
            (workspace / "inputs" / "screenshots").mkdir(parents=True)
            (workspace / "working" / "api-contracts").mkdir(parents=True)
            (workspace / "inputs" / "prd" / "sample.md").write_text(SAMPLE_PRD, encoding="utf-8")
            (workspace / "inputs" / "context" / "api.md").write_text(SAMPLE_CONTEXT, encoding="utf-8")

            write_initial_outputs(workspace)
            write_derivative_outputs(workspace)

            flow = (workspace / "working" / "generated-flow.md").read_text(encoding="utf-8")
            testcases = (workspace / "working" / "generated-testcases.md").read_text(encoding="utf-8")
            contracts = (workspace / "working" / "generated-api-contracts.md").read_text(encoding="utf-8")
            openapi = (workspace / "working" / "api-contracts" / "openapi.yaml").read_text(encoding="utf-8")

            self.assertIn("```mermaid", flow)
            self.assertIn("P_\u767b\u5f55\u9875".upper(), testcases)
            self.assertIn("\u89c4\u5219\u8986\u76d6\u77e9\u9635", testcases)
            self.assertIn("/api/generic/", contracts)
            self.assertIn("title:", openapi)
            self.assertNotIn("P_\u767b\u5f55\u6210\u529f\u540e\u8fdb\u5165\u9996\u9875".upper(), testcases)


if __name__ == "__main__":
    unittest.main()
