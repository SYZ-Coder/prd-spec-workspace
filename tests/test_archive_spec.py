from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.archive_spec import ArchiveConfig, archive


class ArchiveSpecTests(unittest.TestCase):
    def test_archive_writes_assets_snapshot_catalog_and_cleans_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            change_name = "role-image-history-reuse"
            domain = "virtual-role"

            (workspace / "inputs" / "prd").mkdir(parents=True)
            (workspace / "inputs" / "screenshots").mkdir(parents=True)
            (workspace / "inputs" / "notes").mkdir(parents=True)
            (workspace / "inputs" / "context").mkdir(parents=True)
            (workspace / "inputs" / "prd" / "需求.md").write_text("历史生图入口", encoding="utf-8")
            (workspace / "inputs" / "screenshots" / "page.png").write_bytes(b"fake")

            working = workspace / "working"
            working.mkdir(parents=True)
            dsl = {
                "pages": [
                    {
                        "id": "P_HISTORY",
                        "name": "历史生图页",
                        "states": ["normal"],
                        "actions": [{"id": "A_OPEN"}],
                        "unknowns": ["返回落点待确认"],
                    }
                ],
                "transitions": [
                    {
                        "from_page": "P_HISTORY",
                        "to_page": "P_HISTORY",
                        "condition": "用户点击管理",
                        "result": "进入管理态",
                    }
                ],
                "rules": ["没有历史生图内容时，入口隐藏。"],
                "dependencies": ["history_image_storage"],
                "unknowns": ["接口字段待确认"],
            }
            (working / "merged-dsl.json").write_text(json.dumps(dsl, ensure_ascii=False), encoding="utf-8")
            (working / "validation-report.md").write_text("# Validation Report\n\n## Blocking Issues\n- None\n", encoding="utf-8")
            (working / "generated-prd.md").write_text("# 历史生图需求", encoding="utf-8")
            (working / "generated-api-contracts.md").write_text("# 接口契约草案", encoding="utf-8")
            (working / "api-contracts").mkdir()
            (working / "api-contracts" / "openapi.yaml").write_text("openapi: 3.0.0\n", encoding="utf-8")
            (workspace / "outputs" / "diagrams").mkdir(parents=True)
            (workspace / "outputs" / "diagrams" / "flow.md").write_text("# flow", encoding="utf-8")

            change_root = workspace / "openspec" / "changes" / change_name
            (change_root / "specs" / domain).mkdir(parents=True)
            (change_root / "proposal.md").write_text("# Proposal", encoding="utf-8")
            (change_root / "design.md").write_text("# Design", encoding="utf-8")
            (change_root / "tasks.md").write_text("# Tasks", encoding="utf-8")
            (change_root / "specs" / domain / "spec.md").write_text("# Spec", encoding="utf-8")

            archive(ArchiveConfig(workspace=workspace, change_name=change_name, domain=domain, title="历史生图与选图复用"))

            spec_asset = workspace / "knowledge" / "assets" / "specs" / domain / f"{change_name}.md"
            rule_asset = workspace / "knowledge" / "assets" / "rules" / domain / f"{change_name}.md"
            snapshots_root = workspace / "knowledge" / "snapshots"
            catalog = json.loads((workspace / "knowledge" / "catalog.json").read_text(encoding="utf-8-sig"))

            self.assertTrue(spec_asset.exists())
            self.assertTrue(rule_asset.exists())
            matching_snapshots = list(snapshots_root.glob(f"*_{change_name}"))
            self.assertEqual(1, len(matching_snapshots))
            snapshot = matching_snapshots[0]
            self.assertTrue((snapshot / "inputs" / "prd" / "需求.md").exists())
            self.assertTrue((snapshot / "working" / "merged-dsl.json").exists())
            self.assertTrue((snapshot / "outputs" / "diagrams" / "flow.md").exists())
            self.assertTrue((snapshot / "openspec-change" / "proposal.md").exists())
            self.assertEqual([], list((workspace / "inputs" / "prd").iterdir()))
            self.assertEqual([], list((workspace / "working").iterdir()))
            self.assertEqual(change_name, catalog["changes"][0]["change_name"])

            spec_text = spec_asset.read_text(encoding="utf-8-sig")
            self.assertIn("历史生图与选图复用", spec_text)
            self.assertNotIn("?" * 4, spec_text)
            self.assertNotIn(chr(0xFFFD), spec_text)


if __name__ == "__main__":
    unittest.main()


