# 把零散需求变成可执行规格：一个 PRD 结构化工作台的实践

做产品研发的人，应该都遇到过类似场景：PRD 在文档里，原型在截图里，接口说明在 Excel 里，补充规则在会议纪要里。真正进入开发前，团队还要重新把这些材料拼一遍。

问题通常不是没有需求材料，而是材料太散。页面、动作、规则、状态、接口、异常路径和待确认项混在不同文件里，产品、测试、开发各自理解一遍，信息损耗很大。

prd-spec-workspace 想解决的就是这一步：把零散需求材料整理成可校验、可追踪、可执行的规格上下文。

## 它不是普通 PRD 生成器

很多工具可以生成一篇看起来完整的 PRD，但文档完整不代表需求可执行。

常见问题包括：

- 页面有描述，但没有入口和出口。
- 动作有成功路径，但没有失败路径。
- 截图能看出界面，但无法确认业务规则。
- 接口表里有字段，但不知道对应哪个用户动作。
- 产品口头补充过规则，但没有进入测试和开发上下文。

所以这个工作台不是直接写终稿，而是先把需求转换成结构化 DSL，再做校验，最后才生成规格产物。

核心流程是：

`	ext
原始需求材料
-> 结构化 DSL
-> 完整性校验
-> 规格产物
-> 开发执行上下文
-> 知识归档复用
`

DSL 会尽量抽取这些关键对象：

`	ext
pages          页面
actions        动作
rules          规则
transitions    流转
dependencies   依赖
unknowns        待确认项
`

这一步的价值在于：先让需求变得可检查，再让它变得可生成。

## 支持哪些输入材料

工作台统一从 inputs/ 读取需求来源。

推荐目录结构：

`	ext
inputs/prd/          PRD、需求说明、Markdown、Word
inputs/screenshots/  截图、原型图、流程图
inputs/notes/        会议纪要、补充说明、边界条件
inputs/context/      接口说明、权限矩阵、状态表、Excel 表格
`

支持的常见格式包括：

`	ext
.md .txt .docx .xlsx .xls .csv .tsv .json .yaml .html
.png .jpg .jpeg .webp .bmp
`

团队不需要为了工具重新整理一份完美 PRD。已有的 Word、Excel、截图、备注和接口说明，都可以作为需求证据进入流程。

## 一条命令跑完整流程

把材料放入 inputs/ 后，可以执行：

`ash
python scripts/run_pipeline.py --change-name login-register --domain account --title '用户登录注册需求'
`

如果需求强依赖截图或原型，可以开启视觉增强：

`ash
python scripts/run_pipeline.py --change-name login-register --domain account --title '用户登录注册需求' --enable-vision
`

运行后会产生几类结果。

中间分析产物：

`	ext
working/page-source-map.md
working/raw-dsl.json
working/merged-dsl.json
working/validation-report.md
`

规格产物：

`	ext
working/generated-prd.md
openspec/changes/<change-name>/proposal.md
openspec/changes/<change-name>/design.md
openspec/changes/<change-name>/tasks.md
openspec/changes/<change-name>/specs/<domain>/spec.md
`

派生产物：

`	ext
working/generated-flow.md
working/generated-testcases.md
working/generated-api-contracts.md
working/api-contracts/openapi.yaml
`

这样，分析过程、规格草稿、测试用例、接口草案和历史归档不会混在一起，团队后续查阅和复用会更清楚。
