---
name: airflow-api
description: Manage Config, Connection, DAG, DAGRun, DagStats, DagWarning, Dataset, EventLog, ImportError, Monitoring, Permission, Plugin, Pool, Provider, Role, TaskInstance, User, Variable, XCom via Airflow API. Use for config, connection, dag, dagrun, dagstats, dagwarning, dataset, eventlog, importerror, monitoring, permission, plugin, pool, provider, role, taskinstance, user, variable, xcom operations.
---

# Airflow Api

Interact with Airflow APIs for Config, Connection, DAG, DAGRun, DagStats, DagWarning, Dataset, EventLog, ImportError, Monitoring, Permission, Plugin, Pool, Provider, Role, TaskInstance, User, Variable, XCom.

## Capabilities

This skill provides CLI tools to manage:

- **Config**: 2 API endpoints
- **Connection**: 6 API endpoints
- **DAG**: 12 API endpoints
- **DAGRun**: 9 API endpoints
- **DagStats**: 1 API endpoints
- **DagWarning**: 1 API endpoints
- **Dataset**: 11 API endpoints
- **EventLog**: 2 API endpoints
- **ImportError**: 2 API endpoints
- **Monitoring**: 2 API endpoints
- **Permission**: 1 API endpoints
- **Plugin**: 1 API endpoints
- **Pool**: 5 API endpoints
- **Provider**: 1 API endpoints
- **Role**: 5 API endpoints
- **TaskInstance**: 17 API endpoints
- **User**: 5 API endpoints
- **Variable**: 5 API endpoints
- **XCom**: 2 API endpoints

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

# Connection
```bash
python scripts/cli_tool.py connection list
python scripts/cli_tool.py connection detail <id>
```

# DAG
```bash
python scripts/cli_tool.py dag list
python scripts/cli_tool.py dag detail <id>
```

# DAGRun
```bash
python scripts/cli_tool.py dagrun list
python scripts/cli_tool.py dagrun detail <id>
```

# DagStats
```bash
python scripts/cli_tool.py dagstats list
python scripts/cli_tool.py dagstats detail <id>
```

# DagWarning
```bash
python scripts/cli_tool.py dagwarning list
python scripts/cli_tool.py dagwarning detail <id>
```

# Dataset
```bash
python scripts/cli_tool.py dataset list
python scripts/cli_tool.py dataset detail <id>
```

# EventLog
```bash
python scripts/cli_tool.py eventlog list
python scripts/cli_tool.py eventlog detail <id>
```

# ImportError
```bash
python scripts/cli_tool.py importerror list
python scripts/cli_tool.py importerror detail <id>
```

# Monitoring
```bash
python scripts/cli_tool.py monitoring list
python scripts/cli_tool.py monitoring detail <id>
```

# Permission
```bash
python scripts/cli_tool.py permission list
python scripts/cli_tool.py permission detail <id>
```

# Plugin
```bash
python scripts/cli_tool.py plugin list
python scripts/cli_tool.py plugin detail <id>
```

# Pool
```bash
python scripts/cli_tool.py pool list
python scripts/cli_tool.py pool detail <id>
```

# Provider
```bash
python scripts/cli_tool.py provider list
python scripts/cli_tool.py provider detail <id>
```

# Role
```bash
python scripts/cli_tool.py role list
python scripts/cli_tool.py role detail <id>
```

# TaskInstance
```bash
python scripts/cli_tool.py taskinstance list
python scripts/cli_tool.py taskinstance detail <id>
```

# User
```bash
python scripts/cli_tool.py user list
python scripts/cli_tool.py user detail <id>
```

# Variable
```bash
python scripts/cli_tool.py variable list
python scripts/cli_tool.py variable detail <id>
```

# XCom
```bash
python scripts/cli_tool.py xcom list
python scripts/cli_tool.py xcom detail <id>
```


## API Endpoints

For detailed API endpoint documentation, see `references/api_endpoints.md`.

## Implementation

This skill wraps the following API categories:
-   - Config
  - Connection
  - DAG
  - DAGRun
  - DagStats
  - DagWarning
  - Dataset
  - EventLog
  - ImportError
  - Monitoring
  - Permission
  - Plugin
  - Pool
  - Provider
  - Role
  - TaskInstance
  - User
  - Variable
  - XCom

Generated on: 2026-03-07 15:02:24
