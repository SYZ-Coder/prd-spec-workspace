from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.extract_initial_dsl import write_initial_outputs
from scripts.generate_derivatives import write_derivative_outputs


SAMPLE_PRD = """用户登录注册需求。

业务规则
- 注册时手机号必须唯一；
- 验证码有效期为5分钟；
- 登录成功后进入首页；

页面
- 登录页：支持验证码登录和密码登录；
- 注册页：支持手机号验证码注册；
- 首页：承接登录成功后的默认落点；
"""

SAMPLE_CONTEXT = """API 包含 send-code、register、login。"""


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
            self.assertIn("# 流程图文档", flow)
            self.assertIn("## 页面流转总图", flow)
            self.assertIn("P_登录页".upper(), testcases)
            self.assertIn("## 功能测试用例", testcases)
            self.assertIn("规则覆盖矩阵", testcases)
            self.assertIn("# 接口契约草案", contracts)
            self.assertIn("/api/generic/", contracts)
            self.assertIn("title:", openapi)
            self.assertNotIn("P_登录成功后进入首页".upper(), testcases)


if __name__ == "__main__":
    unittest.main()
