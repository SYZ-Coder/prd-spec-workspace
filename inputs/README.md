# Inputs Guide

`inputs/` is the only entry area for raw requirement materials.

Everything the workspace extracts, validates, and generates starts from the files placed here. Good inputs improve extraction accuracy more than any downstream patching.

## Directory Responsibilities

### `inputs/prd/`
Store requirement descriptions and business intent.

Recommended content:

- PRDs
- proposals
- acceptance notes
- business descriptions
- structured requirement text

Best use:

- explain goals and scope
- name important pages or flows explicitly
- describe core rules and edge cases in text

### `inputs/screenshots/`
Store UI evidence.

Recommended content:

- page screenshots
- dialog screenshots
- prototype captures
- flow screenshots
- annotated UI images

Best use:

- show visible structure
- support page classification
- reveal page states and component clues

Important limit:

- screenshots are evidence, not complete business truth
- do not rely on screenshots alone for final business rules

### `inputs/notes/`
Store clarifications and operational details.

Recommended content:

- meeting notes
- verbal follow-ups
- exception handling notes
- edge-case reminders
- internal explanations that do not belong in the PRD

Best use:

- fill gaps left by PRD text
- surface special conditions and risk points
- separate confirmed facts from pending questions

### `inputs/context/`
Store supporting context that affects implementation or interpretation.

Recommended content:

- API descriptions
- role and permission notes
- system constraints
- historical compatibility notes
- integration requirements
- glossary or UI semantics

Best use:

- reduce unsupported guessing
- help generate better dependencies and API drafts
- clarify ownership, permissions, and upstream constraints

## Recommended Input Combinations

### Minimum viable set

- `prd + notes`
- or `screenshots + notes + context`

### Recommended set

- `prd + screenshots + notes + context`

### Strongest set

- `prd + screenshots + flow evidence + notes + context + api docs`

## Input Quality Checklist

1. Name important pages explicitly when possible.
2. Describe success paths and failure paths in text.
3. Call out key rules instead of scattering them across screenshots.
4. Put pending questions into notes instead of mixing them with facts.
5. Include interface or permission context when the requirement depends on them.
6. Preserve branch conditions in flow screenshots or notes.

## Common Mistakes

Avoid these patterns:

- placing generated outputs back into `inputs/`
- mixing old archived requirement files with a new active requirement
- using screenshots without any textual explanation
- hiding critical rules only in chat logs or image annotations
- assuming the extractor should guess missing business facts

## Suggested Workflow

1. Put raw materials into the correct subfolders.
2. Run the pipeline or at least the extract and validate steps.
3. Review `working/input-readiness-report.md` and `working/validation-report.md`.
4. Improve inputs first when extraction quality is weak.
5. Use `extractor-overrides.json` only for vocabulary tuning, not for replacing missing requirement facts.

## Related Documents

- [README.md](D:/spring_AI/prd-spec-workspace/README.md)
- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [guide.md](D:/spring_AI/prd-spec-workspace/guide.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [extractor-overrides.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides.md)
- [extractor-overrides_cn.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides_cn.md)
