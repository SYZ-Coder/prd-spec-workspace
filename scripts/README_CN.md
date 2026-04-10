# Scripts 目录说明

`scripts/` 是本项目的核心执行目录，负责把 `inputs/` 里的需求材料逐步转换为 DSL、规格稿、派生产物和归档知识。

大多数使用者只需要从 `run_pipeline.py` 进入，但在调试抽取、单独重跑某一阶段、排查问题或为下游工具生成上下文包时，也可以直接运行单个脚本。

## 推荐入口

日常使用优先从这里开始：

```bash
python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<需求标题>"
```

它会按顺序串起：

- bootstrap
- 输入检查
- 抽取
- 校验
- 生成文档
- 同步输出

## 这些脚本遵循的统一原则

- 先做结构化理解，再进入下游规格生成
- 先看证据、可信度和 unknowns，再决定是否继续推进
- validation 是硬门槛
- 上下文包在核心产物稳定后再组装

## 各文件作用与使用方式

| 文件 | 作用 | 常见使用方式 |
| --- | --- | --- |
| `__init__.py` | 让 `scripts/` 可以被测试或其他模块导入。 | 一般不直接执行。 |
| `bootstrap_outputs.py` | 初始化本次需求所需的目录和基础输出结构。 | `python scripts/bootstrap_outputs.py --change-name demo --domain account` |
| `extract_initial_dsl.py` | 读取 `inputs/`，抽取页面、动作、规则、流转、依赖和 unknowns，并生成初始 DSL。支持文本、Markdown、CSV/TSV、`.docx`、`.xlsx`，以及当前环境安装 `xlrd` 时的 `.xls`。 | `python scripts/extract_initial_dsl.py --workspace .` |
| `validate_dsl.py` | 校验 `working/merged-dsl.json` 的完整性、一致性和语义质量，输出 `validation-report.md`。 | `python scripts/validate_dsl.py` |
| `generate_drafts.py` | 根据合并后的 DSL 生成 Markdown 需求稿和 OpenSpec 变更包。 | 一般由 `run_pipeline.py` 调用，也可手动重跑。 |
| `generate_derivatives.py` | 生成流程图文稿、测试用例、接口契约草案和 OpenAPI 骨架。 | 一般由 `run_pipeline.py` 调用，也可单独执行。 |
| `render_mermaid_assets.py` | 把派生产物同步整理到 `outputs/`，方便分享和交付。 | `python scripts/render_mermaid_assets.py` |
| `archive_spec.py` | 将稳定需求归档到 `knowledge/`，保留快照和可复用资产。 | `python scripts/archive_spec.py --change-name demo --domain account --title "Demo"` |
| `select_context.py` | 从 `knowledge/` 中列出并选择可复用 bundle、asset 或 snapshot，供新需求引入上下文。 | `python scripts/select_context.py --list` |
| `manage_extractor_overrides.py` | 初始化和维护 `extractor-overrides.json`，让用户通过配置调优抽取器。 | `python scripts/manage_extractor_overrides.py --show` |
| `build_context_pack.py` | 根据当前工作区的需求产物生成可直接复制的 Markdown 上下文包，供 OpenSpec、Superpowers 或 AI Development 使用。 | `python scripts/build_context_pack.py --target openspec --change-name demo --domain account --title "Demo"` |
| `run_pipeline.py` | 主入口脚本，负责把整条流水线按正确顺序执行起来。 | `python scripts/run_pipeline.py --change-name demo --domain account --title "Demo"` |

## 什么时候用哪个脚本

### 开始一条新需求

```bash
python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<需求标题>"
```

### 只调试抽取

```bash
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
```

`extract_initial_dsl.py` 可以直接读取 `inputs/prd/`、`inputs/notes/`、`inputs/context/` 下的 `.md`、`.txt`、`.json`、`.yaml`、`.html`、`.csv`、`.tsv`、`.docx`、`.xlsx`、`.xls` 文件。旧版 `.doc` 建议先转换后再抽取。

### 只调整词汇并重试

```bash
python scripts/manage_extractor_overrides.py --show
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
```

### 只重刷下游规格和派生产物

```bash
python scripts/generate_drafts.py --workspace . --change-name <change-name> --domain <domain> --title "<需求标题>"
python scripts/generate_derivatives.py --workspace .
```

### 只同步分享产物

```bash
python scripts/render_mermaid_assets.py
```

### 为下游工具生成上下文包

```bash
python scripts/build_context_pack.py --target openspec --change-name <change-name> --domain <domain> --title "<需求标题>"
python scripts/build_context_pack.py --target superpowers --change-name <change-name> --domain <domain> --title "<需求标题>" --goal "实现计划与实现辅助"
python scripts/build_context_pack.py --target ai-development --change-name <change-name> --domain <domain> --title "<需求标题>"
```

### 归档一条已完成需求

```bash
python scripts/archive_spec.py --change-name <change-name> --domain <domain> --title "<需求标题>"
```

### 复用历史知识上下文

```bash
python scripts/select_context.py --list
python scripts/select_context.py --bundle <bundle-name>
```

## 推荐执行顺序

1. `bootstrap_outputs.py`
2. `extract_initial_dsl.py`
3. `validate_dsl.py`
4. `generate_drafts.py`
5. `generate_derivatives.py`
6. `render_mermaid_assets.py`
7. `build_context_pack.py`
8. `archive_spec.py`

实际使用中，`run_pipeline.py` 已经替你覆盖了前 1 到 6 步。需要对外复制上下文时，再执行 `build_context_pack.py`。

## 相关文档

- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [docs/README_CN.md](D:/spring_AI/prd-spec-workspace/docs/README_CN.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [new-requirement-sop_cn.md](D:/spring_AI/prd-spec-workspace/docs/new-requirement-sop_cn.md)
- [project-handbook_cn.md](D:/spring_AI/prd-spec-workspace/docs/project-handbook_cn.md)
- [artifact-usage-guide_cn.md](D:/spring_AI/prd-spec-workspace/docs/artifact-usage-guide_cn.md)
- [context-pack-assembly-guide_cn.md](D:/spring_AI/prd-spec-workspace/docs/context-pack-assembly-guide_cn.md)
- [structured-understanding-confidence_cn.md](D:/spring_AI/prd-spec-workspace/docs/structured-understanding-confidence_cn.md)
