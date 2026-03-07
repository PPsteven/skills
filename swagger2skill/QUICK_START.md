# Swagger2Skill - 快速开始

## 最简单的方法

```bash
python3 scripts/swagger2skill.py <openapi-url>
```

就这样！脚本会：
1. ✅ 提取 categories
2. ✅ 显示所有 categories
3. ✅ 让你选择"All"或"Custom"
4. ✅ 生成 skill

---

## 示例：生成 Airflow API Skill

```bash
cd /Users/ppsteven/Projects/skills/swagger2skill

python3 scripts/swagger2skill.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json
```

### 交互步骤

```
🚀 Swagger to Skill Generator

📦 Using OpenAPI source: https://tmp-airflow.momenta.works/api/v1/openapi.json

📖 Parsing OpenAPI Specification

✅ Found 19 API categories:
   1. Config (2 endpoints)
   2. Connection (6 endpoints)
   ...
   19. XCom (2 endpoints)

🎯 Category Selection

Select categories:
1. All categories
2. Custom selection (enter numbers or names)

👉 Your choice (1 or 2): 1

✅ Selected all 19 categories

💾 Skill Details

👉 Skill name (kebab-case, e.g., 'airflow-api'): airflow-api
👉 Output directory (default: /Users/ppsteven/projects/skills):

⚙️  Generating Skill
✓ Created SKILL.md
✓ Created scripts/cli_tool.py
✓ Created references/api_endpoints.md

✅ Skill generated at: /Users/ppsteven/projects/skills/airflow-api
```

---

## 其他用法

### 仅提取 Categories（不生成 Skill）

```bash
python3 scripts/main.py <openapi-url> --extract-only
```

### 获取原始 JSON 数据

```bash
python3 scripts/extract_categories.py <openapi-url>
```

输出：
```json
{
  "categories": [
    {"name": "Config", "endpoint_count": 2},
    ...
  ],
  "total": 19
}
```

### 自定义 Categories 选择

运行脚本后，选择选项 2：
```
👉 Your choice (1 or 2): 2
👉 Enter category numbers/names (comma-separated, e.g., '1,2,3' or 'dag,variable'): 1,3,5
```

或使用 categories 名称：
```
👉 Enter category numbers/names: Config,DAG,Variable
```

---

## 在 Claude Code 中使用

在 Claude Code 终端中运行：

```bash
python3 /Users/ppsteven/Projects/skills/swagger2skill/scripts/swagger2skill.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json
```

或如果脚本在技能目录中：

```bash
python3 ~/.claude/skills/swagger2skill/scripts/swagger2skill.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json
```

---

## 常见命令

| 场景 | 命令 |
|------|------|
| 快速生成 skill | `python3 scripts/swagger2skill.py <url>` |
| 仅查看 categories | `python3 scripts/main.py <url> --extract-only` |
| 获取 JSON 数据 | `python3 scripts/extract_categories.py <url>` |
| 自定义选择 | 运行脚本后选择选项 2 |
| 显示帮助 | `python3 scripts/swagger2skill.py --help` |

---

## 生成的 Skill 位置

默认生成位置：
```
/Users/ppsteven/projects/skills/<skill-name>/
```

例如 airflow-api:
```
/Users/ppsteven/projects/skills/airflow-api/
├── SKILL.md
├── scripts/cli_tool.py
└── references/api_endpoints.md
```

---

## 支持的 OpenAPI 版本

- ✅ OpenAPI 3.0
- ✅ Swagger 2.0
- ✅ 本地文件路径
- ✅ HTTP/HTTPS URL

---

## 故障排除

### 问题：超时错误
**解决：** 检查 URL 是否可访问，增加超时时间

### 问题：No categories found
**解决：** 确保 OpenAPI spec 格式正确，包含 operations

### 问题：Directory does not exist
**解决：** 确保输出目录存在，或使用默认目录

---

## 下一步

1. ✅ 查看生成的 `SKILL.md` 文件
2. ✅ 测试生成的 CLI 工具
3. ✅ 根据需要修改生成的文件
4. ✅ 提交到 Git 仓库

---

## 更多帮助

- **工作流详解**: 参考 `WORKFLOW.md`
- **完整使用指南**: 参考 `USAGE_IN_CLAUDE_CODE.md`
- **问题修复说明**: 参考 `FIX_SUMMARY.md`
- **测试报告**: 参考 `docs/reports/test-execution-*.md`

---

**准备好了？** 现在就试试吧！

```bash
python3 scripts/swagger2skill.py https://tmp-airflow.momenta.works/api/v1/openapi.json
```
