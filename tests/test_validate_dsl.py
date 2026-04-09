from __future__ import annotations

import unittest

from scripts.validate_dsl import validate_dsl_data


class ValidateDslTests(unittest.TestCase):
    def test_validate_dsl_reports_semantic_quality_risks(self) -> None:
        dsl = {
            "pages": [
                {
                    "id": "P_MAIN",
                    "name": "\u4e3b\u6d41\u7a0b\u9875\u9762",
                    "source": ["inputs/prd/sample.md"],
                    "goal": "\u5c55\u793a\u6d41\u7a0b\u5165\u53e3",
                    "entry_points": ["\u7528\u6237\u8fdb\u5165\u4e3b\u6d41\u7a0b\u9875\u9762"],
                    "exit_points": ["\u5b8c\u6210\u4e3b\u6d41\u7a0b\u540e\u79bb\u5f00"],
                    "actions": [
                        {
                            "id": "A_MAIN_1",
                            "trigger": "\u6267\u884c\u4e3b\u6d41\u7a0b\u9875\u9762\u4e3b\u64cd\u4f5c",
                            "actor": "\u7528\u6237",
                            "preconditions": ["\u8f93\u5165\u5b8c\u6574"],
                            "steps": ["\u63d0\u4ea4\u8bf7\u6c42"],
                            "success_results": ["\u5904\u7406\u6210\u529f"],
                            "failure_results": ["\u5904\u7406\u5931\u8d25"],
                        }
                    ],
                    "states": ["\u5f85\u5904\u7406", "\u6210\u529f"],
                    "dependencies": ["\u4e1a\u52a1\u670d\u52a1"],
                    "unknowns": [],
                }
            ],
            "transitions": [],
            "rules": ["\u652f\u4ed8\u6d41\u7a0b\u9700\u6c42", "\u652f\u4ed8\u9875\uff1a\u5c55\u793a\u8ba2\u5355\u5e76\u63d0\u4ea4\u652f\u4ed8"],
            "dependencies": ["\u4e1a\u52a1\u670d\u52a1"],
            "unknowns": [],
        }

        blocking, high_risk, suggestions = validate_dsl_data(dsl)

        self.assertEqual(blocking, [])
        self.assertTrue(any("\u4e3b\u6d41\u7a0b\u9875\u9762" in item for item in high_risk))
        self.assertTrue(any("\u6807\u9898\u6216\u9700\u6c42\u540d" in item for item in high_risk))
        self.assertTrue(any("\u9875\u9762\u58f0\u660e" in item for item in high_risk))
        self.assertTrue(any("\u52a8\u4f5c\u89e6\u53d1\u8bcd" in item for item in suggestions))

    def test_validate_dsl_flags_result_to_result_transition_as_high_risk(self) -> None:
        dsl = {
            "pages": [
                {
                    "id": "P_PAY",
                    "name": "\u652f\u4ed8\u9875",
                    "source": ["inputs/prd/sample.md"],
                    "goal": "\u63d0\u4ea4\u652f\u4ed8\u8bf7\u6c42",
                    "entry_points": ["\u7528\u6237\u8fdb\u5165\u652f\u4ed8\u9875"],
                    "exit_points": ["\u652f\u4ed8\u5b8c\u6210\u540e\u79bb\u5f00"],
                    "actions": [{"id": "A_PAY_1", "trigger": "\u63d0\u4ea4\u652f\u4ed8", "actor": "\u7528\u6237", "preconditions": ["\u8ba2\u5355\u53ef\u652f\u4ed8"], "steps": ["\u63d0\u4ea4\u652f\u4ed8"], "success_results": ["\u652f\u4ed8\u6210\u529f"], "failure_results": ["\u652f\u4ed8\u5931\u8d25"]}],
                    "states": ["\u5f85\u652f\u4ed8", "\u652f\u4ed8\u4e2d", "\u6210\u529f", "\u5931\u8d25"],
                    "dependencies": ["\u652f\u4ed8\u670d\u52a1"],
                    "unknowns": [],
                },
                {
                    "id": "P_RESULT",
                    "name": "\u7ed3\u679c\u9875",
                    "source": ["inputs/prd/sample.md"],
                    "goal": "\u5c55\u793a\u652f\u4ed8\u7ed3\u679c",
                    "entry_points": ["\u652f\u4ed8\u6210\u529f\u540e\u8fdb\u5165\u7ed3\u679c\u9875"],
                    "exit_points": ["\u67e5\u770b\u540e\u8fd4\u56de"],
                    "actions": [{"id": "A_RESULT_1", "trigger": "\u67e5\u770b\u7ed3\u679c", "actor": "\u7528\u6237", "preconditions": ["\u7ed3\u679c\u9875\u5df2\u5c55\u793a"], "steps": ["\u67e5\u770b\u652f\u4ed8\u7ed3\u679c"], "success_results": ["\u5b8c\u6210\u67e5\u770b"], "failure_results": ["\u5c55\u793a\u5931\u8d25"]}],
                    "states": ["\u6210\u529f", "\u5931\u8d25"],
                    "dependencies": ["\u652f\u4ed8\u670d\u52a1"],
                    "unknowns": [],
                },
                {
                    "id": "P_REFUND_RESULT",
                    "name": "\u9000\u6b3e\u7ed3\u679c\u9875",
                    "source": ["inputs/prd/sample.md"],
                    "goal": "\u5c55\u793a\u9000\u6b3e\u5904\u7406\u7ed3\u679c",
                    "entry_points": ["\u9000\u6b3e\u63d0\u4ea4\u540e\u8fdb\u5165\u9000\u6b3e\u7ed3\u679c\u9875"],
                    "exit_points": ["\u67e5\u770b\u540e\u7ed3\u675f"],
                    "actions": [{"id": "A_REFUND_RESULT_1", "trigger": "\u67e5\u770b\u7ed3\u679c", "actor": "\u7528\u6237", "preconditions": ["\u9000\u6b3e\u7ed3\u679c\u9875\u5df2\u5c55\u793a"], "steps": ["\u67e5\u770b\u9000\u6b3e\u7ed3\u679c"], "success_results": ["\u5b8c\u6210\u67e5\u770b"], "failure_results": ["\u5c55\u793a\u5931\u8d25"]}],
                    "states": ["\u6210\u529f", "\u5931\u8d25"],
                    "dependencies": ["\u652f\u4ed8\u670d\u52a1"],
                    "unknowns": [],
                },
            ],
            "transitions": [
                {"from_page": "P_PAY", "trigger": "\u63d0\u4ea4\u652f\u4ed8", "to_page": "P_RESULT", "condition": "\u652f\u4ed8\u6210\u529f", "result": "\u8fdb\u5165\u7ed3\u679c\u9875"},
                {"from_page": "P_REFUND_RESULT", "trigger": "\u67e5\u770b\u7ed3\u679c", "to_page": "P_RESULT", "condition": "\u652f\u4ed8\u6210\u529f", "result": "\u8fdb\u5165\u7ed3\u679c\u9875"},
            ],
            "rules": ["\u652f\u4ed8\u6210\u529f\u540e\u8fdb\u5165\u7ed3\u679c\u9875"],
            "dependencies": ["\u652f\u4ed8\u670d\u52a1"],
            "unknowns": [],
        }

        blocking, high_risk, _ = validate_dsl_data(dsl)

        self.assertEqual(blocking, [])
        self.assertTrue(any("\u7ed3\u679c\u9875" in item and "\u6d41\u8f6c" in item for item in high_risk))

    def test_validate_dsl_flags_transition_trigger_owned_by_other_page(self) -> None:
        dsl = {
            "pages": [
                {
                    "id": "P_LIST",
                    "name": "\u5de5\u5355\u5217\u8868",
                    "source": ["inputs/prd/sample.md"],
                    "goal": "\u67e5\u770b\u5de5\u5355\u5e76\u8fdb\u5165\u8be6\u60c5",
                    "entry_points": ["\u7528\u6237\u8fdb\u5165\u5de5\u5355\u5217\u8868"],
                    "exit_points": ["\u70b9\u51fb\u5de5\u5355\u8fdb\u5165\u8be6\u60c5"],
                    "actions": [{"id": "A_LIST_1", "trigger": "\u67e5\u770b\u8be6\u60c5", "actor": "\u7528\u6237", "preconditions": ["\u5de5\u5355\u5217\u8868\u5df2\u52a0\u8f7d"], "steps": ["\u70b9\u51fb\u5de5\u5355"], "success_results": ["\u8fdb\u5165\u8be6\u60c5\u9875"], "failure_results": ["\u8fdb\u5165\u5931\u8d25"]}],
                    "states": ["\u5f85\u5904\u7406", "\u6210\u529f", "\u5931\u8d25"],
                    "dependencies": ["\u5de5\u5355\u670d\u52a1"],
                    "unknowns": [],
                },
                {
                    "id": "P_APPROVAL",
                    "name": "\u5ba1\u6279\u9875",
                    "source": ["inputs/prd/sample.md"],
                    "goal": "\u63d0\u4ea4\u5ba1\u6279\u8bf7\u6c42",
                    "entry_points": ["\u4ece\u8be6\u60c5\u9875\u8fdb\u5165\u5ba1\u6279\u9875"],
                    "exit_points": ["\u63d0\u4ea4\u5ba1\u6279\u540e\u79bb\u5f00"],
                    "actions": [{"id": "A_APPROVAL_1", "trigger": "\u63d0\u4ea4\u5ba1\u6279", "actor": "\u7528\u6237", "preconditions": ["\u5ba1\u6279\u9875\u5df2\u586b\u5199"], "steps": ["\u63d0\u4ea4\u5ba1\u6279"], "success_results": ["\u8fdb\u5165\u5ba1\u6279\u7ed3\u679c\u9875"], "failure_results": ["\u63d0\u4ea4\u5931\u8d25"]}],
                    "states": ["\u5f85\u586b\u5199", "\u63d0\u4ea4\u4e2d", "\u6210\u529f", "\u5931\u8d25"],
                    "dependencies": ["\u5de5\u5355\u670d\u52a1"],
                    "unknowns": [],
                },
                {
                    "id": "P_APPROVAL_RESULT",
                    "name": "\u5ba1\u6279\u7ed3\u679c\u9875",
                    "source": ["inputs/prd/sample.md"],
                    "goal": "\u5c55\u793a\u5ba1\u6279\u7ed3\u679c",
                    "entry_points": ["\u5ba1\u6279\u5b8c\u6210\u540e\u8fdb\u5165\u5ba1\u6279\u7ed3\u679c\u9875"],
                    "exit_points": ["\u67e5\u770b\u540e\u7ed3\u675f"],
                    "actions": [{"id": "A_RESULT_1", "trigger": "\u67e5\u770b\u7ed3\u679c", "actor": "\u7528\u6237", "preconditions": ["\u5ba1\u6279\u7ed3\u679c\u9875\u5df2\u5c55\u793a"], "steps": ["\u67e5\u770b\u5ba1\u6279\u7ed3\u679c"], "success_results": ["\u67e5\u770b\u5b8c\u6210"], "failure_results": ["\u67e5\u770b\u5931\u8d25"]}],
                    "states": ["\u6210\u529f", "\u5931\u8d25"],
                    "dependencies": ["\u5de5\u5355\u670d\u52a1"],
                    "unknowns": [],
                },
            ],
            "transitions": [
                {"from_page": "P_LIST", "trigger": "\u63d0\u4ea4\u5ba1\u6279\u540e\u8fdb\u5165\u5ba1\u6279\u7ed3\u679c\u9875", "to_page": "P_APPROVAL_RESULT", "condition": "\u5ba1\u6279\u63d0\u4ea4\u6210\u529f", "result": "\u8fdb\u5165\u5ba1\u6279\u7ed3\u679c\u9875"}
            ],
            "rules": ["\u63d0\u4ea4\u5ba1\u6279\u540e\u8fdb\u5165\u5ba1\u6279\u7ed3\u679c\u9875"],
            "dependencies": ["\u5de5\u5355\u670d\u52a1"],
            "unknowns": [],
        }

        blocking, high_risk, _ = validate_dsl_data(dsl)

        self.assertEqual(blocking, [])
        self.assertTrue(any("\u89e6\u53d1\u8bcd" in item or "\u5f52\u5c5e" in item for item in high_risk))

    def test_validate_dsl_flags_missing_middle_state(self) -> None:
        dsl = {
            "pages": [
                {
                    "id": "P_APPROVAL",
                    "name": "\u5ba1\u6279\u9875",
                    "source": ["inputs/prd/sample.md"],
                    "goal": "\u63d0\u4ea4\u5ba1\u6279\u5e76\u7b49\u5f85\u5ba1\u6279\u7ed3\u679c",
                    "entry_points": ["\u7528\u6237\u8fdb\u5165\u5ba1\u6279\u9875"],
                    "exit_points": ["\u5ba1\u6279\u5b8c\u6210\u540e\u79bb\u5f00"],
                    "actions": [{"id": "A_APPROVAL_1", "trigger": "\u63d0\u4ea4\u5ba1\u6279", "actor": "\u7528\u6237", "preconditions": ["\u5ba1\u6279\u4fe1\u606f\u5b8c\u6574"], "steps": ["\u63d0\u4ea4\u5ba1\u6279\u8bf7\u6c42"], "success_results": ["\u8fdb\u5165\u5ba1\u6279\u4e2d\u72b6\u6001"], "failure_results": ["\u63d0\u4ea4\u5931\u8d25"]}],
                    "states": ["\u5f85\u586b\u5199", "\u6210\u529f", "\u5931\u8d25"],
                    "dependencies": ["\u5ba1\u6279\u670d\u52a1"],
                    "unknowns": [],
                }
            ],
            "transitions": [],
            "rules": ["\u63d0\u4ea4\u5ba1\u6279\u540e\u8fdb\u5165\u5ba1\u6279\u4e2d\uff0c\u5ba1\u6279\u901a\u8fc7\u540e\u624d\u80fd\u7ed3\u675f"],
            "dependencies": ["\u5ba1\u6279\u670d\u52a1"],
            "unknowns": [],
        }

        blocking, high_risk, _ = validate_dsl_data(dsl)

        self.assertEqual(blocking, [])
        self.assertTrue(any("\u4e2d\u95f4\u72b6\u6001" in item or "\u5ba1\u6279\u4e2d" in item for item in high_risk))


if __name__ == "__main__":
    unittest.main()
