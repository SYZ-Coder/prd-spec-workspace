from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


DSL_PATH = Path("working/merged-dsl.json")
REPORT_PATH = Path("working/validation-report.md")

REQUIRED_TOP_LEVEL = ["pages", "transitions", "rules", "dependencies", "unknowns"]
REQUIRED_PAGE_FIELDS = [
    "id",
    "name",
    "source",
    "goal",
    "entry_points",
    "exit_points",
    "actions",
    "states",
    "dependencies",
    "unknowns",
]
REQUIRED_ACTION_FIELDS = [
    "id",
    "trigger",
    "actor",
    "preconditions",
    "steps",
    "success_results",
    "failure_results",
]
REQUIRED_TRANSITION_FIELDS = ["from_page", "trigger", "to_page", "condition", "result"]
UNKNOWN_LIMIT = 15
PAGE_DECL_RULE_RE = re.compile(r"^[A-Za-z0-9\u4e00-\u9fff]{1,30}(?:页|页面|弹窗|首页|列表|详情|结果页|结果|中心|工作台|面板|设置|表单|步骤|向导|工作区)[:：]")
TITLE_RULE_RE = re.compile(r"^[^，。；;]{2,32}(?:需求|需求验收|方案|设计|说明)$")
GENERIC_TRIGGER_RE = re.compile(r"^(?:执行.+主操作|提交页面主操作|执行主操作)$")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist")
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        raise ValueError(f"{path} is empty")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("DSL root must be a JSON object")
    return data


def missing_fields(obj: dict[str, Any], required: list[str]) -> list[str]:
    return [field for field in required if field not in obj]


def duplicated(values: list[str]) -> list[str]:
    return [key for key, count in Counter(values).items() if key and count > 1]


def write_report(blocking: list[str], high_risk: list[str], suggestions: list[str]) -> None:
    lines = ["# Validation Report", "", "## Blocking Issues"]
    lines.extend([f"- {item}" for item in blocking] or ["- None"])
    lines.extend(["", "## High Risk Issues"])
    lines.extend([f"- {item}" for item in high_risk] or ["- None"])
    lines.extend(["", "## Suggestions"])
    lines.extend([f"- {item}" for item in suggestions] or ["- None"])
    lines.extend(["", "## Generation Verdict"])
    lines.append("- Blocked" if blocking else "- Ready")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def fail_early(message: str, suggestion_lines: list[str]) -> None:
    write_report([message], [], suggestion_lines)
    print("validation-report.md generated")
    print("Validation result: blocked")
    raise SystemExit(1)


def validate_dsl_data(data: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    blocking: list[str] = []
    high_risk: list[str] = []
    suggestions: list[str] = []

    missing_top = missing_fields(data, REQUIRED_TOP_LEVEL)
    if missing_top:
        blocking.append(f"Missing top-level fields: {', '.join(missing_top)}")

    pages = data.get("pages", [])
    transitions = data.get("transitions", [])
    rules = data.get("rules", [])
    top_dependencies = data.get("dependencies", [])
    top_unknowns = data.get("unknowns", [])

    if not isinstance(pages, list):
        blocking.append("pages must be an array")
        pages = []
    if not isinstance(transitions, list):
        blocking.append("transitions must be an array")
        transitions = []
    if not isinstance(rules, list):
        blocking.append("rules must be an array")
        rules = []
    if not isinstance(top_dependencies, list):
        blocking.append("dependencies must be an array")
        top_dependencies = []
    if not isinstance(top_unknowns, list):
        blocking.append("unknowns must be an array")
        top_unknowns = []

    page_ids: list[str] = []
    page_names: list[str] = []
    action_ids: list[str] = []
    action_triggers: list[str] = []
    state_lookup: dict[str, set[str]] = {}
    page_dependencies: defaultdict[str, list[str]] = defaultdict(list)

    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            blocking.append(f"page[{index}] must be an object")
            continue

        missing_page = missing_fields(page, REQUIRED_PAGE_FIELDS)
        if missing_page:
            blocking.append(f"Page {page.get('id', f'page[{index}]')} is missing fields: {', '.join(missing_page)}")

        page_id = page.get("id", "")
        page_name = page.get("name", "")
        page_ids.append(page_id)
        page_names.append(page_name)
        state_lookup[page_id] = set(page.get("states", [])) if isinstance(page.get("states", []), list) else set()

        if not page.get("entry_points"):
            blocking.append(f"Page missing entry points: {page_id or f'page[{index}]'} / {page_name or 'UNKNOWN'}")
        if not page.get("exit_points"):
            blocking.append(f"Page missing exit points: {page_id or f'page[{index}]'} / {page_name or 'UNKNOWN'}")
        if not page.get("states"):
            high_risk.append(f"Page missing state definitions: {page_id or f'page[{index}]'} / {page_name or 'UNKNOWN'}")

        for dependency in page.get("dependencies", []):
            page_dependencies[page_id].append(dependency)

        actions = page.get("actions", [])
        if not isinstance(actions, list):
            blocking.append(f"Page actions must be an array: {page_id or f'page[{index}]'}")
            continue

        for action_index, action in enumerate(actions, start=1):
            if not isinstance(action, dict):
                blocking.append(f"Page {page_id or f'page[{index}]'} action[{action_index}] must be an object")
                continue
            missing_action = missing_fields(action, REQUIRED_ACTION_FIELDS)
            if missing_action:
                blocking.append(
                    f"Action {action.get('id', f'action[{action_index}]')} is missing fields: {', '.join(missing_action)}"
                )
            action_ids.append(action.get("id", ""))
            trigger = action.get("trigger", "")
            if trigger:
                action_triggers.append(trigger)
            if not action.get("failure_results"):
                blocking.append(
                    f"Action missing failure path: {page_id or f'page[{index}]'} -> {action.get('id', f'action[{action_index}]')}"
                )
            if not action.get("steps"):
                high_risk.append(
                    f"Action missing step definitions: {page_id or f'page[{index}]'} -> {action.get('id', f'action[{action_index}]')}"
                )

    for duplicate_page_id in duplicated(page_ids):
        blocking.append(f"Duplicate page id: {duplicate_page_id}")
    for duplicate_page_name in duplicated(page_names):
        high_risk.append(f"Duplicate page name detected; confirm whether this is the same page in different states: {duplicate_page_name}")
    for duplicate_action_id in duplicated(action_ids):
        blocking.append(f"Duplicate action id: {duplicate_action_id}")

    known_page_ids = {page_id for page_id in page_ids if page_id}
    incoming_count = Counter()
    outgoing_count = Counter()
    rule_counter = Counter(rule.strip() for rule in rules if isinstance(rule, str) and rule.strip())

    for index, transition in enumerate(transitions, start=1):
        if not isinstance(transition, dict):
            blocking.append(f"transition[{index}] must be an object")
            continue
        missing_transition = missing_fields(transition, REQUIRED_TRANSITION_FIELDS)
        if missing_transition:
            blocking.append(f"Transition[{index}] is missing fields: {', '.join(missing_transition)}")
        from_page = transition.get("from_page", "")
        to_page = transition.get("to_page", "")
        if from_page not in known_page_ids:
            blocking.append(f"Transition from_page does not exist: {from_page or f'transition[{index}]'}")
        if to_page not in known_page_ids:
            blocking.append(f"Transition to_page does not exist: {to_page or f'transition[{index}]'}")
        if from_page:
            outgoing_count[from_page] += 1
        if to_page:
            incoming_count[to_page] += 1
        if not transition.get("trigger"):
            blocking.append(f"Transition missing trigger: {from_page} -> {to_page}")
        if transition.get("condition") in {"", None}:
            high_risk.append(f"Transition missing condition detail: {from_page} -> {to_page}")
        if transition.get("result") in {"", None}:
            high_risk.append(f"Transition missing result detail: {from_page} -> {to_page}")

    for page_id in known_page_ids:
        if incoming_count[page_id] == 0:
            page = next((item for item in pages if isinstance(item, dict) and item.get("id") == page_id), None)
            if page and not page.get("entry_points"):
                blocking.append(f"Isolated page: {page_id}")
        if outgoing_count[page_id] == 0:
            page = next((item for item in pages if isinstance(item, dict) and item.get("id") == page_id), None)
            if page and not page.get("exit_points"):
                blocking.append(f"Page has no exit path: {page_id}")

    declared_dependencies = {item for item in top_dependencies if isinstance(item, str) and item.strip()}
    for page_id, dependencies in page_dependencies.items():
        for dependency in dependencies:
            if dependency not in declared_dependencies:
                blocking.append(f"Page dependency not declared at top level: {page_id} -> {dependency}")

    if not rules:
        high_risk.append("Top-level rules is empty; business constraints may be incomplete.")
    for rule, count in rule_counter.items():
        if count > 1:
            suggestions.append(f"Rule is duplicated and can be deduplicated during merge: {rule}")
        if TITLE_RULE_RE.match(rule):
            high_risk.append(f"规则疑似标题或需求名，建议从 rules 中剔除: {rule}")
        if PAGE_DECL_RULE_RE.match(rule):
            high_risk.append(f"规则疑似页面声明，建议移动到页面抽取结果中: {rule}")

    if len(pages) == 1 and page_names and page_names[0] in {"主流程页面", "默认页面"}:
        high_risk.append("仅抽取到主流程页面，说明显式页面声明可能遗漏，请回查输入材料。")

    if len(pages) > 1 and not transitions:
        high_risk.append("已识别多个页面但没有抽取到流转，建议补充流程语句或流程图证据。")

    generic_triggers = [trigger for trigger in action_triggers if GENERIC_TRIGGER_RE.match(trigger)]
    if generic_triggers:
        suggestions.append("部分动作触发词仍是通用占位表达，建议结合页面目标和业务动词继续细化。")
    if action_triggers and len(set(action_triggers)) == 1 and len(action_triggers) > 1:
        high_risk.append("所有动作都使用同一个触发词，可能说明不同用户操作被错误收敛了。")

    unknown_count = len([item for item in top_unknowns if isinstance(item, str) and item.strip()])
    for page in pages:
        if isinstance(page, dict):
            unknown_count += len([item for item in page.get("unknowns", []) if isinstance(item, str) and item.strip()])
    if unknown_count > UNKNOWN_LIMIT:
        high_risk.append(f"Too many unknowns: {unknown_count}. Fill gaps before generating the final spec.")

    for page_id, states in state_lookup.items():
        if states and len(states) == 1:
            suggestions.append(f"Page has very few states; confirm whether loading, empty, or error states are missing: {page_id}")

    suggestions.append("Generate OpenSpec artifacts and archive knowledge only after validation passes.")
    return blocking, high_risk, suggestions


def main() -> None:
    try:
        data = load_json(DSL_PATH)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        fail_early(
            f"Cannot validate merged-dsl: {exc}",
            [
                "Complete Extract and Merge first, and ensure working/merged-dsl.json is a non-empty valid JSON file.",
                "If this is the first run, check working/pipeline-plan.md and working/input-readiness-report.md first.",
            ],
        )

    blocking, high_risk, suggestions = validate_dsl_data(data)
    write_report(blocking, high_risk, suggestions)
    print("validation-report.md generated")
    if blocking:
        print("Validation result: blocked")
        raise SystemExit(1)
    print("Validation result: pass")


if __name__ == "__main__":
    main()
