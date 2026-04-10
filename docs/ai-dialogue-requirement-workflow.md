# AI Dialogue Requirement Workflow

This document explains a frequently misunderstood point in the platform:

- how to start a new requirement through AI dialogue
- what `run_pipeline.py` actually does
- where AI starts to matter in the workflow
- how a user can rely on the platform rules to turn product prototypes or mixed requirement inputs into Markdown specs more accurately

The short version is:

- the platform principle does not change: structure first, validate second, generate specs third
- `run_pipeline.py` is an orchestration script, not the requirement understanding itself
- AI matters in the stages where the platform reads inputs, interprets the requirement, extracts structure, judges risk, and decides whether downstream generation is justified
- the scripts make that process repeatable, testable, and easier for teams to use at scale

## 1. How to Start a New Requirement in AI Dialogue

When you have a new product requirement, first prepare these inputs:

- `inputs/prd/`
- `inputs/screenshots/`
- `inputs/notes/`
- `inputs/context/`

Then start the AI dialogue explicitly, for example:

```text
This is a new requirement. Please follow the platform rules and do structured recognition first.
Do not write a final draft immediately.
Please extract pages, actions, rules, transitions, dependencies, and unknowns from inputs/ first,
and then judge whether the requirement is ready for downstream spec generation.
```

If the requirement is prototype- or screenshot-driven, you can say:

```text
This is a new requirement mainly based on prototype screens and screenshots.
Please classify pages first, then do structured recognition, and only then generate a reviewable Markdown spec draft.
Do not turn unknowns into confirmed facts.
```

In this mode, AI is responsible for:

- reading the raw materials
- doing structured requirement understanding
- identifying pages, actions, rules, states, transitions, and dependencies
- preserving unknowns explicitly
- judging whether the current inputs are strong enough to support downstream generation

In other words, AI dialogue is the requirement recognition and judgment layer.

## 2. What `run_pipeline.py` Does

`run_pipeline.py` is the main orchestration entry point.

It is responsible for running the platform stages in the correct order:

1. inspect input directories
2. detect the current mode
   - `prd`
   - `image-only`
   - `hybrid`
3. generate `working/input-readiness-report.md`
4. generate `working/pipeline-plan.md`
5. trigger extraction scripts
6. trigger validation scripts
7. trigger spec generation when validation passes
8. trigger derivative artifact generation
9. sync outputs into `outputs/`
10. print next-step guidance and archive instructions

You can think of it as:

- it controls workflow order
- it controls stage transitions
- it generates operator-facing guidance
- it does not do free-form requirement interpretation on its own

So `run_pipeline.py` is not the requirement understanding engine. It is the workflow coordinator.

## 3. Where AI Starts to Matter

AI matters in two different but related ways inside this platform.

### 3.1 Dialogue-driven AI

This is the mode closest to what users usually mean when they want the platform skills to recognize a new product requirement accurately.

In that mode, AI is responsible for:

- reading raw materials
- applying the platform rules during extraction
- separating facts, structured inference, and unknowns
- judging recognition quality and risk
- deciding whether Markdown spec generation should continue

This is the most important layer because it affects:

- whether the requirement is understood correctly
- whether key rules are missed
- whether prototypes are misread
- whether transitions are joined incorrectly

### 3.2 Scripted platform rules

The scripts are the engineering form of those same rules.

For example:

- `extract_initial_dsl.py` turns the extraction rules into code
- `validate_dsl.py` turns structural and semantic quality gates into code
- `generate_drafts.py` turns the DSL-to-Markdown and DSL-to-OpenSpec rules into code

So the better mental model is:

- the platform principles define how AI should understand requirements
- the scripts make those principles stable and repeatable

## 4. Why It Looks Like the Platform Is “Just Running Scripts” Now

Because this is not meant to be only a free-form assistant.

It is a workflow platform that combines AI reasoning with engineering execution.

If you only had dialogue and no scripts, you would quickly run into problems such as:

- unstable output shape from run to run
- skipped steps
- weak regression safety
- weak archive and reuse discipline
- harder teamwork and handoff

With scripts in place:

- stages stay explicit
- outputs stay consistent
- tests can protect core behavior
- archive and reuse become manageable
- teams can collaborate on the same structure

So script execution is not a deviation from the core idea. It is how the platform protects it.

## 5. How a User Should Ask AI to Recognize Product Prototype Requirements Precisely

This is the key usage pattern.

### Step 1. Prepare inputs first

At minimum, place:

- prototype or UI screenshots in `inputs/screenshots/`
- clarifying notes in `inputs/notes/`
- PRD or flow descriptions in `inputs/prd/` when available
- interfaces, roles, or permissions in `inputs/context/` when available

### Step 2. Ask for structured recognition first, not a final draft

A recommended dialogue prompt is:

```text
This is a new requirement. Please follow the platform rules and do structured recognition first.
Please extract pages, actions, rules, transitions, dependencies, and unknowns.
Prioritize understanding the page relationships and interaction patterns in the prototype.
Only generate a Markdown requirement draft after the structured layer is clear.
```

### Step 3. Review the structure before generation

Check first:

- whether page recognition is correct
- whether the main flow is correct
- whether important rules are missing
- whether unknowns remain explicit

### Step 4. Then generate Markdown specs

Only when the structure looks trustworthy should you continue into:

- `generated-prd.md`
- OpenSpec change packs
- flow diagrams
- testcase drafts
- API drafts

That is the best way to maximize accuracy from prototype requirement to Markdown specification.

## 6. Recommended Real Usage Mode

The best default is a two-stage pattern: dialogue judgment first, scripted output second.

### Mode A: dialogue recognition first, scripts second

Best for:

- complex requirements
- many prototype screens
- cases where you suspect possible misreading
- teams that want to review structured recognition before writing files

Flow:

1. let AI perform structured recognition in dialogue
2. inspect whether the recognition result is reasonable
3. then run `run_pipeline.py` to produce stable artifacts

### Mode B: scripts first, AI review second

Best for:

- standard requirements
- strong inputs
- teams already comfortable with the platform

Flow:

1. run `run_pipeline.py`
2. then use AI to review `merged-dsl.json`, `validation-report.md`, and `generated-prd.md`

## 7. The Core Idea Does Not Change

Whether you use the dialogue-first mode or the script-first mode, the platform still follows the same center of gravity:

- do not jump directly from prototype to final spec
- do not let AI freely improvise requirement documents
- do not force requirements into fixed business templates

Instead:

- understand the requirement structurally first
- validate the recognition quality second
- generate specs third
- then pass the result into OpenSpec, Superpowers, or AI development workflows

## 8. One-Sentence Summary

If you want one sentence that captures the platform:

It does not use scripts to replace AI requirement understanding. It uses platform rules to stabilize AI requirement understanding, and then uses scripts to turn that into engineered outputs.

## 9. Related Documents

- [README.md](./README.md)
- [README_CN.md](./README_CN.md)
- [Guide](../guide.md)
- [Platform Runtime Mechanism (CN)](./platform-runtime-mechanism_cn.md)
- [Structured Understanding and Confidence Notes (CN)](./structured-understanding-confidence_cn.md)
- [New Requirement SOP (CN)](./new-requirement-sop_cn.md)
- [Artifact Usage Guide (CN)](./artifact-usage-guide_cn.md)
- [scripts/README.md](../scripts/README.md)
