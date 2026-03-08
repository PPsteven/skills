# Swagger2Skill Usage Example with AskUserQuestion Integration

**Date:** 2026-03-08
**Purpose:** Demonstrate complete workflow with AskUserQuestion integration
**Status:** ✅ Implemented and tested

---

## Overview

This document demonstrates how Claude Code should use the swagger2skill skill with AskUserQuestion integration to generate skills from OpenAPI specifications.

---

## Complete Workflow Example

### User Request

```
User: "Generate a skill from this OpenAPI spec: https://example.com/api/openapi.json"
```

---

### Step 1: Extract Categories

**Claude Code Action:**

```bash
python3 swagger2skill/scripts/swagger2skill.py https://example.com/api/openapi.json --json
```

**Expected JSON Output:**

```json
{
  "total_categories": 5,
  "categories": [
    {
      "name": "Config",
      "endpoint_count": 3,
      "endpoints": [
        {
          "method": "GET",
          "path": "/config",
          "summary": "Get configuration",
          "operationId": "getConfig"
        },
        {
          "method": "POST",
          "path": "/config",
          "summary": "Update configuration",
          "operationId": "updateConfig"
        },
        {
          "method": "DELETE",
          "path": "/config",
          "summary": "Reset configuration",
          "operationId": "resetConfig"
        }
      ]
    },
    {
      "name": "Connection",
      "endpoint_count": 6,
      "endpoints": [...]
    },
    {
      "name": "DAG",
      "endpoint_count": 12,
      "endpoints": [...]
    },
    {
      "name": "Variable",
      "endpoint_count": 5,
      "endpoints": [...]
    },
    {
      "name": "Pool",
      "endpoint_count": 4,
      "endpoints": [...]
    }
  ]
}
```

**Claude Code Processing:**

1. Parse JSON output
2. Extract `total_categories` (5)
3. Extract category names and endpoint counts
4. Prepare for AskUserQuestion

---

### Step 2: Ask Selection Method

**Claude Code Action:**

Use AskUserQuestion to ask how the user wants to select categories.

```python
# Pseudocode - actual call uses AskUserQuestion tool
AskUserQuestion({
  "questions": [
    {
      "question": "How would you like to select API categories?",
      "header": "Selection",
      "multiSelect": false,
      "options": [
        {
          "label": "All categories",
          "description": "Include all 5 categories found in the OpenAPI specification"
        },
        {
          "label": "Custom selection",
          "description": "Choose specific categories to include in the generated skill"
        }
      ]
    }
  ]
})
```

**User Response (Example 1 - All Categories):**

```json
{
  "Selection": "All categories"
}
```

→ **Skip to Step 4** (no need for Step 3)

**User Response (Example 2 - Custom Selection):**

```json
{
  "Selection": "Custom selection"
}
```

→ **Continue to Step 3**

---

### Step 3: Multi-Select Categories (Only if Custom Selection)

**Claude Code Action:**

Use AskUserQuestion with `multiSelect: true` to let user choose categories.

```python
# Pseudocode - actual call uses AskUserQuestion tool
AskUserQuestion({
  "questions": [
    {
      "question": "Which API categories do you want to include?",
      "header": "Categories",
      "multiSelect": true,
      "options": [
        {
          "label": "Config",
          "description": "3 endpoints - Configuration management"
        },
        {
          "label": "Connection",
          "description": "6 endpoints - Connection operations"
        },
        {
          "label": "DAG",
          "description": "12 endpoints - DAG management and control"
        },
        {
          "label": "Variable",
          "description": "5 endpoints - Variable operations"
        },
        {
          "label": "Pool",
          "description": "4 endpoints - Pool management"
        }
      ]
    }
  ]
})
```

**User Response:**

```json
{
  "Categories": ["Config", "Connection", "DAG"]
}
```

**Claude Code Processing:**

```python
selected_categories = ["Config", "Connection", "DAG"]
```

---

### Step 4: Ask for Skill Configuration

**Claude Code Action:**

Use AskUserQuestion to get skill name and output directory.

```python
# Pseudocode
AskUserQuestion({
  "questions": [
    {
      "question": "What should the skill be named? (Use kebab-case, e.g., airflow-api, github-api)",
      "header": "Skill Name",
      "multiSelect": false,
      "options": [
        {
          "label": "Use suggested name",
          "description": "Auto-generated name based on API: example-api"
        },
        {
          "label": "Custom name",
          "description": "Enter a custom skill name in kebab-case format"
        }
      ]
    },
    {
      "question": "Where should the skill be created?",
      "header": "Output",
      "multiSelect": false,
      "options": [
        {
          "label": "Current project",
          "description": "/Users/ppsteven/Projects/skills/"
        },
        {
          "label": "Custom directory",
          "description": "Specify a different output directory"
        }
      ]
    }
  ]
})
```

**User Response (Example):**

```json
{
  "Skill Name": "Custom name",
  "Skill Name_notes": "my-api-skill",
  "Output": "Current project"
}
```

**Claude Code Processing:**

```python
skill_name = "my-api-skill"
output_dir = "/Users/ppsteven/Projects/skills/"
```

---

### Step 5: Generate Skill Files

**Claude Code Action:**

Now generate the skill using skill_generator.py.

**First, get full categories data:**

```bash
python3 swagger2skill/scripts/openapi_parser.py https://example.com/api/openapi.json
```

This outputs the full categories JSON with complete endpoint definitions.

**Then, prepare parameters:**

```python
# From previous steps
skill_name = "my-api-skill"
output_dir = "/Users/ppsteven/Projects/skills/"
selected_categories = ["Config", "Connection", "DAG"]

# From openapi_parser.py output
categories_json = {...}  # Full category data

# Convert to JSON strings
categories_json_str = json.dumps(categories_json)
selected_categories_json_str = json.dumps(selected_categories)
```

**Execute generator:**

```bash
python3 swagger2skill/scripts/skill_generator.py \
  "my-api-skill" \
  "/Users/ppsteven/Projects/skills/" \
  '{"Config":[...],"Connection":[...],"DAG":[...]}' \
  '["Config","Connection","DAG"]'
```

**Expected Output:**

```
  ✓ Created SKILL.md
  ✓ Created scripts/cli_tool.py
  ✓ Created references/api_endpoints.md
  ✓ Created references/unsupported_categories.md

✅ Skill generated at: /Users/ppsteven/Projects/skills/my-api-skill

📁 Structure:
   my-api-skill/
   ├── SKILL.md
   ├── scripts/
   │   └── cli_tool.py
   └── references/
       ├── api_endpoints.md
       └── unsupported_categories.md
```

---

### Step 6: Verify and Report

**Claude Code Action:**

Verify the generated skill and report to the user.

**Verification Commands:**

```bash
# 1. Check files exist
ls -la /Users/ppsteven/Projects/skills/my-api-skill/SKILL.md
ls -la /Users/ppsteven/Projects/skills/my-api-skill/scripts/cli_tool.py
ls -la /Users/ppsteven/Projects/skills/my-api-skill/references/api_endpoints.md

# 2. Verify CLI tool is executable
python3 /Users/ppsteven/Projects/skills/my-api-skill/scripts/cli_tool.py --help

# 3. Count generated commands
grep -c "@.*\.command" /Users/ppsteven/Projects/skills/my-api-skill/scripts/cli_tool.py
```

**Expected Results:**

```bash
# File checks
-rw-r--r--  1 user  staff  1234 Mar  8 10:00 SKILL.md
-rwxr-xr-x  1 user  staff  5678 Mar  8 10:00 cli_tool.py
-rw-r--r--  1 user  staff  3456 Mar  8 10:00 api_endpoints.md

# CLI help works
Usage: cli_tool.py [OPTIONS] COMMAND [ARGS]...

  Airflow API CLI Tool

Commands:
  config      Manage Config operations
  connection  Manage Connection operations
  dag         Manage DAG operations

# Command count
21
```

**Final Report to User:**

```
✅ **Skill Generation Complete!**

**Skill Details:**
- **Name:** my-api-skill
- **Location:** `/Users/ppsteven/Projects/skills/my-api-skill`
- **Categories:** 3 selected (Config, Connection, DAG)
- **Commands:** 21 CLI commands generated

**Generated Files:**
- `SKILL.md` - Skill documentation
- `scripts/cli_tool.py` - Click-based CLI tool
- `references/api_endpoints.md` - API reference documentation
- `references/unsupported_categories.md` - Excluded categories (Variable, Pool)

**Next Steps:**

1. Test the CLI tool:
   ```bash
   python3 my-api-skill/scripts/cli_tool.py --help
   python3 my-api-skill/scripts/cli_tool.py config --help
   ```

2. Install as a skill (optional):
   ```bash
   npx skills add /Users/ppsteven/Projects/skills/my-api-skill
   ```

3. Review the generated API documentation:
   ```bash
   cat my-api-skill/references/api_endpoints.md
   ```

The skill is ready to use! 🎉
```

---

## Key Implementation Points

### ✅ Implemented Features

1. **JSON Output Mode**
   - `swagger2skill.py --json` outputs structured category data
   - Claude Code can parse this JSON to build AskUserQuestion options

2. **Multi-Step Selection Flow**
   - Step 2: All vs Custom selection
   - Step 3: Multi-select categories (if Custom)
   - Step 4: Skill name and output directory

3. **Complete Skill Generation**
   - skill_generator.py creates all necessary files
   - CLI tool with Click commands for each endpoint
   - API reference documentation

### ⚠️ Not Yet Implemented

1. **Parallel CLI Generation**
   - Current implementation: Serial for-loop in skill_generator.py
   - Planned: Tasks + parallel agents using cli_command_generator.py

2. **Automatic Skill Validation**
   - Planned: Use skill-creator skill to validate generated skill

3. **Enhanced Error Handling**
   - More robust validation of user inputs
   - Better error messages for common issues

---

## Testing the Implementation

### Manual Test (Human-Readable Output)

```bash
cd /Users/ppsteven/Projects/skills/swagger2skill
python3 scripts/swagger2skill.py test_openapi.json
```

**Expected Output:**

```
============================================================
📖 OpenAPI Categories
============================================================

✅ Found 2 API categories:

   1. Configuration (1 endpoints)
   2. Users (4 endpoints)
```

### Manual Test (JSON Output)

```bash
python3 scripts/swagger2skill.py test_openapi.json --json
```

**Expected Output:**

```json
{
  "total_categories": 2,
  "categories": [
    {
      "name": "Configuration",
      "endpoint_count": 1,
      "endpoints": [
        {
          "method": "GET",
          "path": "/config",
          "summary": "Get system configuration",
          "operationId": "getConfig"
        }
      ]
    },
    {
      "name": "Users",
      "endpoint_count": 4,
      "endpoints": [...]
    }
  ]
}
```

---

## Integration with Claude Code

When a user provides an OpenAPI URL, Claude Code should:

1. **Recognize the task** - User wants to generate a skill from OpenAPI spec
2. **Invoke swagger2skill skill** - Follow the workflow in SKILL.md
3. **Use AskUserQuestion** - For all user selections (not terminal prompts)
4. **Parse JSON output** - From swagger2skill.py --json
5. **Generate and verify** - Create skill and verify it works

**Important:** This is a **Claude Code-driven workflow**, not a standalone Python CLI workflow.

---

## Conclusion

✅ **AskUserQuestion integration is now implemented** and ready to use.

The workflow provides:
- Interactive category selection
- Multi-select support for custom choices
- Structured JSON output for parsing
- Complete skill generation
- Verification and reporting

**Next Phase:** Implement parallel CLI generation (tasks + agents) as described in goal.md 步骤 5.
