from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def unique_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def resolve_assets(
    catalog: dict[str, Any],
    bundles: list[str],
    asset_ids: list[str],
    domain: str,
    change_name: str,
) -> list[dict[str, Any]]:
    bundle_map = {item["bundle_id"]: item for item in catalog.get("bundles", [])}
    asset_map = {item["asset_id"]: item for item in catalog.get("assets", [])}

    resolved_ids: list[str] = []
    for bundle_id in bundles:
        bundle = bundle_map.get(bundle_id)
        if bundle:
            resolved_ids.extend(bundle.get("default_asset_ids") or bundle.get("asset_ids") or [])

    resolved_ids.extend(asset_ids)

    if domain:
        resolved_ids.extend(
            item["asset_id"]
            for item in catalog.get("assets", [])
            if item.get("domain") == domain and item.get("type") in {"rule", "pattern"}
        )
    if change_name:
        resolved_ids.extend(
            item["asset_id"]
            for item in catalog.get("assets", [])
            if item.get("change_name") == change_name
        )

    return [asset_map[item_id] for item_id in unique_keep_order(resolved_ids) if item_id in asset_map]


def format_catalog_listing(
    catalog: dict[str, Any],
    domain: str = "",
    change_name: str = "",
) -> str:
    changes = [
        item
        for item in catalog.get("changes", [])
        if (not domain or item.get("domain") == domain) and (not change_name or item.get("change_name") == change_name)
    ]
    assets = [
        item
        for item in catalog.get("assets", [])
        if (not domain or item.get("domain") == domain) and (not change_name or item.get("change_name") == change_name)
    ]
    bundles = [
        item
        for item in catalog.get("bundles", [])
        if (not domain or item.get("domain") == domain) and (not change_name or item.get("change_name", "") in {"", change_name})
    ]

    lines = [
        "# Context Catalog",
        "",
        f"- Domain Filter: `{domain or 'all'}`",
        f"- Change Filter: `{change_name or 'all'}`",
        "",
        "## Bundles",
    ]
    if bundles:
        for bundle in bundles:
            lines.append(
                f"- {bundle['bundle_id']} | domain={bundle.get('domain', '')} | assets={len(bundle.get('asset_ids', []))} | title={bundle.get('title', '')}"
            )
    else:
        lines.append("- None")

    lines.extend(["", "## Assets"])
    if assets:
        for asset in assets:
            lines.append(
                f"- {asset['asset_id']} | type={asset.get('type', '')} | domain={asset.get('domain', '')} | change={asset.get('change_name', '')} | path={asset.get('path', '')}"
            )
    else:
        lines.append("- None")

    lines.extend(["", "## Changes"])
    if changes:
        for change in changes:
            lines.append(
                f"- {change['change_id']} | change={change.get('change_name', '')} | domain={change.get('domain', '')} | snapshot={change.get('snapshot_path', '')}"
            )
    else:
        lines.append("- None")

    return "\n".join(lines) + "\n"


def format_context_selection(
    domain: str,
    change_name: str,
    bundles: list[str],
    assets: list[dict[str, Any]],
    selected_snapshot: dict[str, Any] | None,
) -> str:
    lines = [
        "# Context Selection",
        "",
        f"- Domain: `{domain or 'unspecified'}`",
        f"- Change Name: `{change_name or 'unspecified'}`",
        f"- Bundles: `{', '.join(bundles) if bundles else 'none'}`",
        "",
        "## Selected Assets",
    ]
    if assets:
        for asset in assets:
            lines.append(
                f"- {asset['asset_id']} | type={asset['type']} | domain={asset['domain']} | path={asset['path']}"
            )
    else:
        lines.append("- None")

    lines.extend(["", "## Selected Snapshot"])
    if selected_snapshot:
        lines.append(
            f"- {selected_snapshot['change_id']} | path={selected_snapshot['snapshot_path']} | title={selected_snapshot['title']}"
        )
    else:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def select_context(
    workspace: Path,
    bundles: list[str],
    asset_ids: list[str],
    domain: str = "",
    change_name: str = "",
    include_snapshot: bool = False,
) -> dict[str, Any]:
    knowledge_root = workspace / "knowledge"
    catalog = read_json(knowledge_root / "catalog.json")
    selected_assets = resolve_assets(catalog, bundles, asset_ids, domain, change_name)

    selected_snapshot = None
    if include_snapshot and change_name:
        for item in catalog.get("changes", []):
            if item.get("change_name") == change_name:
                selected_snapshot = item
                break

    context_root = workspace / "inputs" / "context" / "knowledge"
    if context_root.exists():
        shutil.rmtree(context_root)
    context_root.mkdir(parents=True, exist_ok=True)

    materialized_assets: list[dict[str, Any]] = []
    for asset in selected_assets:
        source = workspace / Path(asset["path"])
        if not source.exists():
            continue
        destination = context_root / Path(asset["path"]).name
        shutil.copy2(source, destination)
        copied = dict(asset)
        copied["materialized_path"] = str(destination.relative_to(workspace)).replace("\\", "/")
        materialized_assets.append(copied)

    snapshot_copy_path = ""
    if selected_snapshot:
        source_snapshot = workspace / Path(selected_snapshot["snapshot_path"])
        snapshot_copy_path = str((context_root / "snapshot").relative_to(workspace)).replace("\\", "/")
        if source_snapshot.exists():
            shutil.copytree(source_snapshot, context_root / "snapshot")

    selection_manifest = {
        "domain": domain,
        "change_name": change_name,
        "bundles": bundles,
        "asset_ids": [item["asset_id"] for item in materialized_assets],
        "snapshot_change_id": selected_snapshot.get("change_id") if selected_snapshot else "",
        "snapshot_materialized_path": snapshot_copy_path,
    }
    write_text(context_root / "selection.json", json.dumps(selection_manifest, ensure_ascii=False, indent=2) + "\n")
    write_text(
        context_root / "context-selection.md",
        format_context_selection(domain, change_name, bundles, materialized_assets, selected_snapshot),
    )
    return selection_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Select archived knowledge assets into inputs/context/knowledge.")
    parser.add_argument("--workspace", default=".", help="Workspace root. Default: current directory.")
    parser.add_argument("--domain", default="", help="Select rule/pattern assets from a domain.")
    parser.add_argument("--change-name", default="", help="Select all assets for a historical change.")
    parser.add_argument("--bundle", action="append", default=[], help="Bundle id to include. Can be repeated.")
    parser.add_argument("--asset-id", action="append", default=[], help="Asset id to include. Can be repeated.")
    parser.add_argument("--include-snapshot", action="store_true", help="Also copy the archived snapshot for the selected change.")
    parser.add_argument("--list", action="store_true", help="List selectable bundles, assets, and changes instead of materializing context.")
    args = parser.parse_args()
    if args.list:
        return args
    if not (args.domain or args.change_name or args.bundle or args.asset_id):
        parser.error("At least one of --domain, --change-name, --bundle, or --asset-id is required.")
    return args


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    if args.list:
        catalog = read_json(workspace / "knowledge" / "catalog.json")
        print(format_catalog_listing(catalog, domain=args.domain, change_name=args.change_name))
        return
    result = select_context(
        workspace=workspace,
        bundles=args.bundle,
        asset_ids=args.asset_id,
        domain=args.domain,
        change_name=args.change_name,
        include_snapshot=args.include_snapshot,
    )
    print("Context selection completed.")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
