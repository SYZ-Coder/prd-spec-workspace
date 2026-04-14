from __future__ import annotations

import argparse
from pathlib import Path

try:
    from scripts.workspace_utils import resolve_workspace
except ModuleNotFoundError:
    from workspace_utils import resolve_workspace


def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("", encoding="utf-8")


def build_paths(workspace: Path, change_name: str, domain: str) -> list[Path]:
    return [
        workspace / "inputs" / "prd" / ".gitkeep",
        workspace / "inputs" / "screenshots" / ".gitkeep",
        workspace / "inputs" / "notes" / ".gitkeep",
        workspace / "inputs" / "context" / ".gitkeep",
        workspace / "working" / "page-source-map.md",
        workspace / "working" / "page-classification.json",
        workspace / "working" / "screenshot-text-evidence.json",
        workspace / "working" / "screenshot-evidence.md",
        workspace / "working" / "transition-map.md",
        workspace / "working" / "shared-rules.md",
        workspace / "working" / "raw-dsl.json",
        workspace / "working" / "merged-dsl.json",
        workspace / "working" / "validation-report.md",
        workspace / "working" / "generated-prd.md",
        workspace / "working" / "generated-flow.md",
        workspace / "working" / "generated-testcases.md",
        workspace / "working" / "generated-api-contracts.md",
        workspace / "working" / "api-contracts" / "openapi.yaml",
        workspace / "outputs" / "diagrams" / ".gitkeep",
        workspace / "outputs" / "testcases" / ".gitkeep",
        workspace / "outputs" / "contracts" / ".gitkeep",
        workspace / "knowledge" / "specs" / ".gitkeep",
        workspace / "knowledge" / "patterns" / ".gitkeep",
        workspace / "knowledge" / "rules" / ".gitkeep",
        workspace / "knowledge" / "api" / ".gitkeep",
        workspace / "knowledge" / "decisions" / ".gitkeep",
        workspace / "knowledge" / "assets" / "specs" / ".gitkeep",
        workspace / "knowledge" / "assets" / "rules" / ".gitkeep",
        workspace / "knowledge" / "assets" / "patterns" / ".gitkeep",
        workspace / "knowledge" / "assets" / "api" / ".gitkeep",
        workspace / "knowledge" / "assets" / "decisions" / ".gitkeep",
        workspace / "knowledge" / "bundles" / ".gitkeep",
        workspace / "knowledge" / "snapshots" / ".gitkeep",
        workspace / "knowledge" / "catalog.json",
        workspace / "openspec" / "changes" / change_name / "proposal.md",
        workspace / "openspec" / "changes" / change_name / "design.md",
        workspace / "openspec" / "changes" / change_name / "tasks.md",
        workspace / "openspec" / "changes" / change_name / "specs" / domain / "spec.md",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap working, output, knowledge, and OpenSpec change files.")
    parser.add_argument("--workspace", help="Workspace root. Auto-detects .prd-spec or standalone workspace when omitted.")
    parser.add_argument("--change-name", required=True, help="OpenSpec change folder name.")
    parser.add_argument("--domain", default="account", help="OpenSpec domain name. Default: account")
    args = parser.parse_args()

    workspace = resolve_workspace(args.workspace)
    for path in build_paths(workspace, args.change_name, args.domain):
        touch(path)

    print("Bootstrap complete.")
    print(f"- workspace: {workspace}")
    print(f"- change: openspec/changes/{args.change_name}")
    print(f"- domain: {args.domain}")


if __name__ == "__main__":
    main()
