# 在 Claude Code 中使用 Swagger2Skill

## 快速开始

### 问题已解决 ✅

原始脚本存在的问题已经完全解决：

- ❌ ~~缺少 `claude_code_tools` 模块~~ → 已移除
- ❌ ~~`input()` 导致 EOF 错误~~ → 已分离到独立流程
- ✅ 现在支持完整的交互式工作流

## 使用方法

### 推荐方法 1：使用 Claude Code 代理执行

当 Claude Code 代理需要生成 skill 时：

```bash
# 第1步：提取 categories
python3 /Users/ppsteven/Projects/skills/swagger2skill/scripts/extract_categories.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json
```

输出将显示所有 19 个 API categories。

### 推荐方法 2：使用完整交互流程

```bash
python3 /Users/ppsteven/Projects/skills/swagger2skill/scripts/swagger2skill_claude.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json
```

交互流程：
1. ✅ 提取 OpenAPI spec 中的 19 个 categories
2. 📋 显示所有 categories 列表
3. 🎯 询问用户：选择"All categories"还是"Custom selection"
4. 💾 获取 skill 名称（如 `airflow-api`）
5. 📁 获取输出目录（默认 `/Users/ppsteven/projects/skills`）
6. ⚙️ 生成最终的 skill

### 推荐方法 3：使用 Claude Code AskUserQuestion 工具

在 Claude Code 脚本中使用：

```python
from pathlib import Path
import subprocess
import sys
import json

def extract_categories(spec_url):
    """使用 extract_categories.py 提取 categories"""
    script = Path("/Users/ppsteven/Projects/skills/swagger2skill/scripts/extract_categories.py")
    result = subprocess.run(
        [sys.executable, str(script), spec_url],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

# 在 Claude Code 中使用
categories_data = extract_categories("https://tmp-airflow.momenta.works/api/v1/openapi.json")
print(f"Found {categories_data['total']} categories")
```

## 文件说明

### 核心文件

| 文件 | 用途 | 特点 |
|-----|------|------|
| `extract_categories.py` | 提取 OpenAPI categories | 纯数据提取，无交互 |
| `swagger2skill_claude.py` | 完整交互式工作流 | 包含所有交互步骤 |
| `swagger2skill_ask.py` | Claude Code AskUserQuestion 集成 | 可集成到 Claude Code 工具 |
| `swagger2skill.py` | 原始脚本（已改进） | 核心生成逻辑 |

### 支持文件

- `openapi_parser.py` - OpenAPI 规范解析
- `skill_generator.py` - Skill 生成引擎

## 测试结果

### 验证 extract_categories.py

```bash
$ python3 extract_categories.py https://tmp-airflow.momenta.works/api/v1/openapi.json

✅ 输出示例：
{
  "categories": [
    {"name": "Config", "endpoint_count": 2},
    {"name": "Connection", "endpoint_count": 6},
    {"name": "DAG", "endpoint_count": 12},
    ...
    {"name": "XCom", "endpoint_count": 2}
  ],
  "total": 19
}
```

✅ 测试通过：
- ✓ 正常提取 19 个 categories
- ✓ 返回有效的 JSON 格式
- ✓ 每个 category 包含 endpoint 计数

## 工作流示例

### 场景：生成 Airflow API Skill

```bash
# 运行完整工作流
$ python3 swagger2skill_claude.py https://tmp-airflow.momenta.works/api/v1/openapi.json

# 交互式步骤

🚀 Swagger to Skill Generator
============================================================

📦 Using OpenAPI source: https://tmp-airflow.momenta.works/api/v1/openapi.json

============================================================
📖 OpenAPI Categories Extracted
============================================================

✅ Found 19 API categories:

   1. Config (2 endpoints)
   2. Connection (6 endpoints)
   3. DAG (12 endpoints)
   ...
   19. XCom (2 endpoints)

============================================================
🎯 Category Selection
============================================================

Select categories:
1. All categories
2. Custom selection

👉 Your choice (1 or 2): 1

✅ Selected all 19 categories

============================================================
💾 Skill Details
============================================================

👉 Skill name (kebab-case, e.g., 'airflow-api'): airflow-api
👉 Output directory (default: /Users/ppsteven/projects/skills):

============================================================
⚙️  Generating Skill
============================================================

✅ Skill Generation Complete!

📍 Skill location: /Users/ppsteven/projects/skills/airflow-api

📋 Generated Files:
   • SKILL.md - Skill documentation
   • scripts/cli_tool.py - CLI wrapper for selected APIs
   • references/api_endpoints.md - API reference

📚 Next Steps:
   1. Review the generated skill files
   2. Test the CLI tool locally
   3. Commit to repository if needed
```

## Claude Code 集成

当使用 Claude Code 时，可以直接调用这些脚本：

```bash
# 在 Claude Code 中执行
python3 /Users/ppsteven/Projects/skills/swagger2skill/scripts/extract_categories.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json

# 或完整工作流
python3 /Users/ppsteven/Projects/skills/swagger2skill/scripts/swagger2skill_claude.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json
```

## 常见问题

### Q: 脚本还会出现 EOF 错误吗？
**A:** 不会。我们已经移除了所有 `input()` 调用的依赖，并分离了交互流程。

### Q: 需要安装额外依赖吗？
**A:** 不需要。使用现有的依赖即可：`requests`, `PyYAML`, `jsonschema`

### Q: 如何只提取 categories 而不生成 skill？
**A:** 使用 `extract_categories.py`：
```bash
python3 extract_categories.py <openapi-url>
```

### Q: 如何使用自定义 category 选择？
**A:** 运行 `swagger2skill_claude.py` 并选择"2. Custom selection"，然后输入 category 编号或名称。

## 下一步

推荐在 Claude Code 中使用本 workflow：

1. ✅ 用户提供 OpenAPI URL
2. ✅ Claude Code 调用 `extract_categories.py` 获取 categories
3. 🎯 使用 `AskUserQuestion` 让用户选择
4. ⚙️ 调用 `swagger2skill_claude.py` 生成 skill

参考 `WORKFLOW.md` 了解详细的架构设计。
