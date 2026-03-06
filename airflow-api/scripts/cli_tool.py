#!/usr/bin/env python3
"""
Airflow API CLI Tool

A comprehensive command-line interface for managing Apache Airflow through its REST API.
Supports DAGs, task instances, variables, connections, and datasets.

Usage:
    python cli_tool.py [OPTIONS] COMMAND [ARGS]...

Environment Variables:
    AIRFLOW_API_URL - Base URL for Airflow API (default: http://localhost:8080/api/v1)
    AIRFLOW_USERNAME - Username for authentication
    AIRFLOW_PASSWORD - Password for authentication
"""

import os
import sys
import json
import click
from typing import Optional, Dict, Any
import requests
from urllib.parse import urljoin

# Configuration
DEFAULT_API_URL = "http://localhost:8080/api/v1"


class AirflowAPIClient:
    """Client for interacting with Airflow REST API"""
    
    def __init__(self, api_url: str, username: Optional[str] = None, password: Optional[str] = None):
        self.api_url = api_url.rstrip('/')
        self.session = requests.Session()
        if username and password:
            self.session.auth = (username, password)
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to Airflow API"""
        url = urljoin(f"{self.api_url}/", endpoint.lstrip('/'))
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json() if response.text else {}
        except requests.exceptions.RequestException as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
    
    def get(self, endpoint: str) -> Dict[str, Any]:
        return self._request("GET", endpoint)
    
    def post(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        return self._request("POST", endpoint, json=data)
    
    def put(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        return self._request("PUT", endpoint, json=data)
    
    def delete(self, endpoint: str) -> None:
        self._request("DELETE", endpoint)


@click.group()
@click.option('--api-url', envvar='AIRFLOW_API_URL', default=DEFAULT_API_URL,
              help='Airflow API base URL')
@click.option('--username', envvar='AIRFLOW_USERNAME', help='API username')
@click.option('--password', envvar='AIRFLOW_PASSWORD', help='API password')
@click.pass_context
def cli(ctx, api_url: str, username: Optional[str], password: Optional[str]):
    """Airflow API CLI Manager
    
    Manage Apache Airflow DAGs, tasks, variables, connections, and datasets.
    """
    ctx.ensure_object(dict)
    ctx.obj['client'] = AirflowAPIClient(api_url, username, password)


# DAG Commands
@cli.group()
def dag():
    """DAG management commands"""
    pass


@dag.command('list')
@click.option('--limit', type=int, default=100, help='Maximum number of DAGs to return')
@click.option('--offset', type=int, default=0, help='Offset for pagination')
@click.pass_context
def dag_list(ctx, limit: int, offset: int):
    """List all DAGs"""
    client = ctx.obj['client']
    params = {'limit': limit, 'offset': offset}
    result = client.get(f'/dags?limit={limit}&offset={offset}')
    click.echo(json.dumps(result, indent=2))


@dag.command('get')
@click.option('--dag-id', required=True, help='DAG ID')
@click.pass_context
def dag_get(ctx, dag_id: str):
    """Get DAG details"""
    client = ctx.obj['client']
    result = client.get(f'/dags/{dag_id}')
    click.echo(json.dumps(result, indent=2))


@dag.command('pause')
@click.option('--dag-id', required=True, help='DAG ID')
@click.pass_context
def dag_pause(ctx, dag_id: str):
    """Pause a DAG"""
    client = ctx.obj['client']
    client.patch(f'/dags/{dag_id}', data={'is_paused': True})
    click.echo(f"DAG '{dag_id}' paused successfully")


@dag.command('unpause')
@click.option('--dag-id', required=True, help='DAG ID')
@click.pass_context
def dag_unpause(ctx, dag_id: str):
    """Unpause a DAG"""
    client = ctx.obj['client']
    client.patch(f'/dags/{dag_id}', data={'is_paused': False})
    click.echo(f"DAG '{dag_id}' unpaused successfully")


# DAG Run Commands
@cli.group()
def dagrun():
    """DAG run management commands"""
    pass


@dagrun.command('list')
@click.option('--dag-id', required=True, help='DAG ID')
@click.option('--limit', type=int, default=100, help='Maximum number of runs')
@click.pass_context
def dagrun_list(ctx, dag_id: str, limit: int):
    """List DAG runs for a DAG"""
    client = ctx.obj['client']
    result = client.get(f'/dags/{dag_id}/dagRuns?limit={limit}')
    click.echo(json.dumps(result, indent=2))


@dagrun.command('trigger')
@click.option('--dag-id', required=True, help='DAG ID')
@click.option('--conf', type=str, help='JSON configuration for the run')
@click.pass_context
def dagrun_trigger(ctx, dag_id: str, conf: Optional[str]):
    """Trigger a DAG run"""
    client = ctx.obj['client']
    data = {}
    if conf:
        data['conf'] = json.loads(conf)
    result = client.post(f'/dags/{dag_id}/dagRuns', data=data)
    click.echo(json.dumps(result, indent=2))


@dagrun.command('get')
@click.option('--dag-id', required=True, help='DAG ID')
@click.option('--dag-run-id', required=True, help='DAG run ID')
@click.pass_context
def dagrun_get(ctx, dag_id: str, dag_run_id: str):
    """Get DAG run details"""
    client = ctx.obj['client']
    result = client.get(f'/dags/{dag_id}/dagRuns/{dag_run_id}')
    click.echo(json.dumps(result, indent=2))


# Task Instance Commands
@cli.group()
def task():
    """Task instance management commands"""
    pass


@task.command('list')
@click.option('--dag-id', required=True, help='DAG ID')
@click.option('--limit', type=int, default=100, help='Maximum number of tasks')
@click.pass_context
def task_list(ctx, dag_id: str, limit: int):
    """List task instances for a DAG"""
    client = ctx.obj['client']
    result = client.get(f'/dags/{dag_id}/tasks?limit={limit}')
    click.echo(json.dumps(result, indent=2))


@task.command('get')
@click.option('--dag-id', required=True, help='DAG ID')
@click.option('--task-id', required=True, help='Task ID')
@click.pass_context
def task_get(ctx, dag_id: str, task_id: str):
    """Get task details"""
    client = ctx.obj['client']
    result = client.get(f'/dags/{dag_id}/tasks/{task_id}')
    click.echo(json.dumps(result, indent=2))


# Variable Commands
@cli.group()
def variable():
    """Variable management commands"""
    pass


@variable.command('list')
@click.option('--limit', type=int, default=100, help='Maximum number of variables')
@click.pass_context
def variable_list(ctx, limit: int):
    """List all variables"""
    client = ctx.obj['client']
    result = client.get(f'/variables?limit={limit}')
    click.echo(json.dumps(result, indent=2))


@variable.command('get')
@click.option('--key', required=True, help='Variable key')
@click.pass_context
def variable_get(ctx, key: str):
    """Get variable value"""
    client = ctx.obj['client']
    result = client.get(f'/variables/{key}')
    click.echo(json.dumps(result, indent=2))


@variable.command('create')
@click.option('--key', required=True, help='Variable key')
@click.option('--value', required=True, help='Variable value')
@click.pass_context
def variable_create(ctx, key: str, value: str):
    """Create a new variable"""
    client = ctx.obj['client']
    data = {'key': key, 'value': value}
    result = client.post('/variables', data=data)
    click.echo(json.dumps(result, indent=2))


@variable.command('update')
@click.option('--key', required=True, help='Variable key')
@click.option('--value', required=True, help='Variable value')
@click.pass_context
def variable_update(ctx, key: str, value: str):
    """Update a variable"""
    client = ctx.obj['client']
    data = {'key': key, 'value': value}
    result = client.put(f'/variables/{key}', data=data)
    click.echo(json.dumps(result, indent=2))


@variable.command('delete')
@click.option('--key', required=True, help='Variable key')
@click.pass_context
def variable_delete(ctx, key: str):
    """Delete a variable"""
    client = ctx.obj['client']
    client.delete(f'/variables/{key}')
    click.echo(f"Variable '{key}' deleted successfully")


# Connection Commands
@cli.group()
def connection():
    """Connection management commands"""
    pass


@connection.command('list')
@click.option('--limit', type=int, default=100, help='Maximum number of connections')
@click.pass_context
def connection_list(ctx, limit: int):
    """List all connections"""
    client = ctx.obj['client']
    result = client.get(f'/connections?limit={limit}')
    click.echo(json.dumps(result, indent=2))


@connection.command('get')
@click.option('--conn-id', required=True, help='Connection ID')
@click.pass_context
def connection_get(ctx, conn_id: str):
    """Get connection details"""
    client = ctx.obj['client']
    result = client.get(f'/connections/{conn_id}')
    click.echo(json.dumps(result, indent=2))


@connection.command('create')
@click.option('--conn-id', required=True, help='Connection ID')
@click.option('--conn-type', required=True, help='Connection type')
@click.option('--host', help='Host')
@click.option('--port', type=int, help='Port')
@click.option('--login', help='Login/username')
@click.option('--password', help='Password')
@click.pass_context
def connection_create(ctx, conn_id: str, conn_type: str, host: Optional[str], 
                     port: Optional[int], login: Optional[str], password: Optional[str]):
    """Create a new connection"""
    client = ctx.obj['client']
    data = {
        'conn_id': conn_id,
        'conn_type': conn_type,
        'host': host,
        'port': port,
        'login': login,
        'password': password
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}
    result = client.post('/connections', data=data)
    click.echo(json.dumps(result, indent=2))


@connection.command('delete')
@click.option('--conn-id', required=True, help='Connection ID')
@click.pass_context
def connection_delete(ctx, conn_id: str):
    """Delete a connection"""
    client = ctx.obj['client']
    client.delete(f'/connections/{conn_id}')
    click.echo(f"Connection '{conn_id}' deleted successfully")


# Dataset Commands
@cli.group()
def dataset():
    """Dataset management commands"""
    pass


@dataset.command('list')
@click.option('--limit', type=int, default=100, help='Maximum number of datasets')
@click.pass_context
def dataset_list(ctx, limit: int):
    """List all datasets"""
    client = ctx.obj['client']
    result = client.get(f'/datasets?limit={limit}')
    click.echo(json.dumps(result, indent=2))


@dataset.command('get')
@click.option('--dataset-id', required=True, help='Dataset URI')
@click.pass_context
def dataset_get(ctx, dataset_id: str):
    """Get dataset details"""
    client = ctx.obj['client']
    result = client.get(f'/datasets/{dataset_id}')
    click.echo(json.dumps(result, indent=2))


@dataset.command('create')
@click.option('--uri', required=True, help='Dataset URI')
@click.pass_context
def dataset_create(ctx, uri: str):
    """Create a new dataset"""
    client = ctx.obj['client']
    data = {'uri': uri}
    result = client.post('/datasets', data=data)
    click.echo(json.dumps(result, indent=2))


if __name__ == '__main__':
    cli(obj={})
