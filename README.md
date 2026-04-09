# prd-spec-workspace

A generic requirement-to-spec workspace for turning PRDs, screenshots, notes, and context files into structured DSL, reviewable specs, OpenSpec change packs, test cases, flows, and API drafts.

中文说明见 [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md).

## What This Project Is

This repository is a tooling workspace for requirement analysis.

It is designed to help teams take mixed requirement inputs such as:

- product requirement documents
- screenshots or prototypes
- meeting notes
- interface or permission context
- flow descriptions

and convert them into a consistent set of structured outputs.

The core idea is:

`raw requirement materials -> structured DSL -> validation -> spec artifacts -> reusable knowledge`

This project is intentionally tool-oriented, not business-template-oriented. It should stay generic and let users extend extraction accuracy through configuration instead of hardcoding product domains into the code.

## End-to-End Flow

```mermaid
flowchart LR
    A["inputs/prd\ninputs/screenshots\ninputs/notes\ninputs/context"] --> B["Extract\nraw-dsl.json\npage-source-map.md"]
    B --> C["Merge\nmerged-dsl.json\ntransition-map.md\nshared-rules.md"]
    C --> D["Validate\nvalidation-report.md"]
    D -->|Ready| E["Generate Drafts\ngenerated-prd.md\nOpenSpec change pack"]
    D -->|Blocked| H["Fix Inputs or Overrides\ninputs/*\nextractor-overrides.json"]
    H --> B
    E --> F["Derivative Outputs\nflow\ntestcases\napi contracts\nopenapi.yaml"]
    F --> G["Archive\nknowledge/*\nsnapshots/*"]
```

## Why Use It

This workspace is useful when a team wants to:

- reduce ambiguity before implementation starts
- make requirement analysis more structured and repeatable
- separate confirmed facts from inferred structure and unknowns
- generate implementation-facing artifacts from the same requirement source
- archive reusable knowledge after a requirement is complete
- give AI agents a more stable and reviewable requirement context

## Key Capabilities

### 1. Requirement Extraction

The extractor reads materials from `inputs/` and produces a structured DSL that includes:

- pages
- transitions
- rules
- dependencies
- unknowns

### 2. Validation Before Generation

The pipeline validates the merged DSL before downstream generation, which helps catch:

- isolated pages
- missing exit paths
- invalid transitions
- duplicated ids
- missing dependency declarations
- overly noisy or incomplete extraction results

### 3. Multi-Artifact Generation

From one validated DSL, the workspace can generate:

- Markdown requirement draft
- OpenSpec proposal / design / tasks / spec
- flow diagrams
- test cases
- API contract draft
- OpenAPI YAML skeleton

### 4. Knowledge Archiving

Completed requirements can be archived into `knowledge/` so the workspace can retain reusable assets without polluting the next active requirement.

### 5. User-Extensible Extraction

Teams can improve extraction accuracy without changing Python code by using:

- `extractor-overrides.json`
- `scripts/manage_extractor_overrides.py`

## Standard Outputs

### Working Artifacts

- `working/page-source-map.md`
- `working/raw-dsl.json`
- `working/transition-map.md`
- `working/shared-rules.md`
- `working/merged-dsl.json`
- `working/validation-report.md`
- `working/generated-prd.md`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`

### OpenSpec Change Pack

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`

### Published Outputs

- `outputs/diagrams/`
- `outputs/testcases/`
- `outputs/contracts/`

### Knowledge Outputs

- `knowledge/specs/`
- `knowledge/patterns/`
- `knowledge/rules/`
- `knowledge/api/`
- `knowledge/decisions/`
- `knowledge/snapshots/`

## What Users Actually Get

This platform is useful not just because it generates files, but because those files can drive the next step of delivery.

After one requirement run, a team usually gets three kinds of value:

- a structured requirement core for understanding and validation
- reviewable specs for product, QA, and engineering alignment
- ready-to-copy context packs for downstream execution tools

In practice, that means the workspace can help a team move from raw materials to:

- requirement clarification
- implementation planning
- API alignment
- testcase design
- AI-assisted development
- reusable archived knowledge

## Output-to-Tool Map

```mermaid
flowchart LR
    A["working/merged-dsl.json
validation-report.md"] --> B["Review and Clarify"]
    C["generated-prd.md
generated-flow.md"] --> B
    D["OpenSpec change pack
proposal / design / tasks / spec"] --> E["OpenSpec Execution"]
    F["generated-testcases.md
generated-api-contracts.md
validation-report.md"] --> E
    D --> G["Superpowers Workflows"]
    F --> G
    H["generated-prd.md
generated-flow.md
generated-testcases.md
generated-api-contracts.md
openapi.yaml"] --> I["General AI / Dev AI"]
    A --> I
    J["build_context_pack.py"] --> K["context-pack-openspec.md"]
    J --> L["context-pack-superpowers.md"]
    J --> M["context-pack-ai-development.md"]
    K --> E
    L --> G
    M --> I
```

## How Outputs Are Used

### 1. Review and Clarify

Use these when the team wants to understand the requirement and find ambiguity early:

- `working/merged-dsl.json`
- `working/validation-report.md`
- `working/generated-prd.md`
- `working/generated-flow.md`

### 2. Drive OpenSpec Execution

Use these when the next step is change planning, execution planning, or implementation tracking in OpenSpec:

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- plus `working/validation-report.md` as a guardrail

### 3. Drive Superpowers Workflows

Use these when the next step is design refinement, implementation planning, implementation support, or acceptance support:

- OpenSpec change pack files
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/generated-flow.md`
- `working/validation-report.md`

### 4. Feed General AI / Dev AI

Use these when the next step is AI-assisted coding, testcase design, interface discussion, or requirement interpretation:

- `working/generated-prd.md`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/validation-report.md`
- optionally `working/merged-dsl.json`

## Context Pack Assembly

The workspace can now assemble reusable Markdown context packs for downstream tools.

Use:

```bash
python scripts/build_context_pack.py --target openspec --change-name my-change --domain account --title "My Requirement"
python scripts/build_context_pack.py --target superpowers --change-name my-change --domain account --title "My Requirement" --goal "Implementation planning and support"
python scripts/build_context_pack.py --target ai-development --change-name my-change --domain account --title "My Requirement"
```

Default outputs:

- `working/context-pack-openspec.md`
- `working/context-pack-superpowers.md`
- `working/context-pack-ai-development.md`

These are meant to be copied directly into OpenSpec-oriented workflows, Superpowers workflows, or general AI development sessions.

## Repository Layout

```text
inputs/
  prd/
  screenshots/
  notes/
  context/

scripts/
  bootstrap_outputs.py
  extract_initial_dsl.py
  validate_dsl.py
  generate_drafts.py
  generate_derivatives.py
  render_mermaid_assets.py
  archive_spec.py
  select_context.py
  manage_extractor_overrides.py
  build_context_pack.py
  run_pipeline.py

working/
openspec/
outputs/
knowledge/
docs/
prompts/
tests/
examples/
```

## Quick Start

### 1. Prepare the workspace

```bash
python scripts/bootstrap_outputs.py --change-name demo-change --domain account
```

### 2. Put materials into `inputs/`

Recommended minimum:

- one PRD or equivalent requirement note
- one notes file
- one context file if interfaces or permissions matter

Best-case input set:

- `prd + screenshots + notes + context + flow evidence`

### 3. Run the pipeline

```bash
python scripts/run_pipeline.py --change-name demo-change --domain account --title "Sample Requirement"
```

### 4. Review generated artifacts

Focus on:

- `working/merged-dsl.json`
- `working/validation-report.md`
- `working/generated-prd.md`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`

### 5. Archive when stable

```bash
python scripts/archive_spec.py --change-name demo-change --domain account --title "Sample Requirement"
```

## Typical Commands

```bash
python scripts/bootstrap_outputs.py --change-name my-change --domain account
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
python scripts/run_pipeline.py --change-name my-change --domain account --title "My Requirement"
python scripts/archive_spec.py --change-name my-change --domain account --title "My Requirement"
python scripts/select_context.py --list
python scripts/build_context_pack.py --target openspec --change-name my-change --domain account --title "My Requirement"
```

## Extending Extraction

If your team uses domain-specific wording, you do not need to edit the extractor code first.

Initialize overrides:

```bash
python scripts/manage_extractor_overrides.py --init
```

Inspect overrides:

```bash
python scripts/manage_extractor_overrides.py --show
```

Extend overrides:

```bash
python scripts/manage_extractor_overrides.py --add-page-suffix 看板
python scripts/manage_extractor_overrides.py --add-action-prefix 导出
python scripts/manage_extractor_overrides.py --add-rule-keyword 实时刷新
python scripts/manage_extractor_overrides.py --add-rule-category 报表规则 --add-category-keyword 实时刷新
```

Detailed guides:

- [Extractor Overrides Guide](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides.md)
- [Extractor Overrides 中文版](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides_cn.md)

## Documentation

- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [Guide](D:/spring_AI/prd-spec-workspace/guide.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [Direct Use Checklist](D:/spring_AI/prd-spec-workspace/docs/direct-use-checklist.md)
- [New Requirement SOP (CN)](D:/spring_AI/prd-spec-workspace/docs/new-requirement-sop_cn.md)
- [Project Handbook (CN)](D:/spring_AI/prd-spec-workspace/docs/project-handbook_cn.md)
- [Artifact Usage Guide (CN)](D:/spring_AI/prd-spec-workspace/docs/artifact-usage-guide_cn.md)
- [Context Pack Templates (CN)](D:/spring_AI/prd-spec-workspace/docs/context-pack-templates/README_CN.md)
- [Context Pack Assembly Guide (CN)](D:/spring_AI/prd-spec-workspace/docs/context-pack-assembly-guide_cn.md)
- [Context Pack Assembly Guide (CN)](D:/spring_AI/prd-spec-workspace/docs/context-pack-assembly-guide_cn.md)
- [Extractor Overrides Guide](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides.md)
- [Contributing](D:/spring_AI/prd-spec-workspace/CONTRIBUTING.md)
- [CHANGELOG](D:/spring_AI/prd-spec-workspace/CHANGELOG.md)

## Examples

- [Examples README](D:/spring_AI/prd-spec-workspace/examples/README.md)
- [auth-basic](D:/spring_AI/prd-spec-workspace/examples/auth-basic)
- [payment-refund](D:/spring_AI/prd-spec-workspace/examples/payment-refund)
- [reporting-dashboard](D:/spring_AI/prd-spec-workspace/examples/reporting-dashboard)

## Testing

```bash
python -m unittest tests.test_extract_initial_dsl tests.test_manage_extractor_overrides tests.test_validate_dsl tests.test_generate_drafts tests.test_generate_derivatives tests.test_run_pipeline tests.test_archive_spec tests.test_select_context -v
```

## Contributing

If you want to contribute, start with:

- [Contributing](D:/spring_AI/prd-spec-workspace/CONTRIBUTING.md)
- [.github/ISSUE_TEMPLATE/bug_report.md](D:/spring_AI/prd-spec-workspace/.github/ISSUE_TEMPLATE/bug_report.md)
- [.github/ISSUE_TEMPLATE/feature_request.md](D:/spring_AI/prd-spec-workspace/.github/ISSUE_TEMPLATE/feature_request.md)

## License

This repository uses MIT:

- [LICENSE](D:/spring_AI/prd-spec-workspace/LICENSE)
