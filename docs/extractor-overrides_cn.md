# 提取器扩展配置使用指南

## 文档目的

`extractor-overrides.json` 是需求抽取器的用户扩展入口，用来在不修改 Python 代码的前提下，持续优化需求识别效果。

适用场景：

- 新产品线使用了默认抽取器还不认识的页面命名方式
- 团队常用一些行业动作词，例如 `导出`、`派单`、`核销`
- 业务规则经常使用默认关键词之外的表述
- 希望把抽取优化沉淀成配置，而不是把业务模板硬编码进主流程

## 快速开始

初始化配置文件：

```bash
python scripts/manage_extractor_overrides.py --init
```

查看当前配置：

```bash
python scripts/manage_extractor_overrides.py --show
```

常见追加命令：

```bash
python scripts/manage_extractor_overrides.py --add-page-suffix 看板
python scripts/manage_extractor_overrides.py --add-action-prefix 导出
python scripts/manage_extractor_overrides.py --add-standalone-action 核销
python scripts/manage_extractor_overrides.py --add-rule-keyword 实时刷新
python scripts/manage_extractor_overrides.py --add-rule-category 报表规则 --add-category-keyword 实时刷新
```

## 文件位置

配置文件位于仓库根目录：

`extractor-overrides.json`

运行以下脚本时会自动加载：

- `python scripts/extract_initial_dsl.py --workspace .`
- `python scripts/run_pipeline.py --change-name ...`

## 可扩展字段

### `page_suffixes`

用于扩展“什么名称看起来像页面”。

示例：

```json
{
  "page_suffixes": ["看板", "驾驶舱", "门户"]
}
```

如果团队常写 `分析看板`、`经营驾驶舱`、`客户门户`，而不是 `XX页`，就应该补这个字段。

### `action_prefixes`

用于扩展动作短语前缀。

示例：

```json
{
  "action_prefixes": ["导出", "派单", "核销"]
}
```

例如页面描述中出现 `支持导出报表`，抽取器就更容易生成 `导出报表` 这样的动作。

### `standalone_actions`

用于补充那些可能单独出现的动作词。

示例：

```json
{
  "standalone_actions": ["核销", "派单"]
}
```

### `ignored_standalone_actions`

用于屏蔽噪声较大的通用动作词。

示例：

```json
{
  "ignored_standalone_actions": ["查询"]
}
```

### `rule_keywords`

用于扩展规则识别关键词。

示例：

```json
{
  "rule_keywords": ["实时刷新", "幂等", "T+1"]
}
```

如果默认规则识别漏掉了关键约束，可以优先补这里。

### `rule_categories`

用于自定义规则分组。

示例：

```json
{
  "rule_categories": {
    "报表规则": ["实时刷新", "导出", "汇总口径"],
    "履约规则": ["派单", "签收", "核销"]
  }
}
```

### `section_aliases`

用于补充你们团队自己的 PRD 标题习惯。

示例：

```json
{
  "section_aliases": {
    "验收规则": "rules",
    "页面清单": "pages",
    "流程说明": "flow"
  }
}
```

## 推荐调优顺序

1. 如果 PRD 章节没被识别，先补 `section_aliases`。
2. 如果页面经常被抽成 `主流程页面`，补 `page_suffixes`。
3. 如果动作太泛或者缺动作，补 `action_prefixes` / `standalone_actions`。
4. 如果规则漏抽，补 `rule_keywords`。
5. 如果规则分组不好评审，再补 `rule_categories`。

## 示例

假设你在做报表产品，可以这样配置：

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

这样可以帮助抽取器更稳定地识别：

- `分析看板` 是页面
- `导出报表` 是动作
- `报表数据需要实时刷新` 是规则

## 修改后的验证方式

修改配置后，建议重新执行：

```bash
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
```

重点检查以下文件：

- `working/raw-dsl.json`
- `working/merged-dsl.json`
- `working/shared-rules.md`
- `working/validation-report.md`

## 使用建议

- 优先补“小而准”的词，不要一次堆很多模糊词汇。
- 优先补“可复用”的稳定业务词，不要为一次性需求堆临时词。
- 某个词如果同时影响页面识别和规则识别，补完后要一起复查两边结果。
- 如果补词后噪声明显上升，先删除该词，再换更具体的词。

## 使用边界

`extractor-overrides.json` 适合做“词汇和分类调优”，不适合做下面这些事：

- 为单条需求硬编码整条业务流程
- 强行指定固定页面图
- 用配置替代 validation
- 把待确认信息写死成事实

如果某个信息只对当前一次需求有效，更适合写在原始 PRD、notes 或 context 里，而不是放进共享 overrides。
