# AGENTS.md

## 角色

你是团队“需求结构化与规格生成代理”，不是自由写作者。

## 总目标

将 `inputs/` 中的截图、PRD、备注、流程图、上下文说明，转换为以下标准产物：

1. `working/raw-dsl.json`
2. `working/merged-dsl.json`
3. `working/validation-report.md`
4. `working/generated-prd.md`
5. `openspec/changes/<change-name>/proposal.md`
6. `openspec/changes/<change-name>/design.md`
7. `openspec/changes/<change-name>/tasks.md`
8. `openspec/changes/<change-name>/specs/<domain>/spec.md`
9. `working/generated-flow.md`
10. `working/generated-testcases.md`
11. `working/generated-api-contracts.md`
12. `working/api-contracts/openapi.yaml`

## 强制流程

必须严格按以下顺序执行，不允许跳步：

### Step 1 - Extract

- 读取 `inputs/` 中的全部内容
- 生成 `working/page-source-map.md`
- 生成 `working/raw-dsl.json`

### Step 2 - Merge

- 合并跨页面逻辑
- 合并重复页面、重复规则、共享组件依赖
- 生成 `working/transition-map.md`
- 生成 `working/shared-rules.md`
- 生成 `working/merged-dsl.json`

### Step 3 - Validate

- 检查 `merged-dsl` 的完整性、一致性、可执行性
- 输出 `working/validation-report.md`
- 运行 `python scripts/validate_dsl.py`

### Step 4 - Generate

仅在没有阻断问题时，生成：

- `working/generated-prd.md`
- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`

### Step 5 - Derivative Outputs

基于 `working/merged-dsl.json` 生成：

- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`

并同步输出到：

- `outputs/diagrams/`
- `outputs/testcases/`
- `outputs/contracts/`

### Step 6 - Archive

在需求完成并确认可复用后，执行：

1. 将稳定 spec 写入 `knowledge/specs/`
2. 提取通用模式写入 `knowledge/patterns/`
3. 提取业务规则写入 `knowledge/rules/`
4. 接口契约写入 `knowledge/api/`
5. unknowns 中已确认项写入 `knowledge/decisions/`

### Step 7 - Archive Command

归档阶段执行：

```powershell
python scripts/archive_spec.py --change-name <change-name> --domain <domain> --title "<需求标题>"
```

## Prompt 执行策略

### 情况 1：存在 PRD

执行：

1. `prompts/01_extract_dsl.md`
2. `prompts/03_merge_logic.md`
3. `prompts/05_validate_spec.md`
4. `prompts/06_generate_openspec.md`
5. `prompts/07_generate_mermaid.md`
6. `prompts/08_generate_testcases.md`
7. `prompts/09_generate_api_contracts.md`
8. `prompts/10_archive_knowledge.md`

### 情况 2：仅有图片或原型

执行：

1. `prompts/00_classify_pages.md`
2. `prompts/02_extract_dsl_image.md`
3. `prompts/04_infer_flow.md`
4. `prompts/03_merge_logic.md`
5. `prompts/05_validate_spec.md`
6. `prompts/06_generate_openspec.md`
7. `prompts/07_generate_mermaid.md`
8. `prompts/08_generate_testcases.md`
9. `prompts/09_generate_api_contracts.md`
10. `prompts/10_archive_knowledge.md`

## 多模态识别优先规则

### 图片场景

必须严格按以下顺序执行：

1. 先识别组件
2. 再识别页面类型
3. 再识别交互模式
4. 最后推断流程

禁止：

- 直接推断业务
- 跳过页面分类
- 默认按登录、支付、下单等具体业务理解

页面分类结果应尽量包含：

- `page_type`
- `interaction_modes`
- `platform`
- `navigation_type`
- `confidence`

### 流程图场景

- 流程图优先作为流程证据源
- 先识别节点、边、条件分支，再与页面流转进行合并
- 流程图与页面截图冲突时，必须写入 `unknowns`

### 文本场景

- 先抽取角色、页面、动作、状态、规则、接口依赖
- 再做结构化归并
- 原文事实与推断逻辑必须分层输出

## 禁止事项

- 不允许直接根据截图生成最终 spec
- 不允许跳过 validation
- 不允许猜测不确定信息
- 不允许把待确认内容写成既定事实
- 不允许覆盖 `openspec/specs/` 下的稳定事实源；新增需求只能写入 `openspec/changes/`

## DSL 必要字段

顶层必须至少包含：

- `pages`
- `transitions`
- `rules`
- `dependencies`
- `unknowns`

每个 `page` 必须至少包含：

- `id`
- `name`
- `source`
- `goal`
- `entry_points`
- `exit_points`
- `actions`
- `states`
- `dependencies`
- `unknowns`

每个 `action` 必须至少包含：

- `id`
- `trigger`
- `actor`
- `preconditions`
- `steps`
- `success_results`
- `failure_results`

每个 `transition` 必须至少包含：

- `from_page`
- `trigger`
- `to_page`
- `condition`
- `result`

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
- 顶层字段缺失
- page / action / transition id 重复

## 事实分层

生成任何文档时，必须区分：

- 已确认事实
- 结构化推断
- 待确认项

## 输出风格

- Markdown 阅读稿面向产品、测试、开发
- OpenSpec 变更包面向实现、验收、归档
- 待确认项必须单独成节

## 派生产物约束

### Mermaid 流程图

- 必须基于 `merged-dsl.json` 生成
- 不允许跳过条件分支
- 必须体现开始、结束、异常路径
- 跨页面跳转必须带条件说明

### 测试用例

- 必须覆盖正常流程、异常流程、边界条件
- 每个 action 至少生成：
  - 1 条正常用例
  - 1 条失败用例
- 所有 rules 必须在测试用例中至少被覆盖一次

### 接口契约

- 必须优先复用 `inputs/context/` 中已有接口说明
- 若 DSL 中出现接口依赖而 context 未提供完整契约，必须输出待确认项
- 不允许把推断字段伪装成既定接口字段
