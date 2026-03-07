#!/usr/bin/env python3
"""
Swagger to Skill Generator - Main Interactive Entry Point

Complete workflow:
1. Fetch OpenAPI spec from URL
2. Parse and extract all categories
3. Ask user: all categories or custom selection
4. Generate skill based on selection
"""

import sys
import json
from pathlib import Path
from typing import List, Tuple

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from openapi_parser import OpenAPIParser
from skill_generator import SkillGenerator


def fetch_and_parse_openapi(spec_source: str) -> Tuple[OpenAPIParser, List[str]]:
    """
    Fetch and parse OpenAPI spec, return parser and categories list.

    Args:
        spec_source: URL or file path to OpenAPI spec

    Returns:
        Tuple of (OpenAPIParser, list of category names)
    """
    print("\n" + "="*60)
    print("📖 Parsing OpenAPI Specification")
    print("="*60 + "\n")

    parser = OpenAPIParser(spec_source)

    if not parser.load_spec():
        print("❌ Failed to load OpenAPI specification")
        sys.exit(1)

    parser.extract_categories()
    categories = parser.get_all_categories_list()

    if not categories:
        print("❌ No categories found in specification")
        sys.exit(1)

    print(f"✅ Found {len(categories)} API categories:\n")
    for i, cat in enumerate(categories, 1):
        endpoint_count = len(parser.get_category_details(cat))
        print(f"   {i}. {cat} ({endpoint_count} endpoints)")

    return parser, categories


def prompt_category_selection(categories: List[str]) -> Tuple[str, List[str]]:
    """
    Prompt user for category selection.

    Returns:
        Tuple of (selection_type, selected_categories)
        selection_type: "all" or "custom"
        selected_categories: list of selected category names
    """
    print("\n" + "="*60)
    print("🎯 Category Selection")
    print("="*60 + "\n")

    print("Select categories:")
    print("1. All categories")
    print("2. Custom selection (enter numbers or names)\n")
    choice = input("👉 Your choice (1 or 2): ").strip()

    if choice == "1":
        return "all", categories
    elif choice == "2":
        selection_str = input("👉 Enter category numbers/names (comma-separated): ").strip()
        selected = parse_user_selection(selection_str, categories)
        return "custom", selected
    else:
        print("❌ Invalid choice")
        sys.exit(1)


def parse_user_selection(selection_str: str, categories: List[str]) -> List[str]:
    """
    Parse user input (numbers or names) to actual category list.

    Args:
        selection_str: "1,2,3" or "dag,variable"
        categories: full list of available categories

    Returns:
        Selected category names
    """
    selections = [s.strip() for s in selection_str.split(",")]
    selected = []

    for sel in selections:
        try:
            # Try as number (1-indexed)
            idx = int(sel) - 1
            if 0 <= idx < len(categories):
                selected.append(categories[idx])
            else:
                print(f"⚠️  Skipping invalid index: {sel}")
        except ValueError:
            # Try as name
            if sel in categories:
                selected.append(sel)
            else:
                print(f"⚠️  Skipping unknown category: {sel}")

    if not selected:
        print("❌ No valid categories selected")
        sys.exit(1)

    return selected


def prompt_skill_details() -> Tuple[str, str]:
    """
    Prompt for skill name and output directory.

    Returns:
        Tuple of (skill_name, output_directory)
    """
    print("\n" + "="*60)
    print("💾 Skill Details")
    print("="*60 + "\n")

    # Skill name
    while True:
        skill_name = input("👉 Skill name (kebab-case, e.g., 'airflow-api'): ").strip().lower()

        if not skill_name:
            print("❌ Skill name cannot be empty")
            continue

        if not all(c.isalnum() or c == '-' for c in skill_name):
            print("❌ Skill name can only contain lowercase letters, numbers, and hyphens")
            continue

        if skill_name.startswith('-') or skill_name.endswith('-'):
            print("❌ Skill name cannot start or end with a hyphen")
            continue

        break

    # Output directory
    default_dir = "/Users/ppsteven/projects/skills"
    output_dir = input(f"👉 Output directory (default: {default_dir}): ").strip()

    if not output_dir:
        output_dir = default_dir

    output_path = Path(output_dir)
    if not output_path.exists():
        print(f"❌ Directory does not exist: {output_dir}")
        sys.exit(1)

    return skill_name, output_dir


def generate_skill(
    parser: OpenAPIParser,
    selected_categories: List[str],
    skill_name: str,
    output_dir: str
) -> bool:
    """
    Generate the skill with selected categories.

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*60)
    print("⚙️  Generating Skill")
    print("="*60 + "\n")

    all_categories = parser.get_all_categories_list()

    generator = SkillGenerator(
        skill_name,
        output_dir,
        parser.categories,
        selected_categories,
        all_categories
    )

    if not generator.generate():
        print("❌ Skill generation failed")
        return False

    # Success summary
    print("\n" + "="*60)
    print("✅ Skill Generation Complete!")
    print("="*60)
    print(f"\n📍 Skill location: {generator.skill_dir}\n")
    print("📋 Generated Files:")
    print(f"   • SKILL.md - Skill documentation")
    print(f"   • scripts/cli_tool.py - CLI wrapper for selected APIs")
    print(f"   • references/api_endpoints.md - API reference")
    if len(selected_categories) < len(all_categories):
        print(f"   • references/unsupported_categories.md - Unimplemented categories")
    print()

    return True


def main():
    """Main workflow."""
    print("\n" + "="*60)
    print("🚀 Swagger to Skill Generator")
    print("="*60 + "\n")

    # Get OpenAPI source from CLI argument
    if len(sys.argv) < 2:
        print("❌ OpenAPI source is required")
        print("Usage: /swagger2skill <openapi-url-or-file>")
        sys.exit(1)

    spec_source = sys.argv[1]
    print(f"📦 Using OpenAPI source: {spec_source}\n")

    # Step 1: Parse OpenAPI spec
    parser, categories = fetch_and_parse_openapi(spec_source)

    # Step 2: Ask user for category selection
    selection_type, selected_categories = prompt_category_selection(categories)

    if selection_type == "all":
        print(f"\n✅ Selected all {len(selected_categories)} categories")
    else:
        print(f"\n✅ Selected {len(selected_categories)} categories:")
        for cat in selected_categories:
            print(f"   • {cat}")

    # Step 3: Get skill name and output directory
    skill_name, output_dir = prompt_skill_details()

    # Step 4: Generate skill
    if generate_skill(parser, selected_categories, skill_name, output_dir):
        print("📚 Next Steps:")
        print("   1. Review the generated skill files")
        print("   2. Test the CLI tool locally")
        print("   3. Commit to repository if needed")
        print()
    else:
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
