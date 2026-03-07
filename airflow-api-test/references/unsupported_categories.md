# Unsupported API Categories

The following API categories are available in the specification but were NOT included in this skill:

## Connection

**Endpoints**: 6

**Available operations**:
- `GET /connections`
- `POST /connections`
- `POST /connections/test`
- `DELETE /connections/{connection_id}`
- `GET /connections/{connection_id}`
- ... and 1 more

## DAGRun

**Endpoints**: 9

**Available operations**:
- `GET /dags/{dag_id}/dagRuns`
- `POST /dags/{dag_id}/dagRuns`
- `DELETE /dags/{dag_id}/dagRuns/{dag_run_id}`
- `GET /dags/{dag_id}/dagRuns/{dag_run_id}`
- `PATCH /dags/{dag_id}/dagRuns/{dag_run_id}`
- ... and 4 more

## DagStats

**Endpoints**: 1

**Available operations**:
- `GET /dagStats`

## DagWarning

**Endpoints**: 1

**Available operations**:
- `GET /dagWarnings`

## Dataset

**Endpoints**: 11

**Available operations**:
- `GET /dags/{dag_id}/dagRuns/{dag_run_id}/upstreamDatasetEvents`
- `DELETE /dags/{dag_id}/datasets/queuedEvent`
- `GET /dags/{dag_id}/datasets/queuedEvent`
- `DELETE /dags/{dag_id}/datasets/queuedEvent/{uri}`
- `GET /dags/{dag_id}/datasets/queuedEvent/{uri}`
- ... and 6 more

## EventLog

**Endpoints**: 2

**Available operations**:
- `GET /eventLogs`
- `GET /eventLogs/{event_log_id}`

## ImportError

**Endpoints**: 2

**Available operations**:
- `GET /importErrors`
- `GET /importErrors/{import_error_id}`

## Monitoring

**Endpoints**: 2

**Available operations**:
- `GET /health`
- `GET /version`

## Permission

**Endpoints**: 1

**Available operations**:
- `GET /permissions`

## Plugin

**Endpoints**: 1

**Available operations**:
- `GET /plugins`

## Pool

**Endpoints**: 5

**Available operations**:
- `GET /pools`
- `POST /pools`
- `DELETE /pools/{pool_name}`
- `GET /pools/{pool_name}`
- `PATCH /pools/{pool_name}`

## Provider

**Endpoints**: 1

**Available operations**:
- `GET /providers`

## Role

**Endpoints**: 5

**Available operations**:
- `GET /roles`
- `POST /roles`
- `DELETE /roles/{role_name}`
- `GET /roles/{role_name}`
- `PATCH /roles/{role_name}`

## TaskInstance

**Endpoints**: 17

**Available operations**:
- `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances`
- `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}`
- `PATCH /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}`
- `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/dependencies`
- `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/links`
- ... and 12 more

## User

**Endpoints**: 5

**Available operations**:
- `GET /users`
- `POST /users`
- `DELETE /users/{username}`
- `GET /users/{username}`
- `PATCH /users/{username}`

## Variable

**Endpoints**: 5

**Available operations**:
- `GET /variables`
- `POST /variables`
- `DELETE /variables/{variable_key}`
- `GET /variables/{variable_key}`
- `PATCH /variables/{variable_key}`

## XCom

**Endpoints**: 2

**Available operations**:
- `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries`
- `GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries/{xcom_key}`

