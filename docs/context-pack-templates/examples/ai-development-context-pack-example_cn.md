# AI Development 示例上下文包

下面是一份可直接参考的 AI Development 示例上下文包，使用需求 `user-login-register` 作为样例。

```md
# AI Development Context Pack

## Requirement Meta

- Change Name: `user-login-register`
- Domain: `account`
- Title: `用户登录注册需求`
- Target: `代码实现`

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

## 对应建议复制文件

- `working/generated-prd.md`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/merged-dsl.json`
- `working/validation-report.md`
