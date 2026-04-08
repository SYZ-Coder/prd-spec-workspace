# 项目总手册

这份文档面向第一次接触 `prd-spec-workspace` 的使用者，也面向后续维护这个仓库的产品、测试、研发和 AI 协作者。

目标是回答四类问题：

- 这个项目是做什么的
- 一条需求应该怎么开始、怎么推进、怎么归档
- 使用这个项目时有哪些高价值技巧和注意事项
- 仓库里每个关键目录、每个关键文件分别负责什么

说明边界：

- 本文覆盖仓库中的人工维护文件和核心工程目录
- 对 `.git/objects/`、`__pycache__/`、IDE 缓存等自动生成内容不逐文件展开
- `working/`、`outputs/`、`openspec/changes/`、`knowledge/snapshots/` 属于运行期或归档期产物，内容会随每条需求变化

## 1. 项目定位

`prd-spec-workspace` 是一个通用的“需求材料 -> 结构化规格”工作区。

它不是某个固定业务模板，也不是只适配某个行业的脚本集合。它更像一套规范化流水线，用来把以下原始输入：

- PRD
- 会议纪要
- 页面截图或原型图
- 流程图
- 接口说明
- 权限和角色上下文

转换为一组可评审、可实现、可归档的标准化产物，例如：

- DSL 中间结构
- 校验报告
- Markdown 需求稿
- OpenSpec 变更包
- Mermaid 流程图
- 测试用例
- 接口契约草案
- OpenAPI 骨架
- 可复用知识资产

## 2. 适用场景

适合使用这个项目的场景包括：

- 团队希望在开发前先把需求理解结构化
- 一个需求来自多种材料，人工整理成本高
- 团队想区分“已确认事实 / 结构化推断 / 待确认项”
- 希望从同一份需求上下文生成多个下游产物
- 希望保留历史需求上下文，并支持下一次需求按需复用
- 希望让 AI 协作者基于更稳定的 DSL 和文档工作

## 3. 一条需求怎么开始

建议按下面的顺序开始一条新需求。

### Step 1. 准备输入材料

将材料放入这些目录：

- `inputs/prd/`：PRD、方案、验收说明
- `inputs/screenshots/`：截图、原型、弹窗、流程截图
- `inputs/notes/`：会议纪要、边界说明、补充规则
- `inputs/context/`：接口说明、权限规则、技术上下文

最低建议：

- 一份 PRD 或等价文本说明
- 一份 notes 补充说明
- 如果存在接口/权限依赖，再补一份 context

### Step 2. 初始化工作区并运行流水线

推荐直接运行：

```bash
python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<需求标题>"
```

这会帮助你完成：

- 初始化本次需求所需的输出目录
- 检查 `inputs/` 的可用性
- 生成 `pipeline-plan.md`
- 抽取 DSL
- 校验 DSL
- 在校验通过后继续生成下游规格和派生产物

### Step 3. 优先检查中间产物

第一次运行后，优先看：

- `working/input-readiness-report.md`
- `working/pipeline-plan.md`
- `working/raw-dsl.json`
- `working/merged-dsl.json`
- `working/validation-report.md`

重点确认：

- 页面是否识别合理
- 关键规则是否进入 `rules`
- 流转是否完整
- `unknowns` 是否足够显式
- 是否出现明显占位页、占位动作或误判

### Step 4. 评审规格和派生产物

如果 `validation-report.md` 没有 blocker，再检查：

- `working/generated-prd.md`
- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`

### Step 5. 归档稳定需求

当本次需求完成并且产物稳定后，执行：

```bash
python scripts/archive_spec.py --change-name <change-name> --domain <domain> --title "<需求标题>"
```

归档后，项目会把可复用知识沉淀到 `knowledge/`，并把本次上下文保留为快照，供后续按需引用。

## 4. 使用技巧

### 4.1 优先补输入，不要先改输出稿

如果抽取效果不好，优先修：

- PRD 的页面命名
- 流程句的表达清晰度
- 备注中的异常流程
- context 里的接口和权限信息

不要一开始就去手改生成稿，否则问题只会被藏起来。

### 4.2 抽取器扩展优先用配置，不要直接改主逻辑

如果问题来自你们团队的专业词汇，优先使用：

```bash
python scripts/manage_extractor_overrides.py --init
python scripts/manage_extractor_overrides.py --show
```

然后通过 `extractor-overrides.json` 扩展：

- 页面后缀
- 动作前缀
- 规则关键词
- 规则分类
- 章节别名

### 4.3 不要把旧需求整包灌回新需求

知识库复用应当是“按需引入”，不是“全部复制”。

优先使用：

```bash
python scripts/select_context.py --list
python scripts/select_context.py --bundle <bundle-name>
python scripts/select_context.py --change-name <change-name> --include-snapshot
```

### 4.4 Validation 是硬门槛

只要 `working/validation-report.md` 里还有 blocker，就不应把生成稿当成可交付规格。

### 4.5 截图只能提供证据，不能替代业务事实

截图适合提供：

- 页面结构
- 可见组件
- UI 状态
- 页面之间的弱流程线索

截图不适合单独定义：

- 完整业务规则
- 权限策略
- 接口字段语义
- 异常处理原则

## 5. 推荐的团队使用方式

一种比较稳的协作方式是：

- 产品负责 `inputs/prd/` 和 `inputs/notes/`
- 设计或分析补 `inputs/screenshots/`
- 开发补 `inputs/context/`
- 团队先看 `validation-report.md`
- 再一起评审 PRD、测试稿、接口草案
- 稳定后执行归档

## 6. 目录总览

### 核心目录

- `scripts/`：核心脚本实现
- `prompts/`：各阶段提示文档
- `inputs/`：需求原始输入入口
- `working/`：分析过程中的中间产物
- `outputs/`：适合对外分享的派生产物
- `openspec/`：OpenSpec 配置和变更包
- `knowledge/`：归档知识和历史快照
- `tests/`：回归测试
- `docs/`：用户文档和使用说明
- `examples/`：示例需求
- `schemas/`：结构约束定义

### 支撑目录

- `.github/ISSUE_TEMPLATE/`：issue 模板
- `.codex/`：Codex 技能支持文件
- `.amazonq/`：Amazon Q 技能/提示支持文件
- `.idea/`：本地 IDE 配置
- `.git/`：Git 仓库元数据

## 7. 逐目录与逐文件说明

### 7.1 仓库根目录文件

| 路径 | 作用 |
| --- | --- |
| `README.md` | 英文项目主页，介绍项目定位、流程、命令、文档入口。 |
| `README_CN.md` | 中文项目主页，适合中文团队快速入门。 |
| `guide.md` | 英文操作指南，偏“如何使用”。 |
| `GUIDE_CN.md` | 中文操作指南，偏“如何开始一条需求并推进”。 |
| `AGENTS.md` | 面向 AI 代理的强约束执行说明，定义标准产物、固定流程、禁止事项、DSL 字段要求。 |
| `CHANGELOG.md` | 项目功能、文档和结构的变更记录。 |
| `CONTRIBUTING.md` | 贡献说明，帮助外部贡献者理解怎么提 issue 和改动。 |
| `LICENSE` | 开源许可证。 |

### 7.2 `docs/`

| 路径 | 作用 |
| --- | --- |
| `docs/direct-use-checklist.md` | 团队落地执行清单，适合作为上线前和每次需求执行时的 checklist。 |
| `docs/extractor-overrides.md` | 英文版抽取器扩展说明。 |
| `docs/extractor-overrides_cn.md` | 中文版抽取器扩展说明。 |
| `docs/project-handbook_cn.md` | 本文档，作为项目总手册、索引和使用说明。 |

### 7.3 `inputs/`

| 路径 | 作用 |
| --- | --- |
| `inputs/README.md` | 说明输入目录如何使用、应放什么材料、输入质量怎么把控。 |
| `inputs/prd/` | 放 PRD、需求说明、业务描述。 |
| `inputs/screenshots/` | 放截图、原型、流程图截图。 |
| `inputs/notes/` | 放会议纪要、边界条件、异常说明。 |
| `inputs/context/` | 放接口文档、权限规则、上下文资料。 |

### 7.4 `prompts/`

| 路径 | 作用 |
| --- | --- |
| `prompts/README.md` | 说明 prompts 目录在整条流水线中的角色。 |
| `prompts/00_classify_pages.md` | 在图片场景下先做页面分类。 |
| `prompts/01_extract_dsl.md` | 基于文本/PRD 抽取初始 DSL。 |
| `prompts/02_extract_dsl_image.md` | 基于图片/原型抽取初始 DSL。 |
| `prompts/03_merge_logic.md` | 合并跨页面逻辑、共享规则、依赖和流转。 |
| `prompts/04_infer_flow.md` | 在视觉证据较多时推断流程线索。 |
| `prompts/05_validate_spec.md` | 指导生成校验报告。 |
| `prompts/06_generate_openspec.md` | 指导生成 OpenSpec 变更包和需求稿。 |
| `prompts/07_generate_mermaid.md` | 指导生成 Mermaid 流程图。 |
| `prompts/08_generate_testcases.md` | 指导生成测试用例。 |
| `prompts/09_generate_api_contracts.md` | 指导生成接口草案和 OpenAPI 骨架。 |
| `prompts/10_archive_knowledge.md` | 指导生成知识归档相关内容。 |

### 7.5 `scripts/`

| 路径 | 作用 |
| --- | --- |
| `scripts/__init__.py` | 让 `scripts` 可作为 Python 包被测试和其他模块导入。 |
| `scripts/bootstrap_outputs.py` | 初始化本次需求所需的目录和基础输出结构。 |
| `scripts/extract_initial_dsl.py` | 从 `inputs/` 中抽取页面、动作、规则、流转、依赖和 unknowns，生成初始 DSL。 |
| `scripts/validate_dsl.py` | 校验 DSL 的完整性、一致性和语义质量，输出 `validation-report.md`。 |
| `scripts/generate_drafts.py` | 基于通过校验的 DSL 生成 Markdown 需求稿和 OpenSpec 变更包。 |
| `scripts/generate_derivatives.py` | 生成流程图文稿、测试用例、接口契约草案和 OpenAPI 文件。 |
| `scripts/render_mermaid_assets.py` | 将派生产物同步整理到 `outputs/`，便于对外分享。 |
| `scripts/archive_spec.py` | 将稳定需求归档到 `knowledge/`，并保留快照与可复用资产。 |
| `scripts/select_context.py` | 从 `knowledge/` 中按需选择 bundle、asset 或 snapshot，装配到新需求上下文。 |
| `scripts/manage_extractor_overrides.py` | 初始化和维护 `extractor-overrides.json`，让用户自己扩展抽取器词表。 |
| `scripts/run_pipeline.py` | 项目主入口脚本，串联 bootstrap、extract、validate、generate、sync 等步骤。 |

### 7.6 `tests/`

| 路径 | 作用 |
| --- | --- |
| `tests/test_extract_initial_dsl.py` | 覆盖 DSL 抽取逻辑和用户 overrides 行为。 |
| `tests/test_validate_dsl.py` | 覆盖 DSL 校验和语义质量检查。 |
| `tests/test_generate_drafts.py` | 覆盖需求稿和 OpenSpec 产物生成。 |
| `tests/test_generate_derivatives.py` | 覆盖流程图、测试稿、接口草案生成。 |
| `tests/test_run_pipeline.py` | 覆盖 `pipeline-plan.md` 等入口输出行为。 |
| `tests/test_archive_spec.py` | 覆盖归档行为和快照/资产沉淀。 |
| `tests/test_select_context.py` | 覆盖知识按需引入能力。 |
| `tests/test_manage_extractor_overrides.py` | 覆盖抽取器扩展配置管理逻辑。 |

### 7.7 `examples/`

| 路径 | 作用 |
| --- | --- |
| `examples/README.md` | 示例目录入口，说明各个示例的用途。 |
| `examples/auth-basic/README.md` | 登录认证类需求示例。 |
| `examples/payment-refund/README.md` | 支付退款类需求示例。 |
| `examples/reporting-dashboard/README.md` | 报表看板类需求示例。 |

### 7.8 `knowledge/`

| 路径 | 作用 |
| --- | --- |
| `knowledge/index.md` | 知识库说明，解释 snapshots、assets、bundles、catalog 的角色。 |
| `knowledge/specs/.gitkeep` | 保持 `specs/` 目录存在，用于存放可复用规格资产。 |
| `knowledge/rules/.gitkeep` | 保持 `rules/` 目录存在，用于存放可复用规则资产。 |
| `knowledge/patterns/.gitkeep` | 保持 `patterns/` 目录存在，用于存放可复用流程或交互模式。 |
| `knowledge/api/.gitkeep` | 保持 `api/` 目录存在，用于存放接口契约和接口上下文。 |
| `knowledge/decisions/.gitkeep` | 保持 `decisions/` 目录存在，用于存放已确认的历史决策。 |

补充说明：

- `knowledge/snapshots/` 是历史需求快照目录，运行归档后自动出现具体需求子目录
- `knowledge/assets/`、`knowledge/bundles/`、`knowledge/catalog.json` 也是归档与上下文选择机制的一部分，可能在运行后生成或更新

### 7.9 `openspec/`

| 路径 | 作用 |
| --- | --- |
| `openspec/config.yaml` | OpenSpec 的基础配置。 |
| `openspec/changes/` | 每条需求的 OpenSpec 变更包输出目录，运行时按 `change-name` 生成。 |

### 7.10 `schemas/`

| 路径 | 作用 |
| --- | --- |
| `schemas/prd-dsl.schema.json` | DSL 的结构约束定义，可用于检查顶层字段和结构完整性。 |

### 7.11 `.github/ISSUE_TEMPLATE/`

| 路径 | 作用 |
| --- | --- |
| `.github/ISSUE_TEMPLATE/bug_report.md` | 缺陷反馈模板。 |
| `.github/ISSUE_TEMPLATE/feature_request.md` | 功能需求模板。 |

### 7.12 Agent / IDE / 仓库支撑文件

| 路径 | 作用 |
| --- | --- |
| `.codex/skills/openspec-propose/SKILL.md` | Codex 的 OpenSpec 提案技能说明。 |
| `.codex/skills/openspec-explore/SKILL.md` | Codex 的需求探索技能说明。 |
| `.codex/skills/openspec-archive-change/SKILL.md` | Codex 的归档技能说明。 |
| `.codex/skills/openspec-apply-change/SKILL.md` | Codex 的 OpenSpec 执行技能说明。 |
| `.amazonq/skills/openspec-propose/SKILL.md` | Amazon Q 对应的 OpenSpec 提案技能说明。 |
| `.amazonq/skills/openspec-explore/SKILL.md` | Amazon Q 对应的探索技能说明。 |
| `.amazonq/skills/openspec-archive-change/SKILL.md` | Amazon Q 对应的归档技能说明。 |
| `.amazonq/skills/openspec-apply-change/SKILL.md` | Amazon Q 对应的执行技能说明。 |
| `.amazonq/prompts/opsx-propose.md` | Amazon Q 的提案提示模板。 |
| `.amazonq/prompts/opsx-explore.md` | Amazon Q 的探索提示模板。 |
| `.amazonq/prompts/opsx-archive.md` | Amazon Q 的归档提示模板。 |
| `.amazonq/prompts/opsx-apply.md` | Amazon Q 的执行提示模板。 |
| `.idea/*` | 本地 IDE 配置，仅服务于开发环境，不参与产品流水线。 |
| `.git/*` | Git 仓库元数据，不属于需求分析逻辑本身。 |

## 8. 新成员最推荐的阅读顺序

如果你是第一次接触这个仓库，建议按这个顺序阅读：

1. [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
2. [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
3. [docs/direct-use-checklist.md](D:/spring_AI/prd-spec-workspace/docs/direct-use-checklist.md)
4. [inputs/README.md](D:/spring_AI/prd-spec-workspace/inputs/README.md)
5. [prompts/README.md](D:/spring_AI/prd-spec-workspace/prompts/README.md)
6. [knowledge/index.md](D:/spring_AI/prd-spec-workspace/knowledge/index.md)
7. [docs/extractor-overrides_cn.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides_cn.md)

## 9. 最常用命令

```bash
python scripts/bootstrap_outputs.py --change-name demo-change --domain account
python scripts/run_pipeline.py --change-name demo-change --domain account --title "示例需求"
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
python scripts/render_mermaid_assets.py
python scripts/archive_spec.py --change-name demo-change --domain account --title "示例需求"
python scripts/select_context.py --list
python scripts/manage_extractor_overrides.py --show
```

## 10. 常见误区

- 把生成稿当作事实源，而不是把 `merged-dsl.json` 当作核心中间层
- 跳过 validation，直接评审生成稿
- 输入材料太少，却期望抽取器自动补齐业务真相
- 把旧需求快照整包塞回新需求，导致上下文污染
- 遇到领域词汇缺口时，直接改主逻辑而不是先用 overrides

## 11. 维护建议

当项目功能发生变化时，建议一起检查这些文档是否需要同步更新：

- [README.md](D:/spring_AI/prd-spec-workspace/README.md)
- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [guide.md](D:/spring_AI/prd-spec-workspace/guide.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [docs/direct-use-checklist.md](D:/spring_AI/prd-spec-workspace/docs/direct-use-checklist.md)
- [knowledge/index.md](D:/spring_AI/prd-spec-workspace/knowledge/index.md)
- [inputs/README.md](D:/spring_AI/prd-spec-workspace/inputs/README.md)
- [prompts/README.md](D:/spring_AI/prd-spec-workspace/prompts/README.md)

这能保证“项目主页、操作指南、目录说明、知识体系说明”始终是同一套口径。
