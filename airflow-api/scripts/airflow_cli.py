#!/usr/bin/env python3
"""
Airflow API CLI Tool

Provides command-line interface to Airflow REST API for querying task status,
retrieving logs, and managing DAG operations.
"""

import os
import sys
import json
import argparse
import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin
import base64


class AirflowAPIClient:
    """Client for Airflow REST API"""

    def __init__(self):
        self.base_url = os.environ.get("AIRFLOW_API_URL")
        if not self.base_url:
            raise ValueError("AIRFLOW_API_URL environment variable is required")

        self.session = requests.Session()
        self._setup_auth()

    def _setup_auth(self):
        """Setup HTTP Basic Authentication"""
        token = os.environ.get("AIRFLOW_API_TOKEN")
        if token:
            self.session.headers.update({"Authorization": token})
        else:
            username = os.environ.get("AIRFLOW_API_USER")
            password = os.environ.get("AIRFLOW_API_PASSWORD")
            if username and password:
                auth_string = base64.b64encode(f"{username}:{password}".encode()).decode()
                self.session.headers.update({"Authorization": f"Basic {auth_string}"})

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to Airflow API"""
        url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request"""
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """POST request"""
        return self._make_request("POST", endpoint, json=json_data)

    def patch(self, endpoint: str, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """PATCH request"""
        return self._make_request("PATCH", endpoint, json=json_data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE request"""
        return self._make_request("DELETE", endpoint)


def print_json(data: Any):
    """Print data as formatted JSON"""
    print(json.dumps(data, indent=2, default=str))


def task_instances(args):
    """List task instances for a DAG run"""
    client = AirflowAPIClient()
    endpoint = f"/dags/{args.dag_id}/dagRuns/{args.dag_run_id}/taskInstances"
    params = {}
    if args.limit:
        params['limit'] = args.limit

    result = client.get(endpoint, params=params)
    print_json(result)


def task_instance(args):
    """Get task instance details"""
    client = AirflowAPIClient()
    endpoint = f"/dags/{args.dag_id}/dagRuns/{args.dag_run_id}/taskInstances/{args.task_id}"
    result = client.get(endpoint)
    print_json(result)


def task_logs(args):
    """Retrieve task logs"""
    client = AirflowAPIClient()
    try_number = args.try_number or 1
    endpoint = f"/dags/{args.dag_id}/dagRuns/{args.dag_run_id}/taskInstances/{args.task_id}/logs/{try_number}"
    result = client.get(endpoint)

    # Extract and print logs
    if isinstance(result, dict) and 'content' in result:
        print(result['content'])
    else:
        print_json(result)


def set_task_note(args):
    """Set task instance note"""
    client = AirflowAPIClient()
    endpoint = f"/dags/{args.dag_id}/dagRuns/{args.dag_run_id}/taskInstances/{args.task_id}/setNote"
    data = {"note": args.note}
    result = client.patch(endpoint, json_data=data)
    print_json(result)


def dags(args):
    """List all DAGs"""
    client = AirflowAPIClient()
    params = {}
    if args.limit:
        params['limit'] = args.limit

    result = client.get("/dags", params=params)
    print_json(result)


def dag_details(args):
    """Get DAG details"""
    client = AirflowAPIClient()
    endpoint = f"/dags/{args.dag_id}/details"
    result = client.get(endpoint)
    print_json(result)


def dag_tasks(args):
    """Get DAG tasks"""
    client = AirflowAPIClient()
    endpoint = f"/dags/{args.dag_id}/tasks"
    result = client.get(endpoint)
    print_json(result)


def trigger_dag(args):
    """Trigger DAG run"""
    client = AirflowAPIClient()
    endpoint = f"/dags/{args.dag_id}/dagRuns"

    data = {}
    if args.conf:
        try:
            data['conf'] = json.loads(args.conf)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in --conf", file=sys.stderr)
            sys.exit(1)

    result = client.post(endpoint, json_data=data)
    print_json(result)


def dag_runs(args):
    """List DAG runs"""
    client = AirflowAPIClient()
    endpoint = f"/dags/{args.dag_id}/dagRuns"
    params = {}
    if args.limit:
        params['limit'] = args.limit

    result = client.get(endpoint, params=params)
    print_json(result)


def dag_run_details(args):
    """Get DAG run details"""
    client = AirflowAPIClient()
    endpoint = f"/dags/{args.dag_id}/dagRuns/{args.dag_run_id}"
    result = client.get(endpoint)
    print_json(result)


def clear_tasks(args):
    """Clear task instances"""
    client = AirflowAPIClient()
    endpoint = f"/dags/{args.dag_id}/clearTaskInstances"

    data = {"dag_run_id": args.dag_run_id}
    if args.task_id:
        data['task_ids'] = [args.task_id]

    result = client.post(endpoint, json_data=data)
    print_json(result)


def connections(args):
    """List connections"""
    client = AirflowAPIClient()
    params = {}
    if args.limit:
        params['limit'] = args.limit

    result = client.get("/connections", params=params)
    print_json(result)


def connection(args):
    """Get connection details"""
    client = AirflowAPIClient()
    endpoint = f"/connections/{args.connection_id}"
    result = client.get(endpoint)
    print_json(result)


def variables(args):
    """List variables"""
    client = AirflowAPIClient()
    params = {}
    if args.limit:
        params['limit'] = args.limit

    result = client.get("/variables", params=params)
    print_json(result)


def variable(args):
    """Get variable value"""
    client = AirflowAPIClient()
    endpoint = f"/variables/{args.variable_key}"
    result = client.get(endpoint)
    print_json(result)


def pools(args):
    """List pools"""
    client = AirflowAPIClient()
    params = {}
    if args.limit:
        params['limit'] = args.limit

    result = client.get("/pools", params=params)
    print_json(result)


def health(args):
    """Check Airflow health"""
    client = AirflowAPIClient()
    result = client.get("/health")
    print_json(result)


def version(args):
    """Get Airflow version"""
    client = AirflowAPIClient()
    result = client.get("/version")
    print_json(result)


def main():
    parser = argparse.ArgumentParser(
        description="Airflow REST API CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List task instances for a DAG run
  %(prog)s task-instances my_dag run_id_123

  # Get task logs
  %(prog)s task-logs my_dag run_id_123 task_1

  # Trigger a DAG run
  %(prog)s trigger-dag my_dag --conf '{"key": "value"}'

  # List all DAGs
  %(prog)s dags --limit 20
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Task commands
    task_instances_parser = subparsers.add_parser('task-instances', help='List task instances')
    task_instances_parser.add_argument('dag_id', help='DAG ID')
    task_instances_parser.add_argument('dag_run_id', help='DAG run ID')
    task_instances_parser.add_argument('--limit', type=int, help='Limit number of results')
    task_instances_parser.set_defaults(func=task_instances)

    task_instance_parser = subparsers.add_parser('task-instance', help='Get task instance details')
    task_instance_parser.add_argument('dag_id', help='DAG ID')
    task_instance_parser.add_argument('dag_run_id', help='DAG run ID')
    task_instance_parser.add_argument('task_id', help='Task ID')
    task_instance_parser.set_defaults(func=task_instance)

    task_logs_parser = subparsers.add_parser('task-logs', help='Get task logs')
    task_logs_parser.add_argument('dag_id', help='DAG ID')
    task_logs_parser.add_argument('dag_run_id', help='DAG run ID')
    task_logs_parser.add_argument('task_id', help='Task ID')
    task_logs_parser.add_argument('--try-number', type=int, help='Try number (default: 1)')
    task_logs_parser.set_defaults(func=task_logs)

    set_note_parser = subparsers.add_parser('set-task-note', help='Set task instance note')
    set_note_parser.add_argument('dag_id', help='DAG ID')
    set_note_parser.add_argument('dag_run_id', help='DAG run ID')
    set_note_parser.add_argument('task_id', help='Task ID')
    set_note_parser.add_argument('note', help='Note text')
    set_note_parser.set_defaults(func=set_task_note)

    # DAG commands
    dags_parser = subparsers.add_parser('dags', help='List DAGs')
    dags_parser.add_argument('--limit', type=int, help='Limit number of results')
    dags_parser.set_defaults(func=dags)

    dag_details_parser = subparsers.add_parser('dag-details', help='Get DAG details')
    dag_details_parser.add_argument('dag_id', help='DAG ID')
    dag_details_parser.set_defaults(func=dag_details)

    dag_tasks_parser = subparsers.add_parser('dag-tasks', help='Get DAG tasks')
    dag_tasks_parser.add_argument('dag_id', help='DAG ID')
    dag_tasks_parser.set_defaults(func=dag_tasks)

    trigger_parser = subparsers.add_parser('trigger-dag', help='Trigger DAG run')
    trigger_parser.add_argument('dag_id', help='DAG ID')
    trigger_parser.add_argument('--conf', help='Configuration as JSON string')
    trigger_parser.set_defaults(func=trigger_dag)

    dag_runs_parser = subparsers.add_parser('dag-runs', help='List DAG runs')
    dag_runs_parser.add_argument('dag_id', help='DAG ID')
    dag_runs_parser.add_argument('--limit', type=int, help='Limit number of results')
    dag_runs_parser.set_defaults(func=dag_runs)

    dag_run_parser = subparsers.add_parser('dag-run-details', help='Get DAG run details')
    dag_run_parser.add_argument('dag_id', help='DAG ID')
    dag_run_parser.add_argument('dag_run_id', help='DAG run ID')
    dag_run_parser.set_defaults(func=dag_run_details)

    clear_parser = subparsers.add_parser('clear-tasks', help='Clear task instances')
    clear_parser.add_argument('dag_id', help='DAG ID')
    clear_parser.add_argument('dag_run_id', help='DAG run ID')
    clear_parser.add_argument('--task-id', help='Specific task ID (optional)')
    clear_parser.set_defaults(func=clear_tasks)

    # Configuration commands
    connections_parser = subparsers.add_parser('connections', help='List connections')
    connections_parser.add_argument('--limit', type=int, help='Limit number of results')
    connections_parser.set_defaults(func=connections)

    connection_parser = subparsers.add_parser('connection', help='Get connection details')
    connection_parser.add_argument('connection_id', help='Connection ID')
    connection_parser.set_defaults(func=connection)

    variables_parser = subparsers.add_parser('variables', help='List variables')
    variables_parser.add_argument('--limit', type=int, help='Limit number of results')
    variables_parser.set_defaults(func=variables)

    variable_parser = subparsers.add_parser('variable', help='Get variable value')
    variable_parser.add_argument('variable_key', help='Variable key')
    variable_parser.set_defaults(func=variable)

    pools_parser = subparsers.add_parser('pools', help='List pools')
    pools_parser.add_argument('--limit', type=int, help='Limit number of results')
    pools_parser.set_defaults(func=pools)

    # System commands
    health_parser = subparsers.add_parser('health', help='Check Airflow health')
    health_parser.set_defaults(func=health)

    version_parser = subparsers.add_parser('version', help='Get Airflow version')
    version_parser.set_defaults(func=version)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except ValueError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
