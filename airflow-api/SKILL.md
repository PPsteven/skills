---
name: airflow-api
title: Airflow API Manager
summary: CLI tool for managing Apache Airflow DAGs, tasks, variables, connections, and datasets
tags: [airflow, scheduling, workflow, orchestration]
author: Claude Code
version: 1.0.0
created: 2026-03-06
---

# Airflow API Manager

A comprehensive CLI tool for managing Apache Airflow through its REST API, with support for DAGs, task instances, variables, connections, and datasets.

## Capabilities

This skill provides programmatic access to Airflow's core operations:

- **DAG Management** - List, retrieve, and manage Directed Acyclic Graphs
- **Task Execution** - Query and manage task instances across DAG runs
- **DAG Runs** - Create, list, and monitor DAG run execution
- **Variables** - Store and retrieve pipeline variables
- **Connections** - Manage external service connections
- **Datasets** - Create and manage Airflow datasets for event-driven workflows

## Supported API Categories

The skill wraps the following Airflow API v1 categories (6 categories, 60 endpoints):

- **Connection** - 6 endpoints
- **DAG** - 12 endpoints
- **DAGRun** - 9 endpoints
- **Dataset** - 11 endpoints
- **TaskInstance** - 17 endpoints
- **Variable** - 5 endpoints

## Quick Start

Use the CLI tool to interact with Airflow:

```bash
python scripts/cli_tool.py --help
```

### Example Commands

```bash
# List all DAGs
python scripts/cli_tool.py dag list

# Get DAG details
python scripts/cli_tool.py dag get --dag-id my_dag

# Create a variable
python scripts/cli_tool.py variable create --key env --value production

# List connections
python scripts/cli_tool.py connection list

# Trigger a DAG run
python scripts/cli_tool.py dagrun trigger --dag-id my_dag
```

## Configuration

Set the Airflow API endpoint via environment variable:

```bash
export AIRFLOW_API_URL="http://localhost:8080/api/v1"
export AIRFLOW_USERNAME="admin"
export AIRFLOW_PASSWORD="password"
```

Authentication can also be provided via CLI flags:

```bash
python scripts/cli_tool.py --api-url http://localhost:8080/api/v1 \
                          --username admin \
                          --password password \
                          dag list
```

## Documentation

Detailed API endpoint documentation: See `references/api_endpoints.md`

## Generated From

- **Source**: https://tmp-airflow.momenta.works/api/v1/openapi.json
- **OpenAPI Version**: 2.10.5
- **Generated**: 2026-03-06 16:44:15
