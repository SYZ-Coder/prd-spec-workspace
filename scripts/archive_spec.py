#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


CATALOG_VERSION = "1.0"
ASSET_TYPES = ("spec", "rule", "pattern", "decision", "api")


@dataclass
class ArchiveConfig:
    workspace: Path
    change_name: str
    domain: str
    title: str
    dry_run: bool = False


def read_text(path: Path, default: str = "") -> str:
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8").strip()


def write_text(path: Path, content: str, dry_run: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        print(f"[DRY-RUN] write -> {path}")
        return
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: dict[str, Any], dry_run: bool = False) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n", dry_run=dry_run)


def copy_file(src: Path, dst: Path, dry_run: bool = False) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        print(f"[DRY-RUN] copy -> {src} => {dst}")
        return
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path, dry_run: bool = False) -> None:
    if not src.exists():
        return
    if dry_run:
        print(f"[DRY-RUN] copy tree -> {src} => {dst}")
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def clear_directory(directory: Path, dry_run: bool = False, preserve_names: set[str] | None = None) -> None:
    if not directory.exists():
        return
    preserve_names = preserve_names or set()
    for child in directory.iterdir():
        if child.name in preserve_names:
            continue
        if dry_run:
            print(f"[DRY-RUN] remove -> {child}")
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def load_json(path: Path) -> dict[str, Any]:
    raw = read_text(path, "{}")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff_-]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "unknown"


def unique_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = item.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def ensure_catalog(knowledge_root: Path) -> dict[str, Any]:
    catalog_path = knowledge_root / "catalog.json"
    if catalog_path.exists():
        catalog = load_json(catalog_path)
    else:
        catalog = {}
    catalog.setdefault("version", CATALOG_VERSION)
    catalog.setdefault("changes", [])
    catalog.setdefault("assets", [])
    catalog.setdefault("bundles", [])
    return catalog


def replace_entry(entries: list[dict[str, Any]], key: str, value: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    filtered = [item for item in entries if item.get(key) != value]
    filtered.append(payload)
    filtered.sort(key=lambda item: str(item.get(key, "")))
    return filtered


def relative_to_workspace(workspace: Path, path: Path) -> str:
    return str(path.relative_to(workspace)).replace("\\", "/")


def build_paths(cfg: ArchiveConfig) -> dict[str, Path]:
    workspace = cfg.workspace
    change_root = workspace / "openspec" / "changes" / cfg.change_name
    working_root = workspace / "working"
    outputs_root = workspace / "outputs"
    knowledge_root = workspace / "knowledge"
    snapshot_name = f"{datetime.now().strftime('%Y-%m-%d')}_{cfg.change_name}"
    assets_root = knowledge_root / "assets"

    return {
        "workspace": workspace,
        "change_root": change_root,
        "working_root": working_root,
        "outputs_root": outputs_root,
        "knowledge_root": knowledge_root,
        "catalog": knowledge_root / "catalog.json",
        "knowledge_index": knowledge_root / "index.md",
        "bundles_root": knowledge_root / "bundles",
        "bundle_change": knowledge_root / "bundles" / f"{cfg.change_name}.json",
        "bundle_domain": knowledge_root / "bundles" / f"{cfg.domain}-core.json",
        "snapshot_root": knowledge_root / "snapshots" / snapshot_name,
        "snapshot_manifest": knowledge_root / "snapshots" / snapshot_name / "manifest.json",
        "snapshot_inputs": knowledge_root / "snapshots" / snapshot_name / "inputs",
        "snapshot_working": knowledge_root / "snapshots" / snapshot_name / "working",
        "snapshot_outputs": knowledge_root / "snapshots" / snapshot_name / "outputs",
        "snapshot_change": knowledge_root / "snapshots" / snapshot_name / "openspec-change",
        "proposal": change_root / "proposal.md",
        "design": change_root / "design.md",
        "tasks": change_root / "tasks.md",
        "delta_spec": change_root / "specs" / cfg.domain / "spec.md",
        "merged_dsl": working_root / "merged-dsl.json",
        "validation_report": working_root / "validation-report.md",
        "generated_prd": working_root / "generated-prd.md",
        "generated_api_contracts": working_root / "generated-api-contracts.md",
        "openapi": working_root / "api-contracts" / "openapi.yaml",
        "generated_flow": working_root / "generated-flow.md",
        "generated_testcases": working_root / "generated-testcases.md",
        "asset_spec": assets_root / "specs" / cfg.domain / f"{cfg.change_name}.md",
        "asset_rule": assets_root / "rules" / cfg.domain / f"{cfg.change_name}.md",
        "asset_pattern": assets_root / "patterns" / cfg.domain / f"{cfg.change_name}.md",
        "asset_decision": assets_root / "decisions" / cfg.domain / f"{cfg.change_name}.md",
        "asset_api_md": assets_root / "api" / cfg.domain / f"{cfg.change_name}.md",
        "asset_api_yaml": assets_root / "api" / cfg.domain / f"{cfg.change_name}.openapi.yaml",
        "legacy_spec": knowledge_root / "specs" / f"{cfg.change_name}.md",
        "legacy_rule": knowledge_root / "rules" / f"{cfg.change_name}.md",
        "legacy_pattern": knowledge_root / "patterns" / f"{cfg.change_name}.md",
        "legacy_decision": knowledge_root / "decisions" / f"{cfg.change_name}.md",
        "legacy_api_md": knowledge_root / "api" / f"{cfg.change_name}.md",
        "legacy_api_yaml": knowledge_root / "api" / f"{cfg.change_name}.openapi.yaml",
    }


def extract_rules_from_dsl(dsl: dict[str, Any]) -> list[str]:
    return unique_keep_order(list(dsl.get("rules", []) or []))


def extract_unknowns_from_dsl(dsl: dict[str, Any]) -> list[str]:
    unknowns = list(dsl.get("unknowns", []) or [])
    for page in dsl.get("pages", []) or []:
        unknowns.extend(page.get("unknowns", []) or [])
    return unique_keep_order(unknowns)


def extract_patterns_from_dsl(dsl: dict[str, Any]) -> tuple[list[str], dict[str, list[str]]]:
    patterns: list[str] = []
    examples: dict[str, list[str]] = {}
    for page in dsl.get("pages", []) or []:
        page_name = page.get("name", "") or page.get("id", "")
        if page.get("states"):
            pattern = "页面模式:显式状态建模"
            patterns.append(pattern)
            examples.setdefault(pattern, []).append(page_name)
        if page.get("actions"):
            pattern = "动作模式:提交含失败路径"
            patterns.append(pattern)
            examples.setdefault(pattern, []).append(page_name)
        if "投票" in page_name or "发言" in page_name:
            pattern = "交互模式:回合制流程"
            patterns.append(pattern)
            examples.setdefault(pattern, []).append(page_name)
    return unique_keep_order(patterns), {key: unique_keep_order(value) for key, value in examples.items()}


def collect_tags(cfg: ArchiveConfig, dsl: dict[str, Any]) -> list[str]:
    tags = [cfg.domain, cfg.change_name]
    tags.extend(page.get("id", "") for page in dsl.get("pages", []) or [])
    tags.extend(dep for dep in dsl.get("dependencies", []) or [])
    return unique_keep_order(slugify(tag) for tag in tags if tag)


def build_specs_archive(cfg: ArchiveConfig, paths: dict[str, Path], dsl: dict[str, Any]) -> str:
    page_names = [page.get("name", "") for page in dsl.get("pages", []) or [] if page.get("name")]
    dependencies = unique_keep_order(dsl.get("dependencies", []) or [])
    rules = extract_rules_from_dsl(dsl)
    transitions = dsl.get("transitions", []) or []
    transition_lines = [
        f"- {item.get('from_page', 'UNKNOWN')} -> {item.get('to_page', 'UNKNOWN')}：{item.get('condition', '无条件')} / {item.get('result', '无结果说明')}"
        for item in transitions
    ]
    sections = [
        f"# {cfg.title}（归档版）",
        "",
        "## 基本信息",
        f"- change_name: `{cfg.change_name}`",
        f"- domain: `{cfg.domain}`",
        "",
        "## 页面",
        *([f"- {item}" for item in page_names] or ["- 无"]),
        "",
        "## 流程流转",
        *(transition_lines or ["- 无"]),
        "",
        "## 业务规则",
        *([f"- {item}" for item in rules] or ["- 无"]),
        "",
        "## 依赖",
        *([f"- {item}" for item in dependencies] or ["- 无"]),
        "",
        "## 提案摘要",
        read_text(paths["proposal"], "（无）"),
        "",
        "## 设计摘要",
        read_text(paths["design"], "（无）"),
        "",
        "## Delta Spec",
        read_text(paths["delta_spec"], "（无）"),
        "",
        "## 生成版 PRD 摘要",
        read_text(paths["generated_prd"], "（无）"),
        "",
        "## 校验摘要",
        read_text(paths["validation_report"], "（无）"),
    ]
    return "\n".join(sections).strip() + "\n"


def build_rules_archive(cfg: ArchiveConfig, dsl: dict[str, Any]) -> str:
    rules = extract_rules_from_dsl(dsl)
    lines = [f"# {cfg.title} 规则沉淀", "", "## 业务规则"]
    lines.extend([f"- {item}" for item in rules] or ["- 无"])
    lines.extend(["", "## 建议", "- 仅在同域或强相关玩法需求中引入这些规则。"])
    return "\n".join(lines) + "\n"


def build_patterns_archive(cfg: ArchiveConfig, dsl: dict[str, Any]) -> str:
    patterns, examples = extract_patterns_from_dsl(dsl)
    lines = [f"# {cfg.title} 模式沉淀", "", "## 提炼出的模式"]
    if patterns:
        for pattern in patterns:
            lines.append(f"- {pattern}（示例页面：{'、'.join(examples.get(pattern, [])) or '无'}）")
    else:
        lines.append("- 无")
    lines.extend(["", "## 建议", "- 后续需求只在交互结构相似时复用这些模式。"])
    return "\n".join(lines) + "\n"


def build_decisions_archive(cfg: ArchiveConfig, dsl: dict[str, Any], validation_report: str) -> str:
    unknowns = extract_unknowns_from_dsl(dsl)
    lines = [f"# {cfg.title} 决策与待确认项", "", "## 当前 unknowns"]
    if unknowns:
        for item in unknowns:
            lines.append(f"- 问题：{item}")
            lines.append("  - 当前状态：待确认")
            lines.append("  - 最终决策：")
            lines.append("  - 备注：")
    else:
        lines.append("- 无")
    if validation_report:
        lines.extend(["", "## 校验报告参考", validation_report])
    return "\n".join(lines) + "\n"


def build_asset_manifest(cfg: ArchiveConfig, paths: dict[str, Path], dsl: dict[str, Any]) -> dict[str, Any]:
    tags = collect_tags(cfg, dsl)
    asset_map = {
        "spec": paths["asset_spec"],
        "rule": paths["asset_rule"],
        "pattern": paths["asset_pattern"],
        "decision": paths["asset_decision"],
        "api": paths["asset_api_md"],
    }
    assets: list[dict[str, Any]] = []
    for asset_type, asset_path in asset_map.items():
        asset_id = f"{asset_type}:{cfg.domain}:{cfg.change_name}"
        assets.append(
            {
                "asset_id": asset_id,
                "type": asset_type,
                "domain": cfg.domain,
                "change_name": cfg.change_name,
                "title": cfg.title,
                "tags": tags,
                "path": relative_to_workspace(cfg.workspace, asset_path),
                "optional_context": asset_type != "spec",
                "source_snapshot": relative_to_workspace(cfg.workspace, paths["snapshot_root"]),
            }
        )
    if paths["asset_api_yaml"].exists() or read_text(paths["openapi"]):
        assets.append(
            {
                "asset_id": f"api-schema:{cfg.domain}:{cfg.change_name}",
                "type": "api-schema",
                "domain": cfg.domain,
                "change_name": cfg.change_name,
                "title": cfg.title,
                "tags": tags,
                "path": relative_to_workspace(cfg.workspace, paths["asset_api_yaml"]),
                "optional_context": True,
                "source_snapshot": relative_to_workspace(cfg.workspace, paths["snapshot_root"]),
            }
        )
    return {
        "change_id": paths["snapshot_root"].name,
        "change_name": cfg.change_name,
        "title": cfg.title,
        "domain": cfg.domain,
        "tags": tags,
        "assets": assets,
    }


def build_change_bundle(cfg: ArchiveConfig, asset_manifest: dict[str, Any]) -> dict[str, Any]:
    asset_ids = [item["asset_id"] for item in asset_manifest["assets"]]
    return {
        "bundle_id": cfg.change_name,
        "title": cfg.title,
        "domain": cfg.domain,
        "change_name": cfg.change_name,
        "description": f"{cfg.title} 的按需上下文包。",
        "asset_ids": asset_ids,
        "default_asset_ids": [asset_id for asset_id in asset_ids if not asset_id.startswith("spec:")],
        "tags": asset_manifest["tags"],
    }


def merge_domain_bundle(existing: dict[str, Any], cfg: ArchiveConfig, asset_manifest: dict[str, Any]) -> dict[str, Any]:
    rule_like = [
        item["asset_id"]
        for item in asset_manifest["assets"]
        if item["type"] in {"rule", "pattern", "decision", "api", "api-schema"}
    ]
    merged = dict(existing) if existing else {}
    merged.setdefault("bundle_id", f"{cfg.domain}-core")
    merged.setdefault("title", f"{cfg.domain} 核心知识包")
    merged["domain"] = cfg.domain
    merged["description"] = f"{cfg.domain} 领域的可复用规则、模式与接口知识。"
    merged["asset_ids"] = unique_keep_order(list(merged.get("asset_ids", [])) + rule_like)
    merged["default_asset_ids"] = unique_keep_order(list(merged.get("default_asset_ids", [])) + rule_like)
    merged["tags"] = unique_keep_order(list(merged.get("tags", [])) + asset_manifest["tags"])
    return merged


def build_snapshot_manifest(cfg: ArchiveConfig, paths: dict[str, Path], asset_manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "snapshot_id": paths["snapshot_root"].name,
        "change_name": cfg.change_name,
        "domain": cfg.domain,
        "title": cfg.title,
        "archived_at": datetime.now().isoformat(timespec="seconds"),
        "archived_paths": {
            "inputs": relative_to_workspace(cfg.workspace, paths["snapshot_inputs"]),
            "working": relative_to_workspace(cfg.workspace, paths["snapshot_working"]),
            "outputs": relative_to_workspace(cfg.workspace, paths["snapshot_outputs"]),
            "openspec_change": relative_to_workspace(cfg.workspace, paths["snapshot_change"]),
        },
        "asset_ids": [item["asset_id"] for item in asset_manifest["assets"]],
        "cleanup_targets": [
            "inputs/prd",
            "inputs/notes",
            "inputs/context",
            "inputs/screenshots",
            "working/*",
            "outputs/*",
        ],
        "purpose": "Archive the previous requirement context and clear active workspace artifacts to avoid contaminating the next analysis run.",
    }


def build_index(knowledge_root: Path, cfg: ArchiveConfig, catalog: dict[str, Any]) -> str:
    def section(title: str, items: list[str]) -> list[str]:
        return ["", f"## {title}", *(items or ["- 无"])]

    latest = f"- 最近归档：`{cfg.change_name}` / `{cfg.title}`"
    lines = [
        "# Knowledge Index",
        "",
        "## 说明",
        "- 本目录存放已归档的需求知识资产，供后续需求分析按需复用。",
        latest,
    ]
    change_lines = [
        f"- {item['change_id']} | domain={item['domain']} | title={item['title']} | snapshot={item['snapshot_path']}"
        for item in catalog.get("changes", [])
    ]
    asset_lines = [
        f"- {item['asset_id']} | type={item['type']} | path={item['path']}"
        for item in catalog.get("assets", [])
    ]
    bundle_lines = [
        f"- {item['bundle_id']} | domain={item['domain']} | assets={len(item.get('asset_ids', []))}"
        for item in catalog.get("bundles", [])
    ]
    lines.extend(section("Changes", change_lines))
    lines.extend(section("Assets", asset_lines))
    lines.extend(section("Bundles", bundle_lines))
    return "\n".join(lines) + "\n"


def archive_workspace_snapshot(cfg: ArchiveConfig, paths: dict[str, Path], asset_manifest: dict[str, Any]) -> None:
    copy_tree(cfg.workspace / "inputs", paths["snapshot_inputs"], dry_run=cfg.dry_run)
    copy_tree(paths["working_root"], paths["snapshot_working"], dry_run=cfg.dry_run)
    copy_tree(paths["outputs_root"], paths["snapshot_outputs"], dry_run=cfg.dry_run)
    copy_tree(paths["change_root"], paths["snapshot_change"], dry_run=cfg.dry_run)
    write_json(paths["snapshot_manifest"], build_snapshot_manifest(cfg, paths, asset_manifest), dry_run=cfg.dry_run)


def cleanup_active_workspace(cfg: ArchiveConfig, paths: dict[str, Path]) -> None:
    clear_directory(cfg.workspace / "inputs" / "prd", dry_run=cfg.dry_run)
    clear_directory(cfg.workspace / "inputs" / "notes", dry_run=cfg.dry_run)
    clear_directory(cfg.workspace / "inputs" / "context", dry_run=cfg.dry_run)
    clear_directory(cfg.workspace / "inputs" / "screenshots", dry_run=cfg.dry_run)
    clear_directory(paths["working_root"], dry_run=cfg.dry_run)
    clear_directory(paths["outputs_root"], dry_run=cfg.dry_run)


def archive(cfg: ArchiveConfig) -> None:
    paths = build_paths(cfg)
    if not paths["change_root"].exists():
        raise FileNotFoundError(f"未找到 change 目录: {paths['change_root']}")

    dsl = load_json(paths["merged_dsl"])
    validation_report = read_text(paths["validation_report"])
    api_contract_md = read_text(paths["generated_api_contracts"])

    spec_content = build_specs_archive(cfg, paths, dsl)
    rule_content = build_rules_archive(cfg, dsl)
    pattern_content = build_patterns_archive(cfg, dsl)
    decision_content = build_decisions_archive(cfg, dsl, validation_report)

    write_text(paths["asset_spec"], spec_content, dry_run=cfg.dry_run)
    write_text(paths["asset_rule"], rule_content, dry_run=cfg.dry_run)
    write_text(paths["asset_pattern"], pattern_content, dry_run=cfg.dry_run)
    write_text(paths["asset_decision"], decision_content, dry_run=cfg.dry_run)
    if api_contract_md:
        write_text(paths["asset_api_md"], api_contract_md + "\n", dry_run=cfg.dry_run)
    copy_file(paths["openapi"], paths["asset_api_yaml"], dry_run=cfg.dry_run)

    # Keep backward-compatible top-level files.
    write_text(paths["legacy_spec"], spec_content, dry_run=cfg.dry_run)
    write_text(paths["legacy_rule"], rule_content, dry_run=cfg.dry_run)
    write_text(paths["legacy_pattern"], pattern_content, dry_run=cfg.dry_run)
    write_text(paths["legacy_decision"], decision_content, dry_run=cfg.dry_run)
    if api_contract_md:
        write_text(paths["legacy_api_md"], api_contract_md + "\n", dry_run=cfg.dry_run)
    copy_file(paths["openapi"], paths["legacy_api_yaml"], dry_run=cfg.dry_run)

    asset_manifest = build_asset_manifest(cfg, paths, dsl)
    change_bundle = build_change_bundle(cfg, asset_manifest)
    existing_domain_bundle = load_json(paths["bundle_domain"])
    domain_bundle = merge_domain_bundle(existing_domain_bundle, cfg, asset_manifest)

    write_json(paths["bundle_change"], change_bundle, dry_run=cfg.dry_run)
    write_json(paths["bundle_domain"], domain_bundle, dry_run=cfg.dry_run)

    archive_workspace_snapshot(cfg, paths, asset_manifest)
    cleanup_active_workspace(cfg, paths)

    catalog = ensure_catalog(paths["knowledge_root"])
    catalog["changes"] = replace_entry(
        catalog["changes"],
        "change_id",
        paths["snapshot_root"].name,
        {
            "change_id": paths["snapshot_root"].name,
            "change_name": cfg.change_name,
            "domain": cfg.domain,
            "title": cfg.title,
            "snapshot_path": relative_to_workspace(cfg.workspace, paths["snapshot_root"]),
            "bundle_id": change_bundle["bundle_id"],
            "asset_ids": [item["asset_id"] for item in asset_manifest["assets"]],
            "tags": asset_manifest["tags"],
        },
    )
    for asset in asset_manifest["assets"]:
        catalog["assets"] = replace_entry(catalog["assets"], "asset_id", asset["asset_id"], asset)
    catalog["bundles"] = replace_entry(catalog["bundles"], "bundle_id", change_bundle["bundle_id"], change_bundle)
    catalog["bundles"] = replace_entry(catalog["bundles"], "bundle_id", domain_bundle["bundle_id"], domain_bundle)

    write_json(paths["catalog"], catalog, dry_run=cfg.dry_run)
    write_text(paths["knowledge_index"], build_index(paths["knowledge_root"], cfg, catalog), dry_run=cfg.dry_run)

    print("归档完成：")
    print(f"- spec asset  -> {paths['asset_spec']}")
    print(f"- rule asset  -> {paths['asset_rule']}")
    print(f"- pattern     -> {paths['asset_pattern']}")
    print(f"- decision    -> {paths['asset_decision']}")
    if api_contract_md:
        print(f"- api(md)     -> {paths['asset_api_md']}")
    if paths["openapi"].exists():
        print(f"- api(yaml)   -> {paths['asset_api_yaml']}")
    print(f"- bundle      -> {paths['bundle_change']}")
    print(f"- domain core -> {paths['bundle_domain']}")
    print(f"- snapshot    -> {paths['snapshot_root']}")
    print(f"- catalog     -> {paths['catalog']}")
    print("已清理活动目录：inputs/prd, inputs/notes, inputs/context, inputs/screenshots, working/, outputs/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="归档一次需求分析产物到 knowledge/，并生成可复用知识资产。")
    parser.add_argument("--workspace", default=".", help="工作区根目录，默认当前目录")
    parser.add_argument("--change-name", required=True, help="openspec/changes 下的变更目录名")
    parser.add_argument("--domain", default="account", help="领域名，默认 account")
    parser.add_argument("--title", default="", help="归档标题，默认使用 change-name")
    parser.add_argument("--dry-run", action="store_true", help="仅打印动作，不落盘")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    cfg = ArchiveConfig(
        workspace=workspace,
        change_name=args.change_name,
        domain=args.domain,
        title=args.title.strip() or args.change_name,
        dry_run=args.dry_run,
    )
    archive(cfg)


if __name__ == "__main__":
    main()
