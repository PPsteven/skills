# Swagger2Skill - OpenAPI to Skill Generator

A skill that automatically generates Claude skills from Swagger/OpenAPI specifications.

## Quick Start

### Usage

```bash
# Using with Claude Code
/swagger2skill https://tmp-airflow.momenta.works/api/v1/openapi.json

# Or with a local file
/swagger2skill ~/my-api-openapi.json
```

### What It Does

1. **Parses** your OpenAPI/Swagger specification
2. **Extracts** API categories (from tags)
3. **Displays** available categories for you to choose
4. **Generates** a new skill with:
   - SKILL.md documentation
   - Python CLI tool wrapping selected APIs
   - API endpoint reference
   - Documentation of unsupported categories

## Example Workflow

```
📥 Input
  ↓
  You: /swagger2skill https://tmp-airflow.momenta.works/api/v1/openapi.json
  ↓
📚 Extraction
  ↓
  Available categories:
  1. DAG (6 endpoints)
  2. Variable (4 endpoints)
  3. Task (5 endpoints)
  4. Connection (4 endpoints)
  5. EventLog (2 endpoints)
  6. XCom (3 endpoints)
  ↓
🎯 Selection
  ↓
  You: 1,2
  (Select DAG and Variable)
  ↓
💾 Generation
  ↓
  Created: airflow-api/
  ├── SKILL.md
  ├── scripts/cli_tool.py
  └── references/
      ├── api_endpoints.md
      └── unsupported_categories.md
  ↓
✅ Done!
  You get a ready-to-use skill with CLI tools for DAG and Variable
```

## Key Features

✅ **Automatic Extraction** - No manual transcription of API endpoints
✅ **Category-Based** - Organize APIs by logical categories (tags)
✅ **User Selection** - Choose which categories to implement
✅ **CLI Tool** - Auto-generates Click-based command-line interface
✅ **Ready to Deploy** - Follows Claude skill best practices
✅ **Extensible** - Easy to modify and customize generated code
✅ **Well Documented** - Includes reference documentation and examples

## Generated Skill Structure

```
generated-skill-name/
├── SKILL.md                              # Skill metadata and docs
├── scripts/
│   ├── cli_tool.py                       # CLI tool (needs implementation)
│   ├── openapi_parser.py                 # OpenAPI parser library
│   ├── skill_generator.py                # Skill generator library
│   └── swagger2skill_main.py             # Main entry point
├── references/
│   ├── api_endpoints.md                  # All implemented endpoints
│   ├── openapi_schema_reference.md       # OpenAPI spec reference
│   ├── generated_skill_template.md       # Template examples
│   ├── cli_tool_example.md               # CLI code examples
│   └── unsupported_categories.md         # Unimplemented categories
└── assets/                                # (Optional) Templates
```

## What Gets Generated

### SKILL.md
- Skill metadata (name, description)
- Usage instructions
- Category overview
- CLI examples
- Generated timestamp

### scripts/cli_tool.py
- Click-based CLI framework
- API client wrapper (with auth support)
- Command stubs for each selected category
- TODO markers for implementation
- Error handling template

### references/api_endpoints.md
- Complete documentation of all implemented endpoints
- HTTP method, path, operation ID, parameters
- From/to both are included for reference

### references/unsupported_categories.md
- List of available but unselected categories
- Endpoint counts for each
- Available operations listed
- For future expansion reference

## Implementation After Generation

### 1. Review Generated Files

```bash
cd generated-skill-name/
cat SKILL.md                    # Review skill documentation
cat scripts/cli_tool.py         # Check generated CLI structure
```

### 2. Implement CLI Commands

Replace TODO markers with actual API calls:

```python
# Before:
@item_group.command('list')
def item_list():
    """List items"""
    # TODO: Implement item list endpoint
    click.echo(f"Fetching items...")

# After:
@item_group.command('list')
@click.option('--limit', default=10)
def item_list(limit):
    """List items"""
    result = api.request('GET', f'/api/v1/items?limit={limit}')
    if 'error' in result:
        click.echo(f"❌ {result['error']}", err=True)
        return
    for item in result.get('items', []):
        click.echo(f"  • {item['id']}: {item['name']}")
```

### 3. Test Locally

```bash
# Set up environment
export API_BASE_URL="http://localhost:8080"
export API_TOKEN="your-token"

# Run CLI
python scripts/cli_tool.py --help
python scripts/cli_tool.py <category> --help
python scripts/cli_tool.py <category> <operation> --param value
```

### 4. Deploy

```bash
# Create symlink to Claude Code
ln -s $(pwd) ~/.claude/skills/generated-skill-name

# Create symlink to Cline (optional)
ln -s $(pwd) ~/.cline/skills/generated-skill-name
```

### 5. Version Control

```bash
cd /Users/ppsteven/projects/skills
git add generated-skill-name/
git commit -m "feat: Add generated-skill-name skill"
git push origin main
```

## Supported OpenAPI Versions

- ✅ OpenAPI 3.0.x
- ✅ Swagger 2.0 (converted internally)

## Requirements

### For Running swagger2skill

- Python 3.7+
- No external dependencies (uses standard library)

### For Using Generated Skills

- Python 3.7+
- `click` - CLI framework
- `requests` - HTTP client

Install dependencies:
```bash
pip install click requests
```

## Advanced Usage

### Running Scripts Directly

```bash
# Parse OpenAPI and see categories
python scripts/openapi_parser.py https://api.example.com/openapi.json

# Generate skill programmatically
python scripts/skill_generator.py skill-name output-dir categories.json selected.json
```

### Environment Variables for Generation

```bash
# Optional: Pre-configure API details for generated CLI
export AIRFLOW_BASE_URL="http://airflow.example.com"
export AIRFLOW_TOKEN="your-api-token"
```

## Reference Documentation

Inside the generated skill:

- `references/openapi_schema_reference.md` - OpenAPI specification details
- `references/generated_skill_template.md` - What generated skills look like
- `references/cli_tool_example.md` - Click CLI best practices
- `references/api_endpoints.md` - Your specific API endpoints

## Troubleshooting

### "Invalid OpenAPI specification"
- Verify URL is accessible or file path exists
- Ensure valid JSON format
- Check OpenAPI version (3.0.x or 2.0)

### "No categories found"
- OpenAPI may not use proper tagging
- Check if endpoints have `tags` field in specification
- Some APIs may have untagged endpoints

### Generated CLI not working
- Implement the TODO endpoints first
- Check authentication setup (API token, base URL)
- Verify API is accessible from your environment
- Test with curl or Postman first

### Permission denied when running
```bash
chmod +x scripts/cli_tool.py
chmod +x scripts/swagger2skill_main.py
```

## Examples

### Airflow API
```bash
/swagger2skill https://tmp-airflow.momenta.works/api/v1/openapi.json
# Select: DAG, Variable, Task
# Result: airflow-api skill with CLI for managing DAGs, variables, and tasks
```

### Custom API
```bash
/swagger2skill /path/to/my-api-openapi.json
# Select specific categories
# Result: my-api skill with CLI tools
```

## Architecture

### Components

1. **OpenAPI Parser** (`openapi_parser.py`)
   - Loads OpenAPI JSON/YAML
   - Extracts categories and endpoints
   - Detects version (OpenAPI 3.0 or Swagger 2.0)

2. **Skill Generator** (`skill_generator.py`)
   - Creates skill directory structure
   - Generates SKILL.md template
   - Creates CLI tool skeleton
   - Generates documentation

3. **CLI Tool Template** (Generated `cli_tool.py`)
   - Click-based command framework
   - API client wrapper
   - Request/response handling
   - Error handling

4. **Main Entry Point** (`swagger2skill_main.py`)
   - Orchestrates entire workflow
   - Prompts for user selections
   - Coordinates parser and generator

## Best Practices

✅ **DO:**
- Start with a well-formed OpenAPI specification
- Use meaningful tags for API organization
- Include clear summaries and descriptions
- Test generated CLI before deployment
- Implement error handling for all API calls
- Document any custom modifications
- Version control generated skills

❌ **DON'T:**
- Skip API endpoint implementation
- Ignore authentication requirements
- Use invalid or outdated OpenAPI specs
- Deploy without testing
- Hardcode credentials (use env vars)
- Modify without version control

## Contributing

To improve swagger2skill:

1. Test with various OpenAPI specifications
2. Report issues with specific API formats
3. Suggest improvements to generated code quality
4. Share examples of generated skills

## License

This skill is part of the Claude Skills collection.

## Support

For issues or questions:
- Check troubleshooting section above
- Review reference documentation
- Consult OpenAPI specification docs
- Test with public APIs first (e.g., Petstore API)

## Related Skills

- **skill-creator** - General guidance for creating Claude skills
- **my-skill** - Skill management and discovery
- **frontend-design** - For building UIs to accompany APIs
