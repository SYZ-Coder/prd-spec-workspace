# Prompts 使用说明

`prompts/` 存放的是这条“需求材料 -> 规格产物”流水线按阶段划分的提示文档。

这些 prompt 文件不是某个产品领域的模板，而是用于抽取、合并、校验、生成和归档等阶段的执行说明。

## 如何理解这个目录

可以把这些 prompts 看成工作流积木：

- 它们说明每个阶段应该产出什么
- 它们提醒代理区分事实、结构化推断和 unknowns
- 它们帮助流水线在文本、图片和混合输入场景下保持一致

这些 prompts 应当保持通用、可复用，而不是演变成硬编码业务脚本。

## 各 prompt 文件说明

### `00_classify_pages.md`
用于图片占比较高的场景。

重点：

- 先识别组件
- 再识别页面类型
- 再推断交互模式
- 避免直接跳到业务结论

典型输出：

- `working/page-classification.json`

### `01_extract_dsl.md`
用于存在 PRD 或文本材料的场景。

重点：

- 从文本证据中抽取页面、动作、规则、依赖和 unknowns
- 把事实和结构化推断分层

### `02_extract_dsl_image.md`
用于截图或原型是主要证据源的场景。

重点：

- 把视觉证据转换成临时 DSL 输入
- 当业务语义不明确时保持保守

### `03_merge_logic.md`
用于初始抽取之后。

重点：

- 合并重复页面
- 合并共享规则和依赖
- 对齐跨页面流转
- 输出可继续使用的 merged DSL

典型输出：

- `working/transition-map.md`
- `working/shared-rules.md`
- `working/merged-dsl.json`

### `04_infer_flow.md`
主要用于图片驱动或碎片化输入场景。

重点：

- 根据页面关系推断可能的流程证据
- 支持 merge 和 validation
- 不替代最终 merge 步骤

### `05_validate_spec.md`
用于任何下游生成之前。

重点：

- 检查完整性、一致性和可执行性
- 标出 blocker 和高风险 unknowns
- 确保结构坏掉时不继续生成

典型输出：

- `working/validation-report.md`

### `06_generate_openspec.md`
用于 merged DSL 已通过校验之后。

重点：

- 生成人可评审的 Markdown 需求稿
- 生成 OpenSpec proposal、design、tasks 和 spec 文件

### `07_generate_mermaid.md`
用于基于 merged DSL 生成图表输出。

重点：

- 保留分支条件
- 显示开始、结束和异常路径
- 让跨页面条件保持显式

### `08_generate_testcases.md`
用于根据 DSL 和规则生成测试覆盖。

重点：

- 覆盖正常流、失败流和边界条件
- 确保每条规则至少被覆盖一次
- 确保每个 action 至少有一条成功用例和一条失败用例

### `09_generate_api_contracts.md`
用于生成接口草案和 OpenAPI 骨架。

重点：

- 优先复用 `inputs/context/` 中已有说明
- 区分推断契约和已确认契约
- 缺失 schema 时进入 unknowns，而不是编造事实

### `10_archive_knowledge.md`
用于需求稳定并可复用之后。

重点：

- 总结可复用资产
- 区分一次性上下文和未来知识
- 支持 `knowledge/` 的整理和归档流程

## 使用原则

1. 遵循固定顺序：Extract、Merge、Validate、Generate、Derivative Outputs、Archive。
2. 保持事实、结构化推断和 unknowns 分层。
3. 不要把 unknowns 变成已确认事实。
4. 不要让 prompts 退化成硬编码业务脚本。
5. prompt 文案要和最新 DSL schema、归档模型、结构化理解原则保持一致。

## 什么时候需要更新这些 prompts

当出现这些变化时，应回看这个目录：

- DSL schema 变化
- validation 规则变化
- 输出产物变化
- archive 模型变化
- 图片处理或上下文选择流程变化

当 prompt 行为变化时，也要同步检查这些文件：

- [README.md](D:/spring_AI/prd-spec-workspace/README.md)
- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [guide.md](D:/spring_AI/prd-spec-workspace/guide.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [docs/README_CN.md](D:/spring_AI/prd-spec-workspace/docs/README_CN.md)
- [structured-understanding-confidence_cn.md](D:/spring_AI/prd-spec-workspace/docs/structured-understanding-confidence_cn.md)
- [knowledge/index.md](D:/spring_AI/prd-spec-workspace/knowledge/index.md)

## 相关文档

- [README.md](D:/spring_AI/prd-spec-workspace/README.md)
- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [guide.md](D:/spring_AI/prd-spec-workspace/guide.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [docs/README_CN.md](D:/spring_AI/prd-spec-workspace/docs/README_CN.md)
- [structured-understanding-confidence_cn.md](D:/spring_AI/prd-spec-workspace/docs/structured-understanding-confidence_cn.md)
- [inputs/README.md](D:/spring_AI/prd-spec-workspace/inputs/README.md)
- [knowledge/index.md](D:/spring_AI/prd-spec-workspace/knowledge/index.md)
