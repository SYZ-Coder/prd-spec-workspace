# Tests Directory Guide

`tests/` contains the regression suite for the requirement-to-spec workspace.

These tests verify that the pipeline remains usable as a generic tool, especially around extraction, validation, generation, orchestration, knowledge archive, downstream context packs, and user extensibility.

## What These Tests Protect

The suite is aligned with the same platform principles used in the docs and scripts:

- structured understanding must remain generic and stable
- evidence, confidence, and unknown handling must not silently regress
- operator-facing outputs must stay readable
- downstream context packages must stay buildable

## How to Run Tests

Run the current core regression suite:

```bash
python -m unittest tests.test_extract_initial_dsl tests.test_manage_extractor_overrides tests.test_validate_dsl tests.test_generate_drafts tests.test_generate_derivatives tests.test_run_pipeline tests.test_archive_spec tests.test_select_context tests.test_build_context_pack tests.test_accuracy_examples -v
```

Run a single module:

```bash
python -m unittest tests.test_run_pipeline -v
```

## File-by-File Guide

| File | Purpose | What It Protects |
| --- | --- | --- |
| `test_extract_initial_dsl.py` | Tests the generic extraction logic. | Prevents regressions in page/action/rule/transition extraction, evidence mapping, confidence summaries, and override behavior. |
| `test_manage_extractor_overrides.py` | Tests the override management CLI behavior. | Ensures users can initialize and extend extraction config safely. |
| `test_validate_dsl.py` | Tests DSL validation and semantic quality checks. | Prevents silent regressions in validation rules, blocker reporting, and readable risk surfacing. |
| `test_generate_drafts.py` | Tests PRD and OpenSpec draft generation. | Ensures merged DSL can still produce usable draft artifacts. |
| `test_generate_derivatives.py` | Tests flow, testcase, and API derivative generation. | Protects downstream artifact generation from DSL changes. |
| `test_run_pipeline.py` | Tests the orchestration entry behavior. | Confirms pipeline plan generation and readable operator guidance. |
| `test_archive_spec.py` | Tests archive behavior. | Ensures snapshots and reusable knowledge outputs stay consistent. |
| `test_select_context.py` | Tests knowledge listing and selective context import behavior. | Prevents regressions in multi-requirement knowledge reuse. |
| `test_build_context_pack.py` | Tests downstream context-pack assembly behavior. | Ensures context packs can be generated for OpenSpec, Superpowers, and AI targets. |
| `test_accuracy_examples.py` | Tests example-based accuracy baselines. | Protects the current requirement-understanding baseline across representative product scenarios. |

## When to Run Which Tests

### After changing extraction behavior

Run:

```bash
python -m unittest tests.test_extract_initial_dsl tests.test_manage_extractor_overrides tests.test_validate_dsl tests.test_accuracy_examples -v
```

### After changing downstream generation

Run:

```bash
python -m unittest tests.test_generate_drafts tests.test_generate_derivatives tests.test_validate_dsl -v
```

### After changing pipeline orchestration or operator-facing output

Run:

```bash
python -m unittest tests.test_run_pipeline -v
```

### After changing archive or context reuse

Run:

```bash
python -m unittest tests.test_archive_spec tests.test_select_context -v
```

### After changing context-pack assembly

Run:

```bash
python -m unittest tests.test_build_context_pack -v
```

### Before claiming the workspace is healthy

Run the full set:

```bash
python -m unittest tests.test_extract_initial_dsl tests.test_manage_extractor_overrides tests.test_validate_dsl tests.test_generate_drafts tests.test_generate_derivatives tests.test_run_pipeline tests.test_archive_spec tests.test_select_context tests.test_build_context_pack tests.test_accuracy_examples -v
```

## Test Strategy Notes

These tests are intentionally focused on the pipeline's core behaviors:

- generic requirement extraction instead of fixed business templates
- readable operator outputs
- safe knowledge archiving and selective reuse
- user-controlled extraction extensibility
- downstream artifact generation from merged DSL
- stable evidence and confidence reporting

They do not replace manual review of a real requirement run. A passing test suite means the tool still behaves consistently, not that a specific requirement was perfectly understood.

## Related Documents

- [README.md](./README.md)
- [README_CN.md](./README_CN.md)
- [Documentation Index](../docs/README.md)
- [Chinese Documentation Index](../docs/README_CN.md)
- [scripts/README.md](../scripts/README.md)
- [new-requirement-sop_cn.md](../docs/new-requirement-sop_cn.md)
- [project-handbook_cn.md](../docs/project-handbook_cn.md)
- [Structured Understanding and Confidence Notes (CN)](../docs/structured-understanding-confidence_cn.md)
