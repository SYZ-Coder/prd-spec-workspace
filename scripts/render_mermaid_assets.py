from __future__ import annotations

import argparse
from pathlib import Path

try:
    from scripts.workspace_utils import resolve_workspace
except ModuleNotFoundError:
    from workspace_utils import resolve_workspace

def copy_if_exists(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    content = src.read_text(encoding="utf-8")
    if not content.strip():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy derivative artifacts from working/ into outputs/.")
    parser.add_argument("--workspace", help="Workspace root. Auto-detects .prd-spec or standalone workspace when omitted.")
    args = parser.parse_args()

    workspace = resolve_workspace(args.workspace)
    copied = []

    if copy_if_exists(workspace / "working" / "generated-flow.md", workspace / "outputs" / "diagrams" / "generated-flow.md"):
        copied.append("outputs/diagrams/generated-flow.md")
    if copy_if_exists(workspace / "working" / "generated-testcases.md", workspace / "outputs" / "testcases" / "testcases.md"):
        copied.append("outputs/testcases/testcases.md")
    if copy_if_exists(workspace / "working" / "generated-api-contracts.md", workspace / "outputs" / "contracts" / "api-contracts.md"):
        copied.append("outputs/contracts/api-contracts.md")
    if copy_if_exists(workspace / "working" / "api-contracts" / "openapi.yaml", workspace / "outputs" / "contracts" / "openapi.yaml"):
        copied.append("outputs/contracts/openapi.yaml")

    if copied:
        print("Copied derived artifacts:")
        for item in copied:
            print(f"- {item}")
    else:
        print("No derived artifacts found to copy.")


if __name__ == "__main__":
    main()
