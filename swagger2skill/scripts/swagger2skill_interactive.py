#!/usr/bin/env python3
"""
Swagger to Skill Generator - Interactive Version with Claude Code Integration

This version integrates with Claude Code's AskUserQuestion tool for UI-based selection.
"""

import sys
import json
from pathlib import Path
from typing import List

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from openapi_parser import OpenAPIParser
from skill_generator import SkillGenerator


def generate_skill_from_selections(
    spec_source: str,
    selected_categories: List[str],
    skill_name: str,
    output_dir: str
) -> bool:
    """
    Generate skill with provided selections.

    Args:
        spec_source: URL or file path to OpenAPI spec
        selected_categories: List of selected category names
        skill_name: Name for the generated skill
        output_dir: Directory to create skill in

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*60)
    print("⚙️  Parsing OpenAPI Specification")
    print("="*60 + "\n")

    # Parse OpenAPI
    parser = OpenAPIParser(spec_source)
    if not parser.load_spec():
        return False

    parser.extract_categories()

    # Validate selections
    all_categories = parser.get_all_categories_list()
    if not selected_categories or not all(cat in all_categories for cat in selected_categories):
        print("❌ Invalid category selection")
        return False

    print(f"✅ Parsed OpenAPI spec with {len(all_categories)} categories")
    print(f"✅ Selected {len(selected_categories)} categories:")
    for cat in selected_categories:
        print(f"   • {cat}")

    # Generate skill
    print("\n" + "="*60)
    print("⚙️  Generating Skill")
    print("="*60 + "\n")

    generator = SkillGenerator(
        skill_name,
        output_dir,
        parser.categories,
        selected_categories,
        all_categories
    )

    if not generator.generate():
        return False

    # Success summary
    print("\n" + "="*60)
    print("✅ Skill Generation Complete!")
    print("="*60)
    print(f"\n📍 Skill location: {generator.skill_dir}\n")
    print("📋 Next Steps:")
    print(f"   1. Review the generated files in {generator.skill_dir}")
    print(f"   2. The skill is ready to use or can be deployed")
    print(f"   3. Commit to repository if desired")
    print()

    return True


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("🚀 Swagger to Skill Generator")
    print("="*60 + "\n")

    # Get OpenAPI source from CLI argument
    if len(sys.argv) < 2:
        print("❌ OpenAPI source is required")
        print("Usage: /swagger2skill <openapi-url-or-file>")
        sys.exit(1)

    spec_source = sys.argv[1]
    print(f"Using OpenAPI source: {spec_source}\n")

    # Parse to get categories list
    print("="*60)
    print("📖 Parsing OpenAPI Specification")
    print("="*60 + "\n")

    parser = OpenAPIParser(spec_source)
    if not parser.load_spec():
        sys.exit(1)

    parser.extract_categories()
    categories = parser.get_all_categories_list()

    if not categories:
        print("❌ No categories found in specification")
        sys.exit(1)

    print(f"✅ Found {len(categories)} categories:\n")
    for i, cat in enumerate(categories, 1):
        endpoint_count = len(parser.get_category_details(cat))
        print(f"   {i}. {cat} ({endpoint_count} endpoints)")

    # Now prepare data for Claude Code's AskUserQuestion
    # This is JSON that will be processed by the skill invoker
    prompt_data = {
        "step": "collect_selections",
        "categories": categories,
        "spec_source": spec_source,
        "message": "\n\n**Important**: This skill requires your selections. If you see this message, " \
                   "please respond with the following JSON indicating your choices:\n\n" \
                   f"Categories to select from: {categories}\n\n" \
                   "Please select which categories to include by specifying their names or numbers."
    }

    # Output structured prompt that Claude Code can process
    print("\n" + "="*60)
    print("🎯 Ready for User Selection")
    print("="*60)
    print(json.dumps(prompt_data, indent=2))


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
