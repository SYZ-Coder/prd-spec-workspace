import json
from pathlib import Path

dsl_path = Path("working/merged-dsl.json")
report_path = Path("working/validation-report.md")

if not dsl_path.exists():
    raise FileNotFoundError("working/merged-dsl.json 不存在")

data = json.loads(dsl_path.read_text(encoding="utf-8"))

pages = data.get("pages", [])
transitions = data.get("transitions", [])
rules = data.get("rules", [])
top_dependencies = set(data.get("dependencies", []))
top_unknowns = data.get("unknowns", [])

page_ids = {p["id"] for p in pages}
page_names = {p["name"] for p in pages}

blocking = []
high_risk = []
suggestions = []

# 1. 页面入口/出口检查
for p in pages:
    if not p.get("entry_points"):
        blocking.append(f"页面缺入口: {p['id']} / {p['name']}")
    if not p.get("exit_points"):
        blocking.append(f"页面缺出口: {p['id']} / {p['name']}")

# 2. Action failure path 检查
for p in pages:
    for a in p.get("actions", []):
        if not a.get("failure_results"):
            blocking.append(f"Action 缺失败路径: {p['id']} / {p['name']} -> {a.get('trigger', 'UNKNOWN')}")

# 3. Transition 指向合法性
for t in transitions:
    to_page = t.get("to_page")
    from_page = t.get("from_page")
    if from_page not in page_ids:
        blocking.append(f"Transition from_page 不存在: {from_page}")
    if to_page not in page_ids:
        blocking.append(f"Transition to_page 不存在: {to_page}")

# 4. 依赖声明检查
declared_dependencies = set(top_dependencies)
for p in pages:
    declared_dependencies.update(p.get("dependencies", []))

for p in pages:
    for dep in p.get("dependencies", []):
        if dep not in declared_dependencies:
            high_risk.append(f"页面依赖未在顶层归并: {p['id']} -> {dep}")

# 5. 状态最小检查
for p in pages:
    if not p.get("states"):
        high_risk.append(f"页面无状态定义: {p['id']} / {p['name']}")

# 6. 规则最小检查
if not rules:
    high_risk.append("顶层 rules 为空，可能导致业务约束缺失")

# 7. unknowns 数量检查
unknown_count = len(top_unknowns)
for p in pages:
    unknown_count += len(p.get("unknowns", []))

if unknown_count > 15:
    high_risk.append(f"unknowns 数量过多: {unknown_count}，建议先补齐再生成 spec")

# 8. 孤立页面检查（没有 transition 指向它，也没有 entry_points）
incoming = {pid: 0 for pid in page_ids}
for t in transitions:
    if t.get("to_page") in incoming:
        incoming[t["to_page"]] += 1

for p in pages:
    if incoming[p["id"]] == 0 and not p.get("entry_points"):
        blocking.append(f"孤立页面: {p['id']} / {p['name']}")

# 输出报告
lines = ["# 校验报告", "", "## 一、阻断问题"]
if blocking:
    lines.extend([f"- {x}" for x in blocking])
else:
    lines.append("- 无")

lines.extend(["", "## 二、高风险问题"])
if high_risk:
    lines.extend([f"- {x}" for x in high_risk])
else:
    lines.append("- 无")

lines.extend(["", "## 三、建议补充项"])
if suggestions:
    lines.extend([f"- {x}" for x in suggestions])
else:
    lines.append("- 补充接口依赖、角色权限、异常场景、边界条件会更稳")

lines.extend(["", "## 四、可生成性结论"])
lines.append("- 不可生成" if blocking else "- 可生成")

report_path.write_text("\n".join(lines), encoding="utf-8")
print("validation-report.md generated")