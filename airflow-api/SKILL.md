---
name: airflow-api
description: Interact with Apache Airflow REST API via CLI commands to query task execution status, retrieve logs, and manage DAG operations. This skill should be used when needing to query task runs, retrieve task logs, get DAG details, trigger DAG runs, or perform other Airflow workflow management operations programmatically.
---

# Airflow API Skill

This skill provides a unified CLI interface to interact with Apache Airflow REST API endpoints, enabling programmatic access to task execution status, logs, and DAG management operations.

## Purpose

The Airflow API skill wraps Airflow's REST API into convenient CLI commands, allowing users to:
- Query task execution status and details
- Retrieve task execution logs
- List and trigger DAG runs
- Clear task instances
- Manage connections, variables, and pools
- Monitor Airflow health and system information

## When to Use This Skill

Use this skill when:
- Querying task run status and execution history
- Retrieving task logs for debugging and monitoring
- Triggering DAG runs programmatically
- Managing DAG configuration and execution
- Integrating Airflow operations into automation scripts
- Checking Airflow system health and configuration

## Using the Skill

The skill provides a Python CLI tool at `scripts/airflow_cli.py` that abstracts Airflow REST API operations.

### Environment Setup

Configure Airflow connection via environment variables:

```bash
export AIRFLOW_API_URL="https://airflow.example.com/api/v1"
export AIRFLOW_API_USER="username"
export AIRFLOW_API_PASSWORD="password"
# OR use Basic Auth token
export AIRFLOW_API_TOKEN="Basic base64encodedcredentials"
```

### CLI Commands

Execute the CLI tool using Python:

```bash
python scripts/airflow_cli.py <command> [arguments]
```

#### Task Commands

**List task instances for a DAG run:**
```bash
python scripts/airflow_cli.py task-instances <dag_id> <dag_run_id>
```

**Get task instance details:**
```bash
python scripts/airflow_cli.py task-instance <dag_id> <dag_run_id> <task_id>
```

**Retrieve task logs:**
```bash
python scripts/airflow_cli.py task-logs <dag_id> <dag_run_id> <task_id> [--try-number 1]
```

**Set task instance note:**
```bash
python scripts/airflow_cli.py set-task-note <dag_id> <dag_run_id> <task_id> <note>
```

#### DAG Commands

**List all DAGs:**
```bash
python scripts/airflow_cli.py dags [--limit 10]
```

**Get DAG details:**
```bash
python scripts/airflow_cli.py dag-details <dag_id>
```

**Get DAG tasks:**
```bash
python scripts/airflow_cli.py dag-tasks <dag_id>
```

**Trigger DAG run:**
```bash
python scripts/airflow_cli.py trigger-dag <dag_id> [--conf '{"key": "value"}']
```

**List DAG runs:**
```bash
python scripts/airflow_cli.py dag-runs <dag_id> [--limit 10]
```

**Get DAG run details:**
```bash
python scripts/airflow_cli.py dag-run-details <dag_id> <dag_run_id>
```

**Clear task instances:**
```bash
python scripts/airflow_cli.py clear-tasks <dag_id> <dag_run_id> [--task-id <task_id>]
```

#### Configuration Commands

**List connections:**
```bash
python scripts/airflow_cli.py connections [--limit 10]
```

**Get connection details:**
```bash
python scripts/airflow_cli.py connection <connection_id>
```

**List variables:**
```bash
python scripts/airflow_cli.py variables [--limit 10]
```

**Get variable value:**
```bash
python scripts/airflow_cli.py variable <variable_key>
```

**List pools:**
```bash
python scripts/airflow_cli.py pools [--limit 10]
```

#### System Commands

**Check Airflow health:**
```bash
python scripts/airflow_cli.py health
```

**Get Airflow version:**
```bash
python scripts/airflow_cli.py version
```

### Output Formats

All commands return JSON by default for easy parsing and integration with other tools:

```bash
# Human-readable table output (if available)
python scripts/airflow_cli.py task-instances <dag_id> <dag_run_id>

# JSON output for scripting
python scripts/airflow_cli.py task-instances <dag_id> <dag_run_id> --format json
```

## API Reference

For detailed information about Airflow API endpoints, parameters, and response schemas, refer to `references/api_endpoints.md`.

## Authentication

The skill supports HTTP Basic Authentication. Configure credentials via environment variables:

- `AIRFLOW_API_URL` - Base URL of Airflow API (required)
- `AIRFLOW_API_USER` - Username for Basic Auth (if using username/password)
- `AIRFLOW_API_PASSWORD` - Password for Basic Auth (if using username/password)
- `AIRFLOW_API_TOKEN` - Pre-encoded Basic Auth token (alternative to username/password)

The CLI tool will automatically use these environment variables for all API requests.

## Implementation Details

The CLI tool uses Python's `requests` library to communicate with Airflow's REST API. All responses are parsed and formatted for easy consumption.

Key features:
- Error handling with informative messages
- Support for pagination and filtering
- JSON output for scripting integration
- Environment-based configuration
- No external CLI tool dependencies (pure Python)

## Related Documentation

- Airflow API Documentation: https://airflow.apache.org/docs/apache-airflow/stable/stable-api-ref.html
- API Endpoints Reference: `references/api_endpoints.md`
