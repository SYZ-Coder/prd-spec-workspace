# 产物使用说明

这份文档回答一个核心问题：

最终生成的产物，哪些可以直接作为 `OpenSpec` 的执行输入，哪些更适合喂给 `Superpowers`，哪些适合作为通用 AI 的开发上下文。

结论先说：

- 可以喂给 `OpenSpec`，但优先使用 `openspec/changes/<change-name>/` 下的变更包，而不是只给原始 DSL。
- 可以喂给 `Superpowers`，但最好按技能场景组合产物，而不是单独丢一个文件。
- 可以喂给通用 AI，且非常适合作为需求开发上下文，但必须明确哪些文件是事实层，哪些文件是推断层，哪些文件包含待确认项。

## 1. 先理解产物分层

本项目的产物不是一个层级，而是三层。

### 第一层：结构核心层

这些文件最接近“统一事实骨架 + 结构化推断”：

- `working/raw-dsl.json`
- `working/merged-dsl.json`
- `working/validation-report.md`

用途：

- 让 AI 或工具理解需求的结构化核心
- 做调试、校验、问题定位
- 为下游规格和派生产物提供事实骨架

### 第二层：可评审规格层

这些文件最适合让产品、测试、研发共同评审：

- `working/generated-prd.md`
- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`

用途：

- 做规格评审
- 做实现前对齐
- 直接进入变更执行链路

### 第三层：派生执行层

这些文件更偏实现、测试和接口协作：

- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `outputs/diagrams/`
- `outputs/testcases/`
- `outputs/contracts/`

用途：

- 测试设计
- 接口联调
- 开发任务拆解
- 直接给 AI 作为开发上下文补充

## 2. 哪些产物最适合喂给 OpenSpec

### 可以直接使用的核心输入

优先级最高的是：

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`

原因：

- 它们已经是 OpenSpec 风格的变更包
- 更适合继续做执行计划、任务分解和实施追踪
- 比直接喂 `raw-dsl.json` 更接近实现语义

### 建议额外一起提供的辅助输入

为了提高执行计划质量，建议一起给：

- `working/merged-dsl.json`
- `working/validation-report.md`
- `working/generated-api-contracts.md`
- `working/generated-testcases.md`

作用：

- `merged-dsl.json` 提供统一结构骨架
- `validation-report.md` 告诉 OpenSpec 还有哪些风险或 unknowns
- `generated-api-contracts.md` 帮助识别接口依赖
- `generated-testcases.md` 帮助任务拆分时兼顾验收路径

### 不建议只给 OpenSpec 的文件

不建议只给：

- `raw-dsl.json`
- 纯截图
- 只有 `generated-flow.md`

原因：

- `raw-dsl.json` 过于底层，未完成合并和校验
- 截图不具备稳定的结构化语义
- 仅有流程图不足以支撑完整执行计划

### 适合 OpenSpec 的最小输入包

最小推荐组合：

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/validation-report.md`

## 3. 哪些产物最适合喂给 Superpowers

`Superpowers` 的使用方式更依赖当前要调用的技能，因此建议按场景组合。

### 场景 A：继续做需求澄清 / 设计

适合提供：

- `working/generated-prd.md`
- `working/merged-dsl.json`
- `working/validation-report.md`
- `working/generated-flow.md`

为什么：

- `generated-prd.md` 适合人读和对齐
- `merged-dsl.json` 提供底层结构
- `validation-report.md` 直接暴露风险和待确认项
- `generated-flow.md` 帮助快速理解主流程和异常路径

### 场景 B：继续做实现计划 / 任务拆解

适合提供：

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`

为什么：

- OpenSpec 变更包更接近计划和执行语言
- 测试稿帮助定义验收边界
- 接口草案帮助识别依赖和并行工作面

### 场景 C：直接准备进入实现

适合提供：

- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/generated-testcases.md`
- `working/validation-report.md`

为什么：

- `spec.md` 是实现范围主说明
- `api` 和 `openapi` 让实现边界更清晰
- `testcases` 可以直接转成验收与回归参考
- `validation-report.md` 避免在存在 blocker 时误入实施

### 不建议只给 Superpowers 的文件

不建议只给：

- 单一流程图
- 单一截图集
- 没有经过 validation 的 DSL

## 4. 哪些产物最适合直接喂给通用 AI

这里的“通用 AI”包括：

- 通用大模型聊天助手
- 内部研发 AI 平台
- 代码生成 AI
- 测试设计 AI

### 最适合直接复制给 AI 的组合

如果目标是“让 AI 快速开始需求开发”，推荐组合：

- `working/generated-prd.md`
- `working/generated-flow.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/generated-testcases.md`
- `working/validation-report.md`

这是最平衡的一组，因为它同时覆盖：

- 需求说明
- 流程理解
- 接口依赖
- 验收逻辑
- 风险和待确认项

### 如果 AI 需要更结构化理解

再补：

- `working/merged-dsl.json`

适用场景：

- 需要让 AI 做结构化分析
- 需要让 AI 继续生成其他规格或代码框架
- 需要让 AI 对页面、动作、流转、规则进行程序化处理

### 不建议直接只给 AI 的内容

不建议只给：

- 截图
- `raw-dsl.json`
- 单独的 `tasks.md`

因为：

- 截图过于依赖视觉猜测
- `raw-dsl.json` 尚未合并和校验
- 单独 `tasks.md` 会丢失大量上下文边界

## 5. 按使用目标的目录区分

为了让使用者一眼看出该复制什么，本仓库在 `docs/usage-targets/` 下提供了按目标工具区分的说明目录：

- [README_CN.md](D:/spring_AI/prd-spec-workspace/docs/usage-targets/README_CN.md)
- [OpenSpec](D:/spring_AI/prd-spec-workspace/docs/usage-targets/openspec/README_CN.md)
- [Superpowers](D:/spring_AI/prd-spec-workspace/docs/usage-targets/superpowers/README_CN.md)
- [AI Development](D:/spring_AI/prd-spec-workspace/docs/usage-targets/ai-development/README_CN.md)

用户可以直接按目标目录查“复制哪些文件最合适”。

## 6. 实际推荐的复制策略

### 给 OpenSpec

复制：

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/validation-report.md`

### 给 Superpowers

复制：

- OpenSpec 变更包
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/generated-flow.md`
- `working/validation-report.md`

### 给通用 AI

复制：

- `working/generated-prd.md`
- `working/generated-flow.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/generated-testcases.md`
- `working/validation-report.md`
- 必要时补 `working/merged-dsl.json`

## 7. 最关键的注意事项

- `validation-report.md` 很重要，建议总是一起提供
- `merged-dsl.json` 比 `raw-dsl.json` 更适合作为结构化输入
- 纯截图不应作为任何执行工具的唯一输入
- 若产物里还有明显 unknowns，不要把它们当作既定事实继续传播
- 进入执行前，应优先使用 OpenSpec 变更包而不是只依赖需求稿

## 8. 相关文档

- [new-requirement-sop_cn.md](D:/spring_AI/prd-spec-workspace/docs/new-requirement-sop_cn.md)
- [project-handbook_cn.md](D:/spring_AI/prd-spec-workspace/docs/project-handbook_cn.md)
- [scripts/README_CN.md](D:/spring_AI/prd-spec-workspace/scripts/README_CN.md)
- [tests/README_CN.md](D:/spring_AI/prd-spec-workspace/tests/README_CN.md)
- [usage-targets/README_CN.md](D:/spring_AI/prd-spec-workspace/docs/usage-targets/README_CN.md)
- [context-pack-templates/README_CN.md](D:/spring_AI/prd-spec-workspace/docs/context-pack-templates/README_CN.md)
- [context-pack-templates/examples/README_CN.md](D:/spring_AI/prd-spec-workspace/docs/context-pack-templates/examples/README_CN.md)
- [context-pack-assembly-guide_cn.md](D:/spring_AI/prd-spec-workspace/docs/context-pack-assembly-guide_cn.md)
