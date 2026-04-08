# Contributing

感谢你对 `prd-spec-workspace` 的关注。

这个项目的目标不是做某个固定业务模板，而是持续把“需求材料 -> 结构化 DSL -> spec 产物”的通用链路做得更稳定、更可验证、更可扩展。

## 贡献方向

优先欢迎以下类型的贡献：

- 提升抽取准确度和精度
- 提升 validation 的问题发现能力
- 提升生成稿的可评审性
- 提升 overrides 的可扩展性和可维护性
- 增加跨领域测试样例
- 改进文档、示例和 onboarding 体验

## 开始之前

建议先阅读：

- [README.md](D:/spring_AI/prd-spec-workspace/README.md)
- [AGENTS.md](D:/spring_AI/prd-spec-workspace/AGENTS.md)
- [direct-use-checklist.md](D:/spring_AI/prd-spec-workspace/docs/direct-use-checklist.md)
- [extractor-overrides.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides.md)

## 开发原则

### 1. 保持工具通用性

不要把某一个业务域的页面、动作或流程硬编码成默认逻辑，除非它已经被设计成可配置、可扩展、可关闭的能力。

### 2. 保守优于乱猜

抽取器宁可少抽、留在 `unknowns`，也不要把不确定内容写成既定事实。

### 3. 先验证，再生成

任何影响 DSL 结构的改动，都应兼顾：

- 抽取是否更准确
- validation 是否仍然可信
- 下游生成稿是否仍然可读

### 4. 优先沉淀为测试和配置

如果某次修复只靠“这次记住了”，那它很快还会再坏。

优先把经验沉淀为：

- 回归测试
- 覆盖样例
- overrides 能力
- 文档说明

## 提交流程建议

1. 明确问题场景或目标改进点。
2. 先补测试或样例，证明当前行为不足。
3. 实现最小修复。
4. 跑回归。
5. 更新相关文档。

## 本地验证

提交前建议至少执行：

```bash
python -m unittest tests.test_extract_initial_dsl tests.test_manage_extractor_overrides tests.test_validate_dsl tests.test_generate_drafts tests.test_generate_derivatives tests.test_run_pipeline tests.test_archive_spec tests.test_select_context -v
```

如果改动涉及文档扩展配置，也建议手动检查：

```bash
python scripts/manage_extractor_overrides.py --show
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
```

## Issue 建议

提 issue 时，尽量提供：

- 原始输入片段
- 当前输出片段
- 预期输出
- 是否属于通用问题还是特定领域词汇问题
- 如果是词汇问题，是否可以通过 overrides 解决

## Pull Request 建议

PR 描述建议包含：

- 解决的问题
- 关键改动点
- 新增或修改的测试
- 是否影响 DSL schema、validation 或下游文稿
- 是否需要补文档

## 不建议的改动方式

- 直接为某一个业务需求写死固定页面图
- 跳过 validation 让生成链继续跑
- 用 overrides 写入一次性临时事实
- 为了某个样例通过而破坏通用性

## 文档贡献

文档同样是高价值贡献，尤其欢迎：

- 新用户上手路径优化
- 示例补充
- 常见问题整理
- 多语言文档
- 开源协作说明
