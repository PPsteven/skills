# API Endpoints Reference

**Selected Categories**: Config, Connection, DAG, DAGRun, DagStats, DagWarning, Dataset, EventLog, ImportError, Monitoring, Permission, Plugin, Pool, Provider, Role, TaskInstance, User, Variable, XCom

## Config

### 1. GET /config

**Description**: Get current configuration

- **Method**: `GET`
- **Path**: `/config`
- **Operation ID**: `get_config`
- **Parameters**: 1 parameters

### 2. GET /config/section/{section}/option/{option}

**Description**: Get a option from configuration

- **Method**: `GET`
- **Path**: `/config/section/{section}/option/{option}`
- **Operation ID**: `get_value`
- **Parameters**: 2 parameters

## Connection

### 1. GET /connections

**Description**: List connections

- **Method**: `GET`
- **Path**: `/connections`
- **Operation ID**: `get_connections`
- **Parameters**: 3 parameters

### 2. POST /connections

**Description**: Create a connection

- **Method**: `POST`
- **Path**: `/connections`
- **Operation ID**: `post_connection`
- **Parameters**: 0 parameters

### 3. POST /connections/test

**Description**: Test a connection

Test a connection.

For security reasons, the test connection functionality is disabled by default across Airflow UI, API and CLI.
For more information on capabilities of users, see the documentation:
https://airflow.apache.org/docs/apache-airflow/stable/security/security_model.html#capabilities-of-authenticated-ui-users.
It is strongly advised to not enable the feature until you make sure that only
highly trusted UI/API users have "edit connection" permissions.

Set the "test_connection" flag to "Enabled" in the "core" section of Airflow configuration (airflow.cfg) to enable testing of collections.
It can also be controlled by the environment variable `AIRFLOW__CORE__TEST_CONNECTION`.

*New in version 2.2.0*


- **Method**: `POST`
- **Path**: `/connections/test`
- **Operation ID**: `test_connection`
- **Parameters**: 0 parameters

### 4. DELETE /connections/{connection_id}

**Description**: Delete a connection

- **Method**: `DELETE`
- **Path**: `/connections/{connection_id}`
- **Operation ID**: `delete_connection`
- **Parameters**: 0 parameters

### 5. GET /connections/{connection_id}

**Description**: Get a connection

- **Method**: `GET`
- **Path**: `/connections/{connection_id}`
- **Operation ID**: `get_connection`
- **Parameters**: 0 parameters

### 6. PATCH /connections/{connection_id}

**Description**: Update a connection

- **Method**: `PATCH`
- **Path**: `/connections/{connection_id}`
- **Operation ID**: `patch_connection`
- **Parameters**: 1 parameters

## DAG

### 1. GET /dagSources/{file_token}

**Description**: Get a source code

Get a source code using file token.


- **Method**: `GET`
- **Path**: `/dagSources/{file_token}`
- **Operation ID**: `get_dag_source`
- **Parameters**: 0 parameters

### 2. GET /dags

**Description**: List DAGs

List DAGs in the database.
`dag_id_pattern` can be set to match dags of a specific pattern


- **Method**: `GET`
- **Path**: `/dags`
- **Operation ID**: `get_dags`
- **Parameters**: 8 parameters

### 3. PATCH /dags

**Description**: Update DAGs

Update DAGs of a given dag_id_pattern using UpdateMask.
This endpoint allows specifying `~` as the dag_id_pattern to update all DAGs.
*New in version 2.3.0*


- **Method**: `PATCH`
- **Path**: `/dags`
- **Operation ID**: `patch_dags`
- **Parameters**: 6 parameters

### 4. DELETE /dags/{dag_id}

**Description**: Delete a DAG

Deletes all metadata related to the DAG, including finished DAG Runs and Tasks.
Logs are not deleted. This action cannot be undone.

*New in version 2.2.0*


- **Method**: `DELETE`
- **Path**: `/dags/{dag_id}`
- **Operation ID**: `delete_dag`
- **Parameters**: 0 parameters

### 5. GET /dags/{dag_id}

**Description**: Get basic information about a DAG

Presents only information available in database (DAGModel).
If you need detailed information, consider using GET /dags/{dag_id}/details.


- **Method**: `GET`
- **Path**: `/dags/{dag_id}`
- **Operation ID**: `get_dag`
- **Parameters**: 1 parameters

### 6. PATCH /dags/{dag_id}

**Description**: Update a DAG

- **Method**: `PATCH`
- **Path**: `/dags/{dag_id}`
- **Operation ID**: `patch_dag`
- **Parameters**: 1 parameters

### 7. POST /dags/{dag_id}/clearTaskInstances

**Description**: Clear a set of task instances

Clears a set of task instances associated with the DAG for a specified date range.


- **Method**: `POST`
- **Path**: `/dags/{dag_id}/clearTaskInstances`
- **Operation ID**: `post_clear_task_instances`
- **Parameters**: 0 parameters

### 8. GET /dags/{dag_id}/details

**Description**: Get a simplified representation of DAG

The response contains many DAG attributes, so the response can be large. If possible, consider using GET /dags/{dag_id}.


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/details`
- **Operation ID**: `get_dag_details`
- **Parameters**: 1 parameters

### 9. GET /dags/{dag_id}/tasks

**Description**: Get tasks for DAG

- **Method**: `GET`
- **Path**: `/dags/{dag_id}/tasks`
- **Operation ID**: `get_tasks`
- **Parameters**: 0 parameters

### 10. GET /dags/{dag_id}/tasks/{task_id}

**Description**: Get simplified representation of a task

- **Method**: `GET`
- **Path**: `/dags/{dag_id}/tasks/{task_id}`
- **Operation ID**: `get_task`
- **Parameters**: 0 parameters

### 11. POST /dags/{dag_id}/updateTaskInstancesState

**Description**: Set a state of task instances

Updates the state for multiple task instances simultaneously.


- **Method**: `POST`
- **Path**: `/dags/{dag_id}/updateTaskInstancesState`
- **Operation ID**: `post_set_task_instances_state`
- **Parameters**: 0 parameters

### 12. PUT /parseDagFile/{file_token}

**Description**: Request re-parsing of a DAG file

Request re-parsing of existing DAG files using a file token.


- **Method**: `PUT`
- **Path**: `/parseDagFile/{file_token}`
- **Operation ID**: `reparse_dag_file`
- **Parameters**: 0 parameters

## DAGRun

### 1. GET /dags/{dag_id}/dagRuns

**Description**: List DAG runs

This endpoint allows specifying `~` as the dag_id to retrieve DAG runs for all DAGs.


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns`
- **Operation ID**: `get_dag_runs`
- **Parameters**: 13 parameters

### 2. POST /dags/{dag_id}/dagRuns

**Description**: Trigger a new DAG run.

This will initiate a dagrun. If DAG is paused then dagrun state will remain queued, and the task won't run.


- **Method**: `POST`
- **Path**: `/dags/{dag_id}/dagRuns`
- **Operation ID**: `post_dag_run`
- **Parameters**: 0 parameters

### 3. DELETE /dags/{dag_id}/dagRuns/{dag_run_id}

**Description**: Delete a DAG run

- **Method**: `DELETE`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}`
- **Operation ID**: `delete_dag_run`
- **Parameters**: 0 parameters

### 4. GET /dags/{dag_id}/dagRuns/{dag_run_id}

**Description**: Get a DAG run

- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}`
- **Operation ID**: `get_dag_run`
- **Parameters**: 1 parameters

### 5. PATCH /dags/{dag_id}/dagRuns/{dag_run_id}

**Description**: Modify a DAG run

Modify a DAG run.

*New in version 2.2.0*


- **Method**: `PATCH`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}`
- **Operation ID**: `update_dag_run_state`
- **Parameters**: 0 parameters

### 6. POST /dags/{dag_id}/dagRuns/{dag_run_id}/clear

**Description**: Clear a DAG run

Clear a DAG run.

*New in version 2.4.0*


- **Method**: `POST`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/clear`
- **Operation ID**: `clear_dag_run`
- **Parameters**: 0 parameters

### 7. PATCH /dags/{dag_id}/dagRuns/{dag_run_id}/setNote

**Description**: Update the DagRun note.

Update the manual user note of a DagRun.

*New in version 2.5.0*


- **Method**: `PATCH`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/setNote`
- **Operation ID**: `set_dag_run_note`
- **Parameters**: 0 parameters

### 8. GET /dags/{dag_id}/dagRuns/{dag_run_id}/upstreamDatasetEvents

**Description**: Get dataset events for a DAG run

Get datasets for a dag run.

*New in version 2.4.0*


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/upstreamDatasetEvents`
- **Operation ID**: `get_upstream_dataset_events`
- **Parameters**: 0 parameters

### 9. POST /dags/~/dagRuns/list

**Description**: List DAG runs (batch)

This endpoint is a POST to allow filtering across a large number of DAG IDs, where as a GET it would run in to maximum HTTP request URL length limit.


- **Method**: `POST`
- **Path**: `/dags/~/dagRuns/list`
- **Operation ID**: `get_dag_runs_batch`
- **Parameters**: 0 parameters

## DagStats

### 1. GET /dagStats

**Description**: List Dag statistics

- **Method**: `GET`
- **Path**: `/dagStats`
- **Operation ID**: `get_dag_stats`
- **Parameters**: 1 parameters

## DagWarning

### 1. GET /dagWarnings

**Description**: List dag warnings

- **Method**: `GET`
- **Path**: `/dagWarnings`
- **Operation ID**: `get_dag_warnings`
- **Parameters**: 5 parameters

## Dataset

### 1. GET /dags/{dag_id}/dagRuns/{dag_run_id}/upstreamDatasetEvents

**Description**: Get dataset events for a DAG run

Get datasets for a dag run.

*New in version 2.4.0*


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/upstreamDatasetEvents`
- **Operation ID**: `get_upstream_dataset_events`
- **Parameters**: 0 parameters

### 2. DELETE /dags/{dag_id}/datasets/queuedEvent

**Description**: Delete queued Dataset events for a DAG.

Delete queued Dataset events for a DAG.

*New in version 2.9.0*


- **Method**: `DELETE`
- **Path**: `/dags/{dag_id}/datasets/queuedEvent`
- **Operation ID**: `delete_dag_dataset_queued_events`
- **Parameters**: 1 parameters

### 3. GET /dags/{dag_id}/datasets/queuedEvent

**Description**: Get queued Dataset events for a DAG.

Get queued Dataset events for a DAG.

*New in version 2.9.0*


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/datasets/queuedEvent`
- **Operation ID**: `get_dag_dataset_queued_events`
- **Parameters**: 1 parameters

### 4. DELETE /dags/{dag_id}/datasets/queuedEvent/{uri}

**Description**: Delete a queued Dataset event for a DAG.

Delete a queued Dataset event for a DAG.

*New in version 2.9.0*


- **Method**: `DELETE`
- **Path**: `/dags/{dag_id}/datasets/queuedEvent/{uri}`
- **Operation ID**: `delete_dag_dataset_queued_event`
- **Parameters**: 1 parameters

### 5. GET /dags/{dag_id}/datasets/queuedEvent/{uri}

**Description**: Get a queued Dataset event for a DAG

Get a queued Dataset event for a DAG.

*New in version 2.9.0*


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/datasets/queuedEvent/{uri}`
- **Operation ID**: `get_dag_dataset_queued_event`
- **Parameters**: 1 parameters

### 6. GET /datasets

**Description**: List datasets

- **Method**: `GET`
- **Path**: `/datasets`
- **Operation ID**: `get_datasets`
- **Parameters**: 5 parameters

### 7. GET /datasets/events

**Description**: Get dataset events

Get dataset events

- **Method**: `GET`
- **Path**: `/datasets/events`
- **Operation ID**: `get_dataset_events`
- **Parameters**: 8 parameters

### 8. POST /datasets/events

**Description**: Create dataset event

Create dataset event

- **Method**: `POST`
- **Path**: `/datasets/events`
- **Operation ID**: `create_dataset_event`
- **Parameters**: 0 parameters

### 9. DELETE /datasets/queuedEvent/{uri}

**Description**: Delete queued Dataset events for a Dataset.

Delete queued Dataset events for a Dataset.

*New in version 2.9.0*


- **Method**: `DELETE`
- **Path**: `/datasets/queuedEvent/{uri}`
- **Operation ID**: `delete_dataset_queued_events`
- **Parameters**: 1 parameters

### 10. GET /datasets/queuedEvent/{uri}

**Description**: Get queued Dataset events for a Dataset.

Get queued Dataset events for a Dataset

*New in version 2.9.0*


- **Method**: `GET`
- **Path**: `/datasets/queuedEvent/{uri}`
- **Operation ID**: `get_dataset_queued_events`
- **Parameters**: 1 parameters

### 11. GET /datasets/{uri}

**Description**: Get a dataset

Get a dataset by uri.

- **Method**: `GET`
- **Path**: `/datasets/{uri}`
- **Operation ID**: `get_dataset`
- **Parameters**: 0 parameters

## EventLog

### 1. GET /eventLogs

**Description**: List log entries

List log entries from event log.

- **Method**: `GET`
- **Path**: `/eventLogs`
- **Operation ID**: `get_event_logs`
- **Parameters**: 14 parameters

### 2. GET /eventLogs/{event_log_id}

**Description**: Get a log entry

- **Method**: `GET`
- **Path**: `/eventLogs/{event_log_id}`
- **Operation ID**: `get_event_log`
- **Parameters**: 0 parameters

## ImportError

### 1. GET /importErrors

**Description**: List import errors

- **Method**: `GET`
- **Path**: `/importErrors`
- **Operation ID**: `get_import_errors`
- **Parameters**: 3 parameters

### 2. GET /importErrors/{import_error_id}

**Description**: Get an import error

- **Method**: `GET`
- **Path**: `/importErrors/{import_error_id}`
- **Operation ID**: `get_import_error`
- **Parameters**: 0 parameters

## Monitoring

### 1. GET /health

**Description**: Get instance status

Get the status of Airflow's metadatabase, triggerer and scheduler. It includes info about
metadatabase and last heartbeat of scheduler and triggerer.


- **Method**: `GET`
- **Path**: `/health`
- **Operation ID**: `get_health`
- **Parameters**: 0 parameters

### 2. GET /version

**Description**: Get version information

- **Method**: `GET`
- **Path**: `/version`
- **Operation ID**: `get_version`
- **Parameters**: 0 parameters

## Permission

### 1. GET /permissions

**Description**: List permissions

Get a list of permissions.

*This API endpoint is deprecated, please use the endpoint `/auth/fab/v1` for this operation instead.*


- **Method**: `GET`
- **Path**: `/permissions`
- **Operation ID**: `get_permissions`
- **Parameters**: 2 parameters

## Plugin

### 1. GET /plugins

**Description**: Get a list of loaded plugins

Get a list of loaded plugins.

*New in version 2.1.0*


- **Method**: `GET`
- **Path**: `/plugins`
- **Operation ID**: `get_plugins`
- **Parameters**: 2 parameters

## Pool

### 1. GET /pools

**Description**: List pools

- **Method**: `GET`
- **Path**: `/pools`
- **Operation ID**: `get_pools`
- **Parameters**: 3 parameters

### 2. POST /pools

**Description**: Create a pool

- **Method**: `POST`
- **Path**: `/pools`
- **Operation ID**: `post_pool`
- **Parameters**: 0 parameters

### 3. DELETE /pools/{pool_name}

**Description**: Delete a pool

- **Method**: `DELETE`
- **Path**: `/pools/{pool_name}`
- **Operation ID**: `delete_pool`
- **Parameters**: 0 parameters

### 4. GET /pools/{pool_name}

**Description**: Get a pool

- **Method**: `GET`
- **Path**: `/pools/{pool_name}`
- **Operation ID**: `get_pool`
- **Parameters**: 0 parameters

### 5. PATCH /pools/{pool_name}

**Description**: Update a pool

- **Method**: `PATCH`
- **Path**: `/pools/{pool_name}`
- **Operation ID**: `patch_pool`
- **Parameters**: 1 parameters

## Provider

### 1. GET /providers

**Description**: List providers

Get a list of providers.

*New in version 2.1.0*


- **Method**: `GET`
- **Path**: `/providers`
- **Operation ID**: `get_providers`
- **Parameters**: 0 parameters

## Role

### 1. GET /roles

**Description**: List roles

Get a list of roles.

*This API endpoint is deprecated, please use the endpoint `/auth/fab/v1` for this operation instead.*


- **Method**: `GET`
- **Path**: `/roles`
- **Operation ID**: `get_roles`
- **Parameters**: 3 parameters

### 2. POST /roles

**Description**: Create a role

Create a new role.

*This API endpoint is deprecated, please use the endpoint `/auth/fab/v1` for this operation instead.*


- **Method**: `POST`
- **Path**: `/roles`
- **Operation ID**: `post_role`
- **Parameters**: 0 parameters

### 3. DELETE /roles/{role_name}

**Description**: Delete a role

Delete a role.

*This API endpoint is deprecated, please use the endpoint `/auth/fab/v1` for this operation instead.*


- **Method**: `DELETE`
- **Path**: `/roles/{role_name}`
- **Operation ID**: `delete_role`
- **Parameters**: 0 parameters

### 4. GET /roles/{role_name}

**Description**: Get a role

Get a role.

*This API endpoint is deprecated, please use the endpoint `/auth/fab/v1` for this operation instead.*


- **Method**: `GET`
- **Path**: `/roles/{role_name}`
- **Operation ID**: `get_role`
- **Parameters**: 0 parameters

### 5. PATCH /roles/{role_name}

**Description**: Update a role

Update a role.

*This API endpoint is deprecated, please use the endpoint `/auth/fab/v1` for this operation instead.*


- **Method**: `PATCH`
- **Path**: `/roles/{role_name}`
- **Operation ID**: `patch_role`
- **Parameters**: 1 parameters

## TaskInstance

### 1. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances

**Description**: List task instances

This endpoint allows specifying `~` as the dag_id, dag_run_id to retrieve DAG runs for all DAGs and DAG runs.


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances`
- **Operation ID**: `get_task_instances`
- **Parameters**: 2 parameters

### 2. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}

**Description**: Get a task instance

- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}`
- **Operation ID**: `get_task_instance`
- **Parameters**: 0 parameters

### 3. PATCH /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}

**Description**: Updates the state of a task instance

Updates the state for single task instance.
*New in version 2.5.0*


- **Method**: `PATCH`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}`
- **Operation ID**: `patch_task_instance`
- **Parameters**: 0 parameters

### 4. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/dependencies

**Description**: Get task dependencies blocking task from getting scheduled.

Get task dependencies blocking task from getting scheduled.

*New in version 2.10.0*


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/dependencies`
- **Operation ID**: `get_task_instance_dependencies`
- **Parameters**: 0 parameters

### 5. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/links

**Description**: List extra links

List extra links for task instance.


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/links`
- **Operation ID**: `get_extra_links`
- **Parameters**: 0 parameters

### 6. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/listMapped

**Description**: List mapped task instances

Get details of all mapped task instances.

*New in version 2.3.0*


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/listMapped`
- **Operation ID**: `get_mapped_task_instances`
- **Parameters**: 17 parameters

### 7. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{task_try_number}

**Description**: Get logs

Get logs for a specific task instance and its try number.
To get log from specific character position, following way of using
URLSafeSerializer can be used.

Example:
```
from itsdangerous.url_safe import URLSafeSerializer

request_url = f"api/v1/dags/{DAG_ID}/dagRuns/{RUN_ID}/taskInstances/{TASK_ID}/logs/1"
key = app.config["SECRET_KEY"]
serializer = URLSafeSerializer(key)
token = serializer.dumps({"log_pos": 10000})

response = self.client.get(
    request_url,
    query_string={"token": token},
    headers={"Accept": "text/plain"},
    environ_overrides={"REMOTE_USER": "test"},
)
continuation_token = response.json["continuation_token"]
    metadata = URLSafeSerializer(key).loads(continuation_token)
    log_pos = metadata["log_pos"]
    end_of_log = metadata["end_of_log"]
```
If log_pos is passed as 10000 like the above example, it renders the logs starting
from char position 10000 to last (not the end as the logs may be tailing behind in
running state). This way pagination can be done with metadata as part of the token.


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{task_try_number}`
- **Operation ID**: `get_log`
- **Parameters**: 0 parameters

### 8. PATCH /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/setNote

**Description**: Update the TaskInstance note.

Update the manual user note of a non-mapped Task Instance.

*New in version 2.5.0*


- **Method**: `PATCH`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/setNote`
- **Operation ID**: `set_task_instance_note`
- **Parameters**: 0 parameters

### 9. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/tries

**Description**: List task instance tries

Get details of all task instance tries.

*New in version 2.10.0*


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/tries`
- **Operation ID**: `get_task_instance_tries`
- **Parameters**: 6 parameters

### 10. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/tries/{task_try_number}

**Description**: get taskinstance try

Get details of a task instance try.

*New in version 2.10.0*


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/tries/{task_try_number}`
- **Operation ID**: `get_task_instance_try_details`
- **Parameters**: 4 parameters

### 11. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}

**Description**: Get a mapped task instance

Get details of a mapped task instance.

*New in version 2.3.0*


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}`
- **Operation ID**: `get_mapped_task_instance`
- **Parameters**: 0 parameters

### 12. PATCH /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}

**Description**: Updates the state of a mapped task instance

Updates the state for single mapped task instance.
*New in version 2.5.0*


- **Method**: `PATCH`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}`
- **Operation ID**: `patch_mapped_task_instance`
- **Parameters**: 0 parameters

### 13. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}/dependencies

**Description**: Get task dependencies blocking task from getting scheduled.

Get task dependencies blocking task from getting scheduled.

*New in version 2.10.0*


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}/dependencies`
- **Operation ID**: `get_mapped_task_instance_dependencies`
- **Parameters**: 0 parameters

### 14. PATCH /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}/setNote

**Description**: Update the TaskInstance note.

Update the manual user note of a mapped Task Instance.

*New in version 2.5.0*


- **Method**: `PATCH`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}/setNote`
- **Operation ID**: `set_mapped_task_instance_note`
- **Parameters**: 0 parameters

### 15. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}/tries

**Description**: List mapped task instance tries

Get details of all task instance tries.

*New in version 2.10.0*


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}/tries`
- **Operation ID**: `get_mapped_task_instance_tries`
- **Parameters**: 7 parameters

### 16. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}/tries/{task_try_number}

**Description**: get mapped taskinstance try

Get details of a mapped task instance try.

*New in version 2.10.0*


- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}/tries/{task_try_number}`
- **Operation ID**: `get_mapped_task_instance_try_details`
- **Parameters**: 5 parameters

### 17. POST /dags/~/dagRuns/~/taskInstances/list

**Description**: List task instances (batch)

List task instances from all DAGs and DAG runs.
This endpoint is a POST to allow filtering across a large number of DAG IDs, where as a GET it would run in to maximum HTTP request URL length limits.


- **Method**: `POST`
- **Path**: `/dags/~/dagRuns/~/taskInstances/list`
- **Operation ID**: `get_task_instances_batch`
- **Parameters**: 0 parameters

## User

### 1. GET /users

**Description**: List users

Get a list of users.

*This API endpoint is deprecated, please use the endpoint `/auth/fab/v1` for this operation instead.*


- **Method**: `GET`
- **Path**: `/users`
- **Operation ID**: `get_users`
- **Parameters**: 3 parameters

### 2. POST /users

**Description**: Create a user

Create a new user with unique username and email.

*This API endpoint is deprecated, please use the endpoint `/auth/fab/v1` for this operation instead.*


- **Method**: `POST`
- **Path**: `/users`
- **Operation ID**: `post_user`
- **Parameters**: 0 parameters

### 3. DELETE /users/{username}

**Description**: Delete a user

Delete a user with a specific username.

*This API endpoint is deprecated, please use the endpoint `/auth/fab/v1` for this operation instead.*


- **Method**: `DELETE`
- **Path**: `/users/{username}`
- **Operation ID**: `delete_user`
- **Parameters**: 0 parameters

### 4. GET /users/{username}

**Description**: Get a user

Get a user with a specific username.

*This API endpoint is deprecated, please use the endpoint `/auth/fab/v1` for this operation instead.*


- **Method**: `GET`
- **Path**: `/users/{username}`
- **Operation ID**: `get_user`
- **Parameters**: 0 parameters

### 5. PATCH /users/{username}

**Description**: Update a user

Update fields for a user.

*This API endpoint is deprecated, please use the endpoint `/auth/fab/v1` for this operation instead.*


- **Method**: `PATCH`
- **Path**: `/users/{username}`
- **Operation ID**: `patch_user`
- **Parameters**: 1 parameters

## Variable

### 1. GET /variables

**Description**: List variables

The collection does not contain data. To get data, you must get a single entity.

- **Method**: `GET`
- **Path**: `/variables`
- **Operation ID**: `get_variables`
- **Parameters**: 3 parameters

### 2. POST /variables

**Description**: Create a variable

- **Method**: `POST`
- **Path**: `/variables`
- **Operation ID**: `post_variables`
- **Parameters**: 0 parameters

### 3. DELETE /variables/{variable_key}

**Description**: Delete a variable

- **Method**: `DELETE`
- **Path**: `/variables/{variable_key}`
- **Operation ID**: `delete_variable`
- **Parameters**: 0 parameters

### 4. GET /variables/{variable_key}

**Description**: Get a variable

Get a variable by key.

- **Method**: `GET`
- **Path**: `/variables/{variable_key}`
- **Operation ID**: `get_variable`
- **Parameters**: 0 parameters

### 5. PATCH /variables/{variable_key}

**Description**: Update a variable

Update a variable by key.

- **Method**: `PATCH`
- **Path**: `/variables/{variable_key}`
- **Operation ID**: `patch_variable`
- **Parameters**: 1 parameters

## XCom

### 1. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries

**Description**: List XCom entries

This endpoint allows specifying `~` as the dag_id, dag_run_id, task_id to retrieve XCOM entries for for all DAGs, DAG runs and task instances. XCom values won't be returned as they can be large. Use this endpoint to get a list of XCom entries and then fetch individual entry to get value.

- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries`
- **Operation ID**: `get_xcom_entries`
- **Parameters**: 4 parameters

### 2. GET /dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries/{xcom_key}

**Description**: Get an XCom entry

- **Method**: `GET`
- **Path**: `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries/{xcom_key}`
- **Operation ID**: `get_xcom_entry`
- **Parameters**: 3 parameters

