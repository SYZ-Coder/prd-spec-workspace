from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from scripts.workspace_utils import resolve_workspace
except ModuleNotFoundError:
    from workspace_utils import resolve_workspace

try:
    from scripts.extract_initial_dsl import group_rules
except ModuleNotFoundError:
    from extract_initial_dsl import group_rules


EMPTY_BULLET = "- None"


def load_dsl(workspace: Path) -> dict:
    return json.loads((workspace / "working" / "merged-dsl.json").read_text(encoding="utf-8-sig"))


def get_meta(dsl: dict) -> dict:
    return dsl.get("meta", {})


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8-sig")


def build_flow_doc(dsl: dict) -> str:
    page_nodes = [f"    {page['id']}[{page['name']}]" for page in dsl.get("pages", [])]
    transition_edges = [
        f"    {item['from_page']} -->|{item['trigger']} / {item['condition']}| {item['to_page']}"
        for item in dsl.get("transitions", [])
    ]
    failure_lines: list[str] = []
    for page in dsl.get("pages", []):
        for action in page.get("actions", []):
            for failure in action.get("failure_results", []):
                failure_lines.append(f"- {action['id']}：{failure}")
    return "\n".join(
        [
            "# 流程图文档",
            "",
            "## 页面流转总图",
            "```mermaid",
            "flowchart TD",
            "    START([开始])",
            *page_nodes,
            *transition_edges,
            "    END([结束])",
            "```",
            "",
            "## 核心异常路径",
            *(failure_lines[:8] or [EMPTY_BULLET]),
            "",
        ]
    )


def build_testcases_doc(dsl: dict) -> str:
    lines = ["# 测试用例", "", "## 功能测试用例"]
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

    lines.extend(["", "## 规则覆盖矩阵"])
    for category, items in group_rules(dsl.get("rules", []), get_meta(dsl).get("domain", "generic")).items():
        lines.append(f"### {category}")
        lines.extend(f"- 覆盖规则: {item}" for item in items)
    lines.extend(["", "## 待补充测试项"])
    lines.extend([f"- {item}" for item in dsl.get("unknowns", [])] or [EMPTY_BULLET])
    return "\n".join(lines) + "\n"


def infer_endpoint(domain: str, action_id: str) -> tuple[str, str]:
    name = action_id.lower().replace("a_", "").replace("_", "-")
    return "POST", f"/api/{domain or 'generic'}/{name}"


def build_api_contracts_doc(dsl: dict) -> tuple[str, str]:
    meta = get_meta(dsl)
    domain = meta.get("domain", "generic")
    md_lines = [
        "# 接口契约草案",
        "",
        "## 生成状态",
        "- 草案待确认",
        "- 当前请求参数和返回结构主要由 DSL 动作、前置条件和结果推断得到。",
        "",
        "## 接口列表",
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
    md_lines.extend(["## 待确认项"])
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
    parser.add_argument("--workspace", help="Workspace root. Auto-detects .prd-spec or standalone workspace when omitted.")
    args = parser.parse_args()
    write_derivative_outputs(resolve_workspace(args.workspace))
    print("Derivative artifacts generated.")


if __name__ == "__main__":
    main()
