from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from scripts.extract_initial_dsl import OVERRIDES_FILENAME, default_extractor_overrides, load_extractor_overrides, merge_extractor_overrides
except ModuleNotFoundError:
    from extract_initial_dsl import OVERRIDES_FILENAME, default_extractor_overrides, load_extractor_overrides, merge_extractor_overrides


def config_path(workspace: Path) -> Path:
    return workspace / OVERRIDES_FILENAME


def save_overrides(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def current_custom_overrides(workspace: Path) -> dict[str, Any]:
    path = config_path(workspace)
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return {}
    return json.loads(raw)


def init_overrides(workspace: Path) -> Path:
    path = config_path(workspace)
    if not path.exists():
        save_overrides(path, default_extractor_overrides())
    return path


def add_list_value(workspace: Path, key: str, value: str) -> Path:
    data = current_custom_overrides(workspace)
    items = data.setdefault(key, [])
    if value not in items:
        items.append(value)
    save_overrides(config_path(workspace), data)
    return config_path(workspace)


def add_rule_category_keyword(workspace: Path, category: str, keyword: str) -> Path:
    data = current_custom_overrides(workspace)
    rule_categories = data.setdefault("rule_categories", {})
    keywords = rule_categories.setdefault(category, [])
    if keyword not in keywords:
        keywords.append(keyword)
    save_overrides(config_path(workspace), data)
    return config_path(workspace)


def show_overrides(workspace: Path) -> str:
    custom = current_custom_overrides(workspace)
    merged = load_extractor_overrides(workspace)
    lines = [
        "# Extractor Overrides",
        "",
        f"- Path: `{config_path(workspace)}`",
        "",
        "## Custom Overrides",
        json.dumps(custom, ensure_ascii=False, indent=2) if custom else "{}",
        "",
        "## Effective Overrides",
        json.dumps(merge_extractor_overrides(custom or None), ensure_ascii=False, indent=2),
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage extractor override configuration.")
    parser.add_argument("--workspace", default=".", help="Workspace root. Default: current directory.")
    parser.add_argument("--init", action="store_true", help="Initialize the extractor override file.")
    parser.add_argument("--show", action="store_true", help="Show current override configuration.")
    parser.add_argument("--add-page-suffix", help="Append a page suffix used for page recognition.")
    parser.add_argument("--add-action-prefix", help="Append an action prefix used for action phrase extraction.")
    parser.add_argument("--add-standalone-action", help="Append a standalone action word used for action extraction.")
    parser.add_argument("--add-rule-keyword", help="Append a rule keyword used for rule extraction.")
    parser.add_argument("--add-rule-category", help="Rule category name when adding a category keyword.")
    parser.add_argument("--add-category-keyword", help="Keyword appended to the given rule category.")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    if args.init:
        path = init_overrides(workspace)
        print(f"Initialized extractor overrides: {path}")
        return
    if args.add_page_suffix:
        path = add_list_value(workspace, "page_suffixes", args.add_page_suffix.strip())
        print(f"Updated extractor overrides: {path}")
        return
    if args.add_action_prefix:
        path = add_list_value(workspace, "action_prefixes", args.add_action_prefix.strip())
        print(f"Updated extractor overrides: {path}")
        return
    if args.add_standalone_action:
        path = add_list_value(workspace, "standalone_actions", args.add_standalone_action.strip())
        print(f"Updated extractor overrides: {path}")
        return
    if args.add_rule_keyword:
        path = add_list_value(workspace, "rule_keywords", args.add_rule_keyword.strip())
        print(f"Updated extractor overrides: {path}")
        return
    if args.add_category_keyword:
        if not args.add_rule_category:
            raise SystemExit("--add-category-keyword requires --add-rule-category")
        path = add_rule_category_keyword(workspace, args.add_rule_category.strip(), args.add_category_keyword.strip())
        print(f"Updated extractor overrides: {path}")
        return
    print(show_overrides(workspace))


if __name__ == "__main__":
    main()
