# 使用指南

这份文档是 `prd-spec-workspace` 的中文操作引导，帮助团队从一条全新的需求一路走到可复用知识归档。

如果你想先看项目总览，请阅读 [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)。
如果你偏好英文项目介绍，请阅读 [README.md](D:/spring_AI/prd-spec-workspace/README.md)。
如果你需要团队执行清单版本，请阅读 [direct-use-checklist.md](D:/spring_AI/prd-spec-workspace/docs/direct-use-checklist.md)。

## 1. 开始前准备什么

每条需求尽量准备这四类材料：

- `inputs/prd/`
  产品需求文档、方案说明、验收说明、业务描述。
- `inputs/screenshots/`
  页面截图、原型图、弹窗截图、流程截图、UI 证据。
- `inputs/notes/`
  会议纪要、口头补充、边界说明、异常说明、实现提示。
- `inputs/context/`
  接口说明、角色定义、权限规则、技术约束、上下文资料。

最低建议输入：

- 一份 PRD 或等价需求说明
- 一份 notes 补充说明
- 如果存在接口、权限或角色约束，再补一份 context

最佳输入组合：

- `prd + screenshots + notes + context + flow evidence`

## 2. 理解整条流水线

项目按固定顺序运行：

1. Extract
2. Merge
3. Validate
4. Generate drafts
5. Generate derivative outputs
6. Archive reusable knowledge

最重要的规则是：不要跳过 validation。

平台始终遵循两条原则：

- 先做结构化理解，再生成下游规格稿
- 在确认需求可继续之前，先检查证据、可信度和 unknowns

如果校验报告里还有阻断项，先补输入或调抽取配置，不要强行继续生成。

## 3. 开始一条新需求

先确定 `change-name`、`domain` 和标题。

示例：

```bash
python scripts/bootstrap_outputs.py --change-name auth-basic --domain account
```

也可以直接运行完整入口：

```bash
python scripts/run_pipeline.py --change-name auth-basic --domain account --title "基础认证需求"
```

这会完成：

- 初始化输出目录
- 检查当前输入
- 生成 pipeline plan
- 抽取初始 DSL
- 校验 merged DSL
- 在通过校验后生成下游文档

## 4. 截图重要时如何开启 OCR 和组件核对

如果截图或原型是关键证据，建议开启可选视觉增强：

```bash
python scripts/run_pipeline.py --change-name auth-basic --domain account --title "基础认证需求" --enable-vision
```

推荐使用规则：

- 只有当截图真的影响需求理解时，再开启 `--enable-vision`
- 所有截图放在 `inputs/screenshots/`
- 如果你已经有 OCR 文本，最好补同名侧车文件

侧车文件示例：

- `login.png` 对应 `login.ocr.txt`
- `login.png` 对应 `login.ocr.md`
- `login.png` 对应 `login.ocr.json`

开启视觉增强后，优先检查这些中间产物：

- [screenshot-evidence.md](D:/spring_AI/prd-spec-workspace/working/screenshot-evidence.md)
- [screenshot-ocr.json](D:/spring_AI/prd-spec-workspace/working/screenshot-ocr.json)
- [page-classification.json](D:/spring_AI/prd-spec-workspace/working/page-classification.json)

需要注意：

- OCR 结果只是证据，不是最终事实
- 组件核对只增强 Extract，不替代 validation
- 低可信度 OCR 必须人工复核
- 如果本地没有 `tesseract`，平台仍可运行，但没有侧车 OCR 文件时，视觉结果会保持低可信度

## 5. 第一轮先看哪些产物

第一次跑完后，优先检查：

- `working/pipeline-plan.md`
- `working/input-readiness-report.md`
- `working/raw-dsl.json`
- `working/merged-dsl.json`
- `working/validation-report.md`

重点判断：

- 主要页面识别得对不对
- 关键规则有没有进入 `rules`
- 页面流转是否可读
- `unknowns` 会不会太多
- 需求有没有退化成占位页或过度泛化结果
- 如果开启了视觉增强，OCR 和组件核对结果是否真的与截图相符

## 6. 抽取不准时怎么处理

建议按这个顺序修：

### 方案 A. 先补输入材料

这是优先级最高的修法。

常见做法：

- 在 PRD 里补清晰页面名
- 用明确流程句描述，例如 `成功后进入结果页`
- 补接口、权限、角色上下文
- 补失败场景和边界说明
- 如果截图里有关键字段或按钮，补同名侧车 OCR 文件

### 方案 B. 再调 extractor overrides

如果问题主要来自团队自己的领域词汇，可以用 `extractor-overrides.json`。

初始化：

```bash
python scripts/manage_extractor_overrides.py --init
```

查看当前配置：

```bash
python scripts/manage_extractor_overrides.py --show
```

常见示例：

```bash
python scripts/manage_extractor_overrides.py --add-page-suffix 看板
python scripts/manage_extractor_overrides.py --add-action-prefix 导出
python scripts/manage_extractor_overrides.py --add-rule-keyword 实时刷新
python scripts/manage_extractor_overrides.py --add-rule-category 报表规则 --add-category-keyword 实时刷新
```

调整后重新执行：

```bash
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
```

详细说明见：

- [extractor-overrides.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides.md)
- [extractor-overrides_cn.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides_cn.md)

## 7. 如何评审生成稿

当 validation 通过后，继续检查这些文档：

- `working/generated-prd.md`
- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`

建议从三个视角看：

- 产品视角：目标、规则、待确认项是否清晰
- 测试视角：正常流、失败流、边界条件是否覆盖
- 开发视角：依赖、接口、状态变化、歧义是否足够清楚

## 8. 如何发布或交付输出

适合对外分享或沉淀的结果放在：

- `outputs/diagrams/`
- `outputs/testcases/`
- `outputs/contracts/`

`working/` 更像分析工作区，`outputs/` 更像对外交付层。

## 9. 如何归档可复用知识

当需求完成且内容稳定后，执行归档。

示例：

```bash
python scripts/archive_spec.py --change-name auth-basic --domain account --title "基础认证需求"
```

归档应同时保留两类内容：

- 这条需求的完整快照
- 后续需求可复用的知识资产

归档后可以清理当前 `inputs/`、`working/`、`outputs/`，避免污染下一条需求。

## 10. 如何按需复用知识

知识库只有在“按需引入”时才真正有价值。

建议顺序：

1. 先从新需求自己的 inputs 开始
2. 列出已有 knowledge 资产
3. 只选择有帮助的 bundle、asset 或 snapshot
4. 只有在高度相似需求下，才整包引入旧 snapshot

常用命令：

```bash
python scripts/select_context.py --list
python scripts/select_context.py --list --domain account
python scripts/select_context.py --bundle account-core
```

## 11. 推荐团队协作方式

一个比较顺手的分工模式是：

- 产品准备 `inputs/prd/` 和 `inputs/notes/`
- 设计或分析补充截图和流程证据
- 开发补充 `inputs/context/` 中的接口、权限、依赖说明
- 团队先评审 `working/validation-report.md`
- 稳定后再确认下游文档和归档

## 12. 常见错误

尽量避免这些情况：

- 把截图当成完整业务事实
- 因为生成稿“看起来像对的”就跳过 validation
- 把待确认内容藏进规则或页面描述里
- 新需求一次性引入过多历史上下文
- 抽取不准时，只改输出稿，不去修 inputs 或 overrides
- 把 OCR 文本直接当最终事实，不看截图证据和可信度

## 13. 第一次落地建议

如果团队第一次用这个项目，建议：

1. 先选一条真实但范围不大的需求
2. 准备 `prd + notes + context`
3. 如果页面理解依赖截图，再补截图并考虑开启视觉增强
4. 跑完整条流水线
5. 重点检查 `raw-dsl`、`merged-dsl`、`validation-report`
6. 只有词汇问题再调 overrides
7. 团队一起评审 PRD、测试稿、接口草案
8. 评审通过后再归档

这样能先建立一条稳定基线，再逐步扩大到更复杂需求。

## 14. 相关文档

- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [README.md](D:/spring_AI/prd-spec-workspace/README.md)
- [guide.md](D:/spring_AI/prd-spec-workspace/guide.md)
- [direct-use-checklist.md](D:/spring_AI/prd-spec-workspace/docs/direct-use-checklist.md)
- [extractor-overrides.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides.md)
- [extractor-overrides_cn.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides_cn.md)
- [knowledge/index.md](D:/spring_AI/prd-spec-workspace/knowledge/index.md)
- [structured-understanding-confidence_cn.md](D:/spring_AI/prd-spec-workspace/docs/structured-understanding-confidence_cn.md)
- [ocr-extension-guide_cn.md](D:/spring_AI/prd-spec-workspace/docs/ocr-extension-guide_cn.md)
