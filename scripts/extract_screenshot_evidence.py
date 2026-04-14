from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

try:
    from scripts.workspace_utils import resolve_workspace
except ModuleNotFoundError:
    from workspace_utils import resolve_workspace

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
PAGE_NAME_RE = re.compile(r"([A-Za-z0-9\u4e00-\u9fff]{1,30}(?:页|页面|弹窗|首页|列表|详情|结果页|结果|中心|工作台|面板|设置|表单|步骤|向导|工作区))")
FIELD_HINTS = ["手机号", "用户名", "账号", "密码", "验证码", "搜索", "关键字", "邮箱", "姓名", "订单号", "金额"]
BUTTON_HINTS = ["登录", "注册", "确认", "保存", "提交", "删除", "返回", "取消", "支付", "退款", "搜索", "查询", "导出", "重新生成", "选用"]
TAB_HINTS = ["首页", "收藏", "全部", "我的", "详情", "设置", "列表", "图集"]


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def clean_candidate(text: str) -> str:
    text = normalize_text(text).replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip("-•· ").strip().rstrip("；;。")


def unique_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        value = clean_candidate(item)
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def screenshot_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(path for path in directory.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES)


def read_sidecar_text(image_path: Path) -> tuple[str, str]:
    candidates = [
        image_path.with_suffix(".txt"),
        image_path.with_suffix(".md"),
        image_path.with_suffix(".json"),
        image_path.with_suffix(".ocr.txt"),
        image_path.with_suffix(".ocr.md"),
        image_path.with_suffix(".ocr.json"),
    ]
    for candidate in candidates:
        if not candidate.exists() or candidate.stat().st_size == 0:
            continue
        if candidate.suffix == ".json":
            try:
                data = json.loads(candidate.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            text = data.get("text") or data.get("ocr_text") or "\n".join(data.get("lines", [])) if isinstance(data, dict) else ""
            if text:
                return normalize_text(str(text)), f"sidecar:{candidate.name}"
            continue
        try:
            return normalize_text(candidate.read_text(encoding="utf-8", errors="ignore")), f"sidecar:{candidate.name}"
        except OSError:
            continue
    return "", ""


def run_tesseract(image_path: Path) -> tuple[str, str]:
    if not shutil.which("tesseract"):
        return "", ""
    for lang in ["chi_sim+eng", "eng"]:
        try:
            completed = subprocess.run(["tesseract", str(image_path), "stdout", "-l", lang], capture_output=True, text=True, encoding="utf-8", errors="ignore", check=False)
        except OSError:
            return "", ""
        text = normalize_text(completed.stdout)
        if text:
            return text, f"tesseract:{lang}"
    return "", ""


def extract_components(ocr_text: str) -> dict[str, list[str]]:
    lines = [clean_candidate(line) for line in normalize_text(ocr_text).splitlines() if clean_candidate(line)]
    fields = [line for line in lines if any(hint in line for hint in FIELD_HINTS)]
    buttons = [line for line in lines if len(line) <= 16 and any(hint in line for hint in BUTTON_HINTS)]
    tabs = [line for line in lines if len(line) <= 12 and any(hint in line for hint in TAB_HINTS)]
    labels = [line for line in lines[:8] if line not in fields and line not in buttons and line not in tabs]
    return {
        "fields": unique_keep_order(fields),
        "buttons": unique_keep_order(buttons),
        "tabs": unique_keep_order(tabs),
        "labels": unique_keep_order(labels),
    }


def infer_page_name(image_path: Path, ocr_text: str, components: dict[str, list[str]]) -> str:
    for line in normalize_text(ocr_text).splitlines():
        match = PAGE_NAME_RE.search(clean_candidate(line))
        if match:
            return match.group(1)
    for label in components.get("labels", []):
        match = PAGE_NAME_RE.search(label)
        if match:
            return match.group(1)
    stem = image_path.stem.replace("_", " ").replace("-", " ")
    stem = clean_candidate(stem)
    return f"{stem}页面" if stem else "截图页面"


def infer_page_type(page_name: str, ocr_text: str, components: dict[str, list[str]]) -> str:
    text = f"{page_name} {ocr_text}"
    if components.get("fields"):
        return "form"
    if any(keyword in text for keyword in ["列表", "全部", "筛选", "记录"]):
        return "list"
    if any(keyword in text for keyword in ["详情"]):
        return "detail"
    if any(keyword in text for keyword in ["结果", "成功", "失败", "完成"]):
        return "result"
    if any(keyword in text for keyword in ["工作台", "看板", "面板"]):
        return "dashboard"
    return "generic"


def infer_interaction_modes(page_type: str, components: dict[str, list[str]]) -> list[str]:
    modes: list[str] = []
    if components.get("fields") and components.get("buttons"):
        modes.append("form-submit")
    if page_type in {"list", "dashboard"}:
        modes.append("browse")
    if page_type == "detail":
        modes.append("detail-view")
    if components.get("tabs"):
        modes.append("tab-switch")
    return unique_keep_order(modes or ["browse"])


def infer_platform(image_path: Path, ocr_text: str) -> str:
    text = f"{image_path.name} {ocr_text}".lower()
    if any(keyword in text for keyword in ["android", "ios", "mobile", "bottom", "tabbar"]):
        return "mobile"
    if any(keyword in text for keyword in ["web", "浏览器", "侧边栏", "导航栏"]):
        return "web"
    return "unknown"


def infer_navigation_type(page_type: str, components: dict[str, list[str]]) -> str:
    if components.get("tabs"):
        return "tab"
    if page_type in {"detail", "result", "form"}:
        return "stack"
    return "unknown"


def build_payload_for_image(image_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    ocr_text, engine = read_sidecar_text(image_path)
    confidence = 0.58
    if not ocr_text:
        ocr_text, engine = run_tesseract(image_path)
        confidence = 0.68 if ocr_text else 0.35
    else:
        confidence = 0.86
    components = extract_components(ocr_text)
    page_name = infer_page_name(image_path, ocr_text, components)
    page_type = infer_page_type(page_name, ocr_text, components)
    page_payload = {
        "screenshot": image_path.name,
        "page_name": page_name,
        "page_type": page_type,
        "interaction_modes": infer_interaction_modes(page_type, components),
        "platform": infer_platform(image_path, ocr_text),
        "navigation_type": infer_navigation_type(page_type, components),
        "confidence": round(confidence, 2),
        "components": components,
    }
    ocr_payload = {
        "screenshot": image_path.name,
        "text_evidence": ocr_text,
        "source": normalize_source_label(engine),
        "confidence": round(confidence, 2),
    }
    return ocr_payload, page_payload


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_source_label(engine: str) -> str:
    if not engine:
        return "none"
    if engine.startswith("sidecar:"):
        return engine
    return "local-text-provider"


def build_evidence_doc(ocr_items: list[dict[str, Any]], page_items: list[dict[str, Any]]) -> str:
    lines = ["# Screenshot Evidence", "", "## Text Evidence Sources"]
    if not ocr_items:
        lines.append("- None")
    for item in ocr_items:
        source = item.get("source") or normalize_source_label(str(item.get("engine", "")))
        lines.append(f"- {item['screenshot']} | Source: {source} | Confidence: `{item['confidence']}`")
        text_evidence = item.get("text_evidence") or item.get("ocr_text")
        if text_evidence:
            snippet = str(text_evidence).splitlines()[:3]
            for line in snippet:
                lines.append(f"  - {line}")
    lines.extend(["", "## Page Classification"])
    if not page_items:
        lines.append("- None")
    for item in page_items:
        lines.append(f"- {item['screenshot']} -> {item['page_name']} | type={item['page_type']} | platform={item['platform']} | nav={item['navigation_type']}")
        components = item.get("components", {})
        for key in ["fields", "buttons", "tabs", "labels"]:
            values = components.get(key, [])
            if values:
                lines.append(f"  - {key}: {', '.join(values)}")
    return "\n".join(lines) + "\n"


def write_screenshot_outputs(workspace: Path) -> None:
    screenshots_dir = workspace / "inputs" / "screenshots"
    working_dir = workspace / "working"
    working_dir.mkdir(parents=True, exist_ok=True)
    ocr_items: list[dict[str, Any]] = []
    page_items: list[dict[str, Any]] = []
    for image_path in screenshot_files(screenshots_dir):
        ocr_payload, page_payload = build_payload_for_image(image_path)
        ocr_items.append(ocr_payload)
        page_items.append(page_payload)
    write_json(working_dir / "screenshot-text-evidence.json", {"screenshots": ocr_items})
    write_json(working_dir / "page-classification.json", {"pages": page_items})
    (working_dir / "screenshot-evidence.md").write_text(build_evidence_doc(ocr_items, page_items), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text evidence and component evidence from screenshots.")
    parser.add_argument("--workspace", help="Workspace root. Auto-detects .prd-spec or standalone workspace when omitted.")
    args = parser.parse_args()
    write_screenshot_outputs(resolve_workspace(args.workspace))
    print("Screenshot evidence artifacts generated.")


if __name__ == "__main__":
    main()
