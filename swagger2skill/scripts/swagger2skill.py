#!/usr/bin/env python3
"""
Swagger to Skill Generator - Extract and Display Categories

Purpose: Extract categories from OpenAPI spec and display them
This script is meant to be called from Claude Code to gather data
before using AskUserQuestion tool for user selection.

Output: Structured list of categories with endpoint counts
"""

import sys
import json
from pathlib import Path
from typing import List, Tuple

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



def main():
    """Main workflow: Extract and display categories."""
    if len(sys.argv) < 2:
        print("❌ OpenAPI source is required", file=sys.stderr)
        print("Usage: python3 swagger2skill.py <openapi-url-or-file>", file=sys.stderr)
        sys.exit(1)

    spec_source = sys.argv[1]

    # Parse OpenAPI spec
    parser, categories = fetch_and_parse_openapi(spec_source)

    # Display categories
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
