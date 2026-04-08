# AI Development 上下文包模板

将下面内容复制出来，替换占位符后，可直接作为喂给通用 AI / 开发 AI 的标准上下文包。

```md
# AI Development Context Pack

## Requirement Meta

- Change Name: `<change-name>`
- Domain: `<domain>`
- Title: `<title>`
- Target: `<代码实现 / 测试设计 / 接口联调 / 方案评审 / 缺陷分析>`

## Primary Inputs

请先理解以下需求和流程材料：

- `working/generated-prd.md`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`

## Structured Support

如果需要更强的结构化理解，请继续参考：

- `working/merged-dsl.json`
- `working/validation-report.md`

## Usage Goal

请基于以上材料：

1. 在开始实现或分析前，先指出是否仍存在 blocker 或明显待确认项
2. 将 `validation-report.md` 中的风险纳入判断
3. 不要把 unknowns 当作已确认事实
4. 如果当前目标是代码实现，请优先遵守流程、接口和测试约束

## Notes

- `generated-prd.md` 负责解释范围
- `generated-flow.md` 负责解释流程
- `generated-api-contracts.md` 和 `openapi.yaml` 负责解释接口边界
- `generated-testcases.md` 负责解释验收逻辑
- `merged-dsl.json` 用于补足结构化语义
```

## 建议复制文件清单

- `working/generated-prd.md`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/merged-dsl.json`
- `working/validation-report.md`
