---
name: swagger2skill
description: Generate reusable Claude skills from Swagger/OpenAPI specifications. Use AskUserQuestion for interactive category selection, then generate complete skills with CLI tools and documentation.
---

# Swagger to Skill Generator

**IMPORTANT:** This skill provides an interactive workflow for Claude Code to generate production-ready skills from OpenAPI specifications. Follow the steps exactly as described.

---

## When to Use This Skill

Use this skill when the user:
- Provides an OpenAPI/Swagger specification URL or file path
- Asks to "create a skill from OpenAPI spec"
- Wants to generate API wrappers or CLI tools from API specifications
- References generating skills from Swagger/OpenAPI documentation

---

## Workflow Overview

```
User provides OpenAPI URL
         ↓
[Step 1] Parse spec and extract categories
         ↓
[Step 2] AskUserQuestion: All categories or custom selection?
         ↓
   ┌─────┴─────┐
   ↓           ↓
 "All"      "Custom"
   ↓           ↓
   |    [Step 3] AskUserQuestion (multiSelect): Choose categories
   |           ↓
   └─────┬─────┘
         ↓
[Step 4] AskUserQuestion: Skill name and output directory
         ↓
[Step 5] Generate skill files
         ↓
[Step 6] Verify and report completion
```

---

## Step-by-Step Instructions

### Step 1: Parse OpenAPI Specification

When the user provides an OpenAPI URL or file path, extract all available categories.

**Action:**
```bash
python3 swagger2skill/scripts/swagger2skill.py <openapi-url-or-file>
```

**Expected Output:**
```
============================================================
📖 OpenAPI Categories
============================================================

✅ Found 19 API categories:

   1. Config (3 endpoints)
   2. Connection (6 endpoints)
   3. DAG (12 endpoints)
   4. DAGRun (9 endpoints)
   5. Role (5 endpoints)
   ... and 14 more
```

**Parse this output** to extract:
- Total number of categories
- List of category names
- Endpoint count for each category

**Store this information** for use in the next steps.

---

### Step 2: Ask User for Selection Method

Use `AskUserQuestion` to ask how the user wants to select categories.

**REQUIRED:** Use the AskUserQuestion tool with this exact structure:

```json
{
  "questions": [
    {
      "question": "How would you like to select API categories?",
      "header": "Selection",
      "multiSelect": false,
      "options": [
        {
          "label": "All categories",
          "description": "Include all <N> categories found in the OpenAPI specification"
        },
        {
          "label": "Custom selection",
          "description": "Choose specific categories to include in the generated skill"
        }
      ]
    }
  ]
}
```

**Replace `<N>`** with the actual number of categories found.

**Handle Response:**
- If user selects **"All categories"**: Set `selected_categories = all_categories`
- If user selects **"Custom selection"**: Proceed to Step 3

---

### Step 3: Ask User to Select Categories (Custom Selection Only)

**ONLY run this step if the user chose "Custom selection" in Step 2.**

Use `AskUserQuestion` with `multiSelect: true` to let the user choose multiple categories.

**REQUIRED:** Use the AskUserQuestion tool with this structure:

```json
{
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
          "description": "12 endpoints - DAG management"
        }
        // ... one option for each category
      ]
    }
  ]
}
```

**How to Build Options:**
- For each category from Step 1, create an option with:
  - `label`: Category name (exactly as parsed)
  - `description`: "<count> endpoints - <brief description>"
  - If no description is available, use: "<count> endpoints"

**Handle Response:**
- Extract the list of selected category labels
- Store as `selected_categories`

---

### Step 4: Ask for Skill Configuration

Use `AskUserQuestion` to get skill name and output directory.

**REQUIRED:** Use the AskUserQuestion tool with this structure:

```json
{
  "questions": [
    {
      "question": "What should the skill be named? (Use kebab-case, e.g., airflow-api, github-api)",
      "header": "Skill Name",
      "multiSelect": false,
      "options": [
        {
          "label": "Use suggested name",
          "description": "Auto-generated name based on API: <suggested-name>"
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
}
```

**Suggest a skill name** based on the OpenAPI spec title or URL:
- Extract API name from spec (if available)
- Convert to kebab-case
- Example: "Airflow API" → "airflow-api"

**Handle Response:**
- If user selects "Custom name" or "Custom directory", use the text they provide
- Otherwise, use the suggested defaults

**Validation:**
- Skill name must be kebab-case (lowercase with hyphens)
- Output directory must exist or be creatable

---

### Step 5: Generate Skill Files

Now generate the complete skill using the Python generator.

**Prepare Data:**

1. **Parse the OpenAPI spec again** to get full category details:
   ```bash
   python3 swagger2skill/scripts/openapi_parser.py <openapi-url-or-file>
   ```

2. **Load categories JSON** (output from openapi_parser.py)

3. **Build the command** to invoke skill_generator.py:
   ```bash
   python3 swagger2skill/scripts/skill_generator.py \
     <skill-name> \
     <output-dir> \
     '<categories-json>' \
     '<selected-categories-json>'
   ```

**Example:**
```bash
python3 swagger2skill/scripts/skill_generator.py \
  airflow-api \
  /Users/ppsteven/Projects/skills \
  '{"Config":[...],"Connection":[...],...}' \
  '["Config","Connection","DAG"]'
```

**Execute the command** and monitor the output.

**Expected Output:**
```
  ✓ Created SKILL.md
  ✓ Created scripts/cli_tool.py
  ✓ Created references/api_endpoints.md
  ✓ Created references/unsupported_categories.md

✅ Skill generated at: /Users/ppsteven/Projects/skills/airflow-api

📁 Structure:
   airflow-api/
   ├── SKILL.md
   ├── scripts/
   │   └── cli_tool.py
   └── references/
       ├── api_endpoints.md
       └── unsupported_categories.md
```

---

### Step 6: Verify and Report Completion

After generation completes, verify the skill and report to the user.

**Verification Checklist:**

1. ✅ **Check files exist:**
   ```bash
   ls -la <output-dir>/<skill-name>/SKILL.md
   ls -la <output-dir>/<skill-name>/scripts/cli_tool.py
   ls -la <output-dir>/<skill-name>/references/api_endpoints.md
   ```

2. ✅ **Verify CLI tool is executable:**
   ```bash
   python3 <output-dir>/<skill-name>/scripts/cli_tool.py --help
   ```

3. ✅ **Count generated commands:**
   ```bash
   grep -c "@.*\.command" <output-dir>/<skill-name>/scripts/cli_tool.py
   ```

**Report to User:**

Provide a completion summary with:
- ✅ Skill name and location
- ✅ Number of categories included
- ✅ Number of CLI commands generated
- ✅ Next steps (how to use the generated skill)

**Example Report:**

```
✅ **Skill Generation Complete!**

**Skill Details:**
- **Name:** airflow-api
- **Location:** `/Users/ppsteven/Projects/skills/airflow-api`
- **Categories:** 3 selected (Config, Connection, DAG)
- **Commands:** 21 CLI commands generated

**Generated Files:**
- `SKILL.md` - Skill documentation
- `scripts/cli_tool.py` - Click-based CLI tool
- `references/api_endpoints.md` - API reference documentation

**Next Steps:**
1. Test the CLI tool:
   ```bash
   python3 airflow-api/scripts/cli_tool.py --help
   ```

2. Install as a skill (optional):
   ```bash
   npx skills add /Users/ppsteven/Projects/skills/airflow-api
   ```

3. Review the generated API documentation:
   ```bash
   cat airflow-api/references/api_endpoints.md
   ```
```

---

## Error Handling

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| "Failed to load OpenAPI specification" | Invalid URL or file path | Verify the URL is accessible or file exists |
| "No categories found" | Spec doesn't use `tags` field | Check OpenAPI spec format; tags are required for categorization |
| "Invalid skill name" | Name not in kebab-case | Convert to lowercase with hyphens (e.g., "mySkill" → "my-skill") |
| "Directory not found" | Output path doesn't exist | Create the directory or use an existing path |

### Debugging

If generation fails:

1. **Check OpenAPI spec validity:**
   ```bash
   python3 -c "import json, requests; print(json.dumps(requests.get('<url>').json(), indent=2))"
   ```

2. **Verify parser output:**
   ```bash
   python3 swagger2skill/scripts/swagger2skill.py <url>
   ```

3. **Check Python dependencies:**
   ```bash
   python3 -c "import click, requests; print('OK')"
   ```

---

## Important Notes

### AskUserQuestion Usage

- **Always use AskUserQuestion** for category selection (Step 2 and Step 3)
- **Never skip the interactive selection** - it's a core requirement per goal.md
- **Provide meaningful descriptions** for each option to help users make informed choices

### Category Selection Best Practices

- **Show endpoint counts** in option descriptions to help users understand scope
- **Use multiSelect: true** in Step 3 to allow multiple category selection
- **Preserve exact category names** from the OpenAPI spec (case-sensitive)

### Output Validation

- **Always verify** generated files exist and are valid
- **Test the CLI tool** with `--help` before reporting success
- **Count generated commands** to confirm all endpoints were processed

---

## Script Locations

All Python scripts are in the `swagger2skill/scripts/` directory:

- **swagger2skill.py** - Main script: extracts and displays categories
- **openapi_parser.py** - Parser: extracts full category/endpoint details
- **skill_generator.py** - Generator: creates skill files and CLI tool
- **cli_command_generator.py** - (Future use) Single-category CLI generator for parallel processing

---

## Generated Skill Structure

Each generated skill follows this structure:

```
<skill-name>/
├── SKILL.md                       # Skill metadata and usage documentation
├── scripts/
│   └── cli_tool.py               # Complete Click CLI implementation
├── references/
│   ├── api_endpoints.md          # API reference for selected categories
│   └── unsupported_categories.md # Documentation of excluded categories
└── assets/                        # (Optional) Additional resources
```

---

## Testing the Generated Skill

After generation, test the skill with these commands:

```bash
# 1. View help
python3 <skill-name>/scripts/cli_tool.py --help

# 2. View category commands
python3 <skill-name>/scripts/cli_tool.py <category> --help

# 3. Execute a command (example)
python3 <skill-name>/scripts/cli_tool.py config get-config --help
```

---

## Future Enhancements (Not Yet Implemented)

⚠️ The following features are planned but **not yet implemented**:

- **Parallel CLI generation** using tasks + subagents (see goal.md 步骤 5)
- **Automatic skill validation** using skill-creator skill (see goal.md 步骤 6)
- **CLI command generator agents** for each category (cli_command_generator.py exists but not integrated)

These will be implemented in Phase 2 after AskUserQuestion integration is complete and tested.

---

## Summary

This skill automates skill generation from OpenAPI specs with:

✅ **Interactive category selection** via AskUserQuestion
✅ **Multi-select support** for custom category choices
✅ **Automatic CLI generation** with Click commands for each endpoint
✅ **Complete documentation** including API references
✅ **Verification and testing** of generated skills

Follow the 6-step workflow exactly as documented to ensure proper skill generation.
