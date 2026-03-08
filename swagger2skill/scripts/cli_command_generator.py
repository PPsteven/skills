#!/usr/bin/env python3
"""
CLI Command Generator Agent

This agent is responsible for generating Click CLI commands for a single category.
It reads endpoint definitions and generates complete command implementations.

Usage:
  This script is called by the main swagger2skill orchestrator via Agent tool.

  Input (via command line):
    - Category name
    - OpenAPI spec path/URL
    - Output format (JSON)

  Output (to stdout):
    - JSON containing generated CLI command code for the category
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any
import re

# Import parser
sys.path.insert(0, str(Path(__file__).parent))
from openapi_parser import OpenAPIParser


class CLICommandGenerator:
    """Generate CLI commands for a single category."""

    def __init__(self, category: str, parser: OpenAPIParser):
        """
        Initialize generator for a specific category.

        Args:
            category: Category name
            parser: OpenAPIParser instance with loaded spec
        """
        self.category = category
        self.parser = parser
        self.category_slug = self._slugify(category)

    def _slugify(self, name: str) -> str:
        """Convert name to slug format."""
        return name.lower().replace(' ', '_').replace('-', '_')

    def _endpoint_to_command_name(self, operation_id: str) -> str:
        """Convert operationId to kebab-case command name."""
        if not operation_id:
            return 'command'
        name = re.sub('([a-z])([A-Z])', r'\1-\2', operation_id)
        return name.lower()

    def _get_parameter_type(self, schema: Dict[str, Any]) -> str:
        """Convert OpenAPI schema type to Click type."""
        param_type = schema.get('type', 'string')
        type_map = {
            'string': 'str',
            'integer': 'int',
            'number': 'float',
            'boolean': 'bool',
            'array': 'str',
        }
        return type_map.get(param_type, 'str')

    def _parameter_to_click_option(self, parameter: Dict[str, Any]) -> str:
        """Convert OpenAPI parameter to Click decorator."""
        name = parameter.get('name', 'param')
        param_in = parameter.get('in', 'query')
        required = parameter.get('required', False)
        description = parameter.get('description', f'{name} parameter')
        schema = parameter.get('schema', {})
        param_type = self._get_parameter_type(schema)

        if param_in == 'path':
            return f"@click.argument('{name}')"
        else:
            option_name = f"--{name.replace('_', '-')}"
            decorator = f"@click.option('{option_name}'"

            if param_type != 'str':
                type_map = {
                    'int': 'click.INT',
                    'float': 'click.FLOAT',
                    'bool': 'click.BOOL',
                }
                click_type = type_map.get(param_type, 'click.STRING')
                decorator += f", type={click_type}"

            if required:
                decorator += ", required=True"

            decorator += f", help='{description}'"
            decorator += ")"

            return decorator

    def _generate_endpoint_implementation(self, endpoint: Dict[str, Any]) -> str:
        """Generate a complete Click command for an endpoint."""
        operation_id = endpoint.get('operationId', '')
        command_name = self._endpoint_to_command_name(operation_id)
        path = endpoint.get('path', '')
        method = endpoint.get('method', 'GET')
        summary = endpoint.get('summary', f'{method} {path}')
        description = endpoint.get('description', summary)
        parameters = endpoint.get('parameters', [])

        if isinstance(parameters, int):
            parameters = []
        elif not isinstance(parameters, list):
            parameters = []

        path_params = [p for p in parameters if isinstance(p, dict) and p.get('in') == 'path']
        query_params = [p for p in parameters if isinstance(p, dict) and p.get('in') != 'path']

        func_params = [p.get('name') for p in parameters]
        func_signature = ', '.join(func_params) if func_params else ''
        if func_signature:
            func_signature = ', ' + func_signature

        param_decorators = []
        for param in parameters:
            param_decorators.append(self._parameter_to_click_option(param))

        decorators = '\n'.join(param_decorators) if param_decorators else ''

        query_params_code = ''
        if query_params:
            query_params_code = 'params = {\n'
            for param in query_params:
                pname = param.get('name')
                query_params_code += f"        '{pname}': {pname},\n"
            query_params_code += '    }'
        else:
            query_params_code = 'params = {}'

        formatted_path = path
        endpoint_line = f"endpoint='{formatted_path}',"

        if decorators:
            command_code = f'''
@{self.category_slug}_group.command('{command_name}')
{decorators}
def {self.category_slug}_{command_name.replace('-', '_')}({func_signature.lstrip(', ')}):
    """{description}"""
    {query_params_code}
    result = api.request(
        method='{method}',
        {endpoint_line}
        params=params if params else None,
    )

    if 'error' not in result:
        click.echo(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        click.echo(result['error'], err=True)
'''
        else:
            command_code = f'''
@{self.category_slug}_group.command('{command_name}')
def {self.category_slug}_{command_name.replace('-', '_')}():
    """{description}"""
    result = api.request(
        method='{method}',
        endpoint='{path}',
    )

    if 'error' not in result:
        click.echo(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        click.echo(result['error'], err=True)
'''

        return command_code

    def generate_commands(self) -> Dict[str, Any]:
        """
        Generate all CLI commands for this category.

        Returns:
            Dict with category info and generated command code
        """
        # Get full endpoint definitions (with parameters)
        if hasattr(self.parser, '_full_categories') and self.category in self.parser._full_categories:
            endpoints = self.parser._full_categories[self.category]
        else:
            # Fallback to basic format
            endpoints = self.parser.get_category_details(self.category)

        # Generate category group
        group_code = f'''
@cli.group(name='{self.category_slug}')
def {self.category_slug}_group():
    """Manage {self.category} operations"""
    pass
'''

        # Generate commands for each endpoint
        command_codes = [group_code]

        if endpoints:
            for endpoint in endpoints:
                cmd = self._generate_endpoint_implementation(endpoint)
                command_codes.append(cmd)
        else:
            # Fallback
            fallback_code = f'''
@{self.category_slug}_group.command('list')
def {self.category_slug}_list():
    """List {self.category} items"""
    click.echo("No endpoints found for {self.category}")
'''
            command_codes.append(fallback_code)

        return {
            'category': self.category,
            'category_slug': self.category_slug,
            'endpoint_count': len(endpoints) if isinstance(endpoints, list) else 0,
            'commands_code': '\n'.join(command_codes)
        }


def main():
    """Main entry point for the agent."""
    if len(sys.argv) < 3:
        print(json.dumps({
            'error': 'Missing arguments',
            'usage': 'cli_command_generator.py <category> <openapi-spec-path>'
        }))
        sys.exit(1)

    category = sys.argv[1]
    spec_path = sys.argv[2]

    # Load OpenAPI spec
    parser = OpenAPIParser(spec_path)
    if not parser.load_spec():
        print(json.dumps({
            'error': f'Failed to load OpenAPI spec from {spec_path}'
        }))
        sys.exit(1)

    parser.extract_categories()

    # Generate commands for this category
    generator = CLICommandGenerator(category, parser)
    result = generator.generate_commands()

    # Output as JSON
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
