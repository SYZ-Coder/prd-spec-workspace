from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_dsl import validate_dsl_data


class ValidateDslTests(unittest.TestCase):
    def test_validate_dsl_reports_semantic_quality_risks(self) -> None:
        dsl = {
            "pages": [
                {
                    "id": "P_MAIN",
                    "name": "主流程页面",
                    "source": ["inputs/prd/sample.md"],
                    "goal": "展示流程入口",
                    "entry_points": ["用户进入主流程页面"],
                    "exit_points": ["完成主流程后离开"],
                    "actions": [
                        {
                            "id": "A_MAIN_1",
                            "trigger": "执行主流程页面主操作",
                            "actor": "用户",
                            "preconditions": ["输入完整"],
                            "steps": ["提交请求"],
                            "success_results": ["处理成功"],
                            "failure_results": ["处理失败"],
                        }
                    ],
                    "states": ["待处理", "成功"],
                    "dependencies": ["业务服务"],
                    "unknowns": [],
                }
            ],
            "transitions": [],
            "rules": ["支付流程需求", "支付页：展示订单并提交支付"],
            "dependencies": ["业务服务"],
            "unknowns": [],
        }

        blocking, high_risk, suggestions = validate_dsl_data(dsl)

        self.assertEqual(blocking, [])
        self.assertTrue(any("主流程页面" in item for item in high_risk))
        self.assertTrue(any("标题或需求名" in item for item in high_risk))
        self.assertTrue(any("页面声明" in item for item in high_risk))
        self.assertTrue(any("动作触发词" in item for item in suggestions))


if __name__ == "__main__":
    unittest.main()
