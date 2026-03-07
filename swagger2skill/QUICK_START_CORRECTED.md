# Swagger2Skill - 快速开始 (正确版本)

## 三个阶段的正确工作流

### 阶段 1️⃣：提取 Categories

```bash
python3 scripts/swagger2skill.py <openapi-url>
```

**只做一件事**: 提取并显示所有 categories

**示例**:
```bash
python3 scripts/swagger2skill.py https://tmp-airflow.momenta.works/api/v1/openapi.json
```

**输出**:
```
============================================================
📖 OpenAPI Categories
============================================================

✅ Found 19 API categories:

   1. Config (2 endpoints)
   2. Connection (6 endpoints)
   3. DAG (12 endpoints)
   4. DAGRun (9 endpoints)
   5. DagStats (1 endpoints)
   6. DagWarning (1 endpoints)
   7. Dataset (11 endpoints)
   8. EventLog (2 endpoints)
   9. ImportError (2 endpoints)
   10. Monitoring (2 endpoints)
   11. Permission (1 endpoints)
   12. Plugin (1 endpoints)
   13. Pool (5 endpoints)
   14. Provider (1 endpoints)
   15. Role (5 endpoints)
   16. TaskInstance (17 endpoints)
   17. User (5 endpoints)
   18. Variable (5 endpoints)
   19. XCom (2 endpoints)
```

✅ 就这样！脚本的工作完成了。

---

### 阶段 2️⃣：用户选择 (Claude Code 代理)

**这一步在 Claude Code 中进行**, 使用 `AskUserQuestion` 工具:

```python
# Claude Code 代理的伪代码示例

# 获取用户的选择
selected_option = AskUserQuestion([
    {
        "label": "Select ALL categories",
        "description": "Include all 19 categories in the skill"
    },
    {
        "label": "Custom selection",
        "description": "Choose specific categories to include"
    }
])

# 结果: 用户选择了某个选项
```

**Claude Code 会得到**:
- 用户选择: "All" 或具体的 categories
- 以及其他信息（skill 名称、输出目录等）

---

### 阶段 3️⃣：生成 Skill

**基于用户的选择**, 调用生成脚本:

```bash
# 如果用户选择了"All categories"
python3 scripts/generate_skill.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json \
  airflow-api \
  /Users/ppsteven/projects/skills \
  all

# 如果用户选择了自定义 categories
python3 scripts/generate_skill.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json \
  airflow-api \
  /Users/ppsteven/projects/skills \
  "Config,DAG,Variable,TaskInstance"
```

**输出**:
```
============================================================
⚙️  Generating Skill
============================================================

📋 Generating skill with 19 categories:
   • Config
   • Connection
   • DAG
   ...

============================================================
✅ Skill Generation Complete!
============================================================

📍 Skill location: /Users/ppsteven/projects/skills/airflow-api

📋 Generated Files:
   • SKILL.md - Skill documentation
   • scripts/cli_tool.py - CLI wrapper for selected APIs
   • references/api_endpoints.md - API reference
```

---

## Claude Code 中的完整工作流

在 Claude Code 代理中执行:

```python
import subprocess
import sys

# 阶段 1️⃣：提取 categories
spec_url = "https://tmp-airflow.momenta.works/api/v1/openapi.json"
result = subprocess.run(
    ["python3", "scripts/swagger2skill.py", spec_url],
    capture_output=True, text=True
)
print(result.stdout)  # 显示 categories 给用户

# 阶段 2️⃣：使用 AskUserQuestion 获取用户选择
# (由 Claude Code 框架处理)

# 阶段 3️⃣：基于用户选择生成 skill
subprocess.run([
    "python3", "scripts/generate_skill.py",
    spec_url,
    skill_name,        # 来自用户输入
    output_dir,        # 来自用户输入
    selected_categories  # 来自 AskUserQuestion 的结果
])
```

---

## 关键点

### ✅ 脚本 1: swagger2skill.py

- **只做**: 提取 + 显示
- **输入**: OpenAPI URL
- **输出**: Categories 列表 (人类可读格式)
- **特点**: 轻量级，快速，无交互

### ✅ 脚本 2: generate_skill.py

- **只做**: 生成 Skill
- **输入**: URL + 名称 + 目录 + 选中的 categories
- **输出**: 完整的 skill 目录结构
- **特点**: 快速、简洁、无冗余处理

### ✅ 中间: AskUserQuestion

- **做**: 用户交互和决策
- **由**: Claude Code 代理处理
- **结果**: 用户的选择

---

## 对比：旧的错误流程 vs 新的正确流程

### ❌ 旧流程 (错误)
```
swagger2skill.py
  → 提取 categories
  → 询问用户选择 (input())
  → 获取 skill 名称 (input())
  → 获取输出目录 (input())
  → 生成 skill
```
**问题**: 所有交互都在脚本中，混淆了关注点

### ✅ 新流程 (正确)
```
阶段 1️⃣: swagger2skill.py
  → 提取 categories
  → 显示列表

阶段 2️⃣: Claude Code (AskUserQuestion)
  → 用户选择 categories
  → 用户输入 skill 名称
  → 用户选择输出目录

阶段 3️⃣: generate_skill.py
  → 生成 skill
```
**优点**: 清晰分离，轻量级，易于维护

---

## 故障排除

### 问题：阶段 1️⃣ 超时
**解决**: 检查 URL 是否可访问

### 问题：阶段 3️⃣ 找不到 categories
**解决**: 确保阶段 2️⃣ 正确传递了 categories 名称

### 问题：生成的 skill 文件位置错误
**解决**: 检查 `output_dir` 参数是否正确

---

## 下一步

1. ✅ 运行阶段 1️⃣ 脚本查看 categories
2. ✅ 在 Claude Code 中集成 AskUserQuestion
3. ✅ 调用阶段 3️⃣ 脚本生成 skill
4. ✅ 验证生成的 skill 结构

---

**推荐阅读**: 详见 `WORKFLOW_CORRECT.md` 了解完整设计理由
