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

### Step 5: Generate CLI Commands Using AI

**IMPORTANT:** This step uses Claude Code to intelligently generate CLI commands for each category in parallel. Do NOT use automated script generation - use AI to write high-quality, contextual code.

#### 5.1 Create Tasks for Parallel Generation

For each selected category, create a task to generate its CLI commands.

**Example:** If user selected `["Config", "Connection", "DAG"]`, create 3 tasks:

```python
# Pseudocode - use TaskCreate tool
for category in selected_categories:
    TaskCreate(
        subject=f"Generate CLI commands for {category} category",
        activeForm=f"Generating {category} CLI commands",
        description=f"""
Generate Click CLI commands for the {category} category from OpenAPI spec.

Steps:
1. Get category details: python3 swagger2skill/scripts/get_category_details.py <spec-url> {category}
2. Parse the JSON output to understand all endpoints and parameters
3. Write Click CLI command code for each endpoint with proper:
   - Command names (kebab-case from operationId)
   - Parameter decorators (@click.option, @click.argument)
   - Type conversions (click.INT, click.FLOAT, click.BOOL)
   - Help text from descriptions
   - API request construction
4. Output the complete Click command group code
"""
    )
```

#### 5.2 Execute Tasks in Parallel

For each task, follow this workflow:

**Step 1: Get Category Details**

```bash
python3 swagger2skill/scripts/get_category_details.py <openapi-url-or-file> <category-name>
```

**Example Output:**
```json
{
  "category_name": "Config",
  "endpoint_count": 3,
  "endpoints": [
    {
      "path": "/config",
      "method": "GET",
      "summary": "Get configuration",
      "operationId": "getConfig",
      "description": "Retrieve system configuration",
      "parameters": [
        {
          "name": "format",
          "in": "query",
          "required": false,
          "description": "Output format",
          "schema": {"type": "string"}
        }
      ],
      "requestBody": null,
      "responses": {...}
    },
    ...
  ]
}
```

**Step 2: Generate Click Commands with AI**

**CRITICAL:** Use Claude Code (yourself) to write the Click CLI code. Do NOT use scripts.

For each endpoint in the category details:

1. **Analyze the endpoint:**
   - What is the HTTP method? (GET, POST, DELETE, etc.)
   - What is the path? (e.g., `/config`, `/users/{userId}`)
   - What parameters does it need?
     - Path parameters → `@click.argument()`
     - Query parameters → `@click.option()`
     - Request body → handle separately
   - What types do parameters use? (string, integer, boolean, etc.)

2. **Write the Click command:**
   ```python
   @config_group.command('get-config')
   @click.option('--format', type=click.STRING, help='Output format')
   def config_get_config(format):
       """Retrieve system configuration"""
       params = {
           'format': format,
       }
       result = api.request(
           method='GET',
           endpoint='/config',
           params=params if params else None,
       )

       if 'error' not in result:
           click.echo(json.dumps(result, indent=2, ensure_ascii=False))
       else:
           click.echo(result['error'], err=True)
   ```

3. **Repeat for all endpoints in the category**

4. **Create the category group wrapper:**
   ```python
   @cli.group(name='config')
   def config_group():
       """Manage Config operations"""
       pass

   # ... all commands follow here
   ```

**Step 3: Store Generated Code**

Save the complete category code block for later assembly.

**Expected Output Format:**
```python
# Category: Config
# Endpoint count: 3

@cli.group(name='config')
def config_group():
    """Manage Config operations"""
    pass

@config_group.command('get-config')
@click.option('--format', type=click.STRING, help='Output format')
def config_get_config(format):
    """Retrieve system configuration"""
    # ... implementation

@config_group.command('update-config')
@click.option('--key', required=True, help='Configuration key')
@click.option('--value', required=True, help='Configuration value')
def config_update_config(key, value):
    """Update configuration setting"""
    # ... implementation

# ... more commands
```

#### 5.3 Assemble Final CLI Tool

Once all tasks are complete, assemble the final `cli_tool.py`:

**Template Structure:**
```python
#!/usr/bin/env python3
"""
CLI Tool - {skill_name}

Auto-generated CLI tool for managing APIs.
"""

import click
import json
import requests
from urllib.parse import urljoin
from typing import Optional
import os


class API:
    """API client."""

    def __init__(self, base_url: str = None, token: str = None):
        """Initialize API client."""
        self.base_url = base_url or os.getenv('API_BASE_URL', 'http://localhost:8080')
        self.token = token or os.getenv('API_TOKEN', '')
        self.headers = {
            'Content-Type': 'application/json',
        }
        if self.token:
            self.headers['Authorization'] = f'Bearer {self.token}'

    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make API request."""
        url = urljoin(self.base_url, endpoint)
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs, timeout=30)
            response.raise_for_status()
            return response.json() if response.text else {"status": "success"}
        except Exception as e:
            click.echo(f"❌ Error: {e}", err=True)
            return {"error": str(e)}


# Initialize API client
api = API()


@click.group()
def cli():
    """API CLI Tool"""
    pass


# ============================================================
# GENERATED COMMANDS - INSERT ALL CATEGORY CODE BLOCKS HERE
# ============================================================

{category_1_code}

{category_2_code}

{category_3_code}

# ============================================================


if __name__ == '__main__':
    cli()
```

**Assembly Process:**
1. Insert all generated category code blocks
2. Write to `<output-dir>/<skill-name>/scripts/cli_tool.py`
3. Set executable permissions: `chmod +x cli_tool.py`

#### 5.4 Generate Supporting Files

Create the remaining skill files:

**1. SKILL.md**

```markdown
---
name: {skill_name}
description: Manage {categories} via API
---

# {Skill Title}

Interact with APIs for {categories}.

## Capabilities

This skill provides CLI tools to manage:

{list_of_categories_with_counts}

## Usage

\`\`\`bash
python scripts/cli_tool.py --help
python scripts/cli_tool.py <category> --help
python scripts/cli_tool.py <category> <command> --param value
\`\`\`

...
```

**2. references/api_endpoints.md**

Document all selected endpoints with details from OpenAPI spec.

**3. references/unsupported_categories.md** (if applicable)

List categories that were NOT included in the skill.

**Expected Final Structure:**
```
<skill-name>/
├── SKILL.md
├── scripts/
│   └── cli_tool.py
└── references/
    ├── api_endpoints.md
    └── unsupported_categories.md (optional)
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

- **swagger2skill.py** - Main script: extracts and displays categories with `--json` option for programmatic use
- **openapi_parser.py** - Parser: extracts full category/endpoint details from OpenAPI specs
- **get_category_details.py** - Detail extractor: gets complete endpoint information for a single category (used in parallel task generation)
- **skill_generator.py** - (Legacy) Automated generator - DO NOT USE for new workflows; use AI-driven generation in Step 5 instead

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

## Implementation Status

✅ **Implemented Features:**

- **Interactive category selection** via AskUserQuestion (Step 2, Step 3)
- **Multi-select support** for custom category choices
- **AI-driven parallel CLI generation** using tasks and Claude Code intelligence (Step 5)
- **Complete OpenAPI detail extraction** via get_category_details.py
- **JSON output mode** for programmatic parsing (`--json` flag)

⚠️ **Future Enhancements:**

- **Automatic skill validation** using skill-creator skill (see goal.md 步骤 6)
- **Enhanced error recovery** for malformed OpenAPI specs
- **Support for OpenAPI 3.1** and additional authentication schemes

---

## Summary

This skill automates skill generation from OpenAPI specs with AI-powered intelligence:

✅ **Interactive category selection** via AskUserQuestion (Steps 2-4)
✅ **Multi-select support** for custom category choices
✅ **AI-driven parallel CLI generation** - Claude Code writes high-quality code for each category (Step 5)
✅ **Complete OpenAPI parsing** with full parameter and type information
✅ **Task-based parallelization** for efficient multi-category processing
✅ **Complete documentation** including API references and usage guides
✅ **Verification and testing** of generated skills

**Key Advantage:** Uses Claude Code's intelligence to generate contextual, high-quality CLI commands instead of rigid template-based generation.

Follow the 6-step workflow exactly as documented to ensure proper skill generation.
