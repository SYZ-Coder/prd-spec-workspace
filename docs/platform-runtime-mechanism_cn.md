# 平台运行机制说明

这份文档说明这个工具平台的运行机制：每一步做什么、如何控制、设计亮点是什么、以及后续如何继续优化。

## 1. 平台定位

这个平台不是一个固定业务模板，也不是一个直接替代产品经理和测试的“自动写稿器”。

它更准确的定位是：

- 一个需求结构化中台
- 一个规格生成与衔接中台
- 一个需求上下文标准化平台

它把原始需求输入统一收口到 DSL，再从 DSL 分发到多个下游产物和工具链。

## 2. 总体运行机制

平台运行遵循固定的分层链路：

1. 输入层
2. 抽取层
3. 合并层
4. 校验层
5. 生成层
6. 派生层
7. 归档层
8. 上下文装配层

其核心原则是：

- 先抽取，再校验，再生成
- 先结构化，再面向人和工具输出
- 把事实、推断和待确认项分层
- 把证据和可信度显式暴露，方便人工复核

## 3. 每一步做什么

### Step 1. 输入层

输入位于：

- `inputs/prd/`
- `inputs/screenshots/`
- `inputs/notes/`
- `inputs/context/`

作用：

- 收集原始业务事实
- 收集页面和流程证据
- 收集补充规则和边界条件
- 收集接口、权限、角色等上下文约束

控制点：

- 输入越明确，抽取越稳定
- 不允许把上游生成稿回灌成新一轮 inputs

### Step 2. 抽取层

核心脚本：

- `scripts/extract_initial_dsl.py`

作用：

- 抽取页面
- 抽取动作
- 抽取规则
- 抽取流转
- 抽取依赖
- 输出 unknowns
- 生成证据与可信度摘要

产物：

- `working/raw-dsl.json`
- `working/page-source-map.md`
- `working/transition-map.md`
- `working/shared-rules.md`
- `working/evidence-map.md`
- `working/merged-dsl.json`

控制点：

- 可通过 `extractor-overrides.json` 做领域词扩展
- 抽取策略以“保守优先”为原则，避免乱猜
- 低可信度条目应优先进入人工复核

### Step 3. 校验层

核心脚本：

- `scripts/validate_dsl.py`

作用：

- 检查结构完整性
- 检查页面、动作、流转的一致性
- 检查 unknowns 是否过多
- 检查明显语义风险
- 暴露低可信度结果带来的实施风险

产物：

- `working/validation-report.md`

控制点：

- validation 是硬门槛
- 存在 blocker 时，理论上不应直接进入下游实施

### Step 4. 生成层

核心脚本：

- `scripts/generate_drafts.py`

作用：

- 生成人可评审的需求稿
- 生成 OpenSpec 变更包

产物：

- `working/generated-prd.md`
- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`

控制点：

- 生成必须建立在 merged-dsl 和 validation 基础上
- 这一层的重点是“可评审、可执行”，不是“绝对终稿”

### Step 5. 派生层

核心脚本：

- `scripts/generate_derivatives.py`
- `scripts/render_mermaid_assets.py`

作用：

- 生成流程图文稿
- 生成测试用例
- 生成接口草案
- 生成 OpenAPI 骨架
- 同步到 `outputs/`

产物：

- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `outputs/diagrams/`
- `outputs/testcases/`
- `outputs/contracts/`

控制点：

- 该层偏执行辅助，不应脱离 validation 独立使用

### Step 6. 归档层

核心脚本：

- `scripts/archive_spec.py`

作用：

- 保留本次需求快照
- 提炼可复用知识资产
- 清理活动目录，避免污染下一条需求

产物：

- `knowledge/snapshots/`
- `knowledge/specs/`
- `knowledge/patterns/`
- `knowledge/rules/`
- `knowledge/api/`
- `knowledge/decisions/`

控制点：

- 归档应在需求稳定后执行
- 不应把未确认的 unknowns 当作可复用资产沉淀

### Step 7. 上下文装配层

核心脚本：

- `scripts/select_context.py`
- `scripts/build_context_pack.py`

作用：

- 从历史知识中按需选上下文
- 把当前需求产物组装成可直接复制给下游工具的上下文包

产物：

- `inputs/context/knowledge/...`
- `working/context-pack-openspec.md`
- `working/context-pack-superpowers.md`
- `working/context-pack-ai-development.md`

控制点：

- 强调“按需引入”，避免旧需求污染新需求

## 4. 运行控制方式

平台的控制分为四层。

### 4.1 输入控制

通过 `inputs/` 控制源材料质量。

### 4.2 抽取控制

通过 `extractor-overrides.json` 控制领域词扩展。

### 4.3 流程控制

通过 `run_pipeline.py` 固定执行顺序，避免跳步。

说明：
`run_pipeline.py` 会输出 `pipeline-plan.md`、`input-readiness-report.md` 和终端里的“下一步建议”，这部分文案应保持可读中文，便于团队把它直接当执行单使用。

### 4.4 质量控制

通过 `validate_dsl.py` 和 `tests/` 做结构和行为约束。

## 5. 设计亮点

### 亮点 1：统一 DSL 中间层

这是平台最核心的设计。

好处：

- 不同输入形式都能收口到同一结构
- 下游生成逻辑可以复用
- 便于验证、对比、归档和二次使用

### 亮点 2：先校验，再生成

这比“直接从输入生成终稿”更稳。

好处：

- 可以提前暴露高风险问题
- 可以防止错误直接扩散到 OpenSpec、测试稿和接口稿

### 亮点 3：结构化理解与可信度透明

平台不是只给一个结果，还尽量保留：

- 证据来源
- 可信度摘要
- 低可信度检查项
- 待确认内容

这使得团队可以更快判断：

- 哪些内容可以直接继续执行
- 哪些内容需要补输入或人工确认

### 亮点 4：产物分层清晰

平台把产物分成：

- 结构核心层
- 可评审规格层
- 派生执行层
- 归档与上下文层

这使得不同角色可以只看自己最关心的一层。

### 亮点 5：可扩展而非硬编码

通过：

- `extractor-overrides.json`
- `manage_extractor_overrides.py`

用户可以持续调优抽取器，而不是不断改主代码。

### 亮点 6：可直接衔接下游工具

通过：

- OpenSpec 变更包
- `build_context_pack.py`

平台可以自然接入：

- OpenSpec
- Superpowers
- 通用 AI / 开发 AI

## 6. 当前机制的边界

平台当前不是：

- 无监督终稿机器
- 零人工即可实施的自动需求引擎
- 强语义推理引擎

它更适合：

- 结构化理解需求
- 统一多输入材料
- 生成标准化中间产物
- 为下游工具和人工协作提供稳定上下文

## 7. 后续优化方向

### 优先级 P0

- 继续增强复杂流转语义校验，尤其是相似页面误连问题
- 继续提升证据映射与低可信度项提示的可读性

### 优先级 P1

- 增强 context 直连复用能力，让接口契约优先来自 context
- 增加更多真实需求回归样例，形成长期准确度基线

### 优先级 P2

- 增加截图 / 原型输入的稳定识别基线
- 增加更细粒度的字段级抽取能力
- 增加审批流、工单流、状态机类需求的专项验证

### 优先级 P3

- 为上下文包生成提供更强的参数化模板
- 提供针对不同下游工具的自动推荐打包策略

## 8. 推荐的长期演进方向

如果继续迭代，这个平台最值得坚持的方向不是“补更多硬编码模板”，而是：

- 提升 DSL 质量
- 提升 validation 语义能力
- 提升 context 复用能力
- 提升下游工具衔接能力
- 提升证据映射和可信度表达能力

也就是说，平台应继续朝着“需求结构化中台”发展，而不是回到“特定业务模板脚本”。
