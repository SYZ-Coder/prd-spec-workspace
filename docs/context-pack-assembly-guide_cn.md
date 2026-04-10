# 上下文包组装指南

这份文档专门说明：如何从当前工作区收集需求产物，并快速组装成可喂给 OpenSpec、Superpowers 或通用 AI 的上下文包。

目标不是再解释“哪些产物有用”，而是解决一个更具体的问题：

- 从哪里拿文件
- 怎么判断哪些文件该带上
- 如何一键拼成一个可复制、可转发、可继续执行的上下文包

建议先阅读：

- [产物使用说明](./artifact-usage-guide_cn.md)
- [标准上下文包模板](context-pack-templates/README_CN.md)
- [示例填充版上下文包](context-pack-templates/examples/README_CN.md)

## 1. 先判断你要组装给谁

在组装之前，先确定目标工具：

- OpenSpec
- Superpowers
- 通用 AI / 开发 AI

不同目标的文件侧重点不同：

- OpenSpec 更看重 `openspec/changes/<change-name>/...`
- Superpowers 更看重 “OpenSpec 变更包 + 测试 + 接口 + 校验”
- 通用 AI 更看重 “需求稿 + 流程 + 接口 + 测试 + 校验报告”

## 2. 当前工作区里优先收集哪些文件

### OpenSpec 场景

优先收集：

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/validation-report.md`

建议补充：

- `working/merged-dsl.json`
- `working/generated-api-contracts.md`
- `working/generated-testcases.md`

### Superpowers 场景

优先收集：

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`
- `openspec/changes/<change-name>/specs/<domain>/spec.md`
- `working/generated-prd.md`
- `working/validation-report.md`

建议补充：

- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/merged-dsl.json`

### 通用 AI / 开发 AI 场景

优先收集：

- `working/generated-prd.md`
- `working/generated-flow.md`
- `working/generated-testcases.md`
- `working/generated-api-contracts.md`
- `working/api-contracts/openapi.yaml`
- `working/validation-report.md`

建议补充：

- `working/merged-dsl.json`

## 3. 最推荐的方式：直接使用脚本

现在项目已经提供了脚本：

```bash
python scripts/build_context_pack.py --target openspec --change-name <change-name> --domain <domain> --title "<需求标题>"
python scripts/build_context_pack.py --target superpowers --change-name <change-name> --domain <domain> --title "<需求标题>" --goal "实现计划与实现辅助"
python scripts/build_context_pack.py --target ai-development --change-name <change-name> --domain <domain> --title "<需求标题>"
```

默认会分别输出到：

- `working/context-pack-openspec.md`
- `working/context-pack-superpowers.md`
- `working/context-pack-ai-development.md`

如果你只是想快速拿到一个可复制的上下文包，优先用这条脚本命令。

## 4. 组装上下文包的三种方式

### 方式 A：最稳的手工方式

适合第一次使用。

步骤：

1. 打开对应模板
2. 把模板里的路径替换成本次需求的真实路径
3. 按路径逐个复制文件内容
4. 只保留当前目标需要的部分
5. 将整理后的整段 Markdown 发给目标工具

优点：

- 可控性最高
- 适合人工筛掉噪声
- 适合第一次建立团队标准

### 方式 B：半自动路径清单方式

适合团队已经知道“该带哪些文件”，但不想每次手写路径。

做法是先准备一份文件清单，再一次性读取内容。

例如给 AI Development 准备一份路径清单：

```text
working/generated-prd.md
working/generated-flow.md
working/generated-testcases.md
working/generated-api-contracts.md
working/api-contracts/openapi.yaml
working/merged-dsl.json
working/validation-report.md
```

然后按顺序把这些内容拼到一个 Markdown 文件里。

### 方式 C：PowerShell 一键拼装方式

如果你暂时不想直接使用 `build_context_pack.py`，也可以继续用下面这些 PowerShell 片段。

## 5. 推荐的一键拼装格式

建议生成一个统一的 Markdown 文件，例如：

- `working/context-pack-openspec.md`
- `working/context-pack-superpowers.md`
- `working/context-pack-ai-development.md`

推荐结构：

```md
# Context Pack

## Meta
- Change Name: ...
- Domain: ...
- Title: ...
- Target: ...

## File: path/to/file-a
<文件内容>

## File: path/to/file-b
<文件内容>

## File: path/to/file-c
<文件内容>
```

好处是：

- 结构统一
- 方便复制
- 方便转发
- 方便后续 AI 逐段定位来源

## 6. PowerShell 一键拼装示例

下面给三类目标各一份可直接改的命令。

### 6.1 OpenSpec 上下文包

```powershell
$changeName = "user-login-register"
$domain = "account"
$title = "用户登录注册需求"
$output = "working/context-pack-openspec.md"
$files = @(
  "openspec/changes/$changeName/proposal.md",
  "openspec/changes/$changeName/design.md",
  "openspec/changes/$changeName/tasks.md",
  "openspec/changes/$changeName/specs/$domain/spec.md",
  "working/validation-report.md",
  "working/merged-dsl.json",
  "working/generated-api-contracts.md",
  "working/generated-testcases.md"
)

$lines = @(
  "# OpenSpec Context Pack",
  "",
  "- Change Name: $changeName",
  "- Domain: $domain",
  "- Title: $title",
  ""
)

foreach ($file in $files) {
  if (Test-Path $file) {
    $lines += "## File: $file"
    $lines += ""
    $lines += Get-Content $file
    $lines += ""
  }
}

$lines | Set-Content -Encoding UTF8 $output
```

### 6.2 Superpowers 上下文包

```powershell
$changeName = "user-login-register"
$domain = "account"
$title = "用户登录注册需求"
$output = "working/context-pack-superpowers.md"
$files = @(
  "openspec/changes/$changeName/proposal.md",
  "openspec/changes/$changeName/design.md",
  "openspec/changes/$changeName/tasks.md",
  "openspec/changes/$changeName/specs/$domain/spec.md",
  "working/generated-prd.md",
  "working/generated-flow.md",
  "working/generated-testcases.md",
  "working/generated-api-contracts.md",
  "working/api-contracts/openapi.yaml",
  "working/merged-dsl.json",
  "working/validation-report.md"
)

$lines = @(
  "# Superpowers Context Pack",
  "",
  "- Change Name: $changeName",
  "- Domain: $domain",
  "- Title: $title",
  "- Goal: 实现计划与实现辅助",
  ""
)

foreach ($file in $files) {
  if (Test-Path $file) {
    $lines += "## File: $file"
    $lines += ""
    $lines += Get-Content $file
    $lines += ""
  }
}

$lines | Set-Content -Encoding UTF8 $output
```

### 6.3 AI Development 上下文包

```powershell
$changeName = "user-login-register"
$domain = "account"
$title = "用户登录注册需求"
$output = "working/context-pack-ai-development.md"
$files = @(
  "working/generated-prd.md",
  "working/generated-flow.md",
  "working/generated-testcases.md",
  "working/generated-api-contracts.md",
  "working/api-contracts/openapi.yaml",
  "working/merged-dsl.json",
  "working/validation-report.md"
)

$lines = @(
  "# AI Development Context Pack",
  "",
  "- Change Name: $changeName",
  "- Domain: $domain",
  "- Title: $title",
  "- Target: 代码实现",
  ""
)

foreach ($file in $files) {
  if (Test-Path $file) {
    $lines += "## File: $file"
    $lines += ""
    $lines += Get-Content $file
    $lines += ""
  }
}

$lines | Set-Content -Encoding UTF8 $output
```

## 7. 组装前的检查清单

在一键拼装之前，先确认：

- `working/validation-report.md` 已生成
- 没有 blocker，或者你明确知道 blocker 仍需一起交给下游工具判断
- `change-name` 和 `domain` 使用的是本次需求真实值
- 不需要的旧需求文件没有混入本次上下文包

## 8. 组装后的检查清单

生成上下文包后，建议检查：

- 标题和元信息是否正确
- 每个 `## File:` 小节是否都对应真实文件
- 是否混入了不相关需求内容
- 是否遗漏了 `validation-report.md`
- 是否遗漏了本次目标最关键的文件，例如 OpenSpec 的 `spec.md`、AI 的 `generated-prd.md`

## 9. 团队推荐做法

推荐把这三类上下文包统一落在 `working/`：

- `working/context-pack-openspec.md`
- `working/context-pack-superpowers.md`
- `working/context-pack-ai-development.md`

这样团队后续有三种好处：

- 一眼能知道哪些是“给谁用”的包
- 很容易复制给不同工具
- 归档前也能保留一份本次需求的执行上下文整理稿

## 10. 相关文档

- [标准上下文包模板](context-pack-templates/README_CN.md)
- [示例填充版上下文包](context-pack-templates/examples/README_CN.md)
- [产物使用说明](./artifact-usage-guide_cn.md)
- [新需求标准操作 SOP](./new-requirement-sop_cn.md)
- [scripts/README_CN.md](../scripts/README_CN.md)
