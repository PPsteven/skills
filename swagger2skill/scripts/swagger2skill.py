#!/usr/bin/env python3
"""
Swagger to Skill Generator - Extract and Display Categories

Purpose: Extract categories from OpenAPI spec and display them
This script is meant to be called from Claude Code to gather data
before using AskUserQuestion tool for user selection.

Output: Structured list of categories with endpoint counts (human-readable or JSON)
"""

import sys
import json
from pathlib import Path
from typing import List, Tuple, Dict, Any

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from openapi_parser import OpenAPIParser


def fetch_and_parse_openapi(spec_source: str) -> Tuple[OpenAPIParser, List[str]]:
    """
    Fetch and parse OpenAPI spec, return parser and categories list.

    Args:
        spec_source: URL or file path to OpenAPI spec

    Returns:
        Tuple of (OpenAPIParser, list of category names)
    """
    parser = OpenAPIParser(spec_source)

    if not parser.load_spec():
        print("❌ Failed to load OpenAPI specification", file=sys.stderr)
        sys.exit(1)

    parser.extract_categories()
    categories = parser.get_all_categories_list()

    if not categories:
        print("❌ No categories found in specification", file=sys.stderr)
        sys.exit(1)

    return parser, categories


def display_categories(parser: OpenAPIParser, categories: List[str]):
    """Display all categories with endpoint counts (human readable format)."""
    print("\n" + "="*60)
    print("📖 OpenAPI Categories")
    print("="*60 + "\n")

    print(f"✅ Found {len(categories)} API categories:\n")
    for i, cat in enumerate(categories, 1):
        endpoint_count = len(parser.get_category_details(cat))
        print(f"   {i}. {cat} ({endpoint_count} endpoints)")

    print()


def output_categories_json(parser: OpenAPIParser, categories: List[str]) -> Dict[str, Any]:
    """
    Output categories in JSON format for programmatic use.

    Args:
        parser: OpenAPIParser instance
        categories: List of category names

    Returns:
        Dictionary with category information
    """
    categories_data = []

    for category in categories:
        endpoints = parser.get_category_details(category)
        categories_data.append({
            'name': category,
            'endpoint_count': len(endpoints),
            'endpoints': [
                {
                    'method': ep['method'],
                    'path': ep['path'],
                    'summary': ep.get('summary', ''),
                    'operationId': ep.get('operationId', ''),
                }
                for ep in endpoints
            ]
        })

    result = {
        'total_categories': len(categories),
        'categories': categories_data
    }

    return result


def main():
    """Main workflow: Extract and display categories."""
    if len(sys.argv) < 2:
        print("❌ OpenAPI source is required", file=sys.stderr)
        print("Usage: python3 swagger2skill.py <openapi-url-or-file> [--json]", file=sys.stderr)
        sys.exit(1)

    spec_source = sys.argv[1]
    output_json = '--json' in sys.argv

    # Parse OpenAPI spec
    parser, categories = fetch_and_parse_openapi(spec_source)

    # Output categories
    if output_json:
        # JSON output for Claude Code to parse
        result = output_categories_json(parser, categories)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Human-readable output
        display_categories(parser, categories)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
