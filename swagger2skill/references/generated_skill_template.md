# Generated Skill Template Example

This document shows what a typical generated skill looks like after using swagger2skill.

## Example Scenario

**Input**: User provides Airflow API OpenAPI spec at `https://tmp-airflow.momenta.works/api/v1/openapi.json`
**Available Categories**: DAG, Variable, Task, Connection, EventLog, XCom
**User Selection**: DAG and Variable
**Generated Skill Name**: `airflow-api`

## Generated File Structure

```
airflow-api/
├── SKILL.md                    # Skill metadata and documentation
├── scripts/
│   ├── cli_tool.py            # CLI wrapper for selected APIs
│   └── __init__.py            # Python package marker (optional)
├── references/
│   ├── api_endpoints.md       # All implemented API endpoints
│   └── unsupported_categories.md  # Info about unselected categories
└── assets/                     # Optional templates or resources
```

## SKILL.md Example

```markdown
---
name: airflow-api
description: Manage DAG and Variable via Airflow API. Use for DAG and variable operations.
---

# Airflow API

Interact with Airflow APIs for DAG and Variable management.

## Capabilities

This skill provides CLI tools to manage:

- **DAG**: 6 API endpoints
- **Variable**: 4 API endpoints

## Usage

\`\`\`bash
# List available commands
python scripts/cli_tool.py --help

# Get help for specific category
python scripts/cli_tool.py <category> --help

# Execute an API operation
python scripts/cli_tool.py <category> <operation> --param value
\`\`\`

## CLI Examples

# DAG
\`\`\`bash
python scripts/cli_tool.py dag list
python scripts/cli_tool.py dag detail <id>
\`\`\`

# Variable
\`\`\`bash
python scripts/cli_tool.py variable list
python scripts/cli_tool.py variable detail <id>
\`\`\`

## API Endpoints

For detailed API endpoint documentation, see `references/api_endpoints.md`.

## Implementation

This skill wraps the following API categories:
- DAG
- Variable

Generated on: 2026-03-06 15:30:45
```

## api_endpoints.md Example

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

### 2. GET /api/v1/dags/{dag_id}

**Description**: Get DAG details

- **Method**: `GET`
- **Path**: `/api/v1/dags/{dag_id}`
- **Operation ID**: `get_dag_details`
- **Parameters**: 1 parameters

### 3. POST /api/v1/dags/{dag_id}/dagRuns

**Description**: Trigger DAG run

- **Method**: `POST`
- **Path**: `/api/v1/dags/{dag_id}/dagRuns`
- **Operation ID**: `post_dag_run`
- **Parameters**: 1 parameters

[... more DAG endpoints ...]

## Variable

### 1. GET /api/v1/variables

**Description**: List variables

- **Method**: `GET`
- **Path**: `/api/v1/variables`
- **Operation ID**: `get_variables`
- **Parameters**: 2 parameters

### 2. GET /api/v1/variables/{variable_key}

**Description**: Get variable value

- **Method**: `GET`
- **Path**: `/api/v1/variables/{variable_key}`
- **Operation ID**: `get_variable`
- **Parameters**: 1 parameters

[... more Variable endpoints ...]
```

## unsupported_categories.md Example

```markdown
# Unsupported API Categories

The following API categories are available in the specification but were NOT included in this skill:

## Task

**Endpoints**: 5

**Available operations**:
- `GET /api/v1/tasks`
- `GET /api/v1/tasks/{task_id}`
- `POST /api/v1/tasks`
- `PUT /api/v1/tasks/{task_id}`
- `DELETE /api/v1/tasks/{task_id}`

## Connection

**Endpoints**: 4

**Available operations**:
- `GET /api/v1/connections`
- `GET /api/v1/connections/{conn_id}`
- `POST /api/v1/connections`
- `PUT /api/v1/connections/{conn_id}`

## EventLog

**Endpoints**: 2

**Available operations**:
- `GET /api/v1/eventLogs`
- `GET /api/v1/eventLogs/{event_id}`

## XCom

**Endpoints**: 3

**Available operations**:
- `GET /api/v1/xcom`
- `GET /api/v1/xcom/{xcom_id}`
- `POST /api/v1/xcom`
```

## Generated CLI Tool Stub

```python
#!/usr/bin/env python3
"""
CLI Tool - Airflow API

Auto-generated CLI tool for managing Airflow APIs.
"""

import click
import json
import requests
from urllib.parse import urljoin
from typing import Optional
import os


class AirflowAPI:
    """Airflow API client."""

    def __init__(self, base_url: str = None, token: str = None):
        """Initialize API client."""
        self.base_url = base_url or os.getenv('AIRFLOW_BASE_URL', 'http://localhost:8080')
        self.token = token or os.getenv('AIRFLOW_TOKEN', '')
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
api = AirflowAPI()


@click.group()
def cli():
    """Airflow API CLI Tool"""
    pass


@cli.group(name='dag')
def dag_group():
    """Manage DAG operations"""
    pass


@dag_group.command('list')
@click.option('--limit', default=10, help='Number of items to return')
def dag_list(limit):
    """List DAG items"""
    # TODO: Implement DAG list endpoint
    click.echo(f"Fetching DAG items (limit={limit})...")
    # result = api.request('GET', '/api/v1/dags?limit={limit}')
    # click.echo(json.dumps(result, indent=2))


@dag_group.command('detail')
@click.argument('item_id')
def dag_detail(item_id):
    """Get DAG details"""
    # TODO: Implement DAG detail endpoint
    click.echo(f"Fetching DAG details for {item_id}...")
    # result = api.request('GET', '/api/v1/dags/{item_id}')
    # click.echo(json.dumps(result, indent=2))


@cli.group(name='variable')
def variable_group():
    """Manage Variable operations"""
    pass


@variable_group.command('list')
@click.option('--limit', default=10, help='Number of items to return')
def variable_list(limit):
    """List Variable items"""
    # TODO: Implement Variable list endpoint
    click.echo(f"Fetching Variable items (limit={limit})...")
    # result = api.request('GET', '/api/v1/variables?limit={limit}')
    # click.echo(json.dumps(result, indent=2))


@variable_group.command('detail')
@click.argument('item_id')
def variable_detail(item_id):
    """Get Variable details"""
    # TODO: Implement Variable detail endpoint
    click.echo(f"Fetching Variable details for {item_id}...")
    # result = api.request('GET', '/api/v1/variables/{item_id}')
    # click.echo(json.dumps(result, indent=2))


if __name__ == '__main__':
    cli()
```

## Key Characteristics

✅ **Organized by category** - CLI commands grouped by API category
✅ **Extensible** - Generated code includes TODO markers for implementation
✅ **Documented** - All generated files include clear headers and examples
✅ **Ready to deploy** - Can be immediately symlinked to `~/.claude/skills/`
✅ **Selective** - Only includes chosen categories in CLI and main documentation
✅ **Reference complete** - Unsupported categories documented for future expansion

## Next Steps

After generation, users typically:

1. **Review generated files** - Ensure accuracy and appropriateness
2. **Implement CLI commands** - Replace TODO markers with actual API calls
3. **Test CLI tool** - Verify integration with API
4. **Deploy skill** - Create symlinks to tool directories
5. **Share/version** - Commit to repository and distribute
