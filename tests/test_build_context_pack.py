from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.build_context_pack import build_context_pack, default_output_path, files_for_target


class BuildContextPackTests(unittest.TestCase):
    def test_files_for_target_returns_expected_core_files(self) -> None:
        files = files_for_target("openspec", "user-login-register", "account")
        self.assertIn("openspec/changes/user-login-register/proposal.md", files)
        self.assertIn("openspec/changes/user-login-register/specs/account/spec.md", files)
        self.assertIn("working/validation-report.md", files)

    def test_build_context_pack_writes_markdown_for_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            (workspace / "working").mkdir(parents=True)
            (workspace / "openspec" / "changes" / "user-login-register" / "specs" / "account").mkdir(parents=True)

            file_map = {
                "openspec/changes/user-login-register/proposal.md": "# Proposal\n",
                "openspec/changes/user-login-register/design.md": "# Design\n",
                "openspec/changes/user-login-register/tasks.md": "# Tasks\n",
                "openspec/changes/user-login-register/specs/account/spec.md": "# Spec\n",
                "working/validation-report.md": "# Validation\n",
                "working/merged-dsl.json": "{\n  \"pages\": []\n}\n",
                "working/generated-api-contracts.md": "# APIs\n",
                "working/generated-testcases.md": "# Testcases\n",
            }
            for relative_path, content in file_map.items():
                path = workspace / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            output_path = build_context_pack(
                workspace=workspace,
                target="openspec",
                change_name="user-login-register",
                domain="account",
                title="用户登录注册需求",
            )

            content = output_path.read_text(encoding="utf-8")
            self.assertEqual(default_output_path(workspace, "openspec"), output_path)
            self.assertIn("# OpenSpec Context Pack", content)
            self.assertIn("- Change Name: user-login-register", content)
            self.assertIn("## File: openspec/changes/user-login-register/proposal.md", content)
            self.assertIn("# Proposal", content)
            self.assertIn("## File: working/validation-report.md", content)
            self.assertNotIn("## File: missing.md", content)

    def test_build_context_pack_supports_ai_development_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            (workspace / "working" / "api-contracts").mkdir(parents=True)

            file_map = {
                "working/generated-prd.md": "# PRD\n",
                "working/generated-flow.md": "# Flow\n",
                "working/generated-testcases.md": "# Tests\n",
                "working/generated-api-contracts.md": "# Contracts\n",
                "working/api-contracts/openapi.yaml": "openapi: 3.0.0\n",
                "working/merged-dsl.json": "{\n  \"pages\": []\n}\n",
                "working/validation-report.md": "# Validation\n",
            }
            for relative_path, content in file_map.items():
                path = workspace / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            output_path = build_context_pack(
                workspace=workspace,
                target="ai-development",
                change_name="user-login-register",
                domain="account",
                title="用户登录注册需求",
            )

            content = output_path.read_text(encoding="utf-8")
            self.assertIn("# AI Development Context Pack", content)
            self.assertIn("- Target: 代码实现", content)
            self.assertIn("## File: working/api-contracts/openapi.yaml", content)


if __name__ == "__main__":
    unittest.main()
