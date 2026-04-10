# OpenSpec 使用来源说明

如果你的目标是继续进入 OpenSpec 变更执行链路，优先使用这些文件：

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`

推荐再一起提供：

- `working/validation-report.md`
- `working/merged-dsl.json`
- `working/generated-api-contracts.md`
- `working/generated-testcases.md`

## 为什么这样组合

- OpenSpec 变更包已经是最接近执行语言的产物
- `validation-report.md` 能暴露 blocker 和风险
- `merged-dsl.json` 提供结构化骨架
- 接口和测试稿可以帮助继续细化任务与验收

## 最小推荐复制包

- `proposal.md`
- `design.md`
- `tasks.md`
- `spec.md`
- `validation-report.md`

## 不建议只复制

- `raw-dsl.json`
- 截图
- 单独的流程图

更多说明见：

- [artifact-usage-guide_cn.md](../../artifact-usage-guide_cn.md)
