from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from scripts.extract_initial_dsl import group_rules
except ModuleNotFoundError:
    from extract_initial_dsl import group_rules


def load_dsl(workspace: Path) -> dict:
    return json.loads((workspace / "working" / "merged-dsl.json").read_text(encoding="utf-8"))


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- None"


def get_meta(dsl: dict) -> dict:
    return dsl.get("meta", {})


def build_grouped_rule_lines(dsl: dict) -> list[str]:
    meta = get_meta(dsl)
    grouped = group_rules(dsl.get("rules", []), meta.get("domain", "generic"))
    lines: list[str] = []
    for category, items in grouped.items():
        lines.append(f"### {category}")
        lines.extend([f"- {item}" for item in items])
        lines.append("")
    if not lines:
        return ["- None"]
    if lines[-1] == "":
        lines.pop()
    return lines


def build_generated_prd(title: str, dsl: dict) -> str:
    meta = get_meta(dsl)
    pages = dsl.get("pages", [])
    transitions = dsl.get("transitions", [])
    dependencies = dsl.get("dependencies", [])
    unknowns = dsl.get("unknowns", [])

    lines = [
        f"# {title}",
        "",
        "## 背景",
        f"基于当前 PRD、截图和上下文，生成一份面向 `{meta.get('domain_label', '通用需求')}` 的结构化需求草案。",
        "",
        "## 目标",
        f"- {meta.get('summary', '从输入中提炼页面、流程和业务规则。')}",
        "",
        "## 已确认事实",
        "### 页面清单",
    ]
    lines.extend([f"- {page['name']} ({page['id']})：{page['goal']}" for page in pages] or ["- None"])
    lines.extend(["", "### 页面流转"])
    lines.extend(
        [
            f"- {item['from_page']} -> {item['to_page']}：{item['trigger']} / {item['condition']} / {item['result']}"
            for item in transitions
        ]
        or ["- None"]
    )
    lines.extend(["", "### 关键业务规则"])
    lines.extend(build_grouped_rule_lines(dsl))
    lines.extend(["", "### 依赖", bullet_list(dependencies)])
    lines.extend(["", "## 结构化推断", bullet_list(meta.get("inferred_facts", []))])
    lines.extend(["", "## 待确认项", bullet_list(unknowns)])
    return "\n".join(lines) + "\n"


def build_proposal(title: str, dsl: dict) -> str:
    meta = get_meta(dsl)
    page_names = [page["name"] for page in dsl.get("pages", [])]
    return (
        f"# Proposal: {title}\n\n"
        "## 背景\n"
        f"{meta.get('proposal_background', '当前需求需要从现有输入中归纳页面、动作与业务规则。')}\n\n"
        "## 范围\n"
        f"{bullet_list(page_names)}\n\n"
        "## 影响面\n"
        f"{bullet_list(dsl.get('dependencies', []))}\n\n"
        "## 待确认项\n"
        f"{bullet_list(dsl.get('unknowns', []))}\n"
    )


def build_design(dsl: dict) -> str:
    lines = [
        "# Design",
        "",
        "## 页面流转",
        bullet_list(
            [
                f"{item['from_page']} -> {item['to_page']} ({item['trigger']} / {item['condition']})"
                for item in dsl.get("transitions", [])
            ]
        ),
        "",
        "## 页面状态",
    ]
    for page in dsl.get("pages", []):
        lines.append(f"### {page['name']} ({page['id']})")
        lines.append(bullet_list(page.get("states", [])))
    lines.extend(["", "## 关键业务规则"])
    lines.extend(build_grouped_rule_lines(dsl))
    lines.extend(["", "## 依赖", bullet_list(dsl.get("dependencies", [])), "", "## 待确认项", bullet_list(dsl.get("unknowns", []))])
    return "\n".join(lines) + "\n"


def build_tasks(dsl: dict) -> str:
    meta = get_meta(dsl)
    page_ids = [page["id"] for page in dsl.get("pages", [])]
    lines = [
        "# Tasks",
        "",
        "## Implementation Tasks",
        "- [ ] Confirm screenshot-derived page names, fields, and user actions.",
        "- [ ] Refine merged-dsl.json with product-confirmed states, validation rules, and error paths.",
        "- [ ] Align inferred API contracts with real context interfaces before implementation.",
        f"- [ ] Review `{meta.get('domain_label', '通用需求')}` unknowns and move confirmed items into stable artifacts.",
    ]
    if page_ids:
        lines.append(f"- [ ] Validate page coverage for: {', '.join(page_ids)}.")
    return "\n".join(lines) + "\n"


def build_spec(dsl: dict) -> str:
    meta = get_meta(dsl)
    rules = dsl.get("rules", [])
    scenario_lines: list[str] = []
    for rule in rules[:5]:
        scenario_lines.extend(
            [
                "### Scenario:",
                f"- Given {rule}",
                "- When the system reaches the related business stage",
                "- Then the system must honor this rule and surface the expected result",
                "",
            ]
        )
    if not scenario_lines:
        scenario_lines = [
            "### Scenario:",
            f"- Given the user starts the {meta.get('feature_name', 'current')} flow",
            "- Then the system should follow the validated DSL",
            "",
        ]
    return (
        "# Spec\n\n"
        f"## Requirement: {meta.get('requirement_name', 'General Product Requirement')}\n"
        f"- The system must support the `{meta.get('feature_name', 'current')}` pages, transitions, and business constraints defined in the DSL.\n\n"
        + "\n".join(scenario_lines)
        + "## Unknowns\n"
        + bullet_list(dsl.get("unknowns", []))
        + "\n"
    )


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_draft_outputs(workspace: Path, change_name: str, domain: str, title: str) -> None:
    dsl = load_dsl(workspace)
    write_text(workspace / "working" / "generated-prd.md", build_generated_prd(title, dsl))
    change_root = workspace / "openspec" / "changes" / change_name
    write_text(change_root / "proposal.md", build_proposal(title, dsl))
    write_text(change_root / "design.md", build_design(dsl))
    write_text(change_root / "tasks.md", build_tasks(dsl))
    write_text(change_root / "specs" / domain / "spec.md", build_spec(dsl))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate draft PRD and OpenSpec artifacts from merged DSL.")
    parser.add_argument("--workspace", default=".", help="Workspace root. Default: current directory.")
    parser.add_argument("--change-name", required=True, help="OpenSpec change name.")
    parser.add_argument("--domain", required=True, help="OpenSpec domain.")
    parser.add_argument("--title", required=True, help="Human-readable title.")
    args = parser.parse_args()
    write_draft_outputs(Path(args.workspace).resolve(), args.change_name, args.domain, args.title)
    print("Draft PRD and OpenSpec artifacts generated.")


if __name__ == "__main__":
    main()
