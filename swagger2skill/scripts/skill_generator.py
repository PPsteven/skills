#!/usr/bin/env python3
"""
Skill Generator - Generate skill directory structure and files

Creates a complete skill from parsed OpenAPI data, including SKILL.md,
CLI tools, and reference documentation.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any
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

    def _generate_cli_commands(self) -> str:
        """Generate Click CLI command stubs for each category."""
        commands = []

        for category in self.selected_categories:
            # Create category group
            commands.append(f'''
@cli.group(name='{self._slugify(category)}')
def {self._slugify(category)}_group():
    """Manage {category} operations"""
    pass


@{self._slugify(category)}_group.command('list')
@click.option('--limit', default=10, help='Number of items to return')
def {self._slugify(category)}_list(limit):
    """List {category} items"""
    # TODO: Implement {category} list endpoint
    click.echo(f"Fetching {category} items (limit={{limit}})...")
    # result = api.request('GET', '/api/v1/{self._slugify(category)}?limit={{limit}}')
    # click.echo(json.dumps(result, indent=2))


@{self._slugify(category)}_group.command('detail')
@click.argument('item_id')
def {self._slugify(category)}_detail(item_id):
    """Get {category} details"""
    # TODO: Implement {category} detail endpoint
    click.echo(f"Fetching {category}} details for {{item_id}}...")
    # result = api.request('GET', '/api/v1/{self._slugify(category)}/{{item_id}}')
    # click.echo(json.dumps(result, indent=2))
''')

        return '\n'.join(commands)

    def _generate_endpoints_reference(self):
        """Generate API endpoints reference documentation."""
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
                doc += f"- **Parameters**: {endpoint.get('parameters', 0)} parameters\n\n"

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
        """Generate CLI usage examples."""
        examples = []
        for category in self.selected_categories:
            slug = self._slugify(category)
            examples.append(f"# {category}")
            examples.append(f"```bash")
            examples.append(f"python scripts/cli_tool.py {slug} list")
            examples.append(f"python scripts/cli_tool.py {slug} detail <id>")
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
'''

        filepath = self.skill_dir / 'scripts' / 'skill_generator.py'
        filepath.write_text(cli_code)
        filepath.chmod(0o755)
        print(f"  ✓ Created scripts/skill_generator.py")
