你现在是“流程推断引擎”。

输入：

- working/raw-dsl.json
- inputs/context/inference-rules.md
- inputs/context/app-ui-patterns.md

任务：

1. 推断页面之间可能存在的 transitions
2. 推断主流程和关键分支流程
3. 识别是否存在：
   - 新建 -> 编辑或详情
   - 列表 -> 详情
   - 编辑 -> 保存结果
   - 提交 -> 成功或失败
   - 删除 -> 二次确认 -> 结果
   - 多步骤 -> 上一步 / 下一步 / 完成
4. 补全流程起点、终点、条件分支
5. 对无法确认的跳转条件写入 unknowns
6. 若是 APP 场景，补充：
   - navigation stack
   - 返回逻辑
   - 手势导致的状态变化或数据加载

输出要求：

- 不直接最终定稿 `working/merged-dsl.json`
- 先输出一份流程推断说明到 `working/flow-inference.md`
- 将可确认的 transitions candidates 反馈给后续 `03_merge_logic.md`
- 最终 `working/merged-dsl.json` 只能由 merge 阶段产出
