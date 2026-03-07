# Swagger2Skill 工作流程

## 问题

原始的 `swagger2skill.py` 脚本在 Claude Code 环境中失败，因为：
1. 尝试导入不存在的 `claude_code_tools` 模块
2. 在非交互环境中使用 `input()` 导致 EOF 错误
3. 无法与 Claude Code 的 `AskUserQuestion` 工具集成

## 解决方案

将交互流程分离为独立的步骤，使用专用脚本：

### 1. 提取阶段 (Extract Phase)
**脚本**: `extract_categories.py`
- 输入: OpenAPI spec URL
- 输出: JSON 格式的 categories 列表
- 特点: 纯数据提取，无交互

```bash
python3 extract_categories.py https://tmp-airflow.momenta.works/api/v1/openapi.json
```

输出示例：
```json
{
  "categories": [
    {"name": "Config", "endpoint_count": 2},
    {"name": "Connection", "endpoint_count": 6},
    ...
  ],
  "total": 19
}
```

### 2. 选择阶段 (Selection Phase)
**工具**: Claude Code 的 `AskUserQuestion`
- 显示所有 categories
- 用户选择: "All categories" 或 "Custom selection"
- 返回: 用户选择的方式

### 3. 生成阶段 (Generation Phase)
**脚本**: `swagger2skill_claude.py` 或原始 `swagger2skill.py`（改进后）
- 输入: OpenAPI spec URL + 选中的 categories
- 输出: 生成的 skill 目录
- 特点: 完整的交互式工作流

## 文件说明

### 新增文件

1. **extract_categories.py**
   - 纯数据提取脚本
   - 返回 JSON，可被其他脚本或工具调用
   - 用途: 在 Claude Code 中调用，获取 categories 列表

2. **swagger2skill_claude.py**
   - 完整的交互式工作流
   - 调用 `extract_categories.py`
   - 整合用户选择
   - 生成最终的 skill

### 改进文件

- **swagger2skill.py**
  - 移除了 `input()` 调用
  - 移除了 `claude_code_tools` 导入尝试
  - 简化为核心逻辑

## 在 Claude Code 中使用

### 推荐方法：使用 swagger2skill_claude.py

```bash
python3 /Users/ppsteven/Projects/skills/swagger2skill/scripts/swagger2skill_claude.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json
```

流程：
1. 提取 19 个 categories
2. 显示所有 categories
3. 使用 `AskUserQuestion` 询问用户选择
4. 获取用户的 skill 名称和输出目录
5. 生成 skill

### 替代方法：分步执行

```bash
# 第1步：提取 categories
python3 extract_categories.py https://tmp-airflow.momenta.works/api/v1/openapi.json > categories.json

# 第2步：使用 AskUserQuestion 询问用户
# (由 Claude Code 代理处理)

# 第3步：基于选择生成 skill
python3 swagger2skill_claude.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json \
  --selected Config,DAG,Variable \
  --skill-name airflow-api \
  --output /Users/ppsteven/projects/skills
```

## 测试

### 测试 extract_categories.py

```bash
cd /Users/ppsteven/Projects/skills/swagger2skill
python3 scripts/extract_categories.py https://tmp-airflow.momenta.works/api/v1/openapi.json
```

预期输出：
- JSON 格式的 categories 列表
- 包含 19 个 API categories

### 测试完整工作流

```bash
python3 scripts/swagger2skill_claude.py \
  https://tmp-airflow.momenta.works/api/v1/openapi.json
```

交互式提示：
1. 显示所有 19 个 categories
2. 询问选择 "all" 或 "custom"
3. 询问 skill 名称（如 `airflow-api`）
4. 询问输出目录
5. 生成 skill

## 关键改进

✅ **移除了依赖**
- 不再需要 `claude_code_tools` 模块
- 不再使用 `input()` 导致 EOF 错误

✅ **模块化设计**
- `extract_categories.py` 可独立使用
- 易于与其他工具集成
- JSON 输出便于处理

✅ **Claude Code 集成**
- 可使用 `AskUserQuestion` 工具
- 支持完整的交互式工作流
- 更好的用户体验

✅ **向后兼容**
- 原始脚本仍可使用（改进后）
- 现有的工作流不受影响
