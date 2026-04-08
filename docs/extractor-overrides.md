# Extractor Overrides Guide

## Purpose

`extractor-overrides.json` is the user extension point for improving requirement extraction without changing Python code.

Use it when:

- a new product line uses page names that the default extractor does not recognize
- a team uses domain-specific action words such as `导出`, `派单`, `核销`
- business rules often use keywords that should be extracted or classified more accurately
- the team wants to tune extraction behavior incrementally and keep the main tool generic

## Quick Start

Initialize the file:

```bash
python scripts/manage_extractor_overrides.py --init
```

Show current config:

```bash
python scripts/manage_extractor_overrides.py --show
```

Add common extensions:

```bash
python scripts/manage_extractor_overrides.py --add-page-suffix 看板
python scripts/manage_extractor_overrides.py --add-action-prefix 导出
python scripts/manage_extractor_overrides.py --add-standalone-action 核销
python scripts/manage_extractor_overrides.py --add-rule-keyword 实时刷新
python scripts/manage_extractor_overrides.py --add-rule-category 报表规则 --add-category-keyword 实时刷新
```

## File Location

The file lives at the workspace root:

[`extractor-overrides.json`](D:/spring_AI/prd-spec-workspace/extractor-overrides.json)

The extractor loads it automatically when `python scripts/extract_initial_dsl.py` or `python scripts/run_pipeline.py` runs.

## Supported Fields

### `page_suffixes`

Used to recognize page-like objects.

Example:

```json
{
  "page_suffixes": ["看板", "驾驶舱", "门户"]
}
```

Use this when your team writes `分析看板`, `经营驾驶舱`, `客户门户` instead of `XX页`.

### `action_prefixes`

Used to extract verb phrases from page descriptions.

Example:

```json
{
  "action_prefixes": ["导出", "派单", "核销"]
}
```

If a page description says `支持导出报表`, the extractor can turn it into an action like `导出报表`.

### `standalone_actions`

Used for action words that may appear without a longer prefix phrase.

Example:

```json
{
  "standalone_actions": ["核销", "派单"]
}
```

### `ignored_standalone_actions`

Used to suppress overly generic standalone actions when they create noise.

Example:

```json
{
  "ignored_standalone_actions": ["查询"]
}
```

### `rule_keywords`

Used to decide whether a sentence should be treated as a rule candidate.

Example:

```json
{
  "rule_keywords": ["实时刷新", "幂等", "T+1"]
}
```

Use this when the default keyword set misses important business constraints.

### `rule_categories`

Used to classify rules into more useful groups.

Example:

```json
{
  "rule_categories": {
    "报表规则": ["实时刷新", "导出", "汇总口径"],
    "履约规则": ["派单", "签收", "核销"]
  }
}
```

### `section_aliases`

Used when your documents use custom headings.

Example:

```json
{
  "section_aliases": {
    "验收规则": "rules",
    "页面清单": "pages",
    "流程说明": "flow"
  }
}
```

## Recommended Tuning Order

1. Add `section_aliases` if your PRD headings are not being recognized.
2. Add `page_suffixes` if pages are collapsing into `主流程页面`.
3. Add `action_prefixes` or `standalone_actions` if actions are too generic.
4. Add `rule_keywords` if key constraints are missing from `rules`.
5. Add `rule_categories` if rule grouping is hard to review.

## Example

For a reporting product:

```json
{
  "page_suffixes": ["看板"],
  "action_prefixes": ["导出"],
  "rule_keywords": ["实时刷新"],
  "rule_categories": {
    "报表规则": ["实时刷新", "导出"]
  }
}
```

This can help the extractor recognize:

- `分析看板` as a page
- `导出报表` as an action
- `报表数据需要实时刷新` as a rule

## Verification

After changing the file, rerun:

```bash
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
```

Then review:

- `working/raw-dsl.json`
- `working/merged-dsl.json`
- `working/shared-rules.md`
- `working/validation-report.md`

## Tips

- Prefer small, explicit additions over large noisy vocabularies.
- Add words that are stable across many requirements, not one-off phrasing.
- If a term changes page detection and rule detection at the same time, validate both outputs.
- If extraction becomes noisier after an addition, remove that term and try a narrower one.

## Boundary

`extractor-overrides.json` is meant for vocabulary and classification tuning.

It is not the right place for:

- hardcoding a full business workflow
- forcing a specific page graph for one requirement
- replacing validation with assumptions

If a requirement needs one-off interpretation, keep that in the source PRD or notes instead of pushing it into shared overrides.
