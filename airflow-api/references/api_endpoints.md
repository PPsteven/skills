# Airflow API Endpoints Reference

This document provides a comprehensive reference for all implemented Airflow API endpoints.

## Endpoint Organization

Endpoints are organized by category. For each category, the available operations are listed with their HTTP method and path.


## Connection

- **DELETE** `/connections/{connection_id}`
  Delete a connection
- **GET** `/connections`
  List connections
- **GET** `/connections/{connection_id}`
  Get a connection
- **PATCH** `/connections/{connection_id}`
  Update a connection
- **POST** `/connections`
  Create a connection
- **POST** `/connections/test`
  Test a connection


## DAG

- **DELETE** `/dags/{dag_id}`
  Delete a DAG
- **GET** `/dagSources/{file_token}`
  Get a source code
- **GET** `/dags`
  List DAGs
- **GET** `/dags/{dag_id}`
  Get basic information about a DAG
- **GET** `/dags/{dag_id}/details`
  Get a simplified representation of DAG
- **GET** `/dags/{dag_id}/tasks`
  Get tasks for DAG
- **GET** `/dags/{dag_id}/tasks/{task_id}`
  Get simplified representation of a task
- **PATCH** `/dags`
  Update DAGs
- **PATCH** `/dags/{dag_id}`
  Update a DAG
- **POST** `/dags/{dag_id}/clearTaskInstances`
  Clear a set of task instances
- **POST** `/dags/{dag_id}/updateTaskInstancesState`
  Set a state of task instances
- **PUT** `/parseDagFile/{file_token}`
  Request re-parsing of a DAG file


## DAGRun

- **DELETE** `/dags/{dag_id}/dagRuns/{dag_run_id}`
  Delete a DAG run
- **GET** `/dags/{dag_id}/dagRuns`
  List DAG runs
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}`
  Get a DAG run
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/upstreamDatasetEvents`
  Get dataset events for a DAG run
- **PATCH** `/dags/{dag_id}/dagRuns/{dag_run_id}`
  Modify a DAG run
- **PATCH** `/dags/{dag_id}/dagRuns/{dag_run_id}/setNote`
  Update the DagRun note.
- **POST** `/dags/{dag_id}/dagRuns`
  Trigger a new DAG run.
- **POST** `/dags/{dag_id}/dagRuns/{dag_run_id}/clear`
  Clear a DAG run
- **POST** `/dags/~/dagRuns/list`
  List DAG runs (batch)


## Dataset

- **DELETE** `/dags/{dag_id}/datasets/queuedEvent`
  Delete queued Dataset events for a DAG.
- **DELETE** `/dags/{dag_id}/datasets/queuedEvent/{uri}`
  Delete a queued Dataset event for a DAG.
- **DELETE** `/datasets/queuedEvent/{uri}`
  Delete queued Dataset events for a Dataset.
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/upstreamDatasetEvents`
  Get dataset events for a DAG run
- **GET** `/dags/{dag_id}/datasets/queuedEvent`
  Get queued Dataset events for a DAG.
- **GET** `/dags/{dag_id}/datasets/queuedEvent/{uri}`
  Get a queued Dataset event for a DAG
- **GET** `/datasets`
  List datasets
- **GET** `/datasets/events`
  Get dataset events
- **GET** `/datasets/queuedEvent/{uri}`
  Get queued Dataset events for a Dataset.
- **GET** `/datasets/{uri}`
  Get a dataset
- **POST** `/datasets/events`
  Create dataset event


## TaskInstance

- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances`
  List task instances
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}`
  Get a task instance
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/dependencies`
  Get task dependencies blocking task from getting scheduled.
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/links`
  List extra links
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/listMapped`
  List mapped task instances
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{task_try_number}`
  Get logs
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/tries`
  List task instance tries
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/tries/{task_try_number}`
  get taskinstance try
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}`
  Get a mapped task instance
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}/dependencies`
  Get task dependencies blocking task from getting scheduled.
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}/tries`
  List mapped task instance tries
- **GET** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}/tries/{task_try_number}`
  get mapped taskinstance try
- **PATCH** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}`
  Updates the state of a task instance
- **PATCH** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/setNote`
  Update the TaskInstance note.
- **PATCH** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}`
  Updates the state of a mapped task instance
- **PATCH** `/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/{map_index}/setNote`
  Update the TaskInstance note.
- **POST** `/dags/~/dagRuns/~/taskInstances/list`
  List task instances (batch)


## Variable

- **DELETE** `/variables/{variable_key}`
  Delete a variable
- **GET** `/variables`
  List variables
- **GET** `/variables/{variable_key}`
  Get a variable
- **PATCH** `/variables/{variable_key}`
  Update a variable
- **POST** `/variables`
  Create a variable


## Total Endpoints

- **Categories**: 6
- **Endpoints**: 60

## Authentication

All endpoints require authentication. Provide credentials via:

- Environment variables: `AIRFLOW_USERNAME` and `AIRFLOW_PASSWORD`
- CLI flags: `--username` and `--password`
- HTTP Basic Auth headers

## Base URL

Default: `http://localhost:8080/api/v1`

Can be overridden via `AIRFLOW_API_URL` environment variable or `--api-url` CLI flag.
