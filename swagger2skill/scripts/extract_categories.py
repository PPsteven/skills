#!/usr/bin/env python3
"""
Extract categories from OpenAPI specification.

Usage:
    python3 extract_categories.py <openapi-url-or-file>

Output:
    JSON with categories and endpoint counts
"""

import sys
import json
from pathlib import Path
from typing import List

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from openapi_parser import OpenAPIParser


def extract_categories(spec_source: str) -> dict:
    """
    Extract categories from OpenAPI spec.

    Args:
        spec_source: URL or file path to OpenAPI spec

    Returns:
        Dict with categories and their endpoint counts
    """
    print(f"📥 Fetching from: {spec_source}", file=sys.stderr)

    parser = OpenAPIParser(spec_source)

    if not parser.load_spec():
        print("❌ Failed to load OpenAPI specification", file=sys.stderr)
        sys.exit(1)

    parser.extract_categories()
    categories = parser.get_all_categories_list()

    if not categories:
        print("❌ No categories found in specification", file=sys.stderr)
        sys.exit(1)

    # Build result
    result = {
        "categories": [],
        "total": len(categories)
    }

    for cat in categories:
        endpoint_count = len(parser.get_category_details(cat))
        result["categories"].append({
            "name": cat,
            "endpoint_count": endpoint_count
        })

    return result


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("❌ OpenAPI source is required", file=sys.stderr)
        print("Usage: python3 extract_categories.py <openapi-url-or-file>", file=sys.stderr)
        sys.exit(1)

    spec_source = sys.argv[1]

    try:
        result = extract_categories(spec_source)
        # Output JSON to stdout
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
