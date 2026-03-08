# Swagger2Skill Implementation Gap Analysis

**Date:** 2026-03-08
**Scope:** Compare current implementation vs. goal.md requirements
**Status:** ⚠️ **IMPLEMENTATION INCOMPLETE**

---

## Executive Summary

The current swagger2skill implementation is a **standalone Python CLI tool** that uses terminal-based prompts (`input()`), while goal.md requires a **Claude Code-integrated workflow** using the `AskUserQuestion` tool for interactive selection and parallel agent processing for CLI generation.

**Critical Gap:** The fundamental interaction model is different between current implementation and requirements.

---

## Detailed Comparison

### Goal.md Requirements (Target)

```
步骤 1: 输入 URL
  └─ 用户提供 OpenAPI 规范 URL

步骤 2: 解析并提取 categories
  └─ openapi_parser.py 获取所有 category 列表

步骤 3: 使用 AskUserQuestion 询问选择方式
  └─ 选项 A: 全部 categories (不提)
  └─ 选项 B: 自定义选择 N 个

步骤 4: 获取用户选择
  └─ 若选"全部" → 使用所有 categories
  └─ 若选"自定义" → 列出每个 category 让用户多选

步骤 5: 循环生成 CLI 命令
  └─ 对每个 category
    ├─ 获取所有 endpoints
    ├─ 对每个 endpoint
    │ ├─ 解析参数信息
    │ ├─ 生成 Click 命令定义
    │ └─ 生成对应的 API 调用代码
    └─ 生成该 category 的完整命令组

步骤 6: 验证和生成最终 skill
  └─ 使用 skill-creator 技能验证符合规范
```

**关键改动:**
- 替换当前的 `prompt_category_selection()` 为 `AskUserQuestion` 调用
- 支持批量选择（`multiSelect: true`）
- 显示每个 category 的端点数量作为参考

---

### Current Implementation (Actual)

#### File Structure

```
swagger2skill/
├── SKILL.md                          # ✅ Documented as CLI tool
├── scripts/
│   ├── swagger2skill.py             # ❌ Only displays categories, no selection
│   ├── openapi_parser.py            # ✅ Parses OpenAPI spec
│   ├── skill_generator.py           # ⚠️ Serial CLI generation, no parallelism
│   └── cli_command_generator.py     # ⚠️ Prepared but unused for parallel execution
```

#### Step-by-Step Analysis

| Step | Goal.md Requirement | Current Implementation | Status |
|------|-------------------|----------------------|--------|
| 1 | 输入 URL | ✅ `swagger2skill.py` accepts URL/file path | ✅ **PASS** |
| 2 | 解析并提取 categories | ✅ `openapi_parser.py` extracts categories | ✅ **PASS** |
| 3 | 使用 AskUserQuestion 询问选择方式 | ❌ **Not implemented** - uses CLI prompts instead | ❌ **FAIL** |
| 4 | 获取用户选择 (全部/自定义) | ❌ **Not implemented** - no AskUserQuestion integration | ❌ **FAIL** |
| 5 | 循环生成 CLI 命令 | ⚠️ `skill_generator.py._generate_cli_commands()` - **serial execution** | ⚠️ **INCOMPLETE** |
| 6 | 验证和生成最终 skill | ✅ `skill_generator.generate()` creates complete skill | ✅ **PASS** |

---

## Problem 1: Missing AskUserQuestion Integration

### Current Approach (CLI-based)

The current `swagger2skill.py` is designed as a **standalone Python script**:

```python
# swagger2skill.py (lines 63-77)
def main():
    if len(sys.argv) < 2:
        print("❌ OpenAPI source is required", file=sys.stderr)
        sys.exit(1)

    spec_source = sys.argv[1]
    parser, categories = fetch_and_parse_openapi(spec_source)
    display_categories(parser, categories)
```

**What it does:**
- ✅ Parses OpenAPI spec
- ✅ Displays categories
- ❌ **Does NOT ask for user selection**
- ❌ **Does NOT use AskUserQuestion**

### Expected Approach (Claude Code Integration)

According to goal.md, the workflow should be:

```
1. User provides URL to Claude Code
2. Claude Code calls swagger2skill.py to extract categories
3. Claude Code uses AskUserQuestion with:
   - Question: "How do you want to select categories?"
   - Option A: "All categories" (全部)
   - Option B: "Custom selection" (自定义选择)
4. If "Custom selection":
   - Claude Code uses AskUserQuestion with multiSelect: true
   - Lists all categories with endpoint counts
   - User checks desired categories
5. Claude Code passes selected categories to skill_generator.py
```

**Implementation Status:** ❌ **NOT IMPLEMENTED**

---

## Problem 2: Serial CLI Generation (Not Parallel)

### Current Approach (Serial)

In `skill_generator.py`, line 384-414:

```python
def _generate_cli_commands(self) -> str:
    """Generate Click CLI commands for each endpoint in each category."""
    commands = []

    for category in self.selected_categories:  # ← Serial loop
        category_slug = self._slugify(category)
        endpoints = self.categories.get(category, [])

        # Create category group
        commands.append(f'''...''')

        # Generate command for each endpoint
        if endpoints:
            for endpoint in endpoints:  # ← Nested serial loop
                cmd = self._generate_endpoint_implementation(endpoint, category_slug)
                commands.append(cmd)

    return '\n'.join(commands)
```

**Execution Model:**
- ⏳ Serial for loop through categories
- ⏳ Serial for loop through endpoints
- ❌ No parallelism
- ❌ No task breakdown
- ❌ No subagent usage

### Expected Approach (Parallel with Tasks + Subagents)

According to goal.md 步骤 5 and user requirement #2:

```
Claude Code should:

1. Create TaskList for all categories
   ├─ Task 1: Generate CLI commands for category "Config"
   ├─ Task 2: Generate CLI commands for category "Connection"
   ├─ Task 3: Generate CLI commands for category "DAG"
   └─ Task N: Generate CLI commands for category "..."

2. Spawn parallel agents using Agent tool:
   - Each agent executes: cli_command_generator.py <category> <spec-path>
   - Agents run in parallel (not sequential)
   - Each agent returns generated command code as JSON

3. Collect results from all agents

4. Assemble final cli_tool.py from all command code blocks
```

**Implementation Status:** ⚠️ **PARTIALLY PREPARED**

- ✅ `cli_command_generator.py` exists and can handle single category
- ❌ No orchestration logic to call it in parallel
- ❌ No TaskList creation
- ❌ No Agent tool invocation

---

## Root Cause Analysis

### Architectural Mismatch

| Design Aspect | Goal.md | Current Implementation |
|--------------|---------|----------------------|
| **Execution Environment** | Claude Code (agent-driven) | Standalone Python CLI |
| **User Interaction** | AskUserQuestion tool | Terminal `input()` prompts |
| **CLI Generation** | Parallel (tasks + agents) | Serial (for loops) |
| **Category Selection** | Interactive multi-select | Command-line arguments |

### Why This Matters

The current implementation is a **good Python CLI tool**, but it's **not integrated with Claude Code workflows**.

Goal.md expects the skill to be **invoked by Claude Code**, which:
1. Uses `AskUserQuestion` for interactive selection (not terminal prompts)
2. Spawns parallel agents for CLI generation (not for loops)
3. Uses task management for tracking progress

---

## Recommendations

### Priority 1: Implement AskUserQuestion Integration

**Action Required:**

Create a new orchestration layer in the swagger2skill skill that:

1. Accepts OpenAPI URL from user
2. Calls `swagger2skill.py` to extract categories
3. Uses `AskUserQuestion` to present selection options:
   ```python
   questions = [{
       "question": "How would you like to select API categories?",
       "header": "Selection Mode",
       "multiSelect": false,
       "options": [
           {
               "label": "All categories",
               "description": "Include all 19 categories found in the spec"
           },
           {
               "label": "Custom selection",
               "description": "Choose specific categories to include"
           }
       ]
   }]
   ```

4. If "Custom selection", use second `AskUserQuestion` with `multiSelect: true`:
   ```python
   questions = [{
       "question": "Which categories do you want to include?",
       "header": "Categories",
       "multiSelect": true,
       "options": [
           {"label": "Config", "description": "3 endpoints"},
           {"label": "Connection", "description": "6 endpoints"},
           {"label": "DAG", "description": "12 endpoints"},
           # ... all categories
       ]
   }]
   ```

**Location:** Create new file `swagger2skill/SKILL.md` with orchestration instructions

### Priority 2: Implement Parallel CLI Generation

**Action Required:**

Modify the CLI generation flow to use tasks + parallel agents:

1. **Create task list** for each selected category
   ```python
   for category in selected_categories:
       TaskCreate(
           subject=f"Generate CLI commands for {category}",
           description=f"Generate Click commands for all endpoints in {category} category"
       )
   ```

2. **Spawn parallel agents** using Agent tool
   ```python
   for category in selected_categories:
       Agent(
           prompt=f"Run cli_command_generator.py {category} {spec_path}",
           run_in_background=True  # Enable parallelism
       )
   ```

3. **Collect results** from all agents
   - Parse JSON output from each agent
   - Assemble final `cli_tool.py`

**Location:** Modify `skill_generator.py` or create new orchestration script

---

## Next Steps

1. ✅ **Acknowledge the gap** - Current implementation ≠ goal.md requirements
2. 🔄 **Decide on approach:**
   - Option A: Keep Python CLI tool as-is (document as CLI-only tool)
   - Option B: Build Claude Code integration layer (implement goal.md)
3. 📝 **Update documentation** to reflect actual capabilities vs. planned features
4. 🛠️ **Implement missing features** if Option B is chosen

---

## Conclusion

**Status:** ⚠️ The current swagger2skill implementation is **incomplete** according to goal.md requirements.

**Key Gaps:**
1. ❌ No AskUserQuestion integration (uses CLI prompts instead)
2. ❌ No parallel agent processing (uses serial for loops instead)
3. ❌ Not integrated with Claude Code task management

**Recommendation:** Implement Priority 1 (AskUserQuestion) first, then Priority 2 (parallel agents), to align with goal.md specifications.
