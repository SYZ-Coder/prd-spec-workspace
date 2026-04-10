from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]


def has_content(directory: Path) -> bool:
    if not directory.exists():
        return False
    return any(path.is_file() and path.stat().st_size > 0 for path in directory.rglob("*"))


def count_files(directory: Path) -> int:
    if not directory.exists():
        return 0
    return sum(1 for path in directory.rglob("*") if path.is_file() and path.stat().st_size > 0)


def scan_context_text() -> str:
    context_dir = WORKSPACE / "inputs" / "context"
    if not context_dir.exists():
        return ""
    parts: list[str] = []
    for path in context_dir.rglob("*.md"):
        try:
            parts.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return "\n".join(parts).lower()


def detect_mode() -> str:
    has_prd = has_content(WORKSPACE / "inputs" / "prd")
    has_screenshots = has_content(WORKSPACE / "inputs" / "screenshots")
    if has_prd and has_screenshots:
        return "hybrid"
    if has_prd:
        return "prd"
    return "image-only"


def build_prompt_order(mode: str, enable_vision: bool) -> list[str]:
    prompts: list[str] = []
    if enable_vision:
        prompts.append("prompts/00_classify_pages.md")
    if mode == "hybrid":
        prompts.extend([
            "prompts/01_extract_dsl.md",
            "prompts/04_infer_flow.md",
            "prompts/03_merge_logic.md",
            "prompts/05_validate_spec.md",
            "prompts/06_generate_openspec.md",
            "prompts/07_generate_mermaid.md",
            "prompts/08_generate_testcases.md",
            "prompts/09_generate_api_contracts.md",
            "prompts/10_archive_knowledge.md",
        ])
        return prompts
    if mode == "prd":
        prompts.extend([
            "prompts/01_extract_dsl.md",
            "prompts/03_merge_logic.md",
            "prompts/05_validate_spec.md",
            "prompts/06_generate_openspec.md",
            "prompts/07_generate_mermaid.md",
            "prompts/08_generate_testcases.md",
            "prompts/09_generate_api_contracts.md",
            "prompts/10_archive_knowledge.md",
        ])
        return prompts
    prompts.extend([
        "prompts/02_extract_dsl_image.md",
        "prompts/04_infer_flow.md",
        "prompts/03_merge_logic.md",
        "prompts/05_validate_spec.md",
        "prompts/06_generate_openspec.md",
        "prompts/07_generate_mermaid.md",
        "prompts/08_generate_testcases.md",
        "prompts/09_generate_api_contracts.md",
        "prompts/10_archive_knowledge.md",
    ])
    return prompts


def run_python(script: str, *extra_args: str) -> int:
    cmd = [sys.executable, script, *extra_args]
    completed = subprocess.run(cmd, cwd=WORKSPACE, check=False)
    return completed.returncode


def build_input_readiness_report(mode: str, enable_vision: bool) -> tuple[str, list[str]]:
    prd_count = count_files(WORKSPACE / "inputs" / "prd")
    screenshot_count = count_files(WORKSPACE / "inputs" / "screenshots")
    notes_count = count_files(WORKSPACE / "inputs" / "notes")
    context_count = count_files(WORKSPACE / "inputs" / "context")
    context_text = scan_context_text()

    warnings: list[str] = []
    suggestions: list[str] = []

    if prd_count == 0:
        warnings.append("未发现非空 PRD 文件，业务规则将更多依赖截图和推断。")
    if screenshot_count == 0:
        warnings.append("未发现非空截图文件，页面结构和界面状态的准确度会下降。")
    if notes_count == 0:
        warnings.append("未发现非空备注文件，边界条件和补充规则可能缺失。")
    if context_count == 0:
        warnings.append("未发现非空上下文文件，接口契约和权限约束的准确度会下降。")
    if context_count > 0:
        if not any(keyword in context_text for keyword in ["api", "接口", "openapi", "path", "request", "response"]):
            warnings.append("上下文中未发现明显接口说明，接口产物可能只能停留在草案层。")
        if not any(keyword in context_text for keyword in ["权限", "role", "auth", "鉴权", "托管", "房主"]):
            warnings.append("上下文中未发现明显角色或权限约束，行为规则可能不完整。")

    if mode == "hybrid":
        suggestions.append("当前为混合模式，抽取时应同时使用 PRD 证据和截图/流程证据。")
    elif mode == "prd":
        suggestions.append("当前为 PRD 模式，如有截图建议补充，以提升页面和状态识别准确度。")
    else:
        suggestions.append("当前为纯图片模式，建议补充 PRD 或备注，降低业务误判风险。")

    if enable_vision and screenshot_count > 0:
        suggestions.append("已开启视觉增强，将优先生成多模态视觉证据、页面分类和组件核对中间产物。")
    elif screenshot_count > 0:
        suggestions.append("如需提升截图或原型理解准确度，可增加 --enable-vision 开启多模态视觉证据与组件核对。")

    if notes_count == 0:
        suggestions.append("建议在 inputs/notes/ 中补充异常流程、边界条件和默认规则。")
    if context_count == 0 or any("接口说明" in item for item in warnings):
        suggestions.append("建议在 inputs/context/ 中补充接口说明、权限规则或状态机描述。")

    lines = [
        "# Input Readiness Report",
        "",
        f"- Mode: `{mode}`",
        f"- Vision Enabled: `{str(enable_vision).lower()}`",
        f"- PRD Files: `{prd_count}`",
        f"- Screenshot Files: `{screenshot_count}`",
        f"- Notes Files: `{notes_count}`",
        f"- Context Files: `{context_count}`",
        "",
        "## Warnings",
    ]
    lines.extend([f"- {item}" for item in warnings] or ["- None"])
    lines.extend(["", "## Suggestions"])
    lines.extend([f"- {item}" for item in suggestions] or ["- None"])
    return "\n".join(lines) + "\n", warnings


def write_pipeline_plan(change_name: str, domain: str, title: str, mode: str, prompt_order: list[str], enable_vision: bool = False) -> Path:
    plan_path = WORKSPACE / "working" / "pipeline-plan.md"
    lines = [
        "# Pipeline Plan",
        "",
        f"- 变更名: `{change_name}`",
        f"- 领域: `{domain}`",
        f"- 标题: `{title}`",
        f"- 模式: `{mode}`",
        f"- 视觉增强: `{str(enable_vision).lower()}`",
        "",
        "## Prompt 顺序",
    ]
    lines.extend([f"{index}. `{prompt}`" for index, prompt in enumerate(prompt_order, start=1)])
    lines.extend([
        "",
        "## 说明",
        "- 先按顺序生成 working 目录下的中间产物，再执行校验。",
        "- 若开启视觉增强，会先生成多模态视觉证据、页面分类和组件核对结果，再并入 DSL 抽取。",
        "- 只有在 validation 没有 blocker 时，才继续生成 OpenSpec 和衍生产物。",
        "- 衍生产物生成完成后，再同步到 outputs/。",
        "- 需求内容稳定后，再执行归档命令 archive_spec.py。",
    ])
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return plan_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare and verify the PRD-to-spec pipeline for direct team use.")
    parser.add_argument("--change-name", required=True, help="OpenSpec change folder name.")
    parser.add_argument("--domain", default="account", help="OpenSpec domain name.")
    parser.add_argument("--title", default="", help="Human-readable change title.")
    parser.add_argument("--skip-auto-extract", action="store_true", help="Skip generating initial raw-dsl.json and merged-dsl.json from local inputs.")
    parser.add_argument("--skip-validate", action="store_true", help="Skip validate_dsl.py execution.")
    parser.add_argument("--skip-sync", action="store_true", help="Skip copying derived artifacts to outputs/.")
    parser.add_argument("--enable-vision", action="store_true", help="Enable multimodal visual evidence and component verification for screenshots before DSL extraction.")
    args = parser.parse_args()

    title = args.title.strip() or args.change_name
    mode = detect_mode()
    prompt_order = build_prompt_order(mode, args.enable_vision)

    print(f"Detected mode: {mode}")
    print("Bootstrapping workspace...")
    bootstrap_rc = run_python("scripts/bootstrap_outputs.py", "--change-name", args.change_name, "--domain", args.domain)
    if bootstrap_rc != 0:
        raise SystemExit(bootstrap_rc)

    readiness_report, warnings = build_input_readiness_report(mode, args.enable_vision)
    readiness_path = WORKSPACE / "working" / "input-readiness-report.md"
    readiness_path.write_text(readiness_report, encoding="utf-8")
    if warnings:
        print(f"Input readiness warnings written to: {readiness_path.relative_to(WORKSPACE)}")
    else:
        print("Input readiness check passed without warnings.")

    plan_path = write_pipeline_plan(args.change_name, args.domain, title, mode, prompt_order, enable_vision=args.enable_vision)
    print(f"Pipeline plan written to: {plan_path.relative_to(WORKSPACE)}")
    print("Recommended prompt order:")
    for index, prompt in enumerate(prompt_order, start=1):
        print(f"{index}. {prompt}")

    merged_dsl = WORKSPACE / "working" / "merged-dsl.json"
    if not args.skip_auto_extract:
        if args.enable_vision and has_content(WORKSPACE / "inputs" / "screenshots"):
            print("Generating multimodal screenshot evidence and component verification artifacts ...")
            vision_rc = run_python("scripts/extract_screenshot_evidence.py", "--workspace", str(WORKSPACE))
            if vision_rc != 0:
                raise SystemExit(vision_rc)
        print("Generating initial DSL artifacts from local inputs ...")
        extract_rc = run_python("scripts/extract_initial_dsl.py", "--workspace", str(WORKSPACE))
        if extract_rc != 0:
            raise SystemExit(extract_rc)

    validation_passed = False
    if not args.skip_validate and merged_dsl.exists() and merged_dsl.read_text(encoding="utf-8").strip():
        print("Running DSL validation...")
        validate_rc = run_python("scripts/validate_dsl.py")
        if validate_rc != 0:
            raise SystemExit(validate_rc)
        validation_passed = True
    else:
        print("Skipping validation because working/merged-dsl.json is missing or empty.")

    if validation_passed:
        print("Generating draft PRD and OpenSpec artifacts ...")
        drafts_rc = run_python("scripts/generate_drafts.py", "--workspace", str(WORKSPACE), "--change-name", args.change_name, "--domain", args.domain, "--title", title)
        if drafts_rc != 0:
            raise SystemExit(drafts_rc)

        print("Generating derivative artifacts ...")
        derivatives_rc = run_python("scripts/generate_derivatives.py", "--workspace", str(WORKSPACE))
        if derivatives_rc != 0:
            raise SystemExit(derivatives_rc)

    if not args.skip_sync:
        print("Syncing derived artifacts to outputs/ ...")
        sync_rc = run_python("scripts/render_mermaid_assets.py")
        if sync_rc != 0:
            raise SystemExit(sync_rc)

    print("")
    print("下一步建议")
    print("1. 按 pipeline-plan.md 的顺序检查 working 和 OpenSpec 产物。")
    print("2. 查看 input-readiness-report.md，补齐 warnings 中提示的缺口。")
    print("3. 确认 validation-report.md 中没有 blocker。")
    print(f"4. 归档命令: python scripts/archive_spec.py --change-name {args.change_name} --domain {args.domain} --title \"{title}\"")


if __name__ == "__main__":
    main()
