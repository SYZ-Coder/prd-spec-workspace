from __future__ import annotations

import io
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
            self.assertIn("模式", content)
            self.assertIn("说明", content)

    def test_main_prints_readable_next_steps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            for relative in ["inputs/prd", "inputs/notes", "inputs/context", "inputs/screenshots", "working"]:
                (workspace / relative).mkdir(parents=True, exist_ok=True)
            (workspace / "inputs" / "prd" / "sample.md").write_text("用户登录注册需求", encoding="utf-8")
            (workspace / "working" / "merged-dsl.json").write_text("{}", encoding="utf-8")

            stdout = io.StringIO()
            with patch.object(run_pipeline, "WORKSPACE", workspace), patch.object(run_pipeline, "run_python", return_value=0), patch("sys.stdout", stdout):
                with patch("sys.argv", ["run_pipeline.py", "--change-name", "user-auth", "--domain", "account", "--title", "用户登录注册需求"]):
                    run_pipeline.main()

            output = stdout.getvalue()
            self.assertIn("下一步建议", output)
            self.assertIn("归档命令", output)
            self.assertIn("pipeline-plan.md", output)

    def test_main_runs_optional_vision_stage_when_enabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            for relative in ["inputs/prd", "inputs/notes", "inputs/context", "inputs/screenshots", "working"]:
                (workspace / relative).mkdir(parents=True, exist_ok=True)
            (workspace / "inputs" / "prd" / "sample.md").write_text("登录需求", encoding="utf-8")
            (workspace / "inputs" / "screenshots" / "login.png").write_bytes(b"fake")
            (workspace / "working" / "merged-dsl.json").write_text("{}", encoding="utf-8")

            calls: list[tuple[str, tuple[str, ...]]] = []

            def fake_run_python(script: str, *extra_args: str) -> int:
                calls.append((script, extra_args))
                return 0

            with patch.object(run_pipeline, "WORKSPACE", workspace), patch.object(run_pipeline, "run_python", side_effect=fake_run_python):
                with patch("sys.argv", ["run_pipeline.py", "--change-name", "user-auth", "--domain", "account", "--enable-vision"]):
                    run_pipeline.main()

            scripts = [script for script, _ in calls]
            self.assertIn("scripts/extract_screenshot_evidence.py", scripts)
            self.assertLess(scripts.index("scripts/extract_screenshot_evidence.py"), scripts.index("scripts/extract_initial_dsl.py"))


if __name__ == "__main__":
    unittest.main()
