# API Endpoints Reference

**Selected Categories**: Config, DAG

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

