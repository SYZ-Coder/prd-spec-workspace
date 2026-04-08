# OpenSpec 上下文包模板

将下面内容复制出来，替换占位符后，可直接作为喂给 OpenSpec 的标准上下文包。

```md
# OpenSpec Context Pack

## Change Meta

- Change Name: `<change-name>`
- Domain: `<domain>`
- Title: `<title>`

## Primary Inputs

请优先以以下 OpenSpec 变更包为主：

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`

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

## 建议复制文件清单

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/validation-report.md`
- `working/merged-dsl.json`
- `working/generated-api-contracts.md`
- `working/generated-testcases.md`
