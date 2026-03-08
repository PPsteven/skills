#!/usr/bin/env python3
"""
Get Category Details - Extract detailed information for a single category

Purpose: Fetch complete endpoint details for one category from OpenAPI spec,
formatted for Claude Code to generate CLI commands.

Usage:
  python3 get_category_details.py <openapi-url-or-file> <category-name>

Output:
  JSON with complete category information including all endpoints and parameters
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from openapi_parser import OpenAPIParser


def get_category_details(spec_source: str, category_name: str) -> Dict[str, Any]:
    """
    Get detailed information for a specific category.

    Args:
        spec_source: URL or file path to OpenAPI spec
        category_name: Name of the category to extract

    Returns:
        Dictionary with category details and all endpoints
    """
    # Load and parse OpenAPI spec
    parser = OpenAPIParser(spec_source)

    if not parser.load_spec():
        print(json.dumps({
            'error': 'Failed to load OpenAPI specification',
            'spec_source': spec_source
        }), file=sys.stderr)
        sys.exit(1)

    parser.extract_categories()

    # Check if category exists
    all_categories = parser.get_all_categories_list()
    if category_name not in all_categories:
        print(json.dumps({
            'error': f'Category "{category_name}" not found',
            'available_categories': all_categories
        }), file=sys.stderr)
        sys.exit(1)

    # Get full endpoint details (with complete parameter information)
    if hasattr(parser, '_full_categories') and category_name in parser._full_categories:
        endpoints = parser._full_categories[category_name]
    else:
        # Fallback to basic format
        endpoints = parser.get_category_details(category_name)

    # Build result
    result = {
        'category_name': category_name,
        'endpoint_count': len(endpoints),
        'endpoints': endpoints,
        'spec_info': {
            'version': parser.version,
            'source': spec_source
        }
    }

    return result


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python3 get_category_details.py <openapi-url-or-file> <category-name>", file=sys.stderr)
        print("Example: python3 get_category_details.py https://api.example.com/openapi.json Config", file=sys.stderr)
        sys.exit(1)

    spec_source = sys.argv[1]
    category_name = sys.argv[2]

    # Get category details
    result = get_category_details(spec_source, category_name)

    # Output as JSON
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            'error': str(e),
            'type': type(e).__name__
        }), file=sys.stderr)
        sys.exit(1)
