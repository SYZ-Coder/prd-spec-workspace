from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.extract_initial_dsl import build_initial_dsl, extract_rules_from_text, write_initial_outputs


AUTH_PRD = """用户登录注册需求。

业务规则
- 注册时手机号必须唯一；
- 验证码有效期为5分钟；
- 密码长度必须为8到20位，且至少包含字母和数字；
- 登录成功后进入首页；

页面
- 登录页：支持验证码登录和密码登录；
- 注册页：支持手机号验证码注册；
- 找回密码页：支持重置密码；
- 首页：承接登录成功后的默认落点；
"""

AUTH_CONTEXT = """API 包含 send-code、register、login、reset-password。"""

PAYMENT_PRD = """订单支付退款需求。

业务规则
- 支付成功后进入结果页；
- 退款失败时提示原因；

页面
- 支付页：展示订单信息并提交支付；
- 结果页：展示支付结果并支持发起退款；
"""

PAYMENT_CONTEXT = """API 包含 create-payment、refund-payment、query-payment-result。"""

ANALYTICS_PRD = """分析报表需求。

业务规则
- 报表数据需要实时刷新；

页面
- 分析看板：支持导出报表；
"""


class ExtractInitialDslTests(unittest.TestCase):
    def test_extract_rules_from_text_filters_titles_and_page_declarations(self) -> None:
        rules = extract_rules_from_text(AUTH_PRD)

        self.assertIn("注册时手机号必须唯一", rules)
        self.assertIn("验证码有效期为5分钟", rules)
        self.assertIn("登录成功后进入首页", rules)
        self.assertNotIn("用户登录注册需求", rules)
        self.assertFalse(any(rule.startswith("登录页：") for rule in rules))
        self.assertFalse(any(rule.startswith("注册页：") for rule in rules))

    def test_build_initial_dsl_extracts_generic_pages_actions_and_transitions(self) -> None:
        dsl, _, _, shared_rules = build_initial_dsl(
            prd_text=AUTH_PRD,
            note_text="",
            screenshot_names=[],
            prd_sources=["inputs/prd/sample.md"],
            context_text=AUTH_CONTEXT,
        )

        pages = {page["name"]: page for page in dsl["pages"]}
        self.assertEqual(dsl["meta"]["domain"], "generic")
        self.assertIn("登录页", pages)
        self.assertIn("注册页", pages)
        self.assertIn("找回密码页", pages)
        self.assertIn("首页", pages)
        self.assertIn("提交登录", {action["trigger"] for action in pages["登录页"]["actions"]})
        self.assertIn("提交注册", {action["trigger"] for action in pages["注册页"]["actions"]})
        self.assertTrue(
            any(
                transition["from_page"] == pages["登录页"]["id"] and transition["to_page"] == pages["首页"]["id"]
                for transition in dsl["transitions"]
            )
        )
        self.assertIn("## 准入与校验规则", shared_rules)

    def test_build_initial_dsl_extracts_business_actions_from_page_descriptions(self) -> None:
        dsl, _, _, _ = build_initial_dsl(
            prd_text=PAYMENT_PRD,
            note_text="",
            screenshot_names=[],
            prd_sources=["inputs/prd/payment.md"],
            context_text=PAYMENT_CONTEXT,
        )

        pages = {page["name"]: page for page in dsl["pages"]}
        result_actions = {action["trigger"] for action in pages["结果页"]["actions"]}
        self.assertIn("发起退款", result_actions)
        self.assertTrue(
            any(
                transition["from_page"] == pages["支付页"]["id"] and transition["to_page"] == pages["结果页"]["id"]
                for transition in dsl["transitions"]
            )
        )

    def test_build_initial_dsl_supports_user_overrides(self) -> None:
        overrides = {
            "page_suffixes": ["看板"],
            "action_prefixes": ["导出"],
            "rule_keywords": ["实时刷新"],
        }
        dsl, _, _, _ = build_initial_dsl(
            prd_text=ANALYTICS_PRD,
            note_text="",
            screenshot_names=[],
            prd_sources=["inputs/prd/analytics.md"],
            context_text="",
            overrides=overrides,
        )

        pages = {page["name"]: page for page in dsl["pages"]}
        self.assertIn("分析看板", pages)
        self.assertIn("导出报表", {action["trigger"] for action in pages["分析看板"]["actions"]})
        self.assertIn("报表数据需要实时刷新", dsl["rules"])

    def test_write_initial_outputs_creates_non_empty_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            (workspace / "inputs" / "prd").mkdir(parents=True)
            (workspace / "inputs" / "notes").mkdir(parents=True)
            (workspace / "inputs" / "context").mkdir(parents=True)
            (workspace / "inputs" / "screenshots").mkdir(parents=True)
            (workspace / "working").mkdir(parents=True)
            (workspace / "inputs" / "prd" / "sample.md").write_text(AUTH_PRD, encoding="utf-8")
            (workspace / "inputs" / "context" / "api.md").write_text(AUTH_CONTEXT, encoding="utf-8")
            (workspace / "extractor-overrides.json").write_text(json.dumps({"action_prefixes": ["导出"]}, ensure_ascii=False), encoding="utf-8")

            write_initial_outputs(workspace)

            merged_dsl = json.loads((workspace / "working" / "merged-dsl.json").read_text(encoding="utf-8"))
            self.assertEqual(merged_dsl["meta"]["domain"], "generic")
            self.assertTrue(merged_dsl["pages"])
            self.assertTrue(merged_dsl["rules"])
            self.assertIn("extractor_overrides", merged_dsl)
            self.assertIn("knowledge_graph", merged_dsl)
            evidence_map = (workspace / "working" / "evidence-map.md").read_text(encoding="utf-8")
            self.assertIn("# Evidence Map", evidence_map)
            self.assertIn("Confidence", evidence_map)
            self.assertIn("Low Confidence Checklist", evidence_map)

    def test_write_initial_outputs_merges_optional_vision_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            (workspace / "inputs" / "prd").mkdir(parents=True)
            (workspace / "inputs" / "notes").mkdir(parents=True)
            (workspace / "inputs" / "context").mkdir(parents=True)
            (workspace / "inputs" / "screenshots").mkdir(parents=True)
            (workspace / "working").mkdir(parents=True)
            (workspace / "inputs" / "screenshots" / "login.png").write_bytes(b"fake-image")
            (workspace / "working" / "screenshot-ocr.json").write_text(
                json.dumps(
                    {
                        "screenshots": [
                            {
                                "screenshot": "login.png",
                                "ocr_text": "登录页\n手机号\n验证码\n登录",
                                "confidence": 0.84,
                            }
                        ]
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            (workspace / "working" / "page-classification.json").write_text(
                json.dumps(
                    {
                        "pages": [
                            {
                                "screenshot": "login.png",
                                "page_name": "登录页",
                                "page_type": "form",
                                "interaction_modes": ["form-submit"],
                                "platform": "mobile",
                                "navigation_type": "stack",
                                "confidence": 0.86,
                                "components": {
                                    "fields": ["手机号", "验证码"],
                                    "buttons": ["登录"],
                                    "tabs": [],
                                    "labels": ["登录页"],
                                },
                            }
                        ]
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            write_initial_outputs(workspace)

            merged_dsl = json.loads((workspace / "working" / "merged-dsl.json").read_text(encoding="utf-8"))
            self.assertIn("screenshot_evidence", merged_dsl)
            self.assertEqual("登录页", merged_dsl["pages"][0]["name"])
            self.assertIn("vision-page-classification", merged_dsl["pages"][0]["evidence"])
            self.assertIn("截图视觉核对", merged_dsl["dependencies"])


if __name__ == "__main__":
    unittest.main()
