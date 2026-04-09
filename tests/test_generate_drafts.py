from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.extract_initial_dsl import write_initial_outputs
from scripts.generate_drafts import write_draft_outputs


SAMPLE_PRD = """订单支付需求。

业务规则
- 提交支付前必须完成实名校验；
- 支付成功后跳转支付结果页；
- 支付失败时需提示原因；

页面
- 支付页：展示订单信息并提交支付；
- 支付结果页：展示支付成功或失败状态；
"""

SAMPLE_CONTEXT = """API 包含 create-payment 和 query-payment-result。"""


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
            write_draft_outputs(workspace, "payment-flow", "order", "订单支付需求验收")

            generated_prd = (workspace / "working" / "generated-prd.md").read_text(encoding="utf-8")
            spec = (workspace / "openspec" / "changes" / "payment-flow" / "specs" / "order" / "spec.md").read_text(encoding="utf-8")

            self.assertIn("订单支付需求验收", generated_prd)
            self.assertIn("## 背景", generated_prd)
            self.assertIn("## 已确认事实", generated_prd)
            self.assertIn("## 待确认项", generated_prd)
            self.assertIn("支付页", generated_prd)
            self.assertIn("支付结果页", generated_prd)
            self.assertIn("通用产品需求", generated_prd)
            self.assertIn("## Requirement: 订单支付需求", spec)
            self.assertIn("## Unknowns", spec)
            self.assertIn("订单支付需求", spec)


if __name__ == "__main__":
    unittest.main()
