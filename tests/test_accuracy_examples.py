from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.extract_initial_dsl import write_initial_outputs
from scripts.validate_dsl import validate_dsl_data


WORKSPACE = Path(__file__).resolve().parents[1]
EXAMPLES = WORKSPACE / "examples"


class AccuracyExampleTests(unittest.TestCase):
    def run_example(self, name: str) -> tuple[dict, list[str], list[str], list[str]]:
        example_root = EXAMPLES / name
        self.assertTrue(example_root.exists(), f"example missing: {example_root}")
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            for relative in ["inputs/prd", "inputs/notes", "inputs/context", "inputs/screenshots", "working"]:
                (workspace / relative).mkdir(parents=True, exist_ok=True)
            for child in (example_root / "inputs").rglob("*"):
                if child.is_dir():
                    continue
                target = workspace / child.relative_to(example_root)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(child, target)
            overrides = example_root / "extractor-overrides.json"
            if overrides.exists():
                shutil.copy2(overrides, workspace / "extractor-overrides.json")
            write_initial_outputs(workspace)
            dsl = json.loads((workspace / "working" / "merged-dsl.json").read_text(encoding="utf-8"))
            blocking, high_risk, suggestions = validate_dsl_data(dsl)
            return dsl, blocking, high_risk, suggestions

    def test_auth_basic_example_extracts_expected_pages_and_transition(self) -> None:
        dsl, blocking, high_risk, _ = self.run_example("auth-basic")

        self.assertEqual(blocking, [])
        self.assertEqual(high_risk, [])
        self.assertEqual([page["name"] for page in dsl["pages"]], ["\u767b\u5f55\u9875", "\u6ce8\u518c\u9875", "\u627e\u56de\u5bc6\u7801\u9875", "\u9996\u9875"])
        self.assertTrue(any(rule == "\u6ce8\u518c\u65f6\u624b\u673a\u53f7\u5fc5\u987b\u552f\u4e00" for rule in dsl["rules"]))
        self.assertTrue(any(item["from_page"] == "P_\u767b\u5f55\u9875" and item["to_page"] == "P_\u9996\u9875" for item in dsl["transitions"]))

    def test_payment_refund_example_flags_result_to_result_transition_risk(self) -> None:
        dsl, blocking, high_risk, _ = self.run_example("payment-refund")

        self.assertEqual(blocking, [])
        self.assertEqual([page["name"] for page in dsl["pages"]], ["\u652f\u4ed8\u9875", "\u7ed3\u679c\u9875", "\u9000\u6b3e\u7ed3\u679c\u9875"])
        self.assertTrue(any(item["from_page"] == "P_\u9000\u6b3e\u7ed3\u679c\u9875" and item["to_page"] == "P_\u7ed3\u679c\u9875" for item in dsl["transitions"]))
        self.assertTrue(any("\u7ed3\u679c\u9875" in item and "\u6d41\u8f6c" in item for item in high_risk))

    def test_reporting_dashboard_example_supports_custom_vocabulary(self) -> None:
        dsl, blocking, high_risk, _ = self.run_example("reporting-dashboard")

        self.assertEqual(blocking, [])
        self.assertEqual(high_risk, [])
        self.assertEqual([page["name"] for page in dsl["pages"]], ["\u5206\u6790\u770b\u677f", "\u660e\u7ec6\u5217\u8868"])
        self.assertTrue(any(action["trigger"] == "\u5bfc\u51fa\u62a5\u8868" for page in dsl["pages"] for action in page["actions"]))
        self.assertTrue(any(rule == "\u4ec5\u7ba1\u7406\u5458\u652f\u6301\u5bfc\u51fa\u62a5\u8868" for rule in dsl["rules"]))
        self.assertTrue(any(item["from_page"] == "P_\u5206\u6790\u770b\u677f" and item["to_page"] == "P_\u660e\u7ec6\u5217\u8868" for item in dsl["transitions"]))


if __name__ == "__main__":
    unittest.main()
