from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CONTROL_CHARS_RE = re.compile(r"[\u0000-\u0008\u000b\u000c\u000e-\u001f]")
MULTI_BLANK_RE = re.compile(r"\n{3,}")
LEADING_BULLET_RE = re.compile(r"^\s*[-*•·]+\s*")
LEADING_INDEX_RE = re.compile(r"^\s*(?:\d+[.、)]|[(（]\d+[)）])\s*")
SECTION_HEADING_RE = re.compile(r"^#{1,6}\s*(.+?)\s*$")
TITLE_SUFFIXES = ("需求", "需求验收", "方案", "设计", "说明")
OVERRIDES_FILENAME = "extractor-overrides.json"
DEFAULT_PAGE_SUFFIXES = ["页", "页面", "弹窗", "首页", "列表", "详情", "结果页", "结果", "中心", "工作台", "面板", "设置", "表单", "步骤", "向导", "工作区"]
DEFAULT_ACTION_PREFIXES = ["点击", "提交", "确认", "保存", "返回", "切换", "选择", "上传", "下载", "搜索", "查询", "发起", "查看"]
DEFAULT_STANDALONE_ACTIONS = ["登录", "注册", "支付", "审核", "创建", "编辑", "删除", "重置", "绑定", "发送验证码"]
DEFAULT_IGNORED_STANDALONE_ACTIONS = ["登录", "注册", "支付", "审核", "创建", "编辑", "删除", "重置", "绑定"]
DEFAULT_SECTION_ALIASES = {
    "业务规则": "rules",
    "规则": "rules",
    "约束": "rules",
    "页面": "pages",
    "页面与状态": "pages",
    "页面说明": "pages",
    "流程": "flow",
    "核心流程": "flow",
    "交互流程": "flow",
    "接口": "interfaces",
    "依赖": "dependencies",
    "上下文": "context",
    "补充说明": "notes",
    "备注": "notes",
}
DEFAULT_RULE_KEYWORDS = [
    "必须", "需要", "需", "不可", "不能", "禁止", "支持", "成功", "失败", "有效期", "唯一", "限制", "至少", "最多",
    "自动", "校验", "进入", "返回", "跳转", "提示", "状态", "权限", "协议", "验证码", "密码", "登录", "注册", "支付",
    "上传", "审核", "token", "接口",
]
DEFAULT_RULE_CATEGORIES = {
    "准入与校验规则": ["必须", "需要", "需", "校验", "唯一", "有效期", "限制", "至少", "最多", "协议", "密码", "验证码"],
    "成功与失败规则": ["成功", "失败", "提示", "重试", "失效", "锁定"],
    "页面流转规则": ["进入", "返回", "跳转", "切换"],
    "数据与权限规则": ["token", "权限", "角色", "资料", "接口"],
    "交互规则": ["点击", "提交", "确认", "选择", "上传", "下载", "搜索", "发起", "查看"],
}
GENERIC_STATES = ["待处理", "处理中", "成功", "失败"]
ROLE_KEYWORDS = ["??", "??", "???", "????", "???", "???", "??", "??", "??"]


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = CONTROL_CHARS_RE.sub("", text)
    text = MULTI_BLANK_RE.sub("\n\n", text)
    return text.strip()


def clean_candidate(text: str) -> str:
    compact = text.replace("\n", " ").strip()
    compact = LEADING_BULLET_RE.sub("", compact)
    compact = LEADING_INDEX_RE.sub("", compact)
    compact = re.sub(r"\s+", " ", compact)
    return compact.strip("-•· ").strip().rstrip("；;。")


def unique_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = item.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def slugify(text: str) -> str:
    compact = clean_candidate(text).lower()
    compact = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", compact)
    compact = re.sub(r"_+", "_", compact).strip("_")
    return compact or "unknown"


def deep_copy_jsonable(data: Any) -> Any:
    return json.loads(json.dumps(data, ensure_ascii=False))


def default_extractor_overrides() -> dict[str, Any]:
    return {
        "page_suffixes": list(DEFAULT_PAGE_SUFFIXES),
        "action_prefixes": list(DEFAULT_ACTION_PREFIXES),
        "standalone_actions": list(DEFAULT_STANDALONE_ACTIONS),
        "ignored_standalone_actions": list(DEFAULT_IGNORED_STANDALONE_ACTIONS),
        "rule_keywords": list(DEFAULT_RULE_KEYWORDS),
        "rule_categories": deep_copy_jsonable(DEFAULT_RULE_CATEGORIES),
        "section_aliases": dict(DEFAULT_SECTION_ALIASES),
    }


def merge_extractor_overrides(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    merged = default_extractor_overrides()
    if not overrides:
        return merged
    for key in ["page_suffixes", "action_prefixes", "standalone_actions", "ignored_standalone_actions", "rule_keywords"]:
        values = overrides.get(key, [])
        if isinstance(values, list):
            merged[key] = unique_keep_order(merged[key] + [str(item) for item in values if str(item).strip()])
    if isinstance(overrides.get("rule_categories"), dict):
        for category, keywords in overrides["rule_categories"].items():
            if isinstance(keywords, list):
                merged["rule_categories"].setdefault(str(category), [])
                merged["rule_categories"][str(category)] = unique_keep_order(
                    merged["rule_categories"][str(category)] + [str(item) for item in keywords if str(item).strip()]
                )
    if isinstance(overrides.get("section_aliases"), dict):
        for alias, target in overrides["section_aliases"].items():
            if str(alias).strip() and str(target).strip():
                merged["section_aliases"][str(alias)] = str(target)
    return merged


def load_extractor_overrides(workspace: Path) -> dict[str, Any]:
    path = workspace / OVERRIDES_FILENAME
    if not path.exists():
        return default_extractor_overrides()
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return default_extractor_overrides()
    return merge_extractor_overrides(json.loads(raw))


def build_page_patterns(config: dict[str, Any]) -> tuple[re.Pattern[str], re.Pattern[str]]:
    suffix_pattern = "|".join(sorted((re.escape(item) for item in config["page_suffixes"]), key=len, reverse=True))
    page_name_re = re.compile(rf"(?P<name>[A-Za-z0-9\u4e00-\u9fff]{{1,30}}(?:{suffix_pattern}))")
    page_decl_re = re.compile(rf"^(?P<name>[A-Za-z0-9\u4e00-\u9fff]{{1,30}}(?:{suffix_pattern}))(?P<sep>[:：])?\s*(?P<desc>.*)$")
    return page_name_re, page_decl_re


def build_action_pattern(config: dict[str, Any]) -> re.Pattern[str]:
    prefix_terms = [rf"{re.escape(item)}[^，。；;\n]{{1,16}}" for item in config["action_prefixes"]]
    standalone_terms = [re.escape(item) for item in config["standalone_actions"]]
    return re.compile(r"(" + "|".join(prefix_terms + standalone_terms) + r")")


def read_markdown_tree(directory: Path) -> tuple[str, list[str]]:
    if not directory.exists():
        return "", []
    parts: list[str] = []
    sources: list[str] = []
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.stat().st_size > 0:
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            sources.append(str(path.relative_to(directory.parent)).replace("\\", "/"))
            parts.append(f"# Source: {path.name}\n{content}")
    return normalize_text("\n\n".join(parts)), sources


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists() or path.stat().st_size == 0:
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def load_vision_artifacts(workspace: Path) -> dict[str, Any]:
    working_dir = workspace / "working"
    ocr_payload = read_json_if_exists(working_dir / "screenshot-text-evidence.json") or read_json_if_exists(working_dir / "screenshot-ocr.json")
    classification_payload = read_json_if_exists(working_dir / "page-classification.json")
    return {
        "screenshots": ocr_payload.get("screenshots", []) if isinstance(ocr_payload.get("screenshots", []), list) else [],
        "pages": classification_payload.get("pages", []) if isinstance(classification_payload.get("pages", []), list) else [],
    }


def render_vision_text(vision_artifacts: dict[str, Any]) -> str:
    lines: list[str] = []
    pages = vision_artifacts.get("pages", [])
    if pages:
        lines.append("??")
        for page in pages:
            page_name = clean_candidate(str(page.get("page_name", "")))
            if not page_name:
                continue
            components = page.get("components", {}) if isinstance(page.get("components", {}), dict) else {}
            component_words = unique_keep_order(list(components.get("fields", [])) + list(components.get("buttons", [])) + list(components.get("tabs", [])))
            description = f"?????????{'?'.join(component_words[:6])}" if component_words else "??????"
            lines.append(f"- {page_name}?{description}?")
    for screenshot in vision_artifacts.get("screenshots", []):
        ocr_text = normalize_text(str(screenshot.get("text_evidence") or screenshot.get("ocr_text", "")))
        if ocr_text:
            lines.append(ocr_text)
    return normalize_text("\n".join(lines))


def summarize_screenshot_evidence(vision_artifacts: dict[str, Any]) -> dict[str, Any]:
    screenshots = vision_artifacts.get("screenshots", [])
    pages = vision_artifacts.get("pages", [])
    return {
        "enabled": bool(screenshots or pages),
        "screenshots": screenshots,
        "pages": pages,
        "summary": {
            "text_evidence_count": len(screenshots),
            "classified_page_count": len(pages),
        },
    }


def split_lines(text: str) -> list[str]:
    return [line for line in normalize_text(text).splitlines() if line.strip()]


def section_name(line: str, config: dict[str, Any]) -> str | None:
    cleaned = clean_candidate(line)
    heading_match = SECTION_HEADING_RE.match(line.strip())
    candidate = heading_match.group(1).strip() if heading_match else cleaned
    candidate = candidate.rstrip(":：")
    return config["section_aliases"].get(candidate)


def is_page_declaration(text: str, page_decl_re: re.Pattern[str]) -> bool:
    cleaned = clean_candidate(text)
    match = page_decl_re.match(cleaned)
    if not match:
        return False
    name = match.group("name")
    desc = match.group("desc").strip()
    if not match.group("sep") and any(keyword in name for keyword in ["成功", "失败", "进入", "返回", "跳转", "支持", "展示", "用于", "承接", "点击", "提交"]):
        return False
    return bool(
        match.group("sep")
        or (not desc and len(name) <= 8)
        or desc.startswith("支持")
        or desc.startswith("展示")
        or desc.startswith("用于")
        or desc.startswith("承接")
    )


def parse_page_declaration(text: str, page_decl_re: re.Pattern[str]) -> dict[str, str] | None:
    cleaned = clean_candidate(text)
    match = page_decl_re.match(cleaned)
    if not match or not is_page_declaration(cleaned, page_decl_re):
        return None
    return {"name": match.group("name"), "description": match.group("desc").strip()}


def is_title_line(text: str, page_decl_re: re.Pattern[str]) -> bool:
    cleaned = clean_candidate(text)
    if not cleaned or is_page_declaration(cleaned, page_decl_re):
        return False
    return len(cleaned) <= 32 and cleaned.endswith(TITLE_SUFFIXES)


def split_sections(text: str, config: dict[str, Any]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {
        "rules": [], "pages": [], "flow": [], "interfaces": [], "dependencies": [], "context": [], "notes": [], "other": []
    }
    current = "other"
    for raw_line in split_lines(text):
        if raw_line.startswith("# Source:"):
            continue
        mapped = section_name(raw_line, config)
        if mapped:
            current = mapped
            continue
        sections[current].append(raw_line)
    return sections


def build_meta(text: str, config: dict[str, Any], page_decl_re: re.Pattern[str]) -> dict[str, Any]:
    lines = [clean_candidate(line) for line in split_lines(text) if not line.startswith("# Source:")]
    title = next(
        (line for line in lines if line and not section_name(line, config) and not is_page_declaration(line, page_decl_re)),
        "通用产品需求",
    )
    summary_items = [
        line for line in lines if line and line != title and not is_page_declaration(line, page_decl_re) and not section_name(line, config)
    ][:2]
    summary = "；".join(summary_items) if summary_items else "从输入中抽取页面、流转、规则、依赖与待确认项。"
    return {
        "domain": "generic",
        "domain_label": "通用产品需求",
        "feature_name": title,
        "summary": summary,
        "requirement_name": title,
        "proposal_background": "当前需求需要从 PRD、备注、上下文和截图线索中抽取统一 DSL，再生成可评审的规格草案。",
        "inferred_facts": [
            "页面、动作、流转和规则均基于输入材料进行启发式抽取，仍需结合原始需求确认。",
            "若上下文中缺少正式接口说明，接口契约仅作为推断草案输出。",
        ],
    }


def classify_rule(rule: str, config: dict[str, Any]) -> str:
    for category, keywords in config["rule_categories"].items():
        if any(keyword in rule for keyword in keywords):
            return category
    return "通用规则"


def group_rules(rules: list[str], domain: str = "generic", overrides: dict[str, Any] | None = None) -> dict[str, list[str]]:
    del domain
    config = merge_extractor_overrides(overrides)
    grouped: dict[str, list[str]] = {}
    for rule in rules:
        grouped.setdefault(classify_rule(rule, config), []).append(rule)
    return grouped


def looks_like_rule(text: str, config: dict[str, Any], page_decl_re: re.Pattern[str]) -> bool:
    cleaned = clean_candidate(text)
    if not cleaned or is_title_line(cleaned, page_decl_re) or is_page_declaration(cleaned, page_decl_re):
        return False
    return any(keyword in cleaned for keyword in config["rule_keywords"])


def extract_rules_from_text(text: str, domain: str = "generic", overrides: dict[str, Any] | None = None) -> list[str]:
    del domain
    config = merge_extractor_overrides(overrides)
    _, page_decl_re = build_page_patterns(config)
    sections = split_sections(text, config)
    candidates: list[str] = []
    for section in ("rules", "flow", "interfaces", "dependencies", "notes", "other"):
        for line in sections[section]:
            cleaned = clean_candidate(line)
            if looks_like_rule(cleaned, config, page_decl_re):
                candidates.append(cleaned)
    return unique_keep_order(candidates)


def strip_page_suffix(page_name: str, page_suffixes: list[str]) -> str:
    for suffix in sorted(page_suffixes, key=len, reverse=True):
        if page_name.endswith(suffix) and len(page_name) > len(suffix):
            return page_name[: -len(suffix)]
    return page_name


def page_aliases(page_name: str, page_suffixes: list[str]) -> list[str]:
    aliases = [page_name]
    stripped = strip_page_suffix(page_name, page_suffixes)
    if stripped != page_name and len(stripped) >= 2:
        aliases.append(stripped)
    return unique_keep_order(sorted(aliases, key=len, reverse=True))


def find_page_candidates(text: str, config: dict[str, Any], page_name_re: re.Pattern[str], page_decl_re: re.Pattern[str]) -> list[dict[str, str]]:
    sections = split_sections(text, config)
    candidates: list[dict[str, str]] = []
    for line in sections["pages"] + sections["other"]:
        parsed = parse_page_declaration(line, page_decl_re)
        if parsed:
            candidates.append(parsed)
    if not candidates:
        for line in sections["flow"] + sections["rules"]:
            cleaned = clean_candidate(line)
            for match in page_name_re.finditer(cleaned):
                candidates.append({"name": match.group("name"), "description": ""})
    unique: dict[str, dict[str, str]] = {}
    for item in candidates:
        current = unique.get(item["name"])
        if current is None or (item["description"] and not current["description"]):
            unique[item["name"]] = item
    return list(unique.values())


def infer_page_goal(page_name: str, description: str, all_text: str, page_decl_re: re.Pattern[str]) -> str:
    if description:
        return description
    for line in split_lines(all_text):
        cleaned = clean_candidate(line)
        if page_name in cleaned and not is_page_declaration(cleaned, page_decl_re):
            candidate = cleaned.replace(page_name, "", 1).strip("：:，,。；; ")
            if candidate:
                return candidate
    return f"承接与“{page_name}”相关的核心业务操作。"


def infer_page_states(page_name: str, page_goal: str) -> list[str]:
    combined = f"{page_name} {page_goal}"
    states = set(GENERIC_STATES)
    if any(keyword in combined for keyword in ["登录", "注册", "提交", "发送", "重置", "创建", "编辑"]):
        states.update(["待填写", "提交中"])
    if any(keyword in combined for keyword in ["支付", "审核", "上传"]):
        states.update(["待确认"])
    if any(keyword in combined for keyword in ["列表", "首页", "详情", "结果", "查询", "搜索"]):
        states.update(["空态"])
    return sorted(states)


def infer_page_dependencies(page_name: str, page_goal: str, context_text: str, screenshot_names: list[str]) -> list[str]:
    combined = f"{page_name} {page_goal} {context_text}".lower()
    dependencies: list[str] = []
    dependency_map = {
        "认证服务": ["登录", "注册", "密码", "token", "auth"],
        "验证码服务": ["验证码", "send-code", "sms", "code"],
        "支付服务": ["支付", "订单", "退款"],
        "文件服务": ["上传", "附件", "图片", "文件"],
        "通知服务": ["消息", "通知", "短信", "邮件"],
        "审核服务": ["审核", "审批"],
        "资料服务": ["资料", "档案", "profile"],
        "路由服务": ["跳转", "进入", "返回", "路由", "首页"],
        "接口上下文": ["api", "openapi", "request", "response", "path", "接口"],
    }
    for dependency, keywords in dependency_map.items():
        if any(keyword.lower() in combined for keyword in keywords):
            dependencies.append(dependency)
    if screenshot_names:
        dependencies.append("截图证据")
    return unique_keep_order(dependencies or ["业务服务"])


def infer_page_unknowns(page_name: str, screenshot_names: list[str]) -> list[str]:
    if screenshot_names:
        return []
    return [f"{page_name} 的布局、字段和按钮文案仍需结合截图或原型确认。"]


def infer_primary_trigger(page_name: str, page_goal: str) -> str:
    combined = f"{page_name} {page_goal}"
    mapping = [
        ("找回密码", "提交找回密码"), ("重置密码", "提交重置密码"), ("结果", "查看结果"), ("详情", "查看详情"),
        ("列表", "查看列表"), ("首页", "进入首页"), ("登录", "提交登录"), ("注册", "提交注册"), ("重置", "提交重置"),
        ("支付", "提交支付"), ("审核", "提交审核"), ("上传", "提交上传"), ("创建", "提交创建"), ("编辑", "保存编辑"),
        ("设置", "保存设置"), ("绑定", "提交绑定"), ("搜索", "执行搜索"), ("查询", "执行查询"),
    ]
    for keyword, trigger in mapping:
        if keyword in combined:
            return trigger
    base = strip_page_suffix(page_name, DEFAULT_PAGE_SUFFIXES)
    return f"提交{base}" if len(base) <= 8 else f"执行{base}"


def infer_secondary_triggers(page_goal: str, config: dict[str, Any], action_phrase_re: re.Pattern[str]) -> list[str]:
    triggers = [clean_candidate(match.group(1)) for match in action_phrase_re.finditer(page_goal)]
    ignored = set(config["ignored_standalone_actions"])
    return unique_keep_order([trigger for trigger in triggers if trigger and trigger not in ignored])


def infer_actions(page_id: str, page_name: str, page_goal: str, rules: list[str], config: dict[str, Any], action_phrase_re: re.Pattern[str]) -> list[dict[str, Any]]:
    aliases = page_aliases(page_name, config["page_suffixes"])
    relevant_rules = [rule for rule in rules if any(alias in rule for alias in aliases)]
    primary_trigger = infer_primary_trigger(page_name, page_goal)
    triggers = [primary_trigger]
    triggers.extend(infer_secondary_triggers(page_goal, config, action_phrase_re))
    if any("??" in rule for rule in relevant_rules):
        triggers.append("??????")
    actions: list[dict[str, Any]] = []
    for index, trigger in enumerate(unique_keep_order(triggers)[:3], start=1):
        action_slug = slugify(trigger)
        confidence, evidence = infer_action_confidence(trigger, page_goal, relevant_rules, is_primary=(trigger == primary_trigger))
        actions.append(
            {
                "id": f"A_{slugify(page_id)}_{index}_{action_slug}".upper(),
                "trigger": trigger,
                "actor": "??" if "??" not in trigger and "??" not in trigger else "??",
                "preconditions": [f"???{page_name}", "\u6ee1\u8db3\u539f\u59cb\u63cf\u8ff0\u4e2d\u7684\u89e6\u53d1\u6761\u4ef6"],
                "steps": [
                    f"?{page_name}????{trigger}?????????",
                    f"???{trigger}??????????",
                    "???????????????",
                ],
                "success_results": [f"{trigger}??????????????"],
                "failure_results": [f"{trigger}???????"],
                "confidence": confidence,
                "evidence": evidence,
            }
        )
    return actions



def infer_entry_exit_points(page_name: str, all_text: str, page_decl_re: re.Pattern[str], page_suffixes: list[str]) -> tuple[list[str], list[str]]:
    entry_points: list[str] = []
    exit_points: list[str] = []
    aliases = page_aliases(page_name, page_suffixes)
    for raw_line in split_lines(all_text):
        cleaned = clean_candidate(raw_line)
        if is_page_declaration(cleaned, page_decl_re) and page_name in cleaned:
            entry_points.append(f"用户进入{page_name}")
            continue
        if not any(alias in cleaned for alias in aliases):
            continue
        if any(keyword in cleaned for keyword in ["进入", "访问", "打开", "展示"]):
            entry_points.append(cleaned)
        if any(keyword in cleaned for keyword in ["返回", "跳转", "切换", "完成", "进入"]):
            exit_points.append(cleaned)
    if not entry_points:
        entry_points = [f"用户进入{page_name}"]
    if not exit_points:
        exit_points = [f"完成{page_name}主流程后离开"]
    return unique_keep_order(entry_points), unique_keep_order(exit_points)


def infer_transition_target(line: str, pages: list[dict[str, Any]], page_suffixes: list[str]) -> dict[str, Any] | None:
    for page in pages:
        for alias in page_aliases(page["name"], page_suffixes):
            if re.search(rf"(?:进入|跳转(?:到|至)?|返回|打开){re.escape(alias)}", line):
                return page
    return None


def unique_keep_order_dicts(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for item in items:
        key = item.get("id", "")
        if key and key not in seen:
            seen.add(key)
            result.append(item)
    return result


def infer_transition_sources(line: str, pages: list[dict[str, Any]], target_id: str | None, page_suffixes: list[str]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for page in pages:
        if page["id"] == target_id:
            continue
        aliases = page_aliases(page["name"], page_suffixes)
        if any(alias in line for alias in aliases):
            sources.append(page)
            continue
        primary_trigger = infer_primary_trigger(page["name"], page["goal"])
        simplified_trigger = primary_trigger.replace("提交", "").replace("执行", "").replace("查看", "")
        if simplified_trigger and simplified_trigger in line:
            sources.append(page)
    return unique_keep_order_dicts(sources)



def collect_supporting_lines(all_text: str, keywords: list[str], limit: int = 3) -> list[str]:
    supports: list[str] = []
    for raw_line in split_lines(all_text):
        cleaned = clean_candidate(raw_line)
        if cleaned and any(keyword in cleaned for keyword in keywords):
            supports.append(cleaned)
    return unique_keep_order(supports)[:limit]


def score_confidence(base: float, increments: list[float]) -> float:
    score = base + sum(increments)
    return max(0.35, min(0.99, round(score, 2)))


def infer_page_confidence(page_name: str, description: str, all_text: str, context_text: str, screenshot_names: list[str]) -> tuple[float, list[str]]:
    evidence: list[str] = []
    increments: list[float] = []
    if description:
        evidence.append("page-declaration")
        increments.append(0.22)
    if page_name in all_text:
        evidence.append("text-reference")
        increments.append(0.10)
    if context_text and page_name in context_text:
        evidence.append("context-reference")
        increments.append(0.08)
    if screenshot_names:
        evidence.append("screenshot-reference")
        increments.append(0.05)
    return score_confidence(0.55, increments), unique_keep_order(evidence)


def infer_action_confidence(trigger: str, page_goal: str, relevant_rules: list[str], is_primary: bool) -> tuple[float, list[str]]:
    evidence = ["page-goal"] if trigger and trigger in page_goal else []
    increments = [0.18 if is_primary else 0.10]
    if any(trigger in rule for rule in relevant_rules):
        evidence.append("rule-reference")
        increments.append(0.08)
    if not evidence:
        evidence.append("heuristic-inference")
    return score_confidence(0.56, increments), unique_keep_order(evidence)


def infer_transition_confidence(trigger: str, condition: str, result: str, explicit: bool = True) -> tuple[float, list[str]]:
    evidence = ["explicit-transition-rule" if explicit else "fallback-sequence"]
    increments = [0.20 if explicit else 0.0]
    if condition and condition != "\u4e3b\u6d41\u7a0b\u6210\u529f\u63a8\u8fdb":
        evidence.append("condition-detail")
        increments.append(0.05)
    if result:
        evidence.append("result-detail")
        increments.append(0.04)
    return score_confidence(0.56, increments), evidence


def extract_roles(text: str) -> list[str]:
    return unique_keep_order([keyword for keyword in ROLE_KEYWORDS if keyword in text])


def extract_interface_names(context_text: str) -> list[str]:
    return unique_keep_order(re.findall(r"[a-z]+(?:-[a-z0-9]+)+", context_text.lower()))



def infer_transition_confidence(trigger: str, condition: str, result: str, explicit: bool = True) -> tuple[float, list[str]]:
    evidence = ["explicit-transition-rule" if explicit else "fallback-sequence"]
    increments = [0.20 if explicit else 0.0]
    if condition and condition != "\u4e3b\u6d41\u7a0b\u6210\u529f\u63a8\u8fdb":
        evidence.append("condition-detail")
        increments.append(0.05)
    if result:
        evidence.append("result-detail")
        increments.append(0.04)
    return score_confidence(0.56, increments), evidence


def build_knowledge_graph(
    pages: list[dict[str, Any]],
    transitions: list[dict[str, Any]],
    rules: list[str],
    dependencies: list[str],
    interfaces: list[str],
    roles: list[str],
) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    for role in roles:
        role_id = f"ROLE_{slugify(role)}".upper()
        nodes.append({"id": role_id, "type": "role", "label": role, "confidence": 0.82, "evidence": ["role-reference"]})

    for interface in interfaces:
        interface_id = f"API_{slugify(interface)}".upper()
        nodes.append({"id": interface_id, "type": "interface", "label": interface, "confidence": 0.85, "evidence": ["context-api-reference"]})

    for page in pages:
        nodes.append(
            {
                "id": page["id"],
                "type": "page",
                "label": page["name"],
                "confidence": page.get("confidence", 0.5),
                "evidence": page.get("evidence", []),
            }
        )
        for state in page.get("states", []):
            state_id = f"STATE_{slugify(page['id'])}_{slugify(state)}".upper()
            nodes.append({"id": state_id, "type": "state", "label": state, "confidence": 0.8, "evidence": ["state-inference"]})
            edges.append({"from": page["id"], "to": state_id, "type": "has_state", "label": state, "confidence": 0.8})
        for action in page.get("actions", []):
            nodes.append(
                {
                    "id": action["id"],
                    "type": "action",
                    "label": action["trigger"],
                    "confidence": action.get("confidence", 0.5),
                    "evidence": action.get("evidence", []),
                }
            )
            edges.append(
                {
                    "from": page["id"],
                    "to": action["id"],
                    "type": "has_action",
                    "label": action["trigger"],
                    "confidence": action.get("confidence", 0.5),
                }
            )
            actor = action.get("actor")
            if actor:
                role_id = f"ROLE_{slugify(actor)}".upper()
                nodes.append({"id": role_id, "type": "role", "label": actor, "confidence": 0.82, "evidence": ["action-actor"]})
                edges.append({"from": action["id"], "to": role_id, "type": "performed_by", "label": actor, "confidence": 0.82})
        for dependency in page.get("dependencies", []):
            dep_id = f"D_{slugify(dependency)}".upper()
            nodes.append({"id": dep_id, "type": "dependency", "label": dependency, "confidence": 0.9, "evidence": ["dependency-map"]})
            edges.append({"from": page["id"], "to": dep_id, "type": "depends_on", "label": dependency, "confidence": 0.9})
            if dependency == "?????":
                for interface in interfaces:
                    interface_id = f"API_{slugify(interface)}".upper()
                    edges.append({"from": page["id"], "to": interface_id, "type": "uses_interface", "label": interface, "confidence": 0.78})

    for index, rule in enumerate(rules, start=1):
        rule_id = f"R_{index:03d}"
        nodes.append({"id": rule_id, "type": "rule", "label": rule, "confidence": 0.78, "evidence": ["rule-extraction"]})
        for page in pages:
            aliases = page_aliases(page["name"], DEFAULT_PAGE_SUFFIXES)
            if any(alias in rule for alias in aliases):
                edges.append({"from": page["id"], "to": rule_id, "type": "governed_by", "label": rule, "confidence": 0.76})

    for transition in transitions:
        edges.append(
            {
                "from": transition["from_page"],
                "to": transition["to_page"],
                "type": "transition",
                "label": transition["trigger"],
                "confidence": transition.get("confidence", 0.5),
            }
        )

    dedup_nodes: dict[str, dict[str, Any]] = {}
    for node in nodes:
        dedup_nodes.setdefault(node["id"], node)
    dedup_edges: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str, str, str]] = set()
    for edge in edges:
        key = (edge["from"], edge["to"], edge["type"], edge["label"])
        if key not in seen_edges:
            seen_edges.add(key)
            dedup_edges.append(edge)
    return {"nodes": list(dedup_nodes.values()), "edges": dedup_edges}



def build_confidence_summary(pages: list[dict[str, Any]], transitions: list[dict[str, Any]]) -> dict[str, Any]:
    scores: list[float] = []
    for page in pages:
        scores.append(float(page.get("confidence", 0.0)))
        for action in page.get("actions", []):
            scores.append(float(action.get("confidence", 0.0)))
    for transition in transitions:
        scores.append(float(transition.get("confidence", 0.0)))
    high = len([score for score in scores if score >= 0.8])
    medium = len([score for score in scores if 0.6 <= score < 0.8])
    low = len([score for score in scores if score < 0.6])
    average = round(sum(scores) / len(scores), 2) if scores else 0.0
    return {
        "average": average,
        "high": high,
        "medium": medium,
        "low": low,
        "total": len(scores),
        "note": "Confidence is heuristic and should be read together with evidence references.",
    }


def build_evidence_map(dsl: dict[str, Any]) -> str:
    lines = ["# Evidence Map", "", "## Confidence Summary"]
    summary = dsl.get("confidence_summary", {})
    lines.extend(
        [
            f"- Average Confidence: `{summary.get('average', 0.0)}`",
            f"- High Confidence Items: `{summary.get('high', 0)}`",
            f"- Medium Confidence Items: `{summary.get('medium', 0)}`",
            f"- Low Confidence Items: `{summary.get('low', 0)}`",
            "",
            "## Pages",
        ]
    )
    low_confidence_items: list[str] = []
    for page in dsl.get("pages", []):
        page_confidence = page.get("confidence", 0.0)
        lines.append(
            f"- {page['id']} / {page['name']} | Confidence: `{page_confidence}` | Evidence: {', '.join(page.get('evidence', [])) or 'none'}"
        )
        if page_confidence < 0.65:
            low_confidence_items.append(f"?? `{page['name']}` ????????????????")
        for support in page.get("supporting_lines", []):
            lines.append(f"  - Support: {support}")
        for action in page.get("actions", []):
            action_confidence = action.get("confidence", 0.0)
            lines.append(
                f"  - Action: {action['id']} / {action['trigger']} | Confidence: `{action_confidence}` | Evidence: {', '.join(action.get('evidence', [])) or 'none'}"
            )
            if action_confidence < 0.65:
                low_confidence_items.append(f"?? `{action['trigger']}` ?????????????????")
    lines.extend(["", "## Transitions"])
    for transition in dsl.get("transitions", []):
        transition_confidence = transition.get("confidence", 0.0)
        lines.append(
            f"- {transition['from_page']} -> {transition['to_page']} | Confidence: `{transition_confidence}` | Trigger: {transition['trigger']}"
        )
        if transition_confidence < 0.65:
            low_confidence_items.append(f"?? `{transition['from_page']} -> {transition['to_page']}` ??????????????")
    lines.extend(["", "## Low Confidence Checklist"])
    lines.extend([f"- {item}" for item in unique_keep_order(low_confidence_items)] or ["- None"])
    lines.extend(["", "## Knowledge Graph"])
    graph = dsl.get("knowledge_graph", {})
    lines.append(f"- Nodes: `{len(graph.get('nodes', []))}`")
    lines.append(f"- Edges: `{len(graph.get('edges', []))}`")
    return "\n".join(lines) + "\n"

def build_pages(
    all_text: str,
    prd_sources: list[str],
    screenshot_names: list[str],
    rules: list[str],
    context_text: str,
    config: dict[str, Any],
    page_name_re: re.Pattern[str],
    page_decl_re: re.Pattern[str],
    action_phrase_re: re.Pattern[str],
    vision_artifacts: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    page_candidates = find_page_candidates(all_text, config, page_name_re, page_decl_re)
    if not page_candidates and vision_artifacts:
        page_candidates = [
            {"name": clean_candidate(str(item.get("page_name", ""))), "description": ""}
            for item in vision_artifacts.get("pages", [])
            if clean_candidate(str(item.get("page_name", "")))
        ]
    if not page_candidates:
        page_candidates = [{"name": "?????", "description": ""}]
    source = prd_sources + [f"inputs/screenshots/{name}" for name in screenshot_names]
    vision_lookup = {
        clean_candidate(str(item.get("page_name", ""))): item
        for item in (vision_artifacts or {}).get("pages", [])
        if clean_candidate(str(item.get("page_name", "")))
    }
    pages: list[dict[str, Any]] = []
    for candidate in page_candidates:
        page_name = candidate["name"]
        page_id = f"P_{slugify(page_name)}".upper()
        page_goal = infer_page_goal(page_name, candidate["description"], all_text, page_decl_re)
        entry_points, exit_points = infer_entry_exit_points(page_name, all_text, page_decl_re, config["page_suffixes"])
        confidence, evidence = infer_page_confidence(page_name, candidate["description"], all_text, context_text, screenshot_names)
        page = {
            "id": page_id,
            "name": page_name,
            "source": list(source or prd_sources or ["inputs/prd/*.md"]),
            "goal": page_goal,
            "entry_points": entry_points,
            "exit_points": exit_points,
            "actions": infer_actions(page_id, page_name, page_goal, rules, config, action_phrase_re),
            "states": infer_page_states(page_name, page_goal),
            "dependencies": infer_page_dependencies(page_name, page_goal, context_text, screenshot_names),
            "unknowns": infer_page_unknowns(page_name, screenshot_names),
            "confidence": confidence,
            "evidence": evidence,
            "supporting_lines": collect_supporting_lines(all_text, page_aliases(page_name, config["page_suffixes"])),
            "components": {"fields": [], "buttons": [], "tabs": [], "labels": []},
        }
        vision_page = vision_lookup.get(page_name)
        if vision_page:
            components = vision_page.get("components", {}) if isinstance(vision_page.get("components", {}), dict) else {}
            page["components"] = {
                "fields": unique_keep_order(list(components.get("fields", []))),
                "buttons": unique_keep_order(list(components.get("buttons", []))),
                "tabs": unique_keep_order(list(components.get("tabs", []))),
                "labels": unique_keep_order(list(components.get("labels", []))),
            }
            page["source"] = unique_keep_order(page["source"] + [f"inputs/screenshots/{vision_page.get('screenshot', '')}"])
            page["dependencies"] = unique_keep_order(page["dependencies"] + ["截图视觉核对"])
            page["unknowns"] = [f"{page_name} ?????????????????????????"]
            page["confidence"] = max(float(page["confidence"]), float(vision_page.get("confidence", 0.0) or 0.0))
            page["evidence"] = unique_keep_order(page["evidence"] + ["vision-page-classification"])
            page["supporting_lines"] = unique_keep_order(
                page["supporting_lines"]
                + page["components"]["fields"]
                + page["components"]["buttons"]
                + page["components"]["labels"]
            )
            extra_buttons = [item for item in page["components"]["buttons"] if item and item not in {action["trigger"] for action in page["actions"]}]
            for button in extra_buttons[:2]:
                action_slug = slugify(button)
                page["actions"].append(
                    {
                        "id": f"A_{slugify(page_id)}_V_{action_slug}".upper(),
                        "trigger": button,
                        "actor": "??",
                        "preconditions": [f"?????{page_name}", "???????????"],
                        "steps": [f"???{page_name}???{button}?", "????????", "?????????"],
                        "success_results": [f"{button} ???????????"],
                        "failure_results": [f"{button} ???????????"],
                        "confidence": max(0.72, float(vision_page.get("confidence", 0.0) or 0.0)),
                        "evidence": ["vision-component"],
                    }
                )
        pages.append(page)
    return pages


def build_transitions(pages: list[dict[str, Any]], all_text: str, config: dict[str, Any], page_decl_re: re.Pattern[str]) -> list[dict[str, Any]]:
    transitions: list[dict[str, Any]] = []
    for raw_line in split_lines(all_text):
        cleaned = clean_candidate(raw_line)
        if not cleaned or is_page_declaration(cleaned, page_decl_re) or section_name(cleaned, config):
            continue
        if not any(keyword in cleaned for keyword in ["\u8fdb\u5165", "\u8fd4\u56de", "\u8df3\u8f6c", "\u5207\u6362"]):
            continue
        target_page = infer_transition_target(cleaned, pages, config["page_suffixes"])
        source_pages = infer_transition_sources(cleaned, pages, target_page["id"] if target_page else None, config["page_suffixes"])
        if target_page and source_pages:
            for source_page in source_pages:
                confidence, evidence = infer_transition_confidence(cleaned, "\u6ee1\u8db3\u539f\u59cb\u63cf\u8ff0\u4e2d\u7684\u89e6\u53d1\u6761\u4ef6", f"\u8fdb\u5165{target_page['name']}", explicit=True)
                transitions.append(
                    {
                        "from_page": source_page["id"],
                        "trigger": cleaned,
                        "to_page": target_page["id"],
                        "condition": "\u6ee1\u8db3\u539f\u59cb\u63cf\u8ff0\u4e2d\u7684\u89e6\u53d1\u6761\u4ef6",
                        "result": f"\u8fdb\u5165{target_page['name']}",
                        "confidence": confidence,
                        "evidence": evidence,
                    }
                )
    if not transitions and len(pages) > 1:
        for current_page, next_page in zip(pages, pages[1:]):
            confidence, evidence = infer_transition_confidence(
                f"\u5b8c\u6210{current_page['name']}\u4e3b\u6d41\u7a0b",
                "\u4e3b\u6d41\u7a0b\u6210\u529f\u63a8\u8fdb",
                f"\u8fdb\u5165{next_page['name']}",
                explicit=False,
            )
            transitions.append(
                {
                    "from_page": current_page["id"],
                    "trigger": f"\u5b8c\u6210{current_page['name']}\u4e3b\u6d41\u7a0b",
                    "to_page": next_page["id"],
                    "condition": "\u4e3b\u6d41\u7a0b\u6210\u529f\u63a8\u8fdb",
                    "result": f"\u8fdb\u5165{next_page['name']}",
                    "confidence": confidence,
                    "evidence": evidence,
                }
            )
    return unique_transition_list(transitions)


def unique_transition_list(transitions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str]] = set()
    result: list[dict[str, Any]] = []
    for item in transitions:
        key = (item["from_page"], item["to_page"], item["trigger"])
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def detect_dependencies(pages: list[dict[str, Any]], context_text: str, screenshot_names: list[str], vision_artifacts: dict[str, Any] | None = None) -> list[str]:
    dependencies = [dependency for page in pages for dependency in page.get("dependencies", [])]
    if context_text:
        dependencies.append("接口上下文")
    if screenshot_names:
        dependencies.append("截图证据")
    if vision_artifacts and (vision_artifacts.get("pages") or vision_artifacts.get("screenshots")):
        dependencies.append("截图视觉核对")
    return unique_keep_order(dependencies)


def build_unknowns(pages: list[dict[str, Any]], screenshot_names: list[str], context_text: str, vision_artifacts: dict[str, Any] | None = None) -> list[str]:
    unknowns = [item for page in pages for item in page.get("unknowns", [])]
    if screenshot_names and not (vision_artifacts and (vision_artifacts.get("pages") or vision_artifacts.get("screenshots"))):
        unknowns.append("截图已提供，但尚未完成多模态视觉证据与组件核对，页面细节可信度有限。")
    if not any(keyword in context_text.lower() for keyword in ["api", "openapi", "path", "request", "response", "接口"]):
        unknowns.append("接口 path、请求字段和响应字段仍缺少正式 context 说明。")
    return unique_keep_order(unknowns)


def build_initial_dsl(
    prd_text: str,
    note_text: str,
    screenshot_names: list[str],
    prd_sources: list[str] | None = None,
    context_text: str = "",
    overrides: dict[str, Any] | None = None,
    vision_artifacts: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], str, str, str]:
    config = merge_extractor_overrides(overrides)
    page_name_re, page_decl_re = build_page_patterns(config)
    action_phrase_re = build_action_pattern(config)
    vision_artifacts = vision_artifacts or {"screenshots": [], "pages": []}
    vision_text = render_vision_text(vision_artifacts)
    combined_text = normalize_text("\n\n".join(part for part in [prd_text, note_text, context_text, vision_text] if part.strip()))
    meta = build_meta(combined_text, config, page_decl_re)
    rules = extract_rules_from_text(combined_text, overrides=config)
    pages = build_pages(
        combined_text,
        prd_sources or ["inputs/prd/*.md"],
        screenshot_names,
        rules,
        context_text,
        config,
        page_name_re,
        page_decl_re,
        action_phrase_re,
        vision_artifacts=vision_artifacts,
    )
    transitions = build_transitions(pages, combined_text, config, page_decl_re)
    dependencies = detect_dependencies(pages, context_text, screenshot_names, vision_artifacts)
    unknowns = build_unknowns(pages, screenshot_names, context_text, vision_artifacts)
    interfaces = extract_interface_names(context_text)
    roles = extract_roles("\n".join([combined_text, context_text]))
    knowledge_graph = build_knowledge_graph(pages, transitions, rules, dependencies, interfaces, roles)
    confidence_summary = build_confidence_summary(pages, transitions)
    dsl: dict[str, Any] = {
        "meta": meta,
        "pages": pages,
        "transitions": transitions,
        "rules": rules,
        "dependencies": dependencies,
        "unknowns": unknowns,
        "knowledge_graph": knowledge_graph,
        "confidence_summary": confidence_summary,
        "screenshot_evidence": summarize_screenshot_evidence(vision_artifacts),
        "extractor_overrides": {
            "page_suffixes": config["page_suffixes"],
            "action_prefixes": config["action_prefixes"],
            "rule_keywords": config["rule_keywords"],
        },
    }

    page_source_lines = ["# Page Source Map", "", "## Pages"]
    for page in pages:
        page_source_lines.append(f"- {page['id']} / {page['name']}")
        for source in page["source"]:
            page_source_lines.append(f"  - {source}")

    transition_lines = ["# Transition Map", "", "## Transitions"]
    transition_lines.extend(
        [
            f"- {item['from_page']} --[{item['trigger']} | {item['condition']}]--> {item['to_page']} => {item['result']}"
            for item in transitions
        ]
        or ["- None"]
    )

    grouped_rules = group_rules(rules, overrides=config)
    shared_rule_lines = ["# Shared Rules", "", "## Domain", "- generic"]
    for category, items in grouped_rules.items():
        shared_rule_lines.extend(["", f"## {category}", *[f"- {item}" for item in items]])
    if not grouped_rules:
        shared_rule_lines.extend(["", "## Rules", "- None"])

    return dsl, "\n".join(page_source_lines) + "\n", "\n".join(transition_lines) + "\n", "\n".join(shared_rule_lines) + "\n"

def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_initial_outputs(workspace: Path) -> None:
    prd_text, prd_sources = read_markdown_tree(workspace / "inputs" / "prd")
    note_text, _ = read_markdown_tree(workspace / "inputs" / "notes")
    context_text, _ = read_markdown_tree(workspace / "inputs" / "context")
    screenshot_names = sorted(
        [path.name for path in (workspace / "inputs" / "screenshots").glob("*") if path.is_file() and path.stat().st_size > 0 and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".bmp"}]
    )
    overrides = load_extractor_overrides(workspace)
    vision_artifacts = load_vision_artifacts(workspace)
    dsl, page_map, transition_map, shared_rules = build_initial_dsl(
        prd_text=prd_text,
        note_text=note_text,
        screenshot_names=screenshot_names,
        prd_sources=prd_sources,
        context_text=context_text,
        overrides=overrides,
        vision_artifacts=vision_artifacts,
    )
    evidence_map = build_evidence_map(dsl)
    working_dir = workspace / "working"
    working_dir.mkdir(parents=True, exist_ok=True)
    (working_dir / "page-source-map.md").write_text(page_map, encoding="utf-8")
    (working_dir / "transition-map.md").write_text(transition_map, encoding="utf-8")
    (working_dir / "shared-rules.md").write_text(shared_rules, encoding="utf-8")
    (working_dir / "evidence-map.md").write_text(evidence_map, encoding="utf-8")
    write_json(working_dir / "raw-dsl.json", dsl)
    write_json(working_dir / "merged-dsl.json", dsl)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate initial DSL artifacts from local inputs.")
    parser.add_argument("--workspace", default=".", help="Workspace root. Default: current directory.")
    args = parser.parse_args()
    write_initial_outputs(Path(args.workspace).resolve())
    print("Initial DSL artifacts generated.")


if __name__ == "__main__":
    main()
