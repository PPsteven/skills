1.#!/usr/bin/env python3
"""
Skill Generator - Generate skill directory structure and files

Creates a complete skill from parsed OpenAPI data, including SKILL.md,
CLI tools, and reference documentation with full endpoint implementations.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class SkillGenerator:
    """Generate a complete skill from OpenAPI categories."""

    def __init__(self, skill_name: str, output_dir: str, categories: Dict[str, List[Dict]],
                 selected_categories: List[str], all_categories: List[str]):
        """
        Initialize skill generator.

        Args:
            skill_name: Name for the generated skill
            output_dir: Directory to create skill in
            categories: Dict of all categories and endpoints
            selected_categories: List of selected category names
            all_categories: List of all category names (for unsupported doc)
        """
        self.skill_name = skill_name
        self.skill_dir = Path(output_dir) / skill_name
        self.categories = categories
        self.selected_categories = selected_categories
        self.all_categories = all_categories
        self.unsupported_categories = [c for c in all_categories if c not in selected_categories]

    def generate(self) -> bool:
        """Generate skill files."""
        try:
            # Create directory structure
            self.skill_dir.mkdir(parents=True, exist_ok=True)
            (self.skill_dir / 'scripts').mkdir(exist_ok=True)
            (self.skill_dir / 'references').mkdir(exist_ok=True)
            (self.skill_dir / 'assets').mkdir(exist_ok=True)

            # Generate files
            self._generate_skill_md()
            self._generate_cli_tool()
            self._generate_endpoints_reference()
            if self.unsupported_categories:
                self._generate_unsupported_reference()

            print(f"\n✅ Skill generated at: {self.skill_dir}")
            print(f"\n📁 Structure:")
            print(f"   {self.skill_name}/")
            print(f"   ├── SKILL.md")
            print(f"   ├── scripts/")
            print(f"   │   └── cli_tool.py")
            print(f"   └── references/")
            print(f"       ├── api_endpoints.md")
            if self.unsupported_categories:
                print(f"       └── unsupported_categories.md")

            return True

        except Exception as e:
            print(f"❌ Error generating skill: {e}")
            return False

    def _generate_skill_md(self):
        """Generate SKILL.md for the new skill."""
        categories_str = ', '.join(self.selected_categories)
        description = f"Manage {categories_str} via Airflow API. Use for {', '.join(self.selected_categories).lower()} operations."

        skill_md = f"""---
name: {self.skill_name}
description: {description}
---

# {self._format_title(self.skill_name)}

Interact with Airflow APIs for {categories_str}.

## Capabilities

This skill provides CLI tools to manage:

{self._generate_category_list()}

## Usage

```bash
# List available commands
python scripts/cli_tool.py --help

# Get help for specific category
python scripts/cli_tool.py <category> --help

# Execute an API operation
python scripts/cli_tool.py <category> <operation> --param value
```

## CLI Examples

{self._generate_cli_examples()}

## API Endpoints

For detailed API endpoint documentation, see `references/api_endpoints.md`.

## Implementation

This skill wraps the following API categories:
- {chr(10).join(f"  - {cat}" for cat in self.selected_categories)}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        filepath = self.skill_dir / 'SKILL.md'
        filepath.write_text(skill_md)
        print(f"  ✓ Created SKILL.md")

    def _generate_cli_tool(self):
        """Generate CLI tool script."""
        cli_code = f'''#!/usr/bin/env python3
"""
CLI Tool - {self._format_title(self.skill_name)}

Auto-generated CLI tool for managing Airflow APIs.
"""

import click
import json
import requests
from urllib.parse import urljoin
from typing import Optional
import os


class AirflowAPI:
    """Airflow API client."""

    def __init__(self, base_url: str = None, token: str = None):
        """Initialize API client."""
        self.base_url = base_url or os.getenv('AIRFLOW_BASE_URL', 'http://localhost:8080')
        self.token = token or os.getenv('AIRFLOW_TOKEN', '')
        self.headers = {{
            'Content-Type': 'application/json',
        }}
        if self.token:
            self.headers['Authorization'] = f'Bearer {{self.token}}'

    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make API request."""
        url = urljoin(self.base_url, endpoint)
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs, timeout=30)
            response.raise_for_status()
            return response.json() if response.text else {{"status": "success"}}
        except Exception as e:
            click.echo(f"❌ Error: {{e}}", err=True)
            return {{"error": str(e)}}


# Initialize API client
api = AirflowAPI()


@click.group()
def cli():
    """Airflow API CLI Tool"""
    pass


{self._generate_cli_commands()}


if __name__ == '__main__':
    cli()
'''

        filepath = self.skill_dir / 'scripts' / 'cli_tool.py'
        filepath.write_text(cli_code)
        filepath.chmod(0o755)
        print(f"  ✓ Created scripts/cli_tool.py")


    def _endpoint_to_command_name(self, operation_id: str) -> str:
        """
        Convert operationId to kebab-case command name.

        Args:
            operation_id: Operation ID from OpenAPI spec

        Returns:
            kebab-case command name
        """
        if not operation_id:
            return 'command'

        # Convert camelCase to kebab-case
        # Insert hyphen before uppercase letters that follow lowercase
        name = re.sub('([a-z])([A-Z])', r'\1-\2', operation_id)
        return name.lower()

    def _get_parameter_type(self, schema: Dict[str, Any]) -> str:
        """
        Convert OpenAPI schema type to Click type.

        Args:
            schema: Parameter schema definition

        Returns:
            Click-compatible type string
        """
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
        """
        Convert OpenAPI parameter to Click decorator.

        Args:
            parameter: Parameter definition with name, in, required, schema

        Returns:
            Click decorator string
        """
        name = parameter.get('name', 'param')
        param_in = parameter.get('in', 'query')
        required = parameter.get('required', False)
        description = parameter.get('description', f'{name} parameter')
        schema = parameter.get('schema', {})
        param_type = self._get_parameter_type(schema)

        # Format parameter name for Click
        if param_in == 'path':
            # Path parameters become arguments
            return f"@click.argument('{name}')"
        else:
            # Query, header, cookie parameters become options
            option_name = f"--{name.replace('_', '-')}"
            decorator = f"@click.option('{option_name}'"

            # Add type if not string
            if param_type != 'str':
                # Convert to Click type constants (all caps)
                type_map = {
                    'int': 'click.INT',
                    'float': 'click.FLOAT',
                    'bool': 'click.BOOL',
                }
                click_type = type_map.get(param_type, 'click.STRING')
                decorator += f", type={click_type}"

            # Add required flag
            if required:
                decorator += ", required=True"

            # Add help text
            decorator += f", help='{description}'"
            decorator += ")"

            return decorator

    def _generate_endpoint_implementation(self, endpoint: Dict[str, Any],
                                         category_slug: str) -> str:
        """
        Generate a complete Click command for an endpoint.

        Args:
            endpoint: Endpoint definition with path, method, parameters
            category_slug: Slugified category name

        Returns:
            Complete Click command function as string
        """
        operation_id = endpoint.get('operationId', '')
        command_name = self._endpoint_to_command_name(operation_id)
        path = endpoint.get('path', '')
        method = endpoint.get('method', 'GET')
        summary = endpoint.get('summary', f'{method} {path}')
        description = endpoint.get('description', summary)
        parameters = endpoint.get('parameters', [])

        # Handle both old format (count as int) and new format (list of dicts)
        if isinstance(parameters, int):
            # Old format - parameters count, no details available
            parameters = []
        elif not isinstance(parameters, list):
            parameters = []

        # Separate path and query parameters
        path_params = [p for p in parameters if isinstance(p, dict) and p.get('in') == 'path']
        query_params = [p for p in parameters if isinstance(p, dict) and p.get('in') != 'path']

        # Build function signature with parameters
        func_params = [p.get('name') for p in parameters]
        func_signature = ', '.join(func_params) if func_params else ''
        if func_signature:
            func_signature = ', ' + func_signature

        # Build parameter decorators
        param_decorators = []
        for param in parameters:
            param_decorators.append(self._parameter_to_click_option(param))

        decorators = '\n'.join(param_decorators) if param_decorators else ''

        # Build query params dict for api.request
        query_params_code = ''
        if query_params:
            query_params_code = 'params = {\n'
            for param in query_params:
                pname = param.get('name')
                query_params_code += f"        '{pname}': {pname},\n"
            query_params_code += '    }'
        else:
            query_params_code = 'params = {}'

        # Build path with parameter interpolation
        # For path parameters, we'll use f-string to interpolate them in the generated code
        # But we need to avoid double escaping when generating the string itself
        formatted_path = path
        for param in path_params:
            pname = param.get('name')
            # Keep the path as-is for now; we'll use f-string in the generated code

        # Build endpoint line to be inserted into the generated function
        # Use format() style for the endpoint so parameters can be interpolated
        if path_params:
            # Create format string: /users/{userId} becomes /users/{{userId}} in triple-quoted string
            endpoint_line = f"endpoint='{formatted_path}',"
        else:
            endpoint_line = f"endpoint='{formatted_path}',"

        # Generate the command function
        if decorators:
            command_code = f'''
@{category_slug}_group.command('{command_name}')
{decorators}
def {category_slug}_{command_name.replace('-', '_')}({func_signature.lstrip(', ')}):
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
@{category_slug}_group.command('{command_name}')
def {category_slug}_{command_name.replace('-', '_')}():
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

    def _generate_cli_commands(self) -> str:
        """Generate Click CLI commands for each endpoint in each category."""
        commands = []

        for category in self.selected_categories:
            category_slug = self._slugify(category)
            endpoints = self.categories.get(category, [])

            # Create category group
            commands.append(f'''
@cli.group(name='{category_slug}')
def {category_slug}_group():
    """Manage {category} operations"""
    pass
''')

            # Generate command for each endpoint
            if endpoints:
                for endpoint in endpoints:
                    cmd = self._generate_endpoint_implementation(endpoint, category_slug)
                    commands.append(cmd)
            else:
                # Fallback if no endpoints found
                commands.append(f'''
@{category_slug}_group.command('list')
def {category_slug}_list():
    """List {category} items"""
    click.echo("No endpoints found for {category}")
''')

        return '\n'.join(commands)

    def _generate_endpoints_reference(self):
        """Generate API endpoints reference documentation with full parameter details."""
        doc = "# API Endpoints Reference\n\n"
        doc += f"**Selected Categories**: {', '.join(self.selected_categories)}\n\n"

        for category in self.selected_categories:
            endpoints = self.categories.get(category, [])
            doc += f"## {category}\n\n"

            for i, endpoint in enumerate(endpoints, 1):
                doc += f"### {i}. {endpoint['method']} {endpoint['path']}\n\n"
                if endpoint.get('summary'):
                    doc += f"**Description**: {endpoint['summary']}\n\n"
                if endpoint.get('description'):
                    doc += f"{endpoint['description']}\n\n"
                doc += f"- **Method**: `{endpoint['method']}`\n"
                doc += f"- **Path**: `{endpoint['path']}`\n"
                doc += f"- **Operation ID**: `{endpoint.get('operationId', 'N/A')}`\n"

                # Include detailed parameter information
                parameters = endpoint.get('parameters', [])
                if isinstance(parameters, list) and parameters:
                    doc += f"- **Parameters**: {len(parameters)} parameters\n"
                    for param in parameters:
                        # Handle both old format (count) and new format (list)
                        if isinstance(param, dict):
                            pname = param.get('name', 'unknown')
                            pin = param.get('in', 'query')
                            required = param.get('required', False)
                            schema = param.get('schema', {})
                            ptype = schema.get('type', 'string')
                            pdesc = param.get('description', '')

                            required_tag = "✓ required" if required else "optional"
                            doc += f"  - `{pname}` ({pin}, {ptype}) - {required_tag}"
                            if pdesc:
                                doc += f" - {pdesc}"
                            doc += "\n"
                else:
                    # Old format: parameters is a count
                    doc += f"- **Parameters**: {parameters} parameters\n"

                doc += "\n"

        filepath = self.skill_dir / 'references' / 'api_endpoints.md'
        filepath.write_text(doc)
        print(f"  ✓ Created references/api_endpoints.md")

    def _generate_unsupported_reference(self):
        """Generate documentation for unsupported categories."""
        doc = "# Unsupported API Categories\n\n"
        doc += f"The following API categories are available in the specification but were NOT included in this skill:\n\n"

        for category in self.unsupported_categories:
            endpoints = self.categories.get(category, [])
            doc += f"## {category}\n\n"
            doc += f"**Endpoints**: {len(endpoints)}\n\n"
            doc += "**Available operations**:\n"
            for endpoint in endpoints[:5]:  # Show first 5
                doc += f"- `{endpoint['method']} {endpoint['path']}`\n"
            if len(endpoints) > 5:
                doc += f"- ... and {len(endpoints) - 5} more\n"
            doc += "\n"

        filepath = self.skill_dir / 'references' / 'unsupported_categories.md'
        filepath.write_text(doc)
        print(f"  ✓ Created references/unsupported_categories.md")

    def _format_title(self, name: str) -> str:
        """Format skill name as title."""
        return ' '.join(word.capitalize() for word in name.replace('-', ' ').split())

    def _slugify(self, name: str) -> str:
        """Convert name to slug format."""
        return name.lower().replace(' ', '_').replace('-', '_')

    def _generate_category_list(self) -> str:
        """Generate category list for SKILL.md."""
        items = []
        for category in self.selected_categories:
            endpoint_count = len(self.categories.get(category, []))
            items.append(f"- **{category}**: {endpoint_count} API endpoints")
        return '\n'.join(items)

    def _generate_cli_examples(self) -> str:
        """Generate CLI usage examples with actual endpoints."""
        examples = []
        for category in self.selected_categories:
            slug = self._slugify(category)
            endpoints = self.categories.get(category, [])
            examples.append(f"### {category}")
            examples.append(f"```bash")

            # Show first 2-3 endpoint examples
            for endpoint in endpoints[:3]:
                method = endpoint.get('method', 'GET')
                operation_id = endpoint.get('operationId', '')
                if operation_id:
                    cmd_name = self._endpoint_to_command_name(operation_id)
                    examples.append(f"python scripts/cli_tool.py {slug} {cmd_name}")

            if len(endpoints) > 3:
                examples.append(f"# ... and {len(endpoints) - 3} more commands")

            examples.append(f"```")
            examples.append("")

        return '\n'.join(examples)


def main():
    """CLI interface for skill generator."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: skill_generator.py <skill-name> <output-dir> <categories-json>")
        sys.exit(1)

    skill_name = sys.argv[1]
    output_dir = sys.argv[2]
    categories_json = json.loads(sys.argv[3])
    selected_categories = json.loads(sys.argv[4]) if len(sys.argv) > 4 else list(categories_json.keys())

    generator = SkillGenerator(
        skill_name,
        output_dir,
        categories_json,
        selected_categories,
        list(categories_json.keys())
    )

    if generator.generate():
        print("\n✅ Skill generation complete!")
    else:
        print("\n❌ Skill generation failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
