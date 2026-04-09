# OCR 扩展说明

这份文档说明如何为 `prd-spec-workspace` 扩展 OCR 能力来源，以及用户应该如何把 OCR 结果接入平台。

平台的设计原则是：

- 平台不强绑定某一个 OCR 服务
- 平台只约定 OCR 结果的接入方式
- 用户可以自由替换 OCR 生产方式，只要最终落成平台可读取的输入格式

## 1. 当前平台如何识别 OCR 来源

当你开启视觉增强时：

```bash
python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<需求标题>" --enable-vision
```

平台会按这个顺序寻找 OCR 能力来源：

1. 先读取截图同名侧车文件
2. 再尝试调用本地 `tesseract`
3. 如果两者都不可用，则保留低可信度视觉占位结果

也就是说，平台已经支持“多来源接入”，只是默认优先级是：

`sidecar OCR > local tesseract > empty fallback`

## 2. 最推荐的扩展方式：侧车 OCR 文件

这是最稳妥、最可控的方式。

你可以给每一张截图补一个同名 OCR 文件。当前支持这些格式：

- `login.png` 对应 `login.ocr.txt`
- `login.png` 对应 `login.ocr.md`
- `login.png` 对应 `login.ocr.json`

也兼容：

- `login.txt`
- `login.md`
- `login.json`

### 2.1 文本格式示例

```text
登录页
手机号
验证码
登录
注册
忘记密码
```

### 2.2 Markdown 格式示例

```md
# 登录页
- 手机号
- 验证码
- 登录
- 注册
- 忘记密码
```

### 2.3 JSON 格式示例

```json
{
  "ocr_text": "登录页\n手机号\n验证码\n登录\n注册\n忘记密码"
}
```

也支持：

```json
{
  "text": "登录页\n手机号\n验证码\n登录\n注册"
}
```

或者：

```json
{
  "lines": ["登录页", "手机号", "验证码", "登录", "注册"]
}
```

### 2.4 适用场景

侧车 OCR 最适合这些情况：

- 你已经人工看过截图，想给平台高可信文字输入
- 你已经从别的 OCR 工具导出了结果
- 你希望 OCR 结果稳定、可复核、可版本管理
- 截图上的文字对页面识别和规则抽取非常关键

## 3. 第二种扩展方式：本地 tesseract

如果你的机器已经安装并配置好了 `tesseract`，平台会自动尝试调用它。

你需要做的事情是：

1. 在本地安装 `tesseract`
2. 确保命令行里可直接执行 `tesseract`
3. 再运行：

```bash
python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<需求标题>" --enable-vision
```

### 3.1 适用场景

- 截图数量多，不想手工补侧车文件
- 想先快速得到一轮 OCR 初稿
- 可以接受 OCR 结果仍需人工复核

### 3.2 注意事项

- OCR 质量受截图清晰度影响很大
- 如果截图字体小、压缩重、布局复杂，误识别会明显增加
- 本地 OCR 成功后，也不要跳过人工复核

## 4. 第三种扩展方式：接入你自己的 OCR 工具

如果你团队已经有自己的 OCR 流程，也完全可以接进来。

推荐方式不是直接改平台主流程，而是：

1. 先用你自己的工具产出 OCR 结果
2. 再把结果转换成平台支持的侧车格式
3. 放回 `inputs/screenshots/` 同名文件旁边
4. 再运行 `--enable-vision`

也就是说，只要你的工具最终能输出：

- `.ocr.txt`
- `.ocr.md`
- `.ocr.json`

平台就能消费。

## 5. 推荐给用户的扩展优先级

建议团队按这个顺序选：

1. 优先使用侧车 OCR 文件
2. 其次使用本地 `tesseract`
3. 如果已有自有 OCR 流程，就把结果转成侧车文件

原因是：

- 侧车文件最稳定、最透明、最方便版本管理
- 本地 OCR 最省事，但结果波动更大
- 自有 OCR 工具最灵活，但最好通过平台约定格式接入，而不是直接耦合主脚本

## 6. OCR 扩展后的标准检查动作

无论 OCR 来源是什么，开启视觉增强后都建议先检查：

- [screenshot-evidence.md](D:/spring_AI/prd-spec-workspace/working/screenshot-evidence.md)
- [screenshot-ocr.json](D:/spring_AI/prd-spec-workspace/working/screenshot-ocr.json)
- [page-classification.json](D:/spring_AI/prd-spec-workspace/working/page-classification.json)
- [merged-dsl.json](D:/spring_AI/prd-spec-workspace/working/merged-dsl.json)

重点检查：

- OCR 文本是否合理
- 页面命名是否正确
- 按钮、字段、tab 是否提取到了
- 是否把错误 OCR 当成了页面事实
- DSL 中页面和动作是否被错误拉偏

## 7. 团队实践建议

推荐团队把 OCR 扩展约定成这样：

- 默认无 OCR 时，截图只作为弱证据
- 关键需求截图，由产品/分析补侧车 OCR
- 大批量截图，先跑本地 OCR，再人工修正关键页面侧车文件
- 只有在 OCR 证据可信时，才提升页面理解的置信度

## 8. 当前平台边界

当前平台已经支持：

- 侧车 OCR 文件读取
- 本地 `tesseract` 自动尝试
- OCR 结果并入 `screenshot-ocr.json`
- 页面分类和组件核对并入 `page-classification.json`
- 视觉证据并入 `merged-dsl.json`

当前还没有做的事情：

- 多 OCR provider 的配置化切换
- 远程 OCR 服务适配器
- OCR 结果自动纠错
- 更强的组件级视觉理解

后续如果要继续增强，最适合的方向是增加显式 provider 配置，例如：

```json
{
  "ocr_provider": "sidecar",
  "sidecar_priority": true
}
```

但在现阶段，侧车文件已经足够支撑大部分团队使用。
