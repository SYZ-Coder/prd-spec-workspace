from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import run_pipeline


class RunPipelineTests(unittest.TestCase):
    def test_write_pipeline_plan_uses_readable_chinese_labels(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            (workspace / "working").mkdir(parents=True)
            with patch.object(run_pipeline, "WORKSPACE", workspace):
                plan_path = run_pipeline.write_pipeline_plan(
                    change_name="user-auth",
                    domain="account",
                    title="用户登录注册需求",
                    mode="prd",
                    prompt_order=["prompts/01_extract_dsl.md", "prompts/03_merge_logic.md"],
                )

            content = plan_path.read_text(encoding="utf-8")
            self.assertIn("变更名", content)
            self.assertIn("领域", content)
            self.assertIn("标题", content)
            self.assertIn("说明", content)
            self.assertIn("归档", content)


if __name__ == "__main__":
    unittest.main()
