# 团队直接使用清单

这份清单面向直接使用本仓库的产品、测试、研发和 AI 协作者。

目标是把一次需求从“原始材料”推进到“结构化 spec + 派生产物 + 可归档知识”，并尽量减少遗漏和误操作。

## 一次性上线前检查

在团队正式使用本仓库前，建议先完成一次环境和流程自检。

### 仓库基础检查

- [ ] [README.md](./README.md) 可作为新成员入门文档使用
- [ ] [AGENTS.md](../AGENTS.md) 与实际脚本流程一致
- [ ] `prompts/` 目录齐全，关键 prompt 文件存在
- [ ] `schemas/` 中的 DSL schema 可用于约束输出结构

### 核心脚本检查

- [ ] `python scripts/bootstrap_outputs.py --change-name demo --domain account` 可以执行
- [ ] `python scripts/extract_initial_dsl.py --workspace .` 可以生成 DSL 文件
- [ ] `python scripts/validate_dsl.py` 可以输出校验报告
- [ ] `python scripts/run_pipeline.py --change-name demo --domain account --title "示例需求"` 可以生成流程计划
- [ ] `python scripts/render_mermaid_assets.py` 可以同步衍生产物到 `outputs/`
- [ ] `python scripts/archive_spec.py --change-name demo --domain account --title "示例需求"` 可以完成归档

### 文档与扩展检查

- [ ] [extractor-overrides.md](./extractor-overrides.md) 可供使用者自行调优抽取器
- [ ] `python scripts/manage_extractor_overrides.py --show` 可以正常输出当前扩展配置
- [ ] 团队知道如何通过 `extractor-overrides.json` 做词表优化，而不是直接改主逻辑

## 每个需求的执行清单

### 1. 准备输入材料

至少准备以下内容：

- [ ] 把 PRD 或正式需求说明放入 `inputs/prd/`
- [ ] 把截图、原型或流程图放入 `inputs/screenshots/`
- [ ] 把补充说明、边界条件、会议纪要放入 `inputs/notes/`
- [ ] 把接口、权限、上下文约束放入 `inputs/context/`

建议额外确认：

- [ ] 关键页面是否有截图证据
- [ ] 关键流程是否有文字说明或流程图
- [ ] 关键规则是否有明确原文，不只是口头描述
- [ ] 接口和权限是否已有上下文说明

### 2. 初始化本次需求目录

执行：

```bash
python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<需求标题>"
```

检查：

- [ ] `working/pipeline-plan.md` 已生成
- [ ] `working/input-readiness-report.md` 已生成
- [ ] 当前模式识别合理，例如 `prd` / `hybrid` / `image-only`

### 3. 生成并检查 DSL

检查：

- [ ] `working/raw-dsl.json` 已生成
- [ ] `working/merged-dsl.json` 已生成
- [ ] `working/page-source-map.md` 已生成
- [ ] `working/transition-map.md` 已生成
- [ ] `working/shared-rules.md` 已生成

重点人工复核：

- [ ] 页面是否被正确识别，没有全部塌成 `主流程页面`
- [ ] 关键动作是否被正确抽取，没有全变成占位动作
- [ ] 关键规则是否进入 `rules`
- [ ] 关键流转是否在 `transitions` 中体现
- [ ] 不确定信息是否进入 `unknowns`

### 4. 运行校验

执行：

```bash
python scripts/validate_dsl.py
```

检查：

- [ ] `working/validation-report.md` 已生成
- [ ] 没有 blocker
- [ ] 高风险项已人工评估
- [ ] 如果抽取质量不足，优先补输入或调优 overrides，而不是直接跳过 validation

### 5. 生成规格和派生产物

在没有 blocker 的前提下，检查：

- [ ] `working/generated-prd.md` 已生成
- [ ] `openspec/changes/<change-name>/proposal.md` 已生成
- [ ] `openspec/changes/<change-name>/design.md` 已生成
- [ ] `openspec/changes/<change-name>/tasks.md` 已生成
- [ ] `openspec/changes/<change-name>/specs/<domain>/spec.md` 已生成
- [ ] `working/generated-flow.md` 已生成
- [ ] `working/generated-testcases.md` 已生成
- [ ] `working/generated-api-contracts.md` 已生成
- [ ] `working/api-contracts/openapi.yaml` 已生成

### 6. 同步输出目录

执行：

```bash
python scripts/render_mermaid_assets.py
```

检查：

- [ ] `outputs/diagrams/` 中已有流程图产物
- [ ] `outputs/testcases/` 中已有测试用例产物
- [ ] `outputs/contracts/` 中已有接口契约产物

### 7. 归档并清理活动目录

执行：

```bash
python scripts/archive_spec.py --change-name <change-name> --domain <domain> --title "<需求标题>"
```

检查：

- [ ] `knowledge/snapshots/` 中已有本次需求快照
- [ ] `knowledge/specs/` 已写入稳定规格资产
- [ ] `knowledge/patterns/` 已写入可复用模式
- [ ] `knowledge/rules/` 已写入业务规则资产
- [ ] `knowledge/api/` 已写入接口契约资产
- [ ] `knowledge/decisions/` 已写入已确认决策
- [ ] 活动目录已清理，避免污染下一条需求

## 抽取器调优清单

当你发现 DSL 质量不足时，先按这个顺序处理：

### 优先补输入

- [ ] 页面名称是否在 PRD 或截图说明里有明确表达
- [ ] 动作是否写成了可识别的业务动词
- [ ] 规则是否写成了完整句，而不是零散短语
- [ ] 成功/失败流转是否有清晰文字描述

### 再考虑扩展配置

- [ ] 新页面命名方式是否应补到 `page_suffixes`
- [ ] 新动作词是否应补到 `action_prefixes` 或 `standalone_actions`
- [ ] 新规则关键词是否应补到 `rule_keywords`
- [ ] 新规则类型是否应补到 `rule_categories`
- [ ] 新 PRD 标题习惯是否应补到 `section_aliases`

参考文档：

- [Extractor Overrides 使用指南](./extractor-overrides.md)

## 质量门槛建议

可以把下面这些项作为“本次需求可以继续进入实现”的最低标准：

- [ ] 页面主流程可读
- [ ] 关键规则没有明显漏抽
- [ ] 流转没有断链
- [ ] 测试用例覆盖正常路径和异常路径
- [ ] API 草案没有把推断字段伪装成既定事实
- [ ] unknowns 数量在团队可接受范围内

## 常见错误

### 输入过少

常见表现：

- 页面全塌成通用页面
- 动作全是占位表达
- unknowns 过多

### 跳过 validation

常见后果：

- 错误 DSL 直接进入 spec
- 后续测试稿和接口稿一起偏掉

### 用 overrides 代替事实输入

常见后果：

- 抽取结果被配置带偏
- 某次需求的临时词污染后续所有需求

### 不归档直接开始下一条需求

常见后果：

- `working/`、`outputs/`、`inputs/` 旧内容混入下一次识别

## 建议的团队协作方式

- 产品负责补齐 PRD、规则原文和业务背景
- 测试重点检查规则覆盖和异常路径
- 开发重点检查依赖、流转和接口草案
- AI 或工具执行抽取、校验、生成和归档
- 如果抽取偏差重复出现，优先通过 overrides 和测试样例沉淀优化

## 最后确认

在把本仓库作为团队默认入口前，建议至少完成一次完整演练：

- [ ] 从新建输入开始
- [ ] 跑完整条流水线
- [ ] 评审生成结果
- [ ] 归档并清空活动目录
- [ ] 再开始下一条需求，确认没有污染
