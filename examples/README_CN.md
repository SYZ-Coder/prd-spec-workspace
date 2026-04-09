# 示例目录说明

这个目录现在包含的是“可执行的需求样例基线”，不只是目录约定。

## 已包含示例

- `auth-basic/`
  登录、注册和重置密码需求样例。
- `payment-refund/`
  支付加退款需求样例，包含一个已知的语义风险校验场景。
- `reporting-dashboard/`
  报表看板需求样例，包含自定义抽取器扩展词汇。
- `approval-workflow/`
  审批流需求样例，包含显式中间状态。
- `ticket-lifecycle/`
  工单生命周期需求样例，重点验证触发归属和流转正确性。

## 目录结构

每个示例通常会包含：

- `inputs/prd/`
- `inputs/notes/`
- `inputs/context/`
- `extractor-overrides.json`
- `README.md`
- `README_CN.md`

## 推荐使用方式

1. 把某个示例的 `inputs/` 文件复制到工作区的 `inputs/` 目录。
2. 如果示例提供了 `extractor-overrides.json`，再复制到工作区根目录。
3. 执行 `python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<title>"`。
4. 将生成出来的 DSL 和校验报告与示例预期进行对照。

## 在回归中的作用

这些示例也会被自动化测试用来验证：

- 页面抽取准确度
- 规则抽取覆盖度
- 流转质量
- 语义校验告警
- 自定义词汇支持
