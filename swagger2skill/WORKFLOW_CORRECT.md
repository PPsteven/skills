# Swagger2Skill 正确的工作流

## 三个阶段的设计

### 阶段 1️⃣：提取与显示 (Scripts Only)

**脚本**: `scripts/swagger2skill.py <openapi-url>`

**目的**: 轻量级数据收集，避免占用 Claude Code 上下文

**工作流**:
```
Input:  OpenAPI URL
  ↓
[swagger2skill.py]
  - 解析 OpenAPI 规范
  - 提取所有 categories
  - 计算每个 category 的 endpoints 数
  ↓
Output: 显示 categories 列表 (人类可读格式)
```

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
   ...
   19. XCom (2 endpoints)
```

---

### 阶段 2️⃣：用户选择 (Claude Code AskUserQuestion)

**工具**: Claude Code 的 `AskUserQuestion`

**基于**: 阶段 1️⃣ 的脚本输出

**工作流**:
```
[Claude Code Agent]
  1. 调用阶段 1️⃣ 脚本获取 categories 列表
  2. 使用 AskUserQuestion 工具显示选项
  3. 用户选择:
     - 选项A: "Select ALL categories"
     - 选项B: "Custom selection"
  4. 如果选择自定义:
     - 显示 category 列表让用户选择
  ↓
Output: 用户的选择结果
```

**AskUserQuestion 示例**:
```python
# Claude Code 代理代码伪代码
questions = [
    {
        "question": "How would you like to select API categories?",
        "header": "Category Selection",
        "multiSelect": False,
        "options": [
            {
                "label": "Select ALL categories",
                "description": "Include all 19 categories in the skill"
            },
            {
                "label": "Custom selection",
                "description": "Choose specific categories to include"
            }
        ]
    }
]

# 用户做出选择后，获得结果
```

---

### 阶段 3️⃣：生成 Skill (Scripts)

**脚本**: `scripts/generate_skill.py`

**输入**:
- OpenAPI URL
- Skill 名称
- 输出目录
- 选中的 categories (或 "all")

**工作流**:
```
Input:
  - spec_url: "https://tmp-airflow.momenta.works/api/v1/openapi.json"
  - skill_name: "airflow-api"
  - output_dir: "/Users/ppsteven/projects/skills"
  - categories: "all" 或 "Config,DAG,Variable"
  ↓
[generate_skill.py]
  - 重新解析 OpenAPI 规范
  - 验证 categories 有效
  - 生成 skill 结构
  - 创建所有必需文件
  ↓
Output: 完整的 skill 目录
```

**使用示例**:
```bash
# 生成包含所有 categories 的 skill
python3 scripts/generate_skill.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json \
  airflow-api \
  /Users/ppsteven/projects/skills \
  all

# 生成自定义 categories 的 skill
python3 scripts/generate_skill.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json \
  airflow-api \
  /Users/ppsteven/projects/skills \
  "Config,DAG,Variable,TaskInstance"
```

---

## 完整的 Claude Code 工作流示例

```python
#!/usr/bin/env python
"""Claude Code 工作流示例"""

import subprocess
import json
import sys

def run_cmd(cmd):
    """运行命令并返回输出"""
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.stdout, result.stderr, result.returncode

# 阶段 1️⃣：提取
spec_url = "https://tmp-airflow.momenta.works/api/v1/openapi.json"
stdout, stderr, code = run_cmd(f"python3 scripts/swagger2skill.py {spec_url}")

if code != 0:
    print(f"❌ 提取失败: {stderr}")
    sys.exit(1)

# 显示给用户看
print("=" * 60)
print("📖 这是从 OpenAPI 规范提取的 categories")
print("=" * 60)
print(stdout)

# 阶段 2️⃣：使用 AskUserQuestion 让用户选择
# (由 Claude Code 框架处理)
# 用户选择后，我们得到: user_choice = "all" 或 user_choice = ["Config", "DAG"]

# 假设用户选择了 "all"
user_choice = "all"
skill_name = "airflow-api"
output_dir = "/Users/ppsteven/projects/skills"

# 阶段 3️⃣：生成 skill
generate_cmd = f'python3 scripts/generate_skill.py "{spec_url}" "{skill_name}" "{output_dir}" "{user_choice}"'
stdout, stderr, code = run_cmd(generate_cmd)

if code != 0:
    print(f"❌ 生成失败: {stderr}")
    sys.exit(1)

print(stdout)
print("✅ Skill 生成完成！")
```

---

## 数据流图

```
Claude Code 代理
    ↓
    ├─→ [Step 1] 运行 swagger2skill.py <url>
    │        ↓
    │        输出: 19 个 categories 列表
    │        目的: 轻量级，快速，避免上下文占用
    │
    ├─→ [Step 2] 调用 AskUserQuestion 工具
    │        ↓
    │        显示两个选项:
    │        • All categories
    │        • Custom selection
    │        ↓
    │        用户做出选择
    │        结果: "all" 或 ["Config", "DAG", ...]
    │
    └─→ [Step 3] 运行 generate_skill.py
             ↓
             生成完整的 skill 结构
             ↓
             /Users/ppsteven/projects/skills/airflow-api/
                 ├── SKILL.md
                 ├── scripts/cli_tool.py
                 └── references/api_endpoints.md
```

---

## 脚本说明

### swagger2skill.py

**职责**: 提取 + 显示

**只做**:
- ✅ 解析 OpenAPI 规范
- ✅ 提取 categories
- ✅ 显示列表

**不做**:
- ❌ 不进行用户交互 (input/prompt)
- ❌ 不生成 skill
- ❌ 不进行任何修改操作

### generate_skill.py

**职责**: 生成 Skill

**做**:
- ✅ 解析 OpenAPI 规范
- ✅ 验证 categories
- ✅ 生成 skill 文件结构
- ✅ 创建必需的文件

**不做**:
- ❌ 不做用户交互
- ❌ 不做数据提取优化 (让 swagger2skill.py 做)

---

## 为什么这样设计？

### 避免上下文占用
- 脚本 1️⃣ 快速返回，不会加载太多数据
- Claude Code 上下文用于决策，不浪费在数据上

### 清晰的职责分离
- **Script**: 数据处理
- **Claude Code**: 用户交互和决策
- **Script**: 执行生成

### 易于集成
- 脚本可独立测试
- Claude Code 逻辑清晰
- 易于添加新功能

### 模块化
- 每个脚本单一职责
- 可独立升级或修改
- 易于维护

---

## 快速参考

| 阶段 | 脚本 | 目的 | 输出 |
|------|------|------|------|
| 1️⃣ | `swagger2skill.py` | 提取 categories | 列表显示 |
| 2️⃣ | AskUserQuestion | 用户选择 | 选择结果 |
| 3️⃣ | `generate_skill.py` | 生成 skill | 完整目录 |

---

## 常见问题

**Q: 为什么分成两个脚本？**
A: 这样可以在阶段 2️⃣ (用户选择) 之前完成轻量级的数据提取，避免浪费 Claude Code 上下文。

**Q: 能否合并成一个脚本？**
A: 可以，但不推荐。会导致脚本职责混乱，且无法充分利用 AskUserQuestion 工具。

**Q: 用户选择后如何传递给 generate_skill.py？**
A: Claude Code 代理代码会接收 AskUserQuestion 的返回值，然后作为参数传递给脚本。

---

**设计完成日期**: 2026-03-07
**设计原则**: 轻量 + 清晰 + 模块化
