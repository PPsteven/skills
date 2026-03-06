# Airflow REST API Endpoints Reference

This document provides a comprehensive reference for Airflow REST API endpoints supported by the airflow-api CLI tool.

## Base URL

All API requests use the following base URL format:

```
https://<airflow-server>/api/v1
```

Configure this via the `AIRFLOW_API_URL` environment variable.

## Authentication

All requests require HTTP Basic Authentication:

```
Authorization: Basic base64(username:password)
```

Or use a pre-encoded token:

```
Authorization: Basic <base64-token>
```

## Task Instance Endpoints

### List Task Instances for DAG Run

- **Endpoint**: `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances`
- **CLI Command**: `python scripts/airflow_cli.py task-instances <dag_id> <dag_run_id>`
- **Parameters**:
  - `limit` (query): Maximum number of results to return
  - `offset` (query): Pagination offset
- **Response**: List of task instance objects with state, start_date, end_date, duration, try_number

### Get Task Instance Details

- **Endpoint**: `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}`
- **CLI Command**: `python scripts/airflow_cli.py task-instance <dag_id> <dag_run_id> <task_id>`
- **Response**: Single task instance object with complete details

### Get Task Logs

- **Endpoint**: `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{task_try_number}`
- **CLI Command**: `python scripts/airflow_cli.py task-logs <dag_id> <dag_run_id> <task_id> [--try-number N]`
- **Parameters**:
  - `task_try_number` (path): Try number (starts at 1, default if not specified)
  - `token` (query): Continuation token for large logs (optional)
- **Response**: Task logs as plain text or JSON with content field
- **Note**: Use `--try-number` flag to access logs from specific retry attempts

### Set Task Instance Note

- **Endpoint**: `PATCH /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/setNote`
- **CLI Command**: `python scripts/airflow_cli.py set-task-note <dag_id> <dag_run_id> <task_id> <note>`
- **Request Body**: `{"note": "Your note text"}`
- **Response**: Updated task instance object

### Get Task Dependencies

- **Endpoint**: `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/dependencies`
- **Response**: List of upstream/downstream task dependencies

### Get Task XCom Entries

- **Endpoint**: `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries`
- **Parameters**:
  - `limit` (query): Maximum number of results
  - `offset` (query): Pagination offset
- **Response**: List of XCom entries for inter-task communication values

## DAG Endpoints

### List DAGs

- **Endpoint**: `GET /dags`
- **CLI Command**: `python scripts/airflow_cli.py dags [--limit N]`
- **Parameters**:
  - `limit` (query): Maximum number of DAGs to return (default: 100)
  - `offset` (query): Pagination offset
  - `dag_id_pattern` (query): Filter DAGs by ID pattern
  - `only_active` (query): Return only active DAGs (default: true)
- **Response**: List of DAG objects with id, owner, description, is_active

### Get DAG Details

- **Endpoint**: `GET /dags/{dag_id}/details`
- **CLI Command**: `python scripts/airflow_cli.py dag-details <dag_id>`
- **Response**: DAG object with complete metadata including tags, catchup settings, default_view

### Get DAG Tasks

- **Endpoint**: `GET /dags/{dag_id}/tasks`
- **CLI Command**: `python scripts/airflow_cli.py dag-tasks <dag_id>`
- **Response**: List of task objects with task_id, task_type, operator, retries, pool, pool_slots

### List DAG Runs

- **Endpoint**: `GET /dags/{dag_id}/dagRuns`
- **CLI Command**: `python scripts/airflow_cli.py dag-runs <dag_id> [--limit N]`
- **Parameters**:
  - `limit` (query): Maximum number of runs to return
  - `offset` (query): Pagination offset
  - `state` (query): Filter by state (e.g., "running", "success", "failed")
  - `execution_date_lte` (query): Filter by execution date
  - `execution_date_gte` (query): Filter by execution date
- **Response**: List of DAG run objects with run_id, state, execution_date, start_date, end_date

### Get DAG Run Details

- **Endpoint**: `GET /dags/{dag_id}/dagRuns/{dag_run_id}`
- **CLI Command**: `python scripts/airflow_cli.py dag-run-details <dag_id> <dag_run_id>`
- **Response**: Single DAG run object with complete details

### Trigger DAG Run

- **Endpoint**: `POST /dags/{dag_id}/dagRuns`
- **CLI Command**: `python scripts/airflow_cli.py trigger-dag <dag_id> [--conf '{"key": "value"}']`
- **Request Body**:
  ```json
  {
    "conf": {
      "key": "value"
    }
  }
  ```
- **Response**: Created DAG run object

### Clear Task Instances

- **Endpoint**: `POST /dags/{dag_id}/clearTaskInstances`
- **CLI Command**: `python scripts/airflow_cli.py clear-tasks <dag_id> <dag_run_id> [--task-id <task_id>]`
- **Request Body**:
  ```json
  {
    "dag_run_id": "run_id",
    "task_ids": ["optional_task_1", "optional_task_2"]
  }
  ```
- **Response**: List of cleared task instances

### Update DAG Run Note

- **Endpoint**: `PATCH /dags/{dag_id}/dagRuns/{dag_run_id}/setNote`
- **Request Body**: `{"note": "Your note text"}`
- **Response**: Updated DAG run object

## Connection Endpoints

### List Connections

- **Endpoint**: `GET /connections`
- **CLI Command**: `python scripts/airflow_cli.py connections [--limit N]`
- **Parameters**:
  - `limit` (query): Maximum number of results
  - `offset` (query): Pagination offset
- **Response**: List of connection objects with conn_id, conn_type, host, port, login, schema

### Get Connection Details

- **Endpoint**: `GET /connections/{connection_id}`
- **CLI Command**: `python scripts/airflow_cli.py connection <connection_id>`
- **Response**: Single connection object

### Create Connection

- **Endpoint**: `POST /connections`
- **Request Body**:
  ```json
  {
    "conn_id": "my_connection",
    "conn_type": "http",
    "host": "example.com",
    "port": 8080,
    "login": "user",
    "password": "pass"
  }
  ```
- **Response**: Created connection object

### Update Connection

- **Endpoint**: `PATCH /connections/{connection_id}`
- **Request Body**: Partial connection object to update
- **Response**: Updated connection object

## Variable Endpoints

### List Variables

- **Endpoint**: `GET /variables`
- **CLI Command**: `python scripts/airflow_cli.py variables [--limit N]`
- **Parameters**:
  - `limit` (query): Maximum number of results
  - `offset` (query): Pagination offset
- **Response**: List of variable objects with key, value

### Get Variable Value

- **Endpoint**: `GET /variables/{variable_key}`
- **CLI Command**: `python scripts/airflow_cli.py variable <variable_key>`
- **Response**: Variable object with key and value

### Set Variable

- **Endpoint**: `POST /variables`
- **Request Body**:
  ```json
  {
    "key": "my_variable",
    "value": "my_value"
  }
  ```
- **Response**: Created variable object

### Update Variable

- **Endpoint**: `PATCH /variables/{variable_key}`
- **Request Body**: `{"value": "new_value"}`
- **Response**: Updated variable object

## Pool Endpoints

### List Pools

- **Endpoint**: `GET /pools`
- **CLI Command**: `python scripts/airflow_cli.py pools [--limit N]`
- **Parameters**:
  - `limit` (query): Maximum number of results
  - `offset` (query): Pagination offset
- **Response**: List of pool objects with name, slots, description

### Create Pool

- **Endpoint**: `POST /pools`
- **Request Body**:
  ```json
  {
    "name": "my_pool",
    "slots": 5,
    "description": "Pool description"
  }
  ```
- **Response**: Created pool object

### Update Pool

- **Endpoint**: `PATCH /pools/{pool_name}`
- **Request Body**: `{"slots": 10}`
- **Response**: Updated pool object

## System Endpoints

### Check Airflow Health

- **Endpoint**: `GET /health`
- **CLI Command**: `python scripts/airflow_cli.py health`
- **Response**: Health status object with scheduler, metadatabase, and other component statuses

### Get Airflow Version

- **Endpoint**: `GET /version`
- **CLI Command**: `python scripts/airflow_cli.py version`
- **Response**: Version object with version number

## Common Response Status Codes

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 500 | Internal Server Error |

## Error Response Format

All error responses follow this format:

```json
{
  "detail": "Error description",
  "status": 400,
  "type": "error_type"
}
```

## Pagination

List endpoints support pagination via query parameters:

- `limit`: Maximum number of items to return (default: 100, max: 250)
- `offset`: Number of items to skip

Example:

```
GET /dags?limit=10&offset=20
```

## Filtering

Many list endpoints support filtering via query parameters. Common filters:

- `dag_id_pattern`: Filter by DAG ID using pattern matching
- `state`: Filter by execution state
- `only_active`: Return only active items (true/false)

## Rate Limiting

Airflow API typically has rate limiting. Check the response headers for:

- `X-RateLimit-Limit`: Maximum requests per time window
- `X-RateLimit-Remaining`: Requests remaining in current window
- `X-RateLimit-Reset`: Time when limit resets

## Timeout Recommendations

Recommended timeout values for different operations:

| Operation | Recommended Timeout |
|-----------|-------------------|
| List operations | 10 seconds |
| Single resource queries | 5 seconds |
| Trigger/Create operations | 15 seconds |
| Log retrieval | 20 seconds |
| Clear tasks | 30 seconds |
