# Superpowers 示例上下文包

下面是一份可直接参考的 Superpowers 示例上下文包，使用需求 `user-login-register` 作为样例。

```md
# Superpowers Context Pack

## Change Meta

- Change Name: `user-login-register`
- Domain: `account`
- Title: `用户登录注册需求`
- Current Goal: `实现计划与实现辅助`

## Primary Inputs

请优先理解以下规格和结构化产物：

- `openspec/changes/user-login-register/proposal.md`
- `openspec/changes/user-login-register/design.md`
- `openspec/changes/user-login-register/tasks.md`
- `openspec/changes/user-login-register/specs/account/spec.md`
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

## 对应建议复制文件

- `openspec/changes/user-login-register/proposal.md`
- `openspec/changes/user-login-register/design.md`
- `openspec/changes/user-login-register/tasks.md`
- `openspec/changes/user-login-register/specs/account/spec.md`
- `working/generated-prd.md`
- `working/merged-dsl.json`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/validation-report.md`
