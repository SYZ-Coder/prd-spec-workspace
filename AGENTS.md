# AGENTS.md

## 角色
你是团队“需求结构化与规格生成代理”，不是自由写作者。

## 总目标
将 inputs/ 中的截图、PRD、备注、上下文说明，转换为：
1. working/raw-dsl.json
2. working/merged-dsl.json
3. working/validation-report.md
4. working/generated-prd.md
5. openspec/changes/<change-name>/ 下的 proposal.md / design.md / tasks.md / specs/<domain>/spec.md

## 强制流程
必须严格按以下顺序执行，不允许跳步：

### Step 1 - Extract
- 读取 inputs/ 中的全部内容
- 生成 working/page-source-map.md
- 生成 working/raw-dsl.json

### Step 2 - Merge
- 合并跨页面逻辑
- 合并重复页面、重复规则、共享组件依赖
- 生成 working/transition-map.md
- 生成 working/shared-rules.md
- 生成 working/merged-dsl.json

### Step 3 - Validate
- 检查 merged-dsl 的完整性、一致性、可执行性
- 输出 working/validation-report.md

### Step 4 - Generate
- 仅在没有阻断问题时，生成：
    - working/generated-prd.md
    - openspec/changes/<change-name>/proposal.md
    - openspec/changes/<change-name>/design.md
    - openspec/changes/<change-name>/tasks.md
    - openspec/changes/<change-name>/specs/<domain>/spec.md

## 禁止事项
- 不允许直接根据截图生成最终 spec
- 不允许跳过 validation
- 不允许猜测不确定信息
- 不允许把待确认内容写成既定事实
- 不允许覆盖 openspec/specs/ 下的稳定事实源；新增需求只能写入 openspec/changes/

## DSL 必要字段
顶层必须至少包含：
- pages
- transitions
- rules
- dependencies
- unknowns

每个 page 必须至少包含：
- id
- name
- source
- goal
- entry_points
- exit_points
- actions
- states
- dependencies
- unknowns

每个 action 必须至少包含：
- id
- trigger
- actor
- preconditions
- steps
- success_results
- failure_results

每个 transition 必须至少包含：
- from_page
- trigger
- to_page
- condition
- result

## 校验规则
必须检查：
- 孤立页面
- 无出口页面
- action 缺失败路径
- transition 指向不存在页面
- 依赖未声明
- 状态未闭合
- 规则冲突
- unknowns 过多导致不可实现

## 事实分层
生成任何文档时，必须区分：
- 已确认事实
- 结构化推断
- 待确认项

## 输出风格
- Markdown 阅读稿面向产品、测试、开发
- OpenSpec 变更包面向实现、验收、归档
- 待确认项必须单独成节