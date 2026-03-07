---
name: airflow-api-test
description: Manage Config, DAG via Airflow API. Use for config, dag operations.
---

# Airflow Api Test

Interact with Airflow APIs for Config, DAG.

## Capabilities

This skill provides CLI tools to manage:

- **Config**: 2 API endpoints
- **DAG**: 12 API endpoints

## Usage

```bash
# List available commands
python scripts/cli_tool.py --help

# Get help for specific category
python scripts/cli_tool.py <category> --help

# Execute an API operation
python scripts/cli_tool.py <category> <operation> --param value
```

## CLI Examples

# Config
```bash
python scripts/cli_tool.py config list
python scripts/cli_tool.py config detail <id>
```

# DAG
```bash
python scripts/cli_tool.py dag list
python scripts/cli_tool.py dag detail <id>
```


## API Endpoints

For detailed API endpoint documentation, see `references/api_endpoints.md`.

## Implementation

This skill wraps the following API categories:
-   - Config
  - DAG

Generated on: 2026-03-07 15:15:59
