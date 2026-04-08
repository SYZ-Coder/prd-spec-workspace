# Knowledge Index

`knowledge/` stores archived requirement knowledge so teams can reuse stable context without polluting the next active requirement.

Use this directory in two layers:

- snapshots: complete historical context for one requirement
- reusable assets: distilled specs, rules, patterns, API notes, and confirmed decisions

## Directory Structure

### `catalog.json`
The machine-readable index of archived changes, reusable assets, and bundle relationships.

Use it when you want to:

- list archived requirements
- find reusable assets by domain or tag
- understand which change produced which asset
- support tooling such as context selection

### `index.md`
This human-readable overview. Keep it short and update it when the knowledge model changes.

### `snapshots/`
Each snapshot stores the full working context for one completed requirement.

A snapshot typically includes:

- archived `inputs/`
- archived `working/`
- archived `outputs/`
- archived `openspec/changes/<change-name>/`
- `manifest.json`

Use snapshots when you need traceability or want to revisit exactly how a previous requirement was interpreted.

Do not import snapshots by default for a new requirement. Prefer selective reuse.

### `assets/specs/`
Stable requirement or domain specifications that are worth referencing again.

Examples:

- common process specs
- product capability baselines
- cross-team business specifications

### `assets/rules/`
Reusable business rules or operational constraints extracted from completed requirements.

Examples:

- permission rules
- approval constraints
- data validation rules
- settlement or timing rules

### `assets/patterns/`
Reusable interaction, page-flow, or modeling patterns.

Examples:

- multi-step submission flow
- review and approval pattern
- retry-and-recover pattern
- role-based entry pattern

### `assets/api/`
Reusable interface context, API contracts, or integration notes.

Use this layer when a future requirement depends on a known upstream or downstream interface.

### `assets/decisions/`
Confirmed decisions that were once unknowns and now serve as future context.

Examples:

- confirmed timeout policy
- final permission ownership
- chosen validation strategy
- agreed fallback behavior

### `bundles/`
Bundles are curated context sets for selective reuse.

A bundle may point to:

- a group of reusable assets
- a domain baseline
- a change-specific reusable pack

Use bundles when you want a controlled amount of prior context instead of pulling in everything.

## How to Reuse Knowledge Safely

Recommended order:

1. start from fresh requirement inputs
2. list available knowledge assets
3. select only the assets, bundles, or snapshots that help
4. avoid importing full snapshots unless the new requirement is genuinely close to the archived one

Useful commands:

```bash
python scripts/select_context.py --list
python scripts/select_context.py --list --domain account
python scripts/select_context.py --change-name auth-basic --include-snapshot
python scripts/select_context.py --bundle account-core
```

## Archive Expectations

A good archive should preserve:

- traceability: what the team saw at the time
- reusability: what future requirements can safely inherit
- boundaries: what must stay requirement-specific and should not be reused blindly

## Maintenance Notes

When updating the knowledge model, keep these files aligned:

- [archive_spec.py](D:/spring_AI/prd-spec-workspace/scripts/archive_spec.py)
- [select_context.py](D:/spring_AI/prd-spec-workspace/scripts/select_context.py)
- [README.md](D:/spring_AI/prd-spec-workspace/README.md)
- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [guide.md](D:/spring_AI/prd-spec-workspace/guide.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)

## Current Status

The current workspace supports:

- requirement snapshots
- reusable knowledge assets
- bundles for selective context import
- catalog and index documents for discovery

Keep `knowledge/` focused on reusable context. If something is too specific to one requirement, prefer storing it only in the corresponding snapshot.
