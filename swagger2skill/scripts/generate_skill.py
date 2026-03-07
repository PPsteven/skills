#!/usr/bin/env python3
"""
Swagger to Skill Generator - Generate Skill

Purpose: Generate a skill based on OpenAPI spec and selected categories
This script is called after user has made selections via AskUserQuestion

Input:
  - spec_source: URL or file path to OpenAPI spec
  - skill_name: Name for the skill
  - output_dir: Directory to create skill in
  - selected_categories: Comma-separated list of categories to include (or "all")
"""

import sys
import json
from pathlib import Path
from typing import List

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from openapi_parser import OpenAPIParser
from skill_generator import SkillGenerator


def generate_skill(
    spec_source: str,
    selected_categories: List[str],
    skill_name: str,
    output_dir: str
) -> bool:
    """
    Generate skill with selected categories.

    Args:
        spec_source: URL or file path to OpenAPI spec
        selected_categories: List of category names to include
        skill_name: Name for the generated skill
        output_dir: Directory to create skill in

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*60)
    print("⚙️  Generating Skill")
    print("="*60 + "\n")

    # Parse OpenAPI spec
    parser = OpenAPIParser(spec_source)
    if not parser.load_spec():
        print("❌ Failed to load OpenAPI specification", file=sys.stderr)
        return False

    parser.extract_categories()
    all_categories = parser.get_all_categories_list()

    # Validate selections
    if not all(cat in all_categories for cat in selected_categories):
        print("❌ Invalid category selection", file=sys.stderr)
        return False

    print(f"📋 Generating skill with {len(selected_categories)} categories:")
    for cat in selected_categories:
        print(f"   • {cat}")
    print()

    # Generate skill
    generator = SkillGenerator(
        skill_name,
        output_dir,
        parser.categories,
        selected_categories,
        all_categories
    )

    if not generator.generate():
        print("❌ Skill generation failed", file=sys.stderr)
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
    """Main entry point."""
    if len(sys.argv) < 5:
        print("❌ Missing required arguments", file=sys.stderr)
        print("Usage: python3 generate_skill.py <spec-url> <skill-name> <output-dir> <categories>", file=sys.stderr)
        print("  categories: comma-separated list or 'all'", file=sys.stderr)
        sys.exit(1)

    spec_source = sys.argv[1]
    skill_name = sys.argv[2]
    output_dir = sys.argv[3]
    categories_arg = sys.argv[4]

    # Validate skill name
    if not skill_name or not all(c.isalnum() or c == '-' for c in skill_name):
        print("❌ Invalid skill name (use lowercase letters, numbers, and hyphens)", file=sys.stderr)
        sys.exit(1)

    # Validate output directory
    output_path = Path(output_dir)
    if not output_path.exists():
        print(f"❌ Output directory does not exist: {output_dir}", file=sys.stderr)
        sys.exit(1)

    # Parse categories argument
    if categories_arg.lower() == "all":
        # Need to parse spec first to get all categories
        parser = OpenAPIParser(spec_source)
        if not parser.load_spec():
            print("❌ Failed to load OpenAPI specification", file=sys.stderr)
            sys.exit(1)
        parser.extract_categories()
        selected_categories = parser.get_all_categories_list()
    else:
        # Parse comma-separated list
        selected_categories = [c.strip() for c in categories_arg.split(",") if c.strip()]

    if not selected_categories:
        print("❌ No categories specified", file=sys.stderr)
        sys.exit(1)

    # Generate skill
    if generate_skill(spec_source, selected_categories, skill_name, output_dir):
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
        print("\n❌ Interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
