from __future__ import annotations

import argparse
from pathlib import Path

try:
    from scripts.bootstrap_outputs import build_paths, touch
    from scripts.workspace_utils import project_local_workspace_path
except ModuleNotFoundError:
    from bootstrap_outputs import build_paths, touch
    from workspace_utils import project_local_workspace_path


DEFAULT_CONFIG = """version: 1
mode: project-local
workspace_dir: .prd-spec
notes:
  - Put requirement files into inputs/prd, inputs/notes, inputs/context, and inputs/screenshots.
  - Run the pipeline with --workspace ./.prd-spec when calling tools explicitly.
"""


def init_project_workspace(target_root: Path, change_name: str = "sample-change", domain: str = "account") -> Path:
    workspace = project_local_workspace_path(target_root)
    for path in build_paths(workspace, change_name, domain):
        touch(path)
    config_path = workspace / "config.yaml"
    if not config_path.exists():
        config_path.write_text(DEFAULT_CONFIG, encoding="utf-8-sig")
    return workspace


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a project-local .prd-spec workspace in a business repository.")
    parser.add_argument("--target", default=".", help="Business project root. Default: current directory.")
    parser.add_argument("--change-name", default="sample-change", help="Sample change name used to bootstrap the initial openspec/changes path.")
    parser.add_argument("--domain", default="account", help="Sample domain used to bootstrap the initial openspec/changes path.")
    args = parser.parse_args()

    target_root = Path(args.target).resolve()
    workspace = init_project_workspace(target_root, change_name=args.change_name, domain=args.domain)
    print("Project-local workspace initialized.")
    print(f"- target root: {target_root}")
    print(f"- workspace: {workspace}")
    print("- next: place materials under .prd-spec/inputs/ and run the pipeline with --workspace ./.prd-spec")


if __name__ == "__main__":
    main()
