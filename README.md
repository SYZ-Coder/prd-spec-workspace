# prd-spec-workspace
需求prd转化为AI可识别的spec或者md文档


# 团队 PRD -> Spec 标准模板

## 目标
将原型截图、PRD、备注说明等输入，转换为：
- 结构化 DSL
- 可校验的需求逻辑
- 团队可读的 Markdown PRD
- OpenSpec 变更包

## 标准流程
1. 放入输入文件到 inputs/
2. 运行 Codex
3. 先生成 working/raw-dsl.json
4. 再生成 working/merged-dsl.json
5. 输出 working/validation-report.md
6. 通过后生成：
    - working/generated-prd.md
    - openspec/changes/<change-name>/*

## 输入建议
- screenshots/: 页面截图、流程图、弹窗图
- prd/: 原始 PRD 文档
- notes/: 产品/研发补充说明
- context/: 接口说明、角色权限、埋点说明、历史版本备注

## 约束
- 不允许一步直出 spec
- 必须先结构化再校验
- 所有不确定内容必须写入 unknowns
- 所有页面必须具备入口、出口、状态、依赖、异常路径



# 目录说明
inputs/ 放原始输入
prompts/ 放固定提示词
working/ 放中间产物
openspec/ 放最终规格
AGENTS.md 约束 Codex 行为
.codex/config.toml 约束本项目运行方式

# 推荐输入命令 （两种）
1、交互式执行
请严格遵循 AGENTS.md，执行完整的 PRD -> DSL -> 校验 -> 输出流程。

要求：
1. 先扫描 inputs/ 中的全部文件
2. 生成 working/page-source-map.md 与 working/raw-dsl.json
3. 生成 working/transition-map.md、working/shared-rules.md、working/merged-dsl.json
4. 生成 working/validation-report.md
5. 执行 python scripts/validate_dsl.py
6. 若校验无阻断问题，再生成：
   - working/generated-prd.md
   - openspec/changes/<change-name>/proposal.md
   - openspec/changes/<change-name>/design.md
   - openspec/changes/<change-name>/tasks.md
   - openspec/changes/<change-name>/specs/account/spec.md
7. 所有不确定项必须写入 unknowns 或“待确认项”
8. 不得把推断内容写成既定事实
2、一次性任务执行
   codex "请严格遵循 AGENTS.md，完成 inputs/ 到 working/ 与 openspec/changes/<change-name>/ 的全部生成流程，并运行 python scripts/validate_dsl.py。"3、指定模型执行

# 给你一套“任务级”Codex 指令模板
任务目标：
将墨刀/PRD材料转成可执行 spec。

执行约束：
- 必须遵循 AGENTS.md
- 必须先 DSL 后校验再生成
- 不允许直接跳到 spec
- 不允许省略失败路径、异常场景、依赖项
- 所有未确认信息进入 unknowns
- 输出文件必须落盘到指定目录

执行步骤：
1. 扫描 inputs/ 全部文件并建立来源索引
2. 生成 working/raw-dsl.json
3. 合并跨页面逻辑到 working/merged-dsl.json
4. 输出 working/validation-report.md
5. 若无阻断问题，生成 working/generated-prd.md
6. 生成 openspec/changes/<change-name>/proposal.md
7. 生成 openspec/changes/<change-name>/design.md
8. 生成 openspec/changes/<change-name>/tasks.md
9. 生成 openspec/changes/<change-name>/specs/<domain>/spec.md

质量要求：
- 页面必须有入口和出口
- action 必须有成功和失败路径
- 必须列出跨页面依赖和公共组件依赖
- 必须单列待确认项

# 再补一层：让 Codex 调 Python 脚本做硬校验
仅靠模型检查还不够。
python scripts/validate_dsl.py


# 输入提示词
请严格遵循 AGENTS.md，执行完整的 PRD -> DSL -> 校验 -> OpenSpec 流程。
先扫描 inputs/，再逐步生成 working/ 和 openspec/changes/sms-login/ 下的所有文件。
任何不确定内容不得猜测，统一进入 unknowns。
生成后执行 python scripts/validate_dsl.py，并根据校验结果修正输出。


