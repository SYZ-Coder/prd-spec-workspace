from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from scripts.extract_initial_dsl import group_rules
except ModuleNotFoundError:
    from extract_initial_dsl import group_rules


EMPTY_BULLET = "- None"


def load_dsl(workspace: Path) -> dict:
    return json.loads((workspace / "working" / "merged-dsl.json").read_text(encoding="utf-8"))


def get_meta(dsl: dict) -> dict:
    return dsl.get("meta", {})


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_flow_doc(dsl: dict) -> str:
    page_nodes = [f"    {page['id']}[{page['name']}]" for page in dsl.get("pages", [])]
    transition_edges = [
        f"    {item['from_page']} -->|{item['trigger']} / {item['condition']}| {item['to_page']}"
        for item in dsl.get("transitions", [])
    ]
    failure_lines = []
    for page in dsl.get("pages", []):
        for action in page.get("actions", []):
            for failure in action.get("failure_results", []):
                failure_lines.append(f"- {action['id']}?{failure}")
    return "\n".join(
        [
            "# \u6d41\u7a0b\u56fe\u6587\u6863",
            "",
            "## \u9875\u9762\u6d41\u8f6c\u603b\u56fe",
            "```mermaid",
            "flowchart TD",
            "    START([\u5f00\u59cb])",
            *page_nodes,
            *transition_edges,
            "    END([\u7ed3\u675f])",
            "```",
            "",
            "## \u6838\u5fc3\u5f02\u5e38\u8def\u5f84",
            *(failure_lines[:8] or [EMPTY_BULLET]),
            "",
        ]
    )


def build_testcases_doc(dsl: dict) -> str:
    lines = ["# \u6d4b\u8bd5\u7528\u4f8b", "", "## \u529f\u80fd\u6d4b\u8bd5\u7528\u4f8b"]
    counter = 1
    for page in dsl.get("pages", []):
        lines.append(f"- TC-{counter:03d} | 页面: {page['id']} | 场景: 进入{page['name']} | 类型: 正常")
        lines.append(f"  前置条件: {', '.join(page.get('entry_points', [])) or '待确认'}")
        lines.append(f"  预期结果: 用户可以完成页面目标：{page['goal']}")
        counter += 1
        lines.append(f"- TC-{counter:03d} | 页面: {page['id']} | 场景: 离开{page['name']} | 类型: 正常")
        lines.append(f"  前置条件: {page['name']} 已展示")
        lines.append(f"  预期结果: 用户可以进入后续出口：{', '.join(page.get('exit_points', [])) or '待确认'}")
        counter += 1
        for action in page.get("actions", []):
            lines.append(f"- TC-{counter:03d} | 页面: {page['id']} | 动作: {action['id']} 成功路径 | 类型: 正常")
            lines.append(f"  前置条件: {', '.join(action.get('preconditions', [])) or '待确认'}")
            lines.append(f"  预期结果: {', '.join(action.get('success_results', [])) or '成功结果待确认'}")
            counter += 1
            lines.append(f"- TC-{counter:03d} | 页面: {page['id']} | 动作: {action['id']} 失败路径 | 类型: 异常")
            lines.append(f"  前置条件: {', '.join(action.get('preconditions', [])) or '待确认'}")
            lines.append(f"  预期结果: {', '.join(action.get('failure_results', [])) or '失败结果待确认'}")
            counter += 1

    lines.extend(["", "## \u89c4\u5219\u8986\u76d6\u77e9\u9635"])
    for category, items in group_rules(dsl.get("rules", []), get_meta(dsl).get("domain", "generic")).items():
        lines.append(f"### {category}")
        lines.extend(f"- 覆盖规则: {item}" for item in items)
    lines.extend(["", "## \u5f85\u8865\u5145\u6d4b\u8bd5\u9879"])
    lines.extend([f"- {item}" for item in dsl.get("unknowns", [])] or [EMPTY_BULLET])
    return "\n".join(lines) + "\n"


def infer_endpoint(domain: str, action_id: str) -> tuple[str, str]:
    name = action_id.lower().replace("a_", "").replace("_", "-")
    return "POST", f"/api/{domain or 'generic'}/{name}"


def build_api_contracts_doc(dsl: dict) -> tuple[str, str]:
    meta = get_meta(dsl)
    domain = meta.get("domain", "generic")
    md_lines = [
        "# \u63a5\u53e3\u5951\u7ea6\u8349\u6848",
        "",
        "## \u751f\u6210\u72b6\u6001",
        "- \u8349\u6848\u5f85\u786e\u8ba4",
        "- \u5f53\u524d\u8bf7\u6c42\u53c2\u6570\u548c\u8fd4\u56de\u7ed3\u6784\u4e3b\u8981\u7531 DSL \u52a8\u4f5c\u3001\u524d\u7f6e\u6761\u4ef6\u548c\u7ed3\u679c\u63a8\u65ad\u5f97\u5230\u3002",
        "",
        "## \u63a5\u53e3\u5217\u8868",
    ]
    yaml_lines = [
        "openapi: 3.0.0",
        "info:",
        f"  title: {meta.get('feature_name', 'Draft')} API",
        "  version: 0.1.0",
        "paths:",
    ]
    for page in dsl.get("pages", []):
        for action in page.get("actions", []):
            method, path = infer_endpoint(domain, action["id"])
            md_lines.extend(
                [
                    f"### {action['id']}",
                    "- 来源: inferred-from-dsl",
                    f"- 页面: {page['id']} / {page['name']}",
                    f"- 触发: {action['trigger']}",
                    f"- Method: {method}",
                    f"- Path: {path}",
                    f"- 处理步骤: {', '.join(action.get('steps', [])) or '待确认'}",
                    f"- 前置条件: {', '.join(action.get('preconditions', [])) or '待确认'}",
                    f"- 成功结果: {', '.join(action.get('success_results', [])) or '待确认'}",
                    f"- 失败结果: {', '.join(action.get('failure_results', [])) or '待确认'}",
                    f"- 依赖: {', '.join(page.get('dependencies', [])) or '待确认'}",
                    "- 请求 schema: 需要结合 inputs/context 中的接口说明确认",
                    "",
                ]
            )
            yaml_lines.extend(
                [
                    f"  {path}:",
                    f"    {method.lower()}:",
                    f"      summary: {action['trigger']}",
                    f"      description: inferred from DSL for {action['id']}",
                    "      responses:",
                    "        '200':",
                    f"          description: {'; '.join(action.get('success_results', [])) or 'Success'}",
                    "        '400':",
                    f"          description: {'; '.join(action.get('failure_results', [])) or 'Failure'}",
                ]
            )
    md_lines.extend(["## \u5f85\u786e\u8ba4\u9879"])
    md_lines.extend([f"- {item}" for item in dsl.get("unknowns", [])] or [EMPTY_BULLET])
    return "\n".join(md_lines) + "\n", "\n".join(yaml_lines) + "\n"


def write_derivative_outputs(workspace: Path) -> None:
    dsl = load_dsl(workspace)
    write_text(workspace / "working" / "generated-flow.md", build_flow_doc(dsl))
    write_text(workspace / "working" / "generated-testcases.md", build_testcases_doc(dsl))
    api_md, openapi_yaml = build_api_contracts_doc(dsl)
    write_text(workspace / "working" / "generated-api-contracts.md", api_md)
    write_text(workspace / "working" / "api-contracts" / "openapi.yaml", openapi_yaml)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate derivative artifacts from merged DSL.")
    parser.add_argument("--workspace", default=".", help="Workspace root. Default: current directory.")
    args = parser.parse_args()
    write_derivative_outputs(Path(args.workspace).resolve())
    print("Derivative artifacts generated.")


if __name__ == "__main__":
    main()
