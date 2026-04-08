# 新需求标准操作 SOP

这份 SOP 面向每一条新的产品需求，目标是把需求从原始材料推进到：

- 结构化 DSL
- 校验通过的规格稿
- 测试和接口派生产物
- 可复用知识归档

适用对象：

- 产品经理
- 测试工程师
- 开发工程师
- 需求分析人员
- 使用本仓库协作的 AI 代理

## 1. 使用前提

开始之前，先确认以下条件成立：

- 仓库可以正常打开和读写
- Python 环境可用
- `scripts/` 中核心脚本可执行
- 当前工作区没有未清理的旧需求活动内容，或者你明确知道这些内容与本次需求有关

建议先看：

- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [direct-use-checklist.md](D:/spring_AI/prd-spec-workspace/docs/direct-use-checklist.md)

## 2. 准备本次需求输入

将本次需求的材料放入 `inputs/`：

- `inputs/prd/`
  放 PRD、产品方案、验收说明、业务目标说明。
- `inputs/screenshots/`
  放页面截图、原型图、流程图截图、弹窗截图。
- `inputs/notes/`
  放会议纪要、边界条件、补充规则、待确认背景。
- `inputs/context/`
  放接口文档、权限规则、角色定义、上下文约束。

最低建议：

- 一份 PRD 或等价文本说明
- 一份 notes
- 如果涉及接口、权限、角色、状态机，再加一份 context

输入质量建议：

- 页面名尽量明确写在 PRD 里
- 流程句尽量带条件，例如“成功后进入结果页”
- 异常流程和边界条件不要只停留在口头讨论
- 接口约束尽量单独落成文档放进 `inputs/context/`

## 3. 初始化并启动本次需求

为本次需求确定三个信息：

- `change-name`
- `domain`
- `title`

推荐直接运行主入口：

```bash
python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<需求标题>"
```

示例：

```bash
python scripts/run_pipeline.py --change-name user-login-register --domain account --title "用户登录注册需求"
```

执行后，项目会按顺序完成：

1. 初始化输出目录
2. 检查输入是否齐全
3. 生成 pipeline plan
4. 抽取初始 DSL
5. 合并 DSL
6. 校验 DSL
7. 在通过校验后生成规格稿和派生产物
8. 同步部分结果到 `outputs/`

## 4. 第一轮检查点

第一次执行完成后，优先看以下文件：

- `working/input-readiness-report.md`
- `working/pipeline-plan.md`
- `working/raw-dsl.json`
- `working/merged-dsl.json`
- `working/validation-report.md`

检查重点：

- 模式识别是否合理：`prd` / `hybrid` / `image-only`
- 页面是否识别合理，没有全部塌成占位页
- 关键动作是否被抽取出来
- 关键规则是否进入 `rules`
- 页面流转是否成立
- `unknowns` 是否显式列出，而不是被误写成事实

## 5. 如果抽取质量不够，怎么处理

建议按这个优先级修正：

### 方案 A. 先补输入

优先补：

- 更清楚的页面命名
- 更完整的流程句
- 更明确的异常说明
- 更准确的接口或权限上下文

### 方案 B. 再调抽取器扩展

如果问题来自领域词汇，而不是输入缺失，使用：

```bash
python scripts/manage_extractor_overrides.py --init
python scripts/manage_extractor_overrides.py --show
```

常见扩展项：

- 页面后缀
- 动作前缀
- 规则关键词
- 规则分类
- 章节别名

更多说明见：

- [extractor-overrides_cn.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides_cn.md)
- [extractor-overrides.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides.md)

### 方案 C. 重新执行抽取和校验

```bash
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
```

## 6. 校验通过后的标准动作

当 `working/validation-report.md` 没有 blocker 后，继续检查这些产物：

- `working/generated-prd.md`
- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`

建议评审分工：

- 产品看目标、规则、范围、待确认项
- 测试看正常流、失败流、边界条件和规则覆盖
- 开发看依赖、接口、状态变化、歧义和实现风险

## 7. 发布派生产物

如果需要把结果给其他团队使用，优先使用这些目录：

- `outputs/diagrams/`
- `outputs/testcases/`
- `outputs/contracts/`

原则：

- `working/` 是分析工作区
- `outputs/` 是更适合分享或归档前交付的结果层

如需单独同步派生产物，可执行：

```bash
python scripts/render_mermaid_assets.py
```

## 8. 归档本次需求

当需求完成且内容稳定后，执行归档：

```bash
python scripts/archive_spec.py --change-name <change-name> --domain <domain> --title "<需求标题>"
```

归档目标：

- 保留本次需求的完整快照
- 提炼可复用知识资产
- 清理活动目录，避免污染下一条需求

归档后，重点检查：

- `knowledge/snapshots/<change-name>/`
- `knowledge/index.md`
- `knowledge/catalog.json`（如果当前归档流程已生成）
- `knowledge/assets/`、`knowledge/bundles/`（如果当前归档流程已生成）

## 9. 下一条需求如何复用历史知识

默认策略应为“按需引入”，不是“整包复制”。

推荐顺序：

1. 先用新需求自己的原始输入
2. 列出可选知识资产
3. 只选有帮助的 bundle、asset 或 snapshot
4. 只有在需求高度相似时，才整包引入 snapshot

常用命令：

```bash
python scripts/select_context.py --list
python scripts/select_context.py --list --domain <domain>
python scripts/select_context.py --bundle <bundle-name>
python scripts/select_context.py --change-name <change-name> --include-snapshot
```

## 10. 每次需求的最小完成定义

一条需求至少应满足以下条件，才算完成本次 SOP：

- `working/raw-dsl.json` 已生成
- `working/merged-dsl.json` 已生成
- `working/validation-report.md` 已生成
- 校验没有 blocker
- 需求稿已生成
- 流程图、测试稿、接口草案已生成
- 团队已经人工检查关键页面、关键规则、关键流转
- 稳定需求已归档，或明确说明暂不归档

## 11. 常见失败点

- 输入材料太少，却期待得到高精度规格
- 看到生成稿像是对的，就跳过 validation
- 把待确认项写进事实层
- 只修生成稿，不修输入或抽取配置
- 把旧需求快照整包塞进新需求，造成上下文污染

## 12. 建议的标准命令顺序

```bash
python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<需求标题>"
python scripts/validate_dsl.py
python scripts/render_mermaid_assets.py
python scripts/archive_spec.py --change-name <change-name> --domain <domain> --title "<需求标题>"
```

如果需要手动调试抽取过程：

```bash
python scripts/extract_initial_dsl.py --workspace .
python scripts/validate_dsl.py
python scripts/manage_extractor_overrides.py --show
```

## 13. 相关文档

- [project-handbook_cn.md](D:/spring_AI/prd-spec-workspace/docs/project-handbook_cn.md)
- [direct-use-checklist.md](D:/spring_AI/prd-spec-workspace/docs/direct-use-checklist.md)
- [inputs/README.md](D:/spring_AI/prd-spec-workspace/inputs/README.md)
- [prompts/README.md](D:/spring_AI/prd-spec-workspace/prompts/README.md)
- [scripts/README.md](D:/spring_AI/prd-spec-workspace/scripts/README.md)
- [tests/README.md](D:/spring_AI/prd-spec-workspace/tests/README.md)
- [artifact-usage-guide_cn.md](D:/spring_AI/prd-spec-workspace/docs/artifact-usage-guide_cn.md)
