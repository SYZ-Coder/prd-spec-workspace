# Tests 目录说明

`tests/` 是本项目的回归测试目录，用于保护这条“需求材料 -> DSL -> 校验 -> 规格产物 -> 知识归档”流水线在持续演进时仍然可用。

这些测试重点验证：

- 通用需求抽取能力是否仍然成立
- 校验是否还能拦住高风险结构问题
- 规格稿和派生产物是否还能正确生成
- 流水线入口输出是否仍然可读
- 知识归档和上下文复用是否没有退化
- 用户自定义抽取扩展是否仍然生效
- 上下文包是否还能正确生成给下游工具使用
- 证据映射和可信度表达是否仍然稳定

## 这些测试在保护什么

整套测试和平台的统一原则保持一致：

- 结构化理解能力不能退化成固定业务模板
- evidence / confidence / unknowns 的表达不能悄悄消失
- operator-facing 输出必须保持可读
- 下游上下文包必须继续可组装、可复制、可交接

## 如何运行测试

运行当前核心回归集合：

```bash
python -m unittest tests.test_extract_initial_dsl tests.test_manage_extractor_overrides tests.test_validate_dsl tests.test_generate_drafts tests.test_generate_derivatives tests.test_run_pipeline tests.test_archive_spec tests.test_select_context tests.test_build_context_pack tests.test_accuracy_examples -v
```

运行单个模块：

```bash
python -m unittest tests.test_run_pipeline -v
```

## 各文件作用与保护点

| 文件 | 作用 | 主要保护什么 |
| --- | --- | --- |
| `test_extract_initial_dsl.py` | 测试通用 DSL 抽取逻辑。 | 防止页面、动作、规则、流转抽取、证据映射、可信度摘要和 overrides 行为回退。 |
| `test_manage_extractor_overrides.py` | 测试抽取器扩展配置管理脚本。 | 确保用户可以初始化和追加配置，而不破坏已有行为。 |
| `test_validate_dsl.py` | 测试 DSL 校验和语义质量检查。 | 防止 blocker、高风险项、低可信度风险提示和语义检查退化。 |
| `test_generate_drafts.py` | 测试需求稿和 OpenSpec 草案生成。 | 确保 merged DSL 仍能生成可用的规格稿。 |
| `test_generate_derivatives.py` | 测试流程图、测试稿、接口草案生成。 | 保护下游派生产物不会因 DSL 变化失效。 |
| `test_run_pipeline.py` | 测试主入口编排行为。 | 确保 pipeline plan、下一步建议等操作指引仍然可读且流程顺序正确。 |
| `test_archive_spec.py` | 测试归档行为。 | 确保快照、知识资产和归档清理逻辑稳定。 |
| `test_select_context.py` | 测试知识选择和上下文复用。 | 防止多需求管理和按需引入能力退化。 |
| `test_build_context_pack.py` | 测试上下文包生成脚本。 | 确保可以为 OpenSpec、Superpowers 和 AI Development 生成可复制上下文包。 |
| `test_accuracy_examples.py` | 测试示例需求准确度基线。 | 保护当前需求理解能力在代表性样例上不回退。 |

## 改动后该跑哪些测试

### 改了抽取逻辑

运行：

```bash
python -m unittest tests.test_extract_initial_dsl tests.test_manage_extractor_overrides tests.test_validate_dsl tests.test_accuracy_examples -v
```

### 改了规格生成或派生产物

运行：

```bash
python -m unittest tests.test_generate_drafts tests.test_generate_derivatives tests.test_validate_dsl -v
```

### 改了流水线入口或操作提示

运行：

```bash
python -m unittest tests.test_run_pipeline -v
```

### 改了知识归档或上下文复用

运行：

```bash
python -m unittest tests.test_archive_spec tests.test_select_context -v
```

### 改了上下文包生成能力

运行：

```bash
python -m unittest tests.test_build_context_pack -v
```

### 准备宣布当前工作区健康可用

运行全量核心回归：

```bash
python -m unittest tests.test_extract_initial_dsl tests.test_manage_extractor_overrides tests.test_validate_dsl tests.test_generate_drafts tests.test_generate_derivatives tests.test_run_pipeline tests.test_archive_spec tests.test_select_context tests.test_build_context_pack tests.test_accuracy_examples -v
```

## 测试策略说明

这些测试强调的是“工具行为稳定”，而不是“某一条真实需求一定被完全理解正确”。

也就是说：

- 测试通过，说明主流程、关键约束和输出链路仍然稳定
- 但真实需求仍然需要人工评审 `merged-dsl.json`、`validation-report.md` 和生成稿

## 相关文档

- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [docs/README_CN.md](D:/spring_AI/prd-spec-workspace/docs/README_CN.md)
- [scripts/README_CN.md](D:/spring_AI/prd-spec-workspace/scripts/README_CN.md)
- [new-requirement-sop_cn.md](D:/spring_AI/prd-spec-workspace/docs/new-requirement-sop_cn.md)
- [project-handbook_cn.md](D:/spring_AI/prd-spec-workspace/docs/project-handbook_cn.md)
- [artifact-usage-guide_cn.md](D:/spring_AI/prd-spec-workspace/docs/artifact-usage-guide_cn.md)
- [context-pack-assembly-guide_cn.md](D:/spring_AI/prd-spec-workspace/docs/context-pack-assembly-guide_cn.md)
- [structured-understanding-confidence_cn.md](D:/spring_AI/prd-spec-workspace/docs/structured-understanding-confidence_cn.md)
