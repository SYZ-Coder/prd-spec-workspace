from __future__ import annotations

from pathlib import Path


TOOL_ROOT = Path(__file__).resolve().parents[1]
PROJECT_LOCAL_DIRNAME = ".prd-spec"


def is_standalone_workspace(path: Path) -> bool:
    return (
        path.is_dir()
        and (path / "inputs").exists()
        and (path / "scripts").exists()
        and (path / "AGENTS.md").exists()
    )


def is_project_local_workspace(path: Path) -> bool:
    return path.is_dir() and path.name == PROJECT_LOCAL_DIRNAME and (path / "inputs").exists()


def find_workspace(start: Path) -> Path | None:
    current = start.resolve()
    candidates = [current, *current.parents]
    for candidate in candidates:
        if is_project_local_workspace(candidate):
            return candidate
        project_local = candidate / PROJECT_LOCAL_DIRNAME
        if is_project_local_workspace(project_local):
            return project_local.resolve()
        if is_standalone_workspace(candidate):
            return candidate
    return None


def resolve_workspace(
    workspace_arg: str | None = None,
    *,
    start: Path | None = None,
    tool_root: Path | None = None,
) -> Path:
    if workspace_arg:
        return Path(workspace_arg).resolve()
    discovered = find_workspace(start or Path.cwd())
    if discovered:
        return discovered
    fallback = (tool_root or TOOL_ROOT).resolve()
    return fallback


def project_local_workspace_path(target_root: Path) -> Path:
    return target_root.resolve() / PROJECT_LOCAL_DIRNAME
