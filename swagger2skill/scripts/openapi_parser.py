#!/usr/bin/env python3
"""
OpenAPI Parser - Extract categories and endpoints from Swagger/OpenAPI specs

This script parses OpenAPI 3.0 and Swagger 2.0 specifications to extract
API categories (tags) and their associated endpoints.
"""

import json
import sys
from urllib.request import urlopen
from pathlib import Path
from typing import Dict, List, Any
import urllib.parse


class OpenAPIParser:
    """Parse OpenAPI/Swagger specifications and extract categories."""

    def __init__(self, spec_source: str):
        """
        Initialize parser with OpenAPI spec source.

        Args:
            spec_source: URL or file path to OpenAPI JSON file
        """
        self.spec = None
        self.version = None
        self.spec_source = spec_source
        self.categories = {}

    def load_spec(self) -> bool:
        """
        Load OpenAPI specification from URL or file.

        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if self.spec_source.startswith('http://') or self.spec_source.startswith('https://'):
                print(f"📥 Fetching from: {self.spec_source}")
                with urlopen(self.spec_source, timeout=10) as response:
                    self.spec = json.loads(response.read().decode('utf-8'))
            else:
                print(f"📂 Loading from: {self.spec_source}")
                with open(self.spec_source, 'r') as f:
                    self.spec = json.load(f)

            # Detect version
            if 'openapi' in self.spec:
                self.version = 'OpenAPI 3.0'
            elif 'swagger' in self.spec:
                self.version = 'Swagger 2.0'
            else:
                print("❌ Could not determine OpenAPI/Swagger version")
                return False

            print(f"✅ Loaded {self.version} specification")
            return True

        except Exception as e:
            print(f"❌ Error loading specification: {e}")
            return False

    def extract_categories(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract API categories and endpoints from specification.

        Returns:
            Dictionary mapping category names to list of endpoints
        """
        if not self.spec:
            return {}

        self.categories = {}

        if self.version == 'OpenAPI 3.0':
            self._extract_openapi3_categories()
        elif self.version == 'Swagger 2.0':
            self._extract_swagger2_categories()

        return self.categories

    def _extract_openapi3_categories(self):
        """Extract categories from OpenAPI 3.0 specification."""
        paths = self.spec.get('paths', {})

        for path, methods in paths.items():
            for method, operation in methods.items():
                if method.startswith('x-'):  # Skip extensions
                    continue

                if not isinstance(operation, dict) or 'tags' not in operation:
                    continue

                tags = operation.get('tags', ['Uncategorized'])
                summary = operation.get('summary', f'{method.upper()} {path}')
                operation_id = operation.get('operationId', '')
                parameters = operation.get('parameters', [])

                for tag in tags:
                    if tag not in self.categories:
                        self.categories[tag] = []

                    endpoint = {
                        'path': path,
                        'method': method.upper(),
                        'summary': summary,
                        'operationId': operation_id,
                        'parameters': len(parameters),
                        'description': operation.get('description', ''),
                    }
                    self.categories[tag].append(endpoint)

    def _extract_swagger2_categories(self):
        """Extract categories from Swagger 2.0 specification."""
        paths = self.spec.get('paths', {})

        for path, methods in paths.items():
            for method, operation in methods.items():
                if method.startswith('x-'):  # Skip extensions
                    continue

                if not isinstance(operation, dict) or 'tags' not in operation:
                    continue

                tags = operation.get('tags', ['Uncategorized'])
                summary = operation.get('summary', f'{method.upper()} {path}')
                operation_id = operation.get('operationId', '')
                parameters = operation.get('parameters', [])

                for tag in tags:
                    if tag not in self.categories:
                        self.categories[tag] = []

                    endpoint = {
                        'path': path,
                        'method': method.upper(),
                        'summary': summary,
                        'operationId': operation_id,
                        'parameters': len(parameters),
                        'description': operation.get('description', ''),
                    }
                    self.categories[tag].append(endpoint)

    def display_categories(self):
        """Display extracted categories with endpoint counts."""
        if not self.categories:
            print("❌ No categories found in specification")
            return

        print("\n" + "="*60)
        print(f"📚 Available API Categories ({len(self.categories)} total)")
        print("="*60 + "\n")

        for i, (category, endpoints) in enumerate(sorted(self.categories.items()), 1):
            print(f"{i}. {category} ({len(endpoints)} endpoints)")
            for j, endpoint in enumerate(endpoints[:3], 1):  # Show first 3
                print(f"   • {endpoint['method']} {endpoint['path']}")

            if len(endpoints) > 3:
                print(f"   • ... and {len(endpoints) - 3} more")
            print()

    def get_category_summary(self) -> str:
        """
        Get summary of categories in interactive format.

        Returns:
            Formatted string for user selection
        """
        if not self.categories:
            return "No categories found"

        summary = []
        for i, (category, endpoints) in enumerate(sorted(self.categories.items()), 1):
            summary.append(f"{i}. {category} ({len(endpoints)} endpoints)")

        return '\n'.join(summary)

    def get_category_details(self, category: str) -> List[Dict[str, Any]]:
        """Get detailed information about a specific category."""
        return self.categories.get(category, [])

    def get_all_categories_list(self) -> List[str]:
        """Get sorted list of all category names."""
        return sorted(self.categories.keys())


def main():
    """CLI interface for OpenAPI parser."""
    if len(sys.argv) < 2:
        print("Usage: openapi_parser.py <url_or_file_path>")
        print("Example: openapi_parser.py https://api.example.com/openapi.json")
        print("Example: openapi_parser.py ./openapi.json")
        sys.exit(1)

    spec_source = sys.argv[1]

    # Parse specification
    parser = OpenAPIParser(spec_source)

    if not parser.load_spec():
        sys.exit(1)

    # Extract and display categories
    parser.extract_categories()
    parser.display_categories()

    # Output as JSON for programmatic use
    categories_json = {
        category: [
            {
                'method': ep['method'],
                'path': ep['path'],
                'summary': ep['summary'],
            }
            for ep in endpoints
        ]
        for category, endpoints in parser.categories.items()
    }

    print("\n" + "="*60)
    print("📄 Categories Summary (JSON)")
    print("="*60)
    print(json.dumps(categories_json, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
