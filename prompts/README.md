# Prompts Guide

`prompts/` stores the stage-oriented prompt documents used by the requirement-to-spec workflow.

These prompt files are not product-domain templates. They are execution guides for different pipeline stages such as extraction, merge, validation, generation, and archiving.

## How to Think About This Directory

Use the prompts as workflow building blocks:

- they describe what each stage should produce
- they remind agents to separate facts, inferred structure, and unknowns
- they help keep the pipeline consistent across text, image, and mixed-input scenarios

The prompts should stay generic and reusable across product domains.

## Prompt Files

### `00_classify_pages.md`
Used in image-heavy scenarios.

Focus:

- identify components first
- classify page type
- infer interaction modes
- avoid jumping directly to business conclusions

Typical output:

- `working/page-classification.json`

### `01_extract_dsl.md`
Used when PRD or text materials exist.

Focus:

- extract pages, actions, rules, dependencies, and unknowns from text evidence
- keep facts separate from structured inference

### `02_extract_dsl_image.md`
Used when screenshots or prototypes are the main evidence source.

Focus:

- convert visual evidence into provisional DSL inputs
- remain conservative when business meaning is not explicit

### `03_merge_logic.md`
Used after initial extraction.

Focus:

- merge repeated pages
- merge shared rules and dependencies
- align cross-page transitions
- output a coherent merged DSL

Typical outputs:

- `working/transition-map.md`
- `working/shared-rules.md`
- `working/merged-dsl.json`

### `04_infer_flow.md`
Used mainly for image-driven or fragmented-input scenarios.

Focus:

- infer likely flow evidence from page relationships
- support merge and validation
- do not replace the final merge step

### `05_validate_spec.md`
Used before any downstream generation.

Focus:

- check completeness, consistency, and executability
- identify blockers and high-risk unknowns
- ensure generation does not proceed on broken structure

Typical output:

- `working/validation-report.md`

### `06_generate_openspec.md`
Used when merged DSL has passed validation.

Focus:

- generate reviewable Markdown requirement draft
- generate OpenSpec proposal, design, tasks, and spec files

### `07_generate_mermaid.md`
Used to generate diagram output from merged DSL.

Focus:

- preserve branch conditions
- show start, end, and exception paths
- keep cross-page conditions explicit

### `08_generate_testcases.md`
Used to generate test coverage from DSL and rules.

Focus:

- cover happy path, failure path, and boundary conditions
- ensure every rule is covered at least once
- ensure every action has at least one success and one failure case

### `09_generate_api_contracts.md`
Used to generate API drafts and OpenAPI skeletons.

Focus:

- prefer existing context from `inputs/context/`
- distinguish inferred contracts from confirmed contracts
- keep missing schema details in unknowns instead of inventing facts

### `10_archive_knowledge.md`
Used after the requirement is stable and reusable.

Focus:

- summarize reusable assets
- separate one-off context from future knowledge
- support `knowledge/` curation and archive workflow

## Usage Principles

1. Follow the fixed order: Extract, Merge, Validate, Generate, Derivative Outputs, Archive.
2. Keep facts, structured inference, and unknowns separate.
3. Do not convert unknowns into confirmed facts.
4. Do not let prompts become hardcoded business-domain scripts.
5. Keep prompt wording aligned with the latest DSL schema and archive model.

## When to Update These Prompts

Review this directory when:

- the DSL schema changes
- validation rules change
- output artifacts change
- archive model changes
- image-handling or context-selection workflow changes

When prompt behavior changes, keep these files aligned too:

- [README.md](D:/spring_AI/prd-spec-workspace/README.md)
- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [guide.md](D:/spring_AI/prd-spec-workspace/guide.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [knowledge/index.md](D:/spring_AI/prd-spec-workspace/knowledge/index.md)

## Related Documents

- [README.md](D:/spring_AI/prd-spec-workspace/README.md)
- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [guide.md](D:/spring_AI/prd-spec-workspace/guide.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [inputs/README.md](D:/spring_AI/prd-spec-workspace/inputs/README.md)
- [knowledge/index.md](D:/spring_AI/prd-spec-workspace/knowledge/index.md)
