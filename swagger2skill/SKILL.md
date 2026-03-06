---
name: swagger2skill
description: Generate reusable skills from Swagger/OpenAPI specifications. Use when needing to create a skill that wraps multiple API endpoints from an OpenAPI definition. Extracts API categories, lets users select which ones to implement, then generates a new skill with CLI tools for the selected APIs.
context: fork
agent: general-purpose
argument-hint: "[openapi-url-or-path]"
---

# Swagger to Skill Generator

Generate production-ready skills directly from Swagger/OpenAPI specifications. This skill streamlines API documentation into reusable Claude skills with CLI tools.

## Purpose

When you have an OpenAPI/Swagger definition and want to create a Claude skill that wraps those APIs, this skill automates the entire process:

1. **Parse** the OpenAPI specification (from URL or local file)
2. **Extract and categorize** all API endpoints
3. **Let users choose** which categories to implement
4. **Generate** a complete skill with CLI tools for selected APIs
5. **Document** unsupported categories in references

This eliminates manual API endpoint transcription and ensures consistency across generated skills.

## How to Use This Skill

### Basic Usage

Provide either an OpenAPI URL or file path:

```
/swagger2skill https://tmp-airflow.momenta.works/api/v1/openapi.json
/swagger2skill ~/my-api-openapi.json
```

### Interactive Selection

After processing the OpenAPI file, you'll see:

1. **Available Categories** - List of all API categories found (e.g., DAG, Variable, Task, Connection)
2. **Selection Prompt** - Choose which categories to include in the generated skill
3. **Generation** - Creates a new skill directory with:
   - `SKILL.md` - Complete skill documentation
   - `scripts/cli_tool.py` - CLI wrapper for selected APIs
   - `references/api_endpoints.md` - Documentation of implemented endpoints
   - `references/unsupported_categories.md` - Info about unselected categories (if any exist)

### Output Structure

The generated skill is ready to deploy:

```
generated-skill-name/
├── SKILL.md                              # Skill metadata and instructions
├── scripts/
│   └── cli_tool.py                       # CLI tool wrapping selected APIs
├── references/
│   ├── api_endpoints.md                  # API endpoint documentation
│   └── unsupported_categories.md         # Unimplemented categories (optional)
└── assets/
    └── [optional generated templates]
```

## Implementation Process

### Step 1: Parse OpenAPI Specification

The skill processes the OpenAPI file and extracts:
- API categories (tags in OpenAPI)
- Endpoints per category
- Request parameters and response schemas
- Authentication requirements

**Reference**: See `references/openapi_schema_reference.md` for OpenAPI structure details.

### Step 2: Display Category Selection

Lists all discovered categories with endpoint counts:

```
Available API Categories (12 total):

1. DAG (6 endpoints)
   - List DAGs
   - Get DAG details
   - Trigger DAG
   - ...

2. Variable (4 endpoints)
   - List variables
   - Get variable
   - ...

3. [other categories...]
```

### Step 3: User Selects Categories

Select categories to implement in the generated skill. Only selected categories will have CLI tools generated.

**Example**: If you select DAG, Variable, and Task (3 categories), the generated skill will only include those APIs.

### Step 4: Generate Skill

Creates a new skill directory with:

**SKILL.md Template**: Pre-filled with:
- Name and description based on selected categories
- Usage instructions specific to selected endpoints
- Example commands

**CLI Tool Script** (`scripts/cli_tool.py`):
- Click-based CLI with commands for each selected category
- Request handling and response formatting
- Error handling and authentication

**API Endpoints Documentation** (`references/api_endpoints.md`):
- All implemented API endpoints
- Parameters, request/response examples
- Authentication details

**Unsupported Categories Documentation** (`references/unsupported_categories.md`):
- List of API categories NOT included
- Brief description of each category
- Reference for future expansion

### Step 5: Ready to Deploy

The generated skill is ready to:
- Commit to version control
- Symlink to `~/.claude/skills/`
- Share with team members
- Extend with additional functionality

## Workflow Example

**Scenario**: Create a skill for Airflow DAG management

```
User Input:
/swagger2skill https://tmp-airflow.momenta.works/api/v1/openapi.json

Process:
1. Fetch and parse OpenAPI JSON
2. Find 12 categories: DAG, Variable, Task, Connection, ...
3. Display category list
4. User selects: DAG, Variable
5. Generate skill:
   - airflow-api/
     ├── SKILL.md (documenting DAG and Variable management)
     ├── scripts/cli_tool.py (CLI for DAG/Variable operations)
     ├── references/api_endpoints.md (endpoint details)
     └── references/unsupported_categories.md (Task, Connection, etc.)
```

## Key Features

✅ **Automatic Extraction** - Parses OpenAPI specs without manual transcription
✅ **Category-Based Selection** - Users choose which APIs to include
✅ **CLI Tool Generation** - Auto-generates working Click-based CLI
✅ **Selective Documentation** - References focus only on implemented endpoints
✅ **Deployment Ready** - Generated skill follows best practices for Claude skills
✅ **Extensible** - Users can modify generated skill and add custom features

## References

- `references/openapi_schema_reference.md` - OpenAPI 3.0 specification structure
- `references/generated_skill_template.md` - Example of generated skill output
- `references/cli_tool_example.md` - CLI tool code example

## Implementation Details

### Scripts Used

- `scripts/openapi_parser.py` - Parses OpenAPI and extracts categories/endpoints
- `scripts/skill_generator.py` - Generates skill directory structure and files
- `scripts/cli_generator.py` - Creates Click-based CLI tool code

### Supported OpenAPI Versions

- OpenAPI 3.0.x
- Swagger 2.0 (converted to OpenAPI 3.0 internally)

### Limitations

- Binary/file upload endpoints are documented but not wrapped in CLI
- WebSocket endpoints are noted but not included in CLI
- Complex nested schemas may need manual refinement in generated code

## Troubleshooting

**Issue**: "Invalid OpenAPI specification"
- Verify URL is accessible or file path is correct
- Check OpenAPI version (3.0.x or 2.0 supported)

**Issue**: "No categories found"
- OpenAPI may lack proper tagging structure
- Check if endpoints use `tags` field for categorization

**Issue**: "Generated CLI tool not working"
- Review and adjust authentication setup in `scripts/cli_tool.py`
- Test individual endpoints manually first
