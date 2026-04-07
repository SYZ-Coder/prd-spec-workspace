# PRD / 墨刀原型 → OpenSpec 转换流程指南（团队版）

---

## 一、目标

将以下输入：

* 墨刀原型（截图）
* PRD 文档
* 补充说明（会议/IM）
* 系统上下文（接口/权限）

统一转换为：

* 结构化 DSL（机器可读）
* Markdown PRD（人可读）
* OpenSpec（可执行规格）

---

## 二、核心思想（必须理解）

> ❌ 不是：把原型转成 Markdown
> ✅ 而是：把“需求”转成“结构化模型”

最终流程：

```
inputs → DSL → 校验 → PRD → OpenSpec
```

---

## 三、输入规范（inputs/）

所有需求必须放入 `inputs/`，按类型分类：

```
inputs/
├── screenshots/   # 页面截图（墨刀）
├── prd/           # 主需求文档
├── notes/         # 补充说明
└── context/       # 系统上下文
```

---

### 1️⃣ screenshots/

放：

* 页面截图
* 弹窗截图
* 流程图

作用：

👉 提供 UI / 交互结构

---

### 2️⃣ prd/

放：

* PRD 文档（md / word转md）

作用：

👉 提供业务逻辑

---

### 3️⃣ notes/

放：

* 产品口头补充
* 会议纪要
* 边界说明

作用：

👉 补“隐性逻辑”（最重要）

---

### 4️⃣ context/

放：

* 接口文档
* 权限说明
* 系统规则

作用：

👉 提供系统依赖

---

## 四、标准流程（必须遵循）

### Step 1：结构抽取（Extract）

输出：

```
working/raw-dsl.json
working/page-source-map.md
```

内容：

* 页面
* 用户动作
* 状态
* 初步跳转
* unknowns（不确定项）

---

### Step 2：逻辑归并（Merge）

输出：

```
working/merged-dsl.json
working/transition-map.md
working/shared-rules.md
```

内容：

* 串联跨页面逻辑
* 合并重复规则
* 提取公共依赖

---

### Step 3：校验（Validate）

输出：

```
working/validation-report.md
```

检查：

* 页面是否有入口/出口
* action 是否有失败路径
* 跳转是否合法
* 是否存在孤立页面
* 是否存在依赖缺失
* unknowns 是否过多

---

### Step 4：生成（Generate）

输出：

```
working/generated-prd.md
openspec/changes/<change-name>/*
```

包含：

* proposal.md
* design.md
* tasks.md
* spec.md

---

## 五、DSL 结构说明（核心）

### 顶层结构

```json
{
  "pages": [],
  "transitions": [],
  "rules": [],
  "dependencies": [],
  "unknowns": []
}
```

---

### Page 示例

```json
{
  "id": "P_LOGIN",
  "name": "登录页",
  "goal": "用户完成登录",
  "entry_points": ["应用启动"],
  "exit_points": ["首页"],
  "actions": [],
  "states": [],
  "dependencies": [],
  "unknowns": []
}
```

---

### Action 示例

```json
{
  "trigger": "点击登录",
  "preconditions": ["手机号合法"],
  "success_results": ["跳转首页"],
  "failure_results": ["验证码错误"]
}
```

---

### Transition 示例

```json
{
  "from_page": "P_LOGIN",
  "to_page": "P_HOME",
  "condition": "isNewUser=false"
}
```

---

## 六、完整案例演示（登录流程）

---

### 输入

#### screenshots/

```
login.png
profile.png
home.png
```

#### prd/

```md
用户通过手机号验证码登录
首次登录需要补充资料
```

#### notes/

```md
未勾选协议不可登录
验证码错误提示 toast
```

#### context/

```md
POST /api/login
返回 isNewUser
```

---

### 输出 DSL（核心）

```json
{
  "pages": [
    {
      "id": "P_LOGIN",
      "name": "登录页",
      "actions": [
        {
          "trigger": "点击登录",
          "preconditions": ["手机号合法"],
          "success_results": ["返回 token"],
          "failure_results": ["验证码错误"]
        }
      ]
    }
  ],
  "transitions": [
    {
      "from_page": "P_LOGIN",
      "to_page": "P_PROFILE",
      "condition": "isNewUser=true"
    }
  ]
}
```

---

### 输出 Markdown

```md
## 登录流程

用户登录后：

- 首次 → 资料页
- 非首次 → 首页
```

---

### 输出 OpenSpec

```md
## Requirement: Login

### Scenario: 首次登录
Then 跳转资料页
```

---

## 七、关键规则（必须遵守）

### ❗ 1. 不允许直接生成 spec

必须：

```
DSL → 校验 → spec
```

---

### ❗ 2. 所有不确定项必须进入 unknowns

不允许：

* 猜测
* 编造

---

### ❗ 3. 每个 Action 必须有失败路径

否则：

👉 需求不完整

---

### ❗ 4. 每个页面必须有入口和出口

否则：

👉 流程断链

---

### ❗ 5. 不允许覆盖已有 spec

必须：

```
openspec/specs/   → 稳定事实
openspec/changes/ → 新需求
```

---

## 八、团队最佳实践

---

### 输入规范（建议写入团队制度）

```md
每个需求必须包含：

- screenshots/
- prd/
- notes/
- context/
```

---

### 命名规范

```
login-page.png
account-prd.md
login-notes.md
auth-context.md
```

---

### change-name 规范

```
account-sms-login-add
order-refund-change
```

---

## 九、常见错误

### ❌ 只放截图

→ 缺业务逻辑

---

### ❌ 只放 PRD

→ 缺交互细节

---

### ❌ 不放 context

→ spec 无法落地

---

### ❌ 不做校验

→ 会漏逻辑

---

## 十、总结（一句话）

> inputs 是“需求事实池”，DSL 是“需求模型”，OpenSpec 是“可执行规范”。

---

## 十一、推荐落地步骤

1. 选一个简单需求试跑
2. 跑完整流程
3. 补充规则库（rules.md）
4. 补充组件语义（components.md）
5. 再接开发流程

---

## 十二、后续可扩展方向

* 自动生成 Mermaid 流程图
* 自动生成测试用例
* 自动生成接口契约
* 自动生成 Spring Boot 代码
* 接入 Codex / Cursor 自动开发

---

**（本指南作为团队统一规范，建议纳入工程模板或知识库）**
