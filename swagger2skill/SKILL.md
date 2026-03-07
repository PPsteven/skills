---
name: swagger2skill
description: Generate reusable Claude skills from Swagger/OpenAPI specifications. Automatically fetches and parses OpenAPI specs, extracts API categories, prompts for interactive selection, then generates complete skills with CLI tools and documentation.
---

# Swagger to Skill Generator

Generate production-ready Claude skills from Swagger/OpenAPI specifications using an automated Python workflow.

## How to Use

To generate a skill from an OpenAPI specification, run the main script:

```bash
python scripts/swagger2skill.py <openapi-url-or-file>
```

**Examples:**

From a remote URL:
```bash
python scripts/swagger2skill.py https://tmp-airflow.momenta.works/api/v1/openapi.json
```

From a local file:
```bash
python scripts/swagger2skill.py ./openapi.json
```

## Interactive Workflow

The script guides you through a straightforward 4-step process:

### Step 1: Parse OpenAPI Specification

The script automatically:
- Fetches the OpenAPI spec from URL or file
- Extracts all API categories and endpoint counts
- Displays a summary

**Example output:**
```
✅ Found 19 API categories:

   1. Config (3 endpoints)
   2. Connection (6 endpoints)
   3. DAG (12 endpoints)
   4. DAGRun (9 endpoints)
   5. Role (5 endpoints)
   ... and 14 more
```

### Step 2: Category Selection

The script prompts to choose how to select categories:

**Option A: All categories**
- Include every category found in the OpenAPI spec

**Option B: Custom selection**
- Enter specific categories using:
  - Numbers: `1,3,4,7`
  - Names: `dag,connection,variable`
  - Mixed: `1,connection,5`

### Step 3: Skill Configuration

Provide:
- **Skill name** (kebab-case): `airflow-api`, `my-rest-api`, etc.
- **Output directory** (default: `/Users/ppsteven/projects/skills/`)

### Step 4: Generate

The script creates a complete skill package with:
- `SKILL.md` - Skill metadata and documentation
- `scripts/cli_tool.py` - Click-based CLI wrapper for selected APIs
- `references/api_endpoints.md` - Complete API endpoint reference
- `references/unsupported_categories.md` - Unimplemented categories (if any)

## How It Works

**All logic is in Python scripts** — nothing is duplicated in Claude Code:

1. **Fetch** - Retrieves OpenAPI spec from URL or local file
2. **Parse** - Extracts API categories, endpoints, and metadata
3. **Display** - Shows available categories with endpoint counts
4. **Select** - User chooses all categories or custom subset
5. **Generate** - Creates skill package with:
   - Click CLI tool wrapper for selected APIs
   - Full API documentation and references
   - Deployment-ready structure

## Generated Skill Structure

```
generated-skill-name/
├── SKILL.md                       # Skill metadata
├── scripts/
│   └── cli_tool.py               # CLI implementation
├── references/
│   ├── api_endpoints.md          # API documentation
│   └── unsupported_categories.md # Future expansion reference
```

## Key Features

✅ **Complete automation** - All parsing and extraction in Python
✅ **Interactive selection** - Simple prompts, flexible category input
✅ **Production-ready** - Generated skills ready to use immediately
✅ **Click CLI generation** - Fully functional command-line tool
✅ **Comprehensive documentation** - API references and implementation guides

## Supported Formats

- OpenAPI 3.0.x
- Swagger 2.0

## Script Dependencies

Located in `scripts/` directory:
- `openapi_parser.py` - Parses OpenAPI specs and extracts categories
- `skill_generator.py` - Generates skill files and directory structure

Both are included and automatically used by the main script.

## Example Session

```bash
$ python scripts/swagger2skill.py https://tmp-airflow.momenta.works/api/v1/openapi.json

🚀 Swagger to Skill Generator
============================================================

📦 Using OpenAPI source: https://tmp-airflow.momenta.works/api/v1/openapi.json

============================================================
📖 Parsing OpenAPI Specification
============================================================

✅ Found 19 API categories:

   1. Config (3 endpoints)
   2. Connection (6 endpoints)
   3. DAG (12 endpoints)
   ...

============================================================
🎯 Category Selection
============================================================

How would you like to select API categories?

👉 Enter 'all' or 'custom': all

✅ Selected all 19 categories

============================================================
💾 Skill Details
============================================================

👉 Skill name: airflow-api

👉 Output directory (default: /Users/ppsteven/projects/skills):

============================================================
⚙️  Generating Skill
============================================================

✅ Skill Generation Complete!

📍 Skill location: /Users/ppsteven/projects/skills/airflow-api

📋 Generated Files:
   • SKILL.md
   • scripts/cli_tool.py
   • references/api_endpoints.md
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid OpenAPI specification" | Verify URL is accessible or file path exists |
| "No categories found" | Check if endpoints use `tags` field for categorization in the OpenAPI spec |
| "Connection refused" | For URLs, verify network access; try a local file path as alternative |
