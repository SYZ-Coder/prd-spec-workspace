from __future__ import annotations

import argparse
from pathlib import Path


def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("", encoding="utf-8")


def build_paths(change_name: str, domain: str) -> list[Path]:
    return [
        Path("working/page-source-map.md"),
        Path("working/page-classification.json"),
        Path("working/transition-map.md"),
        Path("working/shared-rules.md"),
        Path("working/raw-dsl.json"),
        Path("working/merged-dsl.json"),
        Path("working/validation-report.md"),
        Path("working/generated-prd.md"),
        Path("working/generated-flow.md"),
        Path("working/generated-testcases.md"),
        Path("working/generated-api-contracts.md"),
        Path("working/api-contracts/openapi.yaml"),
        Path("outputs/diagrams/.gitkeep"),
        Path("outputs/testcases/.gitkeep"),
        Path("outputs/contracts/.gitkeep"),
        Path("knowledge/specs/.gitkeep"),
        Path("knowledge/patterns/.gitkeep"),
        Path("knowledge/rules/.gitkeep"),
        Path("knowledge/api/.gitkeep"),
        Path("knowledge/decisions/.gitkeep"),
        Path("knowledge/assets/specs/.gitkeep"),
        Path("knowledge/assets/rules/.gitkeep"),
        Path("knowledge/assets/patterns/.gitkeep"),
        Path("knowledge/assets/api/.gitkeep"),
        Path("knowledge/assets/decisions/.gitkeep"),
        Path("knowledge/bundles/.gitkeep"),
        Path("knowledge/snapshots/.gitkeep"),
        Path("knowledge/catalog.json"),
        Path("openspec/changes") / change_name / "proposal.md",
        Path("openspec/changes") / change_name / "design.md",
        Path("openspec/changes") / change_name / "tasks.md",
        Path("openspec/changes") / change_name / "specs" / domain / "spec.md",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap working, output, knowledge, and OpenSpec change files.")
    parser.add_argument("--change-name", required=True, help="OpenSpec change folder name.")
    parser.add_argument("--domain", default="account", help="OpenSpec domain name. Default: account")
    args = parser.parse_args()

    for path in build_paths(args.change_name, args.domain):
        touch(path)

    print("Bootstrap complete.")
    print(f"- change: openspec/changes/{args.change_name}")
    print(f"- domain: {args.domain}")


if __name__ == "__main__":
    main()
