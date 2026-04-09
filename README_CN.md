# prd-spec-workspace

通用的需求结构化与规格生成工作区，用于把 PRD、截图、备注、上下文等原始材料，转换为结构化 DSL、可评审规格稿、OpenSpec 变更包、Superpowers 输入、测试用例、流程图和接口草案。

English version: [README.md](D:/spring_AI/prd-spec-workspace/README.md)

## 从这里开始

如果你是第一次打开这个仓库，建议先看这些入口：

- [文档中心](D:/spring_AI/prd-spec-workspace/docs/README_CN.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [新需求标准操作 SOP](D:/spring_AI/prd-spec-workspace/docs/new-requirement-sop_cn.md)
- [产物使用说明](D:/spring_AI/prd-spec-workspace/docs/artifact-usage-guide_cn.md)
- [上下文包组装指南](D:/spring_AI/prd-spec-workspace/docs/context-pack-assembly-guide_cn.md)
- [结构化理解与可信度说明](D:/spring_AI/prd-spec-workspace/docs/structured-understanding-confidence_cn.md)
- [inputs/README_CN.md](D:/spring_AI/prd-spec-workspace/inputs/README_CN.md)
- [prompts/README_CN.md](D:/spring_AI/prd-spec-workspace/prompts/README_CN.md)
- [scripts/README_CN.md](D:/spring_AI/prd-spec-workspace/scripts/README_CN.md)
- [tests/README_CN.md](D:/spring_AI/prd-spec-workspace/tests/README_CN.md)
- [examples/README_CN.md](D:/spring_AI/prd-spec-workspace/examples/README_CN.md)

## 项目定位

这个仓库是一个“需求材料 -> 结构化规格”的工具型工作区。

它适合处理以下输入：

- 产品需求文档
- 页面截图或原型
- 会议纪要和补充说明
- 接口、权限、系统上下文
- 流程说明或流程图证据

核心链路是：`原始需求材料 -> DSL -> 校验 -> 规格产物 -> 知识归档`

## 结构化理解与可信度透明

平台强调两件事：

- 把多模态需求材料先统一收口到结构层，而不是直接写终稿
- 把识别结果的证据和可信度一起暴露出来，方便人工复核

这也是平台提升准确度和可信度的关键方式。

## 两种使用方式

### 1. 对话式 AI 使用

当需求是全新的、有歧义的、或者以原型为主时，推荐用这种方式。

推荐流程：

1. 先把材料放入 `inputs/`
2. 先让 AI 按平台规则做结构化识别
3. 先检查页面、动作、规则、流转、依赖和 unknowns
4. 只有在结构层看起来可信时，再进入 Markdown 规格生成

推荐对话说法：

```text
这是一个新需求，请按平台规则先做结构化识别。
先不要直接写终稿。
请先基于 inputs/ 提取页面、动作、规则、流转、依赖、unknowns，
再判断是否可以继续生成规格稿。
```

参考文档：

- [AI 对话式需求识别工作流](D:/spring_AI/prd-spec-workspace/docs/ai-dialogue-requirement-workflow_cn.md)

### 2. 脚本式使用

当输入已经相对完整，并且你希望快速得到稳定的工程化产物时，推荐用这种方式。

推荐流程：

1. 先把材料放入 `inputs/`
2. 执行 `python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<需求标题>"`
3. 先检查 `working/merged-dsl.json` 和 `working/validation-report.md`
4. 再检查下游规格稿和派生产物
5. 稳定后执行归档

这两种方式的区别是：

- 对话式使用更强调 AI 先做识别与判断
- 脚本式使用更强调流程稳定执行
- 但两者都遵循同一个中心思想：先结构化理解，再校验，再生成规格。

## 快速开始

```bash
python scripts/bootstrap_outputs.py --change-name demo-change --domain account
python scripts/run_pipeline.py --change-name demo-change --domain account --title "示例需求"
python scripts/build_context_pack.py --target openspec --change-name demo-change --domain account --title "示例需求"
python scripts/archive_spec.py --change-name demo-change --domain account --title "示例需求"
```

## 文档导航

推荐先从文档中心进入：

- [文档中心](D:/spring_AI/prd-spec-workspace/docs/README_CN.md)
- [项目总手册](D:/spring_AI/prd-spec-workspace/docs/project-handbook_cn.md)
- [产物使用说明](D:/spring_AI/prd-spec-workspace/docs/artifact-usage-guide_cn.md)
- [上下文包组装指南](D:/spring_AI/prd-spec-workspace/docs/context-pack-assembly-guide_cn.md)
- [结构化理解与可信度说明](D:/spring_AI/prd-spec-workspace/docs/structured-understanding-confidence_cn.md)
- [inputs/README_CN.md](D:/spring_AI/prd-spec-workspace/inputs/README_CN.md)
- [prompts/README_CN.md](D:/spring_AI/prd-spec-workspace/prompts/README_CN.md)
- [scripts/README_CN.md](D:/spring_AI/prd-spec-workspace/scripts/README_CN.md)
- [tests/README_CN.md](D:/spring_AI/prd-spec-workspace/tests/README_CN.md)
- [examples/README_CN.md](D:/spring_AI/prd-spec-workspace/examples/README_CN.md)

## 测试

```bash
python -m unittest tests.test_extract_initial_dsl tests.test_manage_extractor_overrides tests.test_validate_dsl tests.test_generate_drafts tests.test_generate_derivatives tests.test_run_pipeline tests.test_archive_spec tests.test_select_context tests.test_build_context_pack tests.test_accuracy_examples -v
```
