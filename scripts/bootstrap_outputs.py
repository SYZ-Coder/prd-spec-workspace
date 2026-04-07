from pathlib import Path

files = [
    "working/raw-dsl.json",
    "working/merged-dsl.json",
    "working/validation-report.md",
    "working/generated-prd.md",
    "working/page-source-map.md",
    "working/transition-map.md",
    "working/shared-rules.md",
    "openspec/specs/account/spec.md",
]

for file in files:
    path = Path(file)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("", encoding="utf-8")

print("bootstrap done")