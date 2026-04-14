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
DEFAULT_DOMAIN_LABEL = "\u901a\u7528\u4ea7\u54c1\u9700\u6c42"
DEFAULT_SUMMARY = "\u4ece\u8f93\u5165\u6750\u6599\u4e2d\u63d0\u70bc\u9875\u9762\u3001\u6d41\u8f6c\u548c\u4e1a\u52a1\u89c4\u5219\u3002"
DEFAULT_PROPOSAL_BACKGROUND = "\u5f53\u524d\u9700\u6c42\u9700\u8981\u4ece\u73b0\u6709\u8f93\u5165\u4e2d\u5f52\u7eb3\u9875\u9762\u3001\u52a8\u4f5c\u4e0e\u4e1a\u52a1\u89c4\u5219\u3002"


def load_dsl(workspace: Path) -> dict:
    return json.loads((workspace / "working" / "merged-dsl.json").read_text(encoding="utf-8-sig"))


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else EMPTY_BULLET


def get_meta(dsl: dict) -> dict:
    return dsl.get("meta", {})


def build_grouped_rule_lines(dsl: dict) -> list[str]:
    meta = get_meta(dsl)
    grouped = group_rules(dsl.get("rules", []), meta.get("domain", "generic"))
    lines: list[str] = []
    for category, items in grouped.items():
        lines.append(f"### {category}")
        lines.extend(f"- {item}" for item in items)
        lines.append("")
    if not lines:
        return [EMPTY_BULLET]
    if lines[-1] == "":
        lines.pop()
    return lines


def build_generated_prd(title: str, dsl: dict) -> str:
    meta = get_meta(dsl)
    pages = dsl.get("pages", [])
    transitions = dsl.get("transitions", [])
    dependencies = dsl.get("dependencies", [])
    unknowns = dsl.get("unknowns", [])
    domain_label = meta.get("domain_label", DEFAULT_DOMAIN_LABEL)
    summary = meta.get("summary", DEFAULT_SUMMARY)

    lines = [
        f"# {title}",
        "",
        "## \u80cc\u666f",
        f"\u57fa\u4e8e\u5f53\u524d PRD\u3001\u622a\u56fe\u548c\u4e0a\u4e0b\u6587\uff0c\u751f\u6210\u4e00\u4efd\u9762\u5411 `{domain_label}` \u7684\u7ed3\u6784\u5316\u9700\u6c42\u8349\u6848\u3002",
        "",
        "## \u76ee\u6807",
        f"- {summary}",
        "",
        "## \u5df2\u786e\u8ba4\u4e8b\u5b9e",
        "### \u9875\u9762\u6e05\u5355",
    ]
    lines.extend([f"- {page['name']} ({page['id']})\uff1a{page['goal']}" for page in pages] or [EMPTY_BULLET])
    lines.extend(["", "### \u9875\u9762\u6d41\u8f6c"])
    lines.extend(
        [
            f"- {item['from_page']} -> {item['to_page']}\uff1a{item['trigger']} / {item['condition']} / {item['result']}"
            for item in transitions
        ]
        or [EMPTY_BULLET]
    )
    lines.extend(["", "### \u5173\u952e\u4e1a\u52a1\u89c4\u5219"])
    lines.extend(build_grouped_rule_lines(dsl))
    lines.extend(["", "### \u4f9d\u8d56", bullet_list(dependencies)])
    lines.extend(["", "## \u7ed3\u6784\u5316\u63a8\u65ad", bullet_list(meta.get("inferred_facts", []))])
    lines.extend(["", "## \u5f85\u786e\u8ba4\u9879", bullet_list(unknowns)])
    return "\n".join(lines) + "\n"


def build_proposal(title: str, dsl: dict) -> str:
    meta = get_meta(dsl)
    page_names = [page["name"] for page in dsl.get("pages", [])]
    proposal_background = meta.get("proposal_background", DEFAULT_PROPOSAL_BACKGROUND)
    return (
        f"# Proposal: {title}\n\n"
        "## \u80cc\u666f\n"
        f"{proposal_background}\n\n"
        "## \u8303\u56f4\n"
        f"{bullet_list(page_names)}\n\n"
        "## \u5f71\u54cd\u9762\n"
        f"{bullet_list(dsl.get('dependencies', []))}\n\n"
        "## \u5f85\u786e\u8ba4\u9879\n"
        f"{bullet_list(dsl.get('unknowns', []))}\n"
    )


def build_design(dsl: dict) -> str:
    lines = [
        "# Design",
        "",
        "## \u9875\u9762\u6d41\u8f6c",
        bullet_list(
            [
                f"{item['from_page']} -> {item['to_page']} ({item['trigger']} / {item['condition']})"
                for item in dsl.get("transitions", [])
            ]
        ),
        "",
        "## \u9875\u9762\u72b6\u6001",
    ]
    for page in dsl.get("pages", []):
        lines.append(f"### {page['name']} ({page['id']})")
        lines.append(bullet_list(page.get("states", [])))
    lines.extend(["", "## \u5173\u952e\u4e1a\u52a1\u89c4\u5219"])
    lines.extend(build_grouped_rule_lines(dsl))
    lines.extend(["", "## \u4f9d\u8d56", bullet_list(dsl.get("dependencies", [])), "", "## \u5f85\u786e\u8ba4\u9879", bullet_list(dsl.get("unknowns", []))])
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
        f"- [ ] Review `{meta.get('domain_label', 'General Product Requirement')}` unknowns and move confirmed items into stable artifacts.",
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
    path.write_text(content, encoding="utf-8-sig")


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
    parser.add_argument("--workspace", help="Workspace root. Auto-detects .prd-spec or standalone workspace when omitted.")
    parser.add_argument("--change-name", required=True, help="OpenSpec change name.")
    parser.add_argument("--domain", required=True, help="OpenSpec domain.")
    parser.add_argument("--title", required=True, help="Human-readable title.")
    args = parser.parse_args()
    write_draft_outputs(resolve_workspace(args.workspace), args.change_name, args.domain, args.title)
    print("Draft PRD and OpenSpec artifacts generated.")


if __name__ == "__main__":
    main()
