# OpenSpec 示例上下文包

下面是一份可直接参考的 OpenSpec 示例上下文包，使用需求 `user-login-register` 作为样例。

```md
# OpenSpec Context Pack

## Change Meta

- Change Name: `user-login-register`
- Domain: `account`
- Title: `用户登录注册需求`

## Primary Inputs

请优先以以下 OpenSpec 变更包为主：

- `openspec/changes/user-login-register/proposal.md`
- `openspec/changes/user-login-register/design.md`
- `openspec/changes/user-login-register/tasks.md`
- `openspec/changes/user-login-register/specs/account/spec.md`

## Supporting Inputs

为避免执行计划脱离真实约束，请同时参考：

- `working/validation-report.md`
- `working/merged-dsl.json`
- `working/generated-api-contracts.md`
- `working/generated-testcases.md`

## Usage Goal

请基于以上材料：

1. 检查当前变更包是否足以进入执行阶段
2. 识别仍需确认的 blocker / high-risk unknowns
3. 进一步细化实现顺序、执行计划和任务边界
4. 保持事实、结构化推断和待确认项分层，不要把待确认项写成既定事实

## Notes

- 以 `spec.md`、`design.md` 和 `tasks.md` 为主
- `validation-report.md` 必须一起看，避免在存在 blocker 时继续推进
- `raw-dsl.json` 不作为首选输入
```

## 对应建议复制文件

- `openspec/changes/user-login-register/proposal.md`
- `openspec/changes/user-login-register/design.md`
- `openspec/changes/user-login-register/tasks.md`
- `openspec/changes/user-login-register/specs/account/spec.md`
- `working/validation-report.md`
- `working/merged-dsl.json`
- `working/generated-api-contracts.md`
- `working/generated-testcases.md`
