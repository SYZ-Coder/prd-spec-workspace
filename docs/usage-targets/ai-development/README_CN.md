# AI Development 使用来源说明

如果你的目标是直接把需求喂给通用 AI、研发 AI、代码生成 AI 或测试设计 AI，推荐使用一组更平衡的上下文包。

## 推荐直接复制的产物组合

- `working/generated-prd.md`
- `working/generated-flow.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/generated-testcases.md`
- `working/validation-report.md`

如果 AI 还需要更强的结构化理解，再补：

- `working/merged-dsl.json`

## 为什么这组更合适

- `generated-prd.md` 适合快速理解需求范围
- `generated-flow.md` 适合理解主流程和异常路径
- `generated-api-contracts.md` 和 `openapi.yaml` 适合理解接口边界
- `generated-testcases.md` 适合理解验收条件
- `validation-report.md` 适合暴露风险和待确认项

## 不建议只给 AI 的内容

- 纯截图
- `raw-dsl.json`
- 单独 `tasks.md`

因为这些内容容易导致：

- 猜业务
- 缺上下文
- 把待确认项误当事实

## 最稳的做法

把“需求稿 + 流程 + 接口 + 测试 + 校验报告”一起复制给 AI，这样 AI 更容易在实现时保持边界感。

更多说明见：

- [artifact-usage-guide_cn.md](D:/spring_AI/prd-spec-workspace/docs/artifact-usage-guide_cn.md)
