# Scripts Directory Guide

`scripts/` contains the executable pipeline modules for this workspace.

Most users will interact with this directory through `run_pipeline.py`, but each file can also be used independently for debugging, tuning, validation, generation, and archive workflows.

## Recommended Entry Point

For normal use, start here:

```bash
python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<title>"
```

Use the individual scripts when you need to debug a specific stage.

## File-by-File Guide

| File | Purpose | Typical Usage |
| --- | --- | --- |
| `__init__.py` | Makes the `scripts` directory importable by tests and other modules. | Usually not run directly. |
| `bootstrap_outputs.py` | Initializes required folders and base output structure for a new requirement run. | `python scripts/bootstrap_outputs.py --change-name demo --domain account` |
| `extract_initial_dsl.py` | Reads `inputs/` and builds the initial/merged DSL plus supporting analysis files. | `python scripts/extract_initial_dsl.py --workspace .` |
| `validate_dsl.py` | Validates `working/merged-dsl.json` and writes `working/validation-report.md`. | `python scripts/validate_dsl.py` |
| `generate_drafts.py` | Generates the Markdown PRD and OpenSpec draft files from the merged DSL. | Usually called by `run_pipeline.py`; can also be run manually for regeneration. |
| `generate_derivatives.py` | Generates flow, test cases, API draft, and OpenAPI skeleton from the merged DSL. | Usually called by `run_pipeline.py`; can also be run manually. |
| `render_mermaid_assets.py` | Syncs derivative outputs into `outputs/` for easier sharing. | `python scripts/render_mermaid_assets.py` |
| `archive_spec.py` | Archives a stable requirement into `knowledge/`, preserving snapshots and reusable assets. | `python scripts/archive_spec.py --change-name demo --domain account --title "Demo"` |
| `select_context.py` | Lists and selects archived knowledge assets, bundles, or snapshots for reuse in a new requirement. | `python scripts/select_context.py --list` |
| `manage_extractor_overrides.py` | Initializes and updates `extractor-overrides.json` so users can tune extraction without editing core code. | `python scripts/manage_extractor_overrides.py --show` |
| `run_pipeline.py` | Main orchestration entry point. Runs bootstrap, readiness check, extraction, validation, generation, and sync in order. | `python scripts/run_pipeline.py --change-name demo --domain account --title "Demo"` |

## Which Script to Use When

### Start a new requirement

Use:

```bash
python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<title>"
```

### Only debug extraction

Use:

```bash
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
```

### Only adjust vocabulary and retry

Use:

```bash
python scripts/manage_extractor_overrides.py --show
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
```

### Only refresh downstream drafts

Use:

```bash
python scripts/generate_drafts.py --workspace . --change-name <change-name> --domain <domain> --title "<title>"
python scripts/generate_derivatives.py --workspace .
```

### Only publish shareable outputs

Use:

```bash
python scripts/render_mermaid_assets.py
```

### Archive a completed requirement

Use:

```bash
python scripts/archive_spec.py --change-name <change-name> --domain <domain> --title "<title>"
```

### Build a context pack for downstream tools

Use:

```bash
python scripts/build_context_pack.py --target openspec --change-name <change-name> --domain <domain> --title "<title>"
python scripts/build_context_pack.py --target superpowers --change-name <change-name> --domain <domain> --title "<title>" --goal "?????????"
python scripts/build_context_pack.py --target ai-development --change-name <change-name> --domain <domain> --title "<title>"
```

### Reuse archived context

Use:

```bash
python scripts/select_context.py --list
python scripts/select_context.py --bundle <bundle-name>
```

## Recommended Execution Order

1. `bootstrap_outputs.py`
2. `extract_initial_dsl.py`
3. `validate_dsl.py`
4. `generate_drafts.py`
5. `generate_derivatives.py`
6. `render_mermaid_assets.py`
7. `archive_spec.py`

In practice, `run_pipeline.py` covers steps 1 to 6 for you.

## Related Documents

- [README.md](D:/spring_AI/prd-spec-workspace/README.md)
- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [new-requirement-sop_cn.md](D:/spring_AI/prd-spec-workspace/docs/new-requirement-sop_cn.md)
- [project-handbook_cn.md](D:/spring_AI/prd-spec-workspace/docs/project-handbook_cn.md)
