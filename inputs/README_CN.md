# Inputs 使用说明

`inputs/` 是原始需求材料的唯一入口区域。

工作区中的抽取、校验和生成都从这里开始。高质量输入对抽取准确度的提升，通常比后面补改输出稿更有效。

这也意味着：输入质量会直接影响证据质量、可信度水平，以及下游规格产物的稳定性。

## 各目录职责

### `inputs/prd/`
用于存放需求描述和业务意图。

推荐内容：

- PRD
- 方案文档
- 验收说明
- 业务描述
- 结构化需求文本

最佳用途：

- 解释目标和范围
- 显式写出关键页面或关键流程名称
- 用文字描述核心规则和边界条件

### `inputs/screenshots/`
用于存放 UI 证据。

推荐内容：

- 页面截图
- 弹窗截图
- 原型截图
- 流程截图
- 带注释的 UI 图片

最佳用途：

- 展示可见结构
- 支持页面分类
- 暴露页面状态和组件线索

重要边界：

- 截图是证据，不是完整业务事实
- 不应只依赖截图来确定最终业务规则

### `inputs/notes/`
用于存放补充说明和操作细节。

推荐内容：

- 会议纪要
- 口头补充
- 异常处理说明
- 边界条件提醒
- 不适合直接放进 PRD 的内部解释

最佳用途：

- 补上 PRD 没写清楚的内容
- 暴露特殊条件和风险点
- 区分已确认事实和待确认问题

### `inputs/context/`
用于存放影响实现或解读的支持性上下文。

推荐内容：

- API 描述
- 角色和权限说明
- 系统约束
- 历史兼容要求
- 集成依赖说明
- 术语表或 UI 语义说明

最佳用途：

- 减少无依据的猜测
- 帮助生成更准确的依赖和接口草案
- 明确归属关系、权限约束和上下游边界

## 推荐输入组合

### 最低可用组合

- `prd + notes`
- 或 `screenshots + notes + context`

### 推荐组合

- `prd + screenshots + notes + context`

### 最强组合

- `prd + screenshots + flow evidence + notes + context + api docs`

## 输入质量清单

1. 尽量显式写出重要页面名称。
2. 用文字描述成功路径和失败路径。
3. 关键规则不要只散落在截图里。
4. 待确认问题放进 notes，不要混入事实层。
5. 需求依赖接口或权限时，要补充对应 context。
6. 流程截图或 notes 中要保留分支条件。

## 常见错误

尽量避免这些情况：

- 把生成产物重新放回 `inputs/`
- 把旧需求归档文件和新需求活动内容混在一起
- 只给截图，不给任何文字说明
- 把关键规则只藏在聊天记录或图片标注里
- 默认让抽取器猜出缺失的业务事实

## 建议使用流程

1. 先把原始材料放到正确子目录。
2. 运行流水线，或者至少运行抽取和校验步骤。
3. 查看 `working/input-readiness-report.md` 和 `working/validation-report.md`。
4. 如果抽取质量偏弱，优先补输入。
5. `extractor-overrides.json` 只用于词汇调优，不用于代替缺失的需求事实。

## 相关文档

- [README.md](D:/spring_AI/prd-spec-workspace/README.md)
- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [guide.md](D:/spring_AI/prd-spec-workspace/guide.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [docs/README_CN.md](D:/spring_AI/prd-spec-workspace/docs/README_CN.md)
- [structured-understanding-confidence_cn.md](D:/spring_AI/prd-spec-workspace/docs/structured-understanding-confidence_cn.md)
- [extractor-overrides.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides.md)
- [extractor-overrides_cn.md](D:/spring_AI/prd-spec-workspace/docs/extractor-overrides_cn.md)
