# prd-spec-workspace Guide

This guide is the practical walkthrough for running `prd-spec-workspace` from a fresh requirement to reusable archived knowledge.

If you want the project overview first, read [README.md](D:/spring_AI/prd-spec-workspace/README.md).
If you want the documentation hub, read [docs/README.md](D:/spring_AI/prd-spec-workspace/docs/README.md).
If you prefer the Chinese project overview, read [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md).
If you want the execution checklist version, read [direct-use-checklist.md](D:/spring_AI/prd-spec-workspace/docs/direct-use-checklist.md).

## 1. Before You Start

Prepare as much evidence as possible in these four buckets:

- `inputs/prd/`
  Product requirement documents, proposals, acceptance notes, business descriptions.
- `inputs/screenshots/`
  Screenshots, prototypes, dialogs, flow screenshots, UI captures.
- `inputs/notes/`
  Clarifications, meeting notes, exception cases, implementation hints.
- `inputs/context/`
  API documents, role definitions, permission constraints, technical context.

Recommended minimum:

- one PRD or equivalent requirement description
- one notes file
- one context file when interfaces, roles, or permissions matter

Best-case input set:

- `prd + screenshots + notes + context + flow evidence`

## 2. Understand the Pipeline

The workspace follows a fixed order:

1. Extract
2. Merge
3. Validate
4. Generate drafts
5. Generate derivative outputs
6. Archive reusable knowledge

The key rule is: do not skip validation.

Two platform-wide principles also stay constant:

- structure understanding first, then draft downstream artifacts
- check evidence, confidence, and unknowns before deciding the requirement is ready

If validation reports blockers, improve the inputs or extractor overrides first. Do not force generation on top of a broken DSL.

## 3. Start a New Requirement

Choose a `change-name`, `domain`, and title.

Example:

```bash
python scripts/bootstrap_outputs.py --change-name auth-basic --domain account
```

Or run the full pipeline entry directly:

```bash
python scripts/run_pipeline.py --change-name auth-basic --domain account --title "Basic Authentication"
```

This will:

- bootstrap output directories
- inspect current inputs
- generate a pipeline plan
- extract the initial DSL
- validate the merged DSL
- generate downstream artifacts when validation passes

## 4. Enable Multimodal Visual Verification When Screenshots Matter

If screenshots or prototypes are important evidence, enable the optional vision stage:

```bash
python scripts/run_pipeline.py --change-name auth-basic --domain account --title "Basic Authentication" --enable-vision
```

Recommended usage rules:

- use `--enable-vision` only when screenshots materially affect requirement understanding
- keep screenshots under `inputs/screenshots/`
- if you already have reliable screenshot text, add sidecar files with the same basename

Examples:

- `login.png` with `login.txt`
- `login.png` with `login.md`
- `login.png` with `login.json`

When vision mode is enabled, review these files before trusting the DSL:

- [screenshot-evidence.md](D:/spring_AI/prd-spec-workspace/working/screenshot-evidence.md)
- [screenshot-text-evidence.json](D:/spring_AI/prd-spec-workspace/working/screenshot-text-evidence.json) as an internal auxiliary text-evidence file
- [page-classification.json](D:/spring_AI/prd-spec-workspace/working/page-classification.json)

Important constraints:

- Auxiliary text extraction is evidence, not final truth
- component recognition only strengthens the Extract step
- validation remains mandatory
- low-confidence visual or text evidence should be reviewed manually

## 5. Review the First Outputs

After the first run, start with these files:

- `working/pipeline-plan.md`
- `working/input-readiness-report.md`
- `working/raw-dsl.json`
- `working/merged-dsl.json`
- `working/validation-report.md`

Questions to ask:

- Were the main pages detected correctly?
- Did important rules enter `rules`?
- Are the transitions readable?
- Are there too many unknowns?
- Did the requirement collapse into a placeholder page?
- If vision mode was enabled, do visual evidence and component results actually match the screenshots?

## 6. Improve Extraction When Needed

Use this order.

### Option A. Improve the source inputs

This is the preferred fix.

Examples:

- add clearer page names into the PRD
- add flow wording such as `success enters result page`
- add API or permission context
- add notes for edge cases and failure handling
- add screenshot sidecar text if the UI contains important labels or field names

### Option B. Tune extractor overrides

If the weakness comes from domain vocabulary, use `extractor-overrides.json`.

Initialize overrides:

```bash
python scripts/manage_extractor_overrides.py --init
```

Inspect current overrides:

```bash
python scripts/manage_extractor_overrides.py --show
```

Common examples:

```bash
python scripts/manage_extractor_overrides.py --add-page-suffix Dashboard
python scripts/manage_extractor_overrides.py --add-action-prefix Export
python scripts/manage_extractor_overrides.py --add-rule-keyword real-time
python scripts/manage_extractor_overrides.py --add-rule-category reporting --add-category-keyword refresh
```

Then rerun:

```bash
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
```

For details, see:

- [Extractor Overrides Guide](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides.md)
- [Extractor Overrides Guide (CN)](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides_cn.md)

## 7. Review Draft Outputs

When validation passes, the pipeline generates draft outputs.

Review these next:

- `working/generated-prd.md`
- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`

Review from three angles:

- Product: page goals, rules, unknowns.
- QA: success path, failure path, boundary cases.
- Engineering: dependencies, interfaces, state changes, ambiguity.

## 8. Publish or Share Outputs

Once the outputs are good enough for review, use these folders:

- `outputs/diagrams/`
- `outputs/testcases/`
- `outputs/contracts/`

Keep `working/` as the editable analysis space. Treat `outputs/` as the cleaner handoff layer.

## 9. Archive Reusable Knowledge

When a requirement is complete and the generated material is stable, archive it.

Example:

```bash
python scripts/archive_spec.py --change-name auth-basic --domain account --title "Basic Authentication"
```

Archiving should preserve two things:

- the full snapshot of the requirement context
- reusable knowledge assets for future requirements

After archiving, the active `inputs/`, `working/`, and `outputs/` content can be cleaned to avoid contaminating the next requirement.

## 10. Reuse Knowledge Carefully

The knowledge system is useful only if reuse stays selective.

Prefer this order:

1. start with fresh inputs
2. list available knowledge assets
3. select only the bundles, assets, or snapshots that help the new requirement
4. avoid importing a whole old snapshot unless the new requirement is genuinely close to it

Useful commands:

```bash
python scripts/select_context.py --list
python scripts/select_context.py --list --domain account
python scripts/select_context.py --bundle account-core
```

## 11. Suggested Team Rhythm

A practical collaboration pattern is:

- Product owner prepares `inputs/prd/` and `inputs/notes/`
- Designer or analyst adds screenshots or flow evidence
- Engineer adds `inputs/context/` for interfaces, permissions, and dependencies
- Team reviews `working/validation-report.md` before accepting generated drafts
- Stable outputs are archived into `knowledge/`

## 12. Common Mistakes

Avoid these patterns:

- treating screenshots as complete business truth
- skipping validation because the generated draft looks plausible
- letting unknowns remain hidden inside rules or page descriptions
- reusing too much archived context for a new requirement
- fixing a weak extraction only by editing outputs instead of improving inputs or overrides
- treating auxiliary screenshot text as final fact without checking visual evidence and confidence

## 13. Recommended First Trial

If you are adopting this project for the first time:

1. choose one small but real requirement
2. prepare `prd + notes + context`
3. add screenshots if page understanding matters
4. enable vision mode only when screenshots are important evidence
5. inspect `raw-dsl`, `merged-dsl`, and `validation-report`
6. tune overrides only if the gap comes from vocabulary
7. review generated PRD, tests, and API drafts with the team
8. archive the requirement after review

This gives the team a stable baseline before scaling to larger requirements.

## 14. Related Documents

- [README.md](D:/spring_AI/prd-spec-workspace/README.md)
- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [direct-use-checklist.md](D:/spring_AI/prd-spec-workspace/docs/direct-use-checklist.md)
- [extractor-overrides.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides.md)
- [extractor-overrides_cn.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides_cn.md)
- [knowledge/index.md](D:/spring_AI/prd-spec-workspace/knowledge/index.md)
- [Structured Understanding and Confidence Notes (CN)](D:/spring_AI/prd-spec-workspace/docs/structured-understanding-confidence_cn.md)
- [Visual Evidence Extension Guide (CN)](D:/spring_AI/prd-spec-workspace/docs/visual-evidence-extension-guide_cn.md)
