# Superpowers 使用来源说明

如果你的目标是继续用 Superpowers 做：

- 需求澄清
- 设计收口
- 任务拆解
- 实现辅助
- 验收辅助

推荐按场景复制产物，而不是只给单个文件。

## 设计 / 澄清阶段推荐输入

- `working/generated-prd.md`
- `working/merged-dsl.json`
- `working/validation-report.md`
- `working/generated-flow.md`

## 计划 / 拆解阶段推荐输入

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`

## 实现阶段推荐输入

- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/generated-testcases.md`
- `working/validation-report.md`

## 关键原则

- 优先给经过 validation 的产物
- 优先给 OpenSpec 变更包，而不是只给原始 DSL
- 测试稿和接口草案可以显著提高实现辅助效果

更多说明见：

- [artifact-usage-guide_cn.md](../../artifact-usage-guide_cn.md)
