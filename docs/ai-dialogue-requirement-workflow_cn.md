# AI 对话式需求识别工作流

这份文档专门回答一个容易混淆的问题：

- 新需求应该怎么在 AI 对话里发起识别
- `run_pipeline.py` 到底做了什么
- AI 在整条链路里什么时候开始起作用
- 用户怎样借助平台规则，让 AI 更准确地把产品原型 / 需求材料转换成 Markdown 规格文档

先说结论：

- 平台的中心思想不变：先结构化理解，再校验，再生成规格
- `run_pipeline.py` 是流程编排器，不是需求理解本身
- AI 真正起作用的地方，是“按平台规则阅读输入、理解需求、抽取结构、判断风险、决定是否继续生成”
- 脚本的价值是把这套流程工程化、可复现、可回归，而不是取代 AI 的需求理解能力

## 1. 新需求应该怎么在 AI 对话里开始

当你有一条新的产品需求时，建议先准备这些输入：

- `inputs/prd/`
- `inputs/screenshots/`
- `inputs/notes/`
- `inputs/context/`

然后在 AI 对话里明确发起：

```text
这是一个新需求，请按平台规则先做结构化识别。
先不要直接写终稿。
请先基于 inputs/ 提取页面、动作、规则、流转、依赖、unknowns，
再判断是否可以继续生成规格稿。
```

如果是原型 / 截图驱动需求，也可以这样说：

```text
这是一个以原型和截图为主的新需求。
请先做页面分类，再做结构化识别，最后输出可评审的 Markdown 需求稿。
不要把待确认内容写成事实。
```

这时 AI 的职责是：

- 读取原始材料
- 做需求结构化理解
- 识别页面、动作、规则、状态、流转、依赖
- 显式保留 unknowns
- 判断当前输入是否足够支持后续生成

也就是说，AI 对话是“需求识别与判断层”。

## 2. `run_pipeline.py` 做了什么

`run_pipeline.py` 的定位是主入口编排脚本。

它负责把平台的固定流程按顺序串起来：

1. 检查输入目录
2. 判断当前模式
   - `prd`
   - `image-only`
   - `hybrid`
3. 生成 `working/input-readiness-report.md`
4. 生成 `working/pipeline-plan.md`
5. 触发抽取脚本
6. 触发校验脚本
7. 在校验通过后触发规格生成
8. 触发派生产物生成
9. 同步结果到 `outputs/`
10. 打印下一步建议和归档命令

你可以把它理解成：

- 它负责流程顺序
- 它负责运行阶段切换
- 它负责生成操作指引
- 它不负责“拍脑袋理解需求”

所以，`run_pipeline.py` 不是“需求理解器”，而是“流程调度器”。

## 3. AI 在哪里开始起作用

AI 其实在平台里有两种作用方式。

### 3.1 对话式 AI

这是最贴近你说的“根据平台技能规则进行精准识别”的方式。

AI 在这里负责：

- 看原始材料
- 按平台规则做抽取
- 按平台规则区分事实 / 推断 / 待确认项
- 判断识别质量和风险
- 决定是否继续生成 Markdown 规格文档

这一步最关键，因为它决定了：

- 识别是否准确
- 规则有没有漏掉
- 原型是否被误读
- 流转是否被错误拼接

### 3.2 脚本化 AI 规则落地

平台里的脚本，本质上是把前面的规则固化下来。

例如：

- `extract_initial_dsl.py` 把“如何从输入抽 DSL”落成代码
- `validate_dsl.py` 把“哪些结构和语义风险要拦住”落成代码
- `generate_drafts.py` 把“如何从 DSL 生成 Markdown / OpenSpec”落成代码

所以可以这样理解：

- AI 规则先体现在平台设计里
- 再通过脚本变成稳定执行能力

## 4. 为什么看起来像“执行脚本了”

因为这个平台不是一个只靠自由对话的助手，而是一个“AI 规则 + 工程化流程”的工具平台。

如果只有对话，没有脚本，会出现这些问题：

- 每次输出风格不稳定
- 流程容易跳步
- 难以回归验证
- 难以归档和复用
- 很难让团队协作

而脚本化之后：

- 每一步固定
- 每种产物固定
- 可测试
- 可回归
- 可归档
- 可复用

所以“执行脚本”不是偏离中心思想，而是在保护这个中心思想。

## 5. 用户如果想让 AI 精准识别原型需求，应该怎么做

这才是平台的关键用法。

建议这样使用：

### Step 1. 先把输入准备好

至少放入：

- 原型截图或页面截图到 `inputs/screenshots/`
- 补充说明到 `inputs/notes/`
- 如果有 PRD 或流程说明，放到 `inputs/prd/`
- 如果有接口、角色、权限信息，放到 `inputs/context/`

### Step 2. 在 AI 对话里先发起识别，而不是直接要终稿

推荐说法：

```text
这是一个新需求，请按平台规则先做结构化识别。
请先输出页面、动作、规则、流转、依赖、unknowns。
请优先识别产品原型里的页面关系和交互，再判断是否能生成 Markdown 需求稿。
```

### Step 3. 先看结构结果，再决定是否进入生成

优先确认：

- 页面识别对不对
- 主流程对不对
- 规则有没有遗漏
- 待确认项有没有被显式列出

### Step 4. 再让平台生成 Markdown 文档

只有结构层靠谱时，再进入：

- `generated-prd.md`
- OpenSpec 变更包
- 流程图
- 测试稿
- 接口草案

这能最大化保证“产品原型 -> Markdown 规格文档”的准确度。

## 6. 推荐的实际使用模式

最推荐的是“对话判断 + 脚本落地”双阶段模式。

### 模式 A：先对话识别，再脚本执行

适合：

- 新需求比较复杂
- 原型很多
- 你担心 AI 误读
- 你想先人工看一轮结构化识别结果

流程：

1. 先让 AI 在对话里做结构化识别
2. 看识别结果是否合理
3. 再执行 `run_pipeline.py` 稳定产出文档

### 模式 B：直接脚本执行，再让 AI 复核

适合：

- 需求比较标准
- 输入比较完整
- 团队已经熟悉平台

流程：

1. 直接运行 `run_pipeline.py`
2. 再让 AI 重点复核 `merged-dsl.json`、`validation-report.md`、`generated-prd.md`

## 7. 平台中心思想没有变

无论是对话模式还是脚本模式，平台始终坚持的是：

- 不是直接从原型跳终稿
- 不是让 AI 随意发挥写文档
- 不是用固定业务模板套需求

而是：

- 先结构化理解需求
- 再校验识别质量
- 再生成规格文档
- 再把结果送到 OpenSpec、Superpowers 或 AI 开发链路

## 8. 一句话理解

如果只用一句话概括这个平台的使用方式：

它不是“让脚本代替 AI 理解需求”，而是“让 AI 的需求理解能力按平台规则稳定落地，再通过脚本把结果工程化输出”。

## 9. 相关文档

- [README_CN.md](D:/spring_AI/prd-spec-workspace/README_CN.md)
- [GUIDE_CN.md](D:/spring_AI/prd-spec-workspace/GUIDE_CN.md)
- [平台运行机制说明](D:/spring_AI/prd-spec-workspace/docs/platform-runtime-mechanism_cn.md)
- [结构化理解与可信度说明](D:/spring_AI/prd-spec-workspace/docs/structured-understanding-confidence_cn.md)
- [新需求标准操作 SOP](D:/spring_AI/prd-spec-workspace/docs/new-requirement-sop_cn.md)
- [产物使用说明](D:/spring_AI/prd-spec-workspace/docs/artifact-usage-guide_cn.md)
- [scripts/README_CN.md](D:/spring_AI/prd-spec-workspace/scripts/README_CN.md)
