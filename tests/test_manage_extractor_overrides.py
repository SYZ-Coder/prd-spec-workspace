from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.manage_extractor_overrides import add_list_value, add_rule_category_keyword, init_overrides, show_overrides


class ManageExtractorOverridesTests(unittest.TestCase):
    def test_init_creates_override_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            path = init_overrides(workspace)

            self.assertTrue(path.exists())
            content = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn("page_suffixes", content)
            self.assertIn("action_prefixes", content)

    def test_add_list_value_and_rule_category_keyword(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            init_overrides(workspace)
            add_list_value(workspace, "page_suffixes", "看板")
            add_list_value(workspace, "action_prefixes", "导出")
            add_rule_category_keyword(workspace, "报表规则", "实时刷新")

            content = json.loads((workspace / "extractor-overrides.json").read_text(encoding="utf-8"))
            self.assertIn("看板", content["page_suffixes"])
            self.assertIn("导出", content["action_prefixes"])
            self.assertIn("实时刷新", content["rule_categories"]["报表规则"])

    def test_show_includes_effective_overrides(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            init_overrides(workspace)
            add_list_value(workspace, "page_suffixes", "看板")

            output = show_overrides(workspace)
            self.assertIn("Extractor Overrides", output)
            self.assertIn("Effective Overrides", output)
            self.assertIn("看板", output)


if __name__ == "__main__":
    unittest.main()
