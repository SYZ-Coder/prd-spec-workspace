# prd-spec-workspace 操作指南

这份指南说明如何从一个新需求开始，逐步完成结构化识别、校验、规格生成、上下文包组装和知识归档。

如果想先了解项目定位，请看 [README_CN.md](README_CN.md)。如果想看全部文档入口，请看 [docs/README_CN.md](docs/README_CN.md)。

## 1. 准备输入材料

把材料放入 `inputs/` 下对应目录：

- `inputs/prd/`：PRD、需求说明、验收说明、业务背景。
- `inputs/screenshots/`：截图、原型图、弹窗、流程截图、UI 截图。
- `inputs/notes/`：补充说明、会议纪要、异常场景、边界条件。
- `inputs/context/`：接口说明、角色权限、状态机、技术约束。

建议最少准备一份 PRD 或等价需求说明。涉及页面、流程、权限、接口时，最好同时补充截图、备注和上下文文件。

## 2. 理解平台流程

平台固定按以下顺序推进：

1. Extract：从输入材料抽取页面、动作、规则、流转、依赖和 unknowns。
2. Merge：合并重复页面、共享规则和跨页面流转。
3. Validate：检查 DSL 完整性、一致性和可执行性。
4. Generate：在无阻断问题后生成 PRD 草稿和 OpenSpec 变更包。
5. Derivative Outputs：生成流程图、测试用例、接口草案和 OpenAPI 草案。
6. Archive：需求稳定后归档为可复用知识。

关键原则：不要跳过 validation。只要校验报告存在 blocker，就应先修输入、补上下文或调整抽取规则。

## 3. 开始一个新需求

先确定 `change-name`、`domain` 和需求标题。

```bash
python scripts/bootstrap_outputs.py --change-name auth-basic --domain account
```

也可以直接运行完整流程入口：

```bash
python scripts/run_pipeline.py --change-name auth-basic --domain account --title "基础登录注册"
```

脚本会生成 pipeline plan、输入就绪报告、DSL、校验报告，以及在校验通过后的规格产物。

## 4. 对话式 AI 使用

当需求还不够清晰时，建议先让 AI 只做结构化识别，不直接写终稿。

推荐提示词：

```text
这是一个新需求，请按平台规则先做结构化识别。
先不要直接写终稿。
请先基于 inputs/ 提取页面、动作、规则、流转、依赖、unknowns，
再判断是否可以继续生成规格稿。
```

确认结构可信后，再要求继续生成“已确认事实 / 结构化推断 / 待确认项”分层规格初稿。

## 5. 启用多模态视觉增强

如果截图或原型是重要证据，开启视觉增强：

```bash
python scripts/run_pipeline.py --change-name auth-basic --domain account --title "基础登录注册" --enable-vision
```

该模式会先生成视觉证据、页面分类和组件核对结果，再进入 DSL 抽取。

如果你已经有可靠的截图文字信息，可以添加同名侧车文件：

- `login.png` + `login.txt`
- `login.png` + `login.md`
- `login.png` + `login.json`

运行后先检查：

- `working/screenshot-evidence.md`
- `working/screenshot-text-evidence.json`
- `working/page-classification.json`

注意：辅助文字提取只是多模态需求理解的证据来源，不能替代视觉核对、业务判断和 validation。

## 6. 检查第一批产物

第一轮运行后，优先看这些文件：

- `working/pipeline-plan.md`
- `working/input-readiness-report.md`
- `working/raw-dsl.json`
- `working/merged-dsl.json`
- `working/validation-report.md`

重点检查：

- 页面是否识别正确。
- 动作是否覆盖主要交互。
- 规则是否进入 `rules`。
- 流转是否有入口、出口、成功和失败路径。
- unknowns 是否过多或包含阻断项。
- 多模态视觉证据是否真的支持 DSL 中的页面和组件判断。

## 7. 提升抽取准确度

优先补强源材料，而不是直接改最终产物。

常见补强方式：

- 在 PRD 中写清页面名、入口、出口和状态。
- 在 notes 中补充异常流程、边界条件和默认规则。
- 在 context 中补充接口、权限、状态机和依赖约束。
- 对关键截图补同名侧车文本，帮助平台识别按钮、字段和 tab。

如果问题来自领域词汇，可以使用 `extractor-overrides.json`：

```bash
python scripts/manage_extractor_overrides.py --init
python scripts/manage_extractor_overrides.py --show
python scripts/manage_extractor_overrides.py --add-page-suffix Dashboard
python scripts/manage_extractor_overrides.py --add-action-prefix Export
python scripts/manage_extractor_overrides.py --add-rule-keyword real-time
```

然后重新抽取和校验：

```bash
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
```

## 8. 审阅规格产物

校验通过后，重点审阅：

- `working/generated-prd.md`
- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`

产品看目标和规则，测试看正常、异常和边界路径，开发看接口、依赖、状态和待确认项。

## 9. 组装上下文包

需要把产物交给 OpenSpec、Superpowers 或通用 AI 开发工具时，使用：

```bash
python scripts/build_context_pack.py --target openspec --change-name auth-basic --domain account --title "基础登录注册"
python scripts/build_context_pack.py --target superpowers --change-name auth-basic --domain account --title "基础登录注册"
python scripts/build_context_pack.py --target ai-development --change-name auth-basic --domain account --title "基础登录注册"
```

上下文包会把 DSL、校验报告、规格、测试和接口草案组织成更适合复制粘贴的标准输入。

## 10. 归档稳定需求

需求确认稳定后执行归档：

```bash
python scripts/archive_spec.py --change-name auth-basic --domain account --title "基础登录注册"
```

归档会保留需求快照，并提取可复用知识到 `knowledge/`。归档后可以清理当前 `inputs/`、`working/`、`outputs/`，避免污染下一个需求。

## 11. 团队实践建议

- 产品负责人维护 `inputs/prd/` 和 `inputs/notes/`。
- 设计或分析同学维护截图、原型和流程证据。
- 开发同学维护 `inputs/context/` 中的接口、权限和依赖。
- 团队先评审 `validation-report.md`，再接受生成规格。
- 稳定产物再归档，后续新需求按需引用，不要整包滥用旧上下文。

## 12. 常见误区

- 不要把截图当成完整业务事实。
- 不要因为草稿看起来合理就跳过 validation。
- 不要把 unknowns 混入既定规则。
- 不要让旧需求知识默认污染新需求识别。
- 不要把辅助文字提取结果当成最终事实，它只是一类证据。

## 13. 相关文档

- [README_CN.md](README_CN.md)
- [README.md](README.md)
- [文档中心](docs/README_CN.md)
- [新需求标准 SOP](docs/new-requirement-sop_cn.md)
- [产物使用说明](docs/artifact-usage-guide_cn.md)
- [上下文包组装指南](docs/context-pack-assembly-guide_cn.md)
- [多模态视觉证据扩展说明](docs/visual-evidence-extension-guide_cn.md)
