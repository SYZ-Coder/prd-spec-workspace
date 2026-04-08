# Superpowers 上下文包模板

将下面内容复制出来，替换占位符后，可直接作为喂给 Superpowers 的标准上下文包。

```md
# Superpowers Context Pack

## Change Meta

- Change Name: `<change-name>`
- Domain: `<domain>`
- Title: `<title>`
- Current Goal: `<需求澄清 / 设计收口 / 实现计划 / 实现辅助 / 验收辅助>`

## Primary Inputs

请优先理解以下规格和结构化产物：

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/generated-prd.md`
- `working/merged-dsl.json`

## Supporting Inputs

请结合以下材料补全流程、接口、测试和风险边界：

- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/validation-report.md`

## Usage Goal

请基于以上材料：

1. 先判断当前目标更适合继续做澄清、设计、计划还是实现
2. 保持事实、推断、待确认项分层
3. 如果材料仍有 blocker，先指出而不是直接进入实现
4. 如果进入实现计划或实现辅助，请把测试和接口约束也纳入考虑

## Notes

- 如果当前目标是“计划 / 拆解”，优先参考 OpenSpec 变更包
- 如果当前目标是“实现 / 验收”，必须一起看测试稿和接口草案
- 不要只根据流程图或截图推进实现
```

## 建议复制文件清单

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/generated-prd.md`
- `working/merged-dsl.json`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/validation-report.md`
