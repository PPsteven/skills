# Swagger2Skill Usage Guide

Complete guide to using the swagger2skill skill to generate Claude skills from OpenAPI specifications.

## Overview

Swagger2skill streamlines the process of creating Claude skills that wrap API endpoints. Instead of manually documenting and wrapping APIs, you provide an OpenAPI specification and swagger2skill generates:

- Complete skill directory with SKILL.md
- Python CLI tool with all API endpoints
- Comprehensive API documentation
- References for unsupported features

## Quick Start

### 1. Invoke the Skill

```
/swagger2skill [openapi-url-or-file]
```

Examples:
```
/swagger2skill https://tmp-airflow.momenta.works/api/v1/openapi.json
/swagger2skill https://api.stripe.com/openapi.json
/swagger2skill ~/my-api/openapi.json
/swagger2skill ./openapi.json
```

### 2. Select Categories

The skill displays available API categories extracted from the OpenAPI spec's tags:

```
🎯 Select Categories to Include in Generated Skill
============================================================

1. DAG (6 endpoints)
2. Variable (4 endpoints)
3. Task (5 endpoints)
4. Connection (4 endpoints)
5. EventLog (2 endpoints)
6. XCom (3 endpoints)

------------------------------------------------------------
Enter the numbers of categories to include (comma-separated)
Example: 1,2,4
------------------------------------------------------------

👉 Your selection: 1,2
```

### 3. Provide Skill Name

```
💾 Generated Skill Name
============================================================

Enter the name for the generated skill.
(Use lowercase with hyphens, e.g., 'airflow-api', 'my-api-tool')

👉 Skill name: airflow-api
```

### 4. Review Generation

```
⚙️  Generating Skill
============================================================

  ✓ Created SKILL.md
  ✓ Created scripts/cli_tool.py
  ✓ Created references/api_endpoints.md
  ✓ Created references/unsupported_categories.md
```

## Understanding Generated Skills

### SKILL.md

Your generated skill's main documentation:

```markdown
---
name: airflow-api
description: Manage DAG and Variable via Airflow API. Use for DAG and variable operations.
---

# Airflow API

[Skill documentation, usage instructions, examples]
```

### scripts/cli_tool.py

Click-based CLI tool with stubs for each category:

```python
@cli.group(name='dag')
def dag_group():
    """Manage DAG operations"""
    pass

@dag_group.command('list')
@click.option('--limit', default=10)
def dag_list(limit):
    """List DAG items"""
    # TODO: Implement DAG list endpoint
    click.echo(f"Fetching DAG items (limit={limit})...")
```

### references/api_endpoints.md

Complete endpoint documentation for your selected categories:

```markdown
# API Endpoints Reference

**Selected Categories**: DAG, Variable

## DAG

### 1. GET /api/v1/dags

**Description**: List DAGs

- **Method**: `GET`
- **Path**: `/api/v1/dags`
- **Operation ID**: `get_dags`
- **Parameters**: 4 parameters
```

### references/unsupported_categories.md

(Only created if some categories were not selected)

Lists unimplemented categories and their endpoints for future reference:

```markdown
# Unsupported API Categories

The following API categories are available but were NOT included:

## Task

**Endpoints**: 5

**Available operations**:
- `GET /api/v1/tasks`
- `GET /api/v1/tasks/{task_id}`
- ...
```

## Complete Workflow Example

### Scenario: Generate Airflow API Skill

**Step 1: Start**
```
User: /swagger2skill https://tmp-airflow.momenta.works/api/v1/openapi.json
```

**Step 2: See categories**
```
🎯 Select Categories to Include in Generated Skill

1. DAG (6 endpoints)
2. Variable (4 endpoints)
3. Task (5 endpoints)
4. Connection (4 endpoints)
5. EventLog (2 endpoints)
6. XCom (3 endpoints)
```

**Step 3: Select categories**
```
👉 Your selection: 1,2,3

✅ Selected 3 categories:
   • DAG
   • Variable
   • Task
```

**Step 4: Confirm selection**
```
👉 Confirm selection? (yes/no): yes
```

**Step 5: Provide skill name**
```
👉 Skill name: airflow-api
✅ Skill name: airflow-api
👉 Confirm? (yes/no): yes
```

**Step 6: Choose output location**
```
👉 Output directory (or press Enter for default):
✅ Output directory: /Users/ppsteven/projects/skills
```

**Step 7: Generation completes**
```
✅ Skill Generation Complete!

📍 Skill location: /Users/ppsteven/projects/skills/airflow-api

📋 Next Steps:
   1. Review the generated files...
   2. Implement the CLI commands...
   3. Test the CLI tool locally
   4. Create symlink to ~/.claude/skills/
   5. Commit to repository
```

**Result**: New skill ready at `/Users/ppsteven/projects/skills/airflow-api`

## After Generation

### Step 1: Review Generated Files

```bash
cd /Users/ppsteven/projects/skills/airflow-api

# View skill metadata
cat SKILL.md

# View CLI tool structure
cat scripts/cli_tool.py

# View API documentation
cat references/api_endpoints.md
```

### Step 2: Implement CLI Commands

Replace TODO markers with actual API calls. Example:

**Before**:
```python
@dag_group.command('list')
def dag_list():
    """List DAGs"""
    # TODO: Implement DAG list endpoint
    click.echo(f"Fetching DAG items...")
```

**After**:
```python
@dag_group.command('list')
@click.option('--limit', default=10, help='Number of items to return')
def dag_list(limit):
    """List DAGs"""
    click.echo(f"📋 Fetching DAGs (limit={limit})...")
    result = api.request('GET', f'/api/v1/dags?limit={limit}')

    if 'error' in result:
        click.echo(f"❌ {result['error']}", err=True)
        return

    dags = result.get('dags', [])
    click.echo(f"\n✅ Found {len(dags)} DAGs:\n")
    for dag in dags:
        click.echo(f"  • {dag['dag_id']}")
```

### Step 3: Configure API Authentication

Edit `scripts/cli_tool.py` to handle your API's authentication:

```python
class AirflowAPI:
    """Airflow API client."""

    def __init__(self, base_url: str = None, token: str = None):
        """Initialize API client."""
        self.base_url = base_url or os.getenv('AIRFLOW_BASE_URL', 'http://localhost:8080')
        self.token = token or os.getenv('AIRFLOW_TOKEN', '')  # Your auth setup
        # ... rest of initialization
```

### Step 4: Test Locally

```bash
# Set environment variables
export AIRFLOW_BASE_URL="http://airflow.example.com"
export AIRFLOW_TOKEN="your-api-token"

# Test CLI
python scripts/cli_tool.py --help
python scripts/cli_tool.py dag --help
python scripts/cli_tool.py dag list
```

### Step 5: Deploy

```bash
# Create symlinks
ln -s /Users/ppsteven/projects/skills/airflow-api ~/.claude/skills/airflow-api
ln -s /Users/ppsteven/projects/skills/airflow-api ~/.cline/skills/airflow-api

# Version control
cd /Users/ppsteven/projects/skills
git add airflow-api/
git commit -m "feat: Add airflow-api skill"
git push origin main
```

## Common Tasks

### Adding a New Command

In your generated `cli_tool.py`:

```python
@dag_group.command('trigger')
@click.argument('dag_id')
@click.option('--config', help='DAG run configuration')
def dag_trigger(dag_id, config):
    """Trigger a DAG run"""
    click.echo(f"🚀 Triggering DAG: {dag_id}...")

    payload = {'dag_id': dag_id}
    if config:
        payload['conf'] = json.loads(config)

    result = api.request('POST', f'/api/v1/dags/{dag_id}/dagRuns', json=payload)

    if 'error' in result:
        click.echo(f"❌ {result['error']}", err=True)
        return

    click.echo(f"✅ DAG run created: {result.get('dag_run_id')}")
```

### Adding Error Handling

```python
try:
    response = requests.request(method, url, headers=headers, **kwargs, timeout=30)
    response.raise_for_status()
    return response.json() if response.text else {"status": "success"}
except requests.exceptions.Timeout:
    return {"error": "Request timeout"}
except requests.exceptions.HTTPError as e:
    return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
except requests.exceptions.RequestException as e:
    return {"error": str(e)}
```

### Supporting Multiple Output Formats

```python
@dag_group.command('list')
@click.option('--format', type=click.Choice(['text', 'json']), default='text')
def dag_list(format):
    """List DAGs"""
    result = api.request('GET', '/api/v1/dags')
    dags = result.get('dags', [])

    if format == 'json':
        click.echo(json.dumps(dags, indent=2))
    else:
        for dag in dags:
            click.echo(f"  • {dag['dag_id']}")
```

## Troubleshooting

### "Invalid OpenAPI specification"

**Cause**: OpenAPI file is malformed or not accessible

**Solution**:
1. Verify URL is accessible: `curl https://api.example.com/openapi.json`
2. Check JSON syntax: `python -m json.tool openapi.json`
3. Validate against OpenAPI spec: https://www.openapis.org/blog/2020/11/01/openapi-3-1-and-2-0-are-here

### "No categories found"

**Cause**: OpenAPI spec doesn't use tags or endpoints are untagged

**Solution**:
1. Check if spec uses tags: `grep -A5 '"tags"' openapi.json`
2. Some APIs may require manually adding tags to endpoints
3. Unsupported: Generate and manually add categories

### Generated CLI not working

**Cause**: Missing authentication or API configuration

**Solution**:
```bash
# Verify API is accessible
curl -H "Authorization: Bearer $AIRFLOW_TOKEN" \
  http://localhost:8080/api/v1/dags

# Check environment variables
echo $AIRFLOW_BASE_URL
echo $AIRFLOW_TOKEN

# Debug CLI execution
python scripts/cli_tool.py dag list -vvv  # Add verbose logging
```

### Permission denied

**Solution**:
```bash
chmod +x scripts/cli_tool.py
chmod +x scripts/swagger2skill_main.py
```

## Advanced Usage

### Generating Skills Programmatically

```python
import sys
sys.path.insert(0, '/Users/ppsteven/projects/skills/swagger2skill/scripts')

from openapi_parser import OpenAPIParser
from skill_generator import SkillGenerator

# Parse API
parser = OpenAPIParser('https://api.example.com/openapi.json')
parser.load_spec()
parser.extract_categories()

# Generate skill
generator = SkillGenerator(
    'my-api',
    '/Users/ppsteven/projects/skills',
    parser.categories,
    ['DAG', 'Variable'],  # Selected categories
    parser.get_all_categories_list()
)
generator.generate()
```

### Batch Processing Multiple APIs

```bash
#!/bin/bash

apis=(
  "https://api1.example.com/openapi.json"
  "https://api2.example.com/openapi.json"
  "https://api3.example.com/openapi.json"
)

for api_url in "${apis[@]}"; do
  python /Users/ppsteven/projects/skills/swagger2skill/scripts/openapi_parser.py "$api_url"
  # Process categories programmatically
done
```

## Best Practices

✅ **DO:**
- Start with well-formed OpenAPI specs
- Use meaningful category tags
- Test generated CLI before deployment
- Implement error handling
- Document API authentication
- Version control generated skills
- Update SKILL.md with actual examples

❌ **DON'T:**
- Use unvalidated OpenAPI specs
- Skip CLI implementation
- Deploy without testing
- Hardcode credentials
- Ignore API rate limits
- Forget to set required environment variables

## Resources

- **SKILL.md** - Skill metadata and documentation template
- **scripts/openapi_parser.py** - OpenAPI parsing library
- **scripts/skill_generator.py** - Skill generation library
- **references/openapi_schema_reference.md** - OpenAPI spec reference
- **references/generated_skill_template.md** - Example generated output
- **references/cli_tool_example.md** - CLI implementation examples

## Support

For help:
1. Check this guide's troubleshooting section
2. Review generated references
3. Test with public APIs first (e.g., Petstore API: https://petstore.swagger.io/openapi.json)
4. Consult OpenAPI official documentation

## Example APIs to Test With

```bash
# Petstore (simple test API)
/swagger2skill https://petstore.swagger.io/openapi.json

# Airflow (complex real API)
/swagger2skill https://tmp-airflow.momenta.works/api/v1/openapi.json
```

## Getting Started Checklist

- [ ] Understand OpenAPI/Swagger basics
- [ ] Have a valid OpenAPI spec (URL or file)
- [ ] Run `/swagger2skill` with your spec
- [ ] Select desired API categories
- [ ] Review generated skill files
- [ ] Implement CLI commands
- [ ] Test locally with API
- [ ] Deploy and share skill
- [ ] Iterate based on usage

---

Happy skill generating! 🎉
