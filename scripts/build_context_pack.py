from __future__ import annotations

import argparse
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]

TARGET_FILE_MAP: dict[str, list[str]] = {
    "openspec": [
        "openspec/changes/{change_name}/proposal.md",
        "openspec/changes/{change_name}/design.md",
        "openspec/changes/{change_name}/tasks.md",
        "openspec/changes/{change_name}/specs/{domain}/spec.md",
        "working/validation-report.md",
        "working/merged-dsl.json",
        "working/generated-api-contracts.md",
        "working/generated-testcases.md",
    ],
    "superpowers": [
        "openspec/changes/{change_name}/proposal.md",
        "openspec/changes/{change_name}/design.md",
        "openspec/changes/{change_name}/tasks.md",
        "openspec/changes/{change_name}/specs/{domain}/spec.md",
        "working/generated-prd.md",
        "working/generated-flow.md",
        "working/generated-testcases.md",
        "working/generated-api-contracts.md",
        "working/api-contracts/openapi.yaml",
        "working/merged-dsl.json",
        "working/validation-report.md",
    ],
    "ai-development": [
        "working/generated-prd.md",
        "working/generated-flow.md",
        "working/generated-testcases.md",
        "working/generated-api-contracts.md",
        "working/api-contracts/openapi.yaml",
        "working/merged-dsl.json",
        "working/validation-report.md",
    ],
}

TARGET_TITLE_MAP: dict[str, str] = {
    "openspec": "OpenSpec Context Pack",
    "superpowers": "Superpowers Context Pack",
    "ai-development": "AI Development Context Pack",
}


def normalize_target(target: str) -> str:
    normalized = target.strip().lower()
    aliases = {
        "ai": "ai-development",
        "ai_dev": "ai-development",
        "ai-development": "ai-development",
        "superpower": "superpowers",
        "superpowers": "superpowers",
        "openspec": "openspec",
    }
    if normalized not in aliases:
        raise ValueError(f"Unsupported target: {target}")
    return aliases[normalized]


def default_output_path(workspace: Path, target: str) -> Path:
    normalized_target = normalize_target(target)
    return workspace / "working" / f"context-pack-{normalized_target}.md"


def files_for_target(target: str, change_name: str, domain: str) -> list[str]:
    normalized_target = normalize_target(target)
    return [
        template.format(change_name=change_name, domain=domain)
        for template in TARGET_FILE_MAP[normalized_target]
    ]


def collect_target_files(workspace: Path, target: str, change_name: str, domain: str) -> list[Path]:
    files: list[Path] = []
    for relative_path in files_for_target(target, change_name, domain):
        path = workspace / relative_path
        if path.exists() and path.is_file():
            files.append(path)
    return files


def build_context_pack_content(
    workspace: Path,
    target: str,
    change_name: str,
    domain: str,
    title: str,
    goal: str | None = None,
) -> str:
    normalized_target = normalize_target(target)
    files = collect_target_files(workspace, normalized_target, change_name, domain)
    lines = [
        f"# {TARGET_TITLE_MAP[normalized_target]}",
        "",
        f"- Change Name: {change_name}",
        f"- Domain: {domain}",
        f"- Title: {title}",
    ]
    if normalized_target == "ai-development":
        lines.append(f"- Target: {goal or '代码实现'}")
    elif goal:
        lines.append(f"- Goal: {goal}")
    lines.append("")
    for path in files:
        relative = path.relative_to(workspace).as_posix()
        lines.append(f"## File: {relative}")
        lines.append("")
        try:
            lines.extend(path.read_text(encoding="utf-8-sig").splitlines())
        except OSError:
            lines.append("_Unreadable file_")
        lines.append("")
    if not files:
        lines.extend(
            [
                "## Notes",
                "",
                "No matching files were found for this target. Confirm the change-name, domain, and generated outputs first.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_context_pack(
    workspace: Path,
    target: str,
    change_name: str,
    domain: str,
    title: str,
    goal: str | None = None,
    output_path: Path | None = None,
) -> Path:
    normalized_target = normalize_target(target)
    content = build_context_pack_content(workspace, normalized_target, change_name, domain, title, goal=goal)
    destination = output_path or default_output_path(workspace, normalized_target)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8-sig")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a reusable context pack from current workspace artifacts.")
    parser.add_argument("--workspace", default=".", help="Workspace root. Default: current directory.")
    parser.add_argument("--target", required=True, choices=["openspec", "superpowers", "ai-development", "ai"], help="Context pack target.")
    parser.add_argument("--change-name", required=True, help="Requirement change name.")
    parser.add_argument("--domain", required=True, help="Requirement domain.")
    parser.add_argument("--title", required=True, help="Requirement title.")
    parser.add_argument("--goal", help="Optional goal note for the generated context pack.")
    parser.add_argument("--output", help="Optional output file path.")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    output_path = Path(args.output).resolve() if args.output else None
    destination = build_context_pack(
        workspace=workspace,
        target=args.target,
        change_name=args.change_name,
        domain=args.domain,
        title=args.title,
        goal=args.goal,
        output_path=output_path,
    )
    print(f"Context pack written to: {destination}")


if __name__ == "__main__":
    main()
