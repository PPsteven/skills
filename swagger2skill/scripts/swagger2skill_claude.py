#!/usr/bin/env python3
"""
Swagger to Skill Generator - Claude Code Integration

Workflow:
1. Extract categories from OpenAPI spec using extract_categories.py
2. Use AskUserQuestion tool for user selection (all vs custom)
3. Generate skill based on selection
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import List, Tuple

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from openapi_parser import OpenAPIParser
from skill_generator import SkillGenerator


def extract_categories_via_script(spec_source: str) -> dict:
    """
    Extract categories by calling extract_categories.py script.

    Args:
        spec_source: URL or file path to OpenAPI spec

    Returns:
        Dict with categories list
    """
    script_path = Path(__file__).parent / "extract_categories.py"

    try:
        result = subprocess.run(
            [sys.executable, str(script_path), spec_source],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"❌ Failed to extract categories", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            return None

        return json.loads(result.stdout)

    except json.JSONDecodeError:
        print("❌ Invalid JSON output from extract_categories.py", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Error extracting categories: {e}", file=sys.stderr)
        return None


def display_categories(categories_data: dict):
    """Display extracted categories."""
    print("\n" + "="*60)
    print("📖 OpenAPI Categories Extracted")
    print("="*60 + "\n")

    print(f"✅ Found {categories_data['total']} API categories:\n")
    for i, cat_info in enumerate(categories_data['categories'], 1):
        print(f"   {i}. {cat_info['name']} ({cat_info['endpoint_count']} endpoints)")


def ask_for_category_selection(categories_data: dict) -> str:
    """
    Ask user whether to select all categories or custom.

    Returns:
        "all" or "custom"
    """
    print("\n" + "="*60)
    print("🎯 Category Selection")
    print("="*60 + "\n")

    # In interactive/CLI mode, just prompt directly
    print("Select categories:")
    print("1. All categories")
    print("2. Custom selection\n")
    choice = input("👉 Your choice (1 or 2): ").strip()
    return "all" if choice == "1" else "custom"


def get_custom_selection(categories_data: dict) -> List[str]:
    """
    Get custom category selection from user.

    Returns:
        List of selected category names
    """
    categories_list = [cat['name'] for cat in categories_data['categories']]

    print("\n" + "="*60)
    print("🎯 Custom Category Selection")
    print("="*60 + "\n")

    print("Enter category numbers or names (comma-separated)")
    print("Examples:")
    print("  • 1,2,3,4")
    print("  • DAG,Variable,TaskInstance")
    print("  • All\n")

    selection_str = input("👉 Your selection: ").strip()

    if selection_str.lower() == "all":
        return categories_list

    selections = [s.strip() for s in selection_str.split(",")]
    selected = []

    for sel in selections:
        try:
            # Try as number (1-indexed)
            idx = int(sel) - 1
            if 0 <= idx < len(categories_list):
                selected.append(categories_list[idx])
            else:
                print(f"⚠️  Skipping invalid index: {sel}")
        except ValueError:
            # Try as name
            if sel in categories_list:
                selected.append(sel)
            else:
                print(f"⚠️  Skipping unknown category: {sel}")

    if not selected:
        print("❌ No valid categories selected")
        sys.exit(1)

    return selected


def get_skill_details() -> Tuple[str, str]:
    """
    Get skill name and output directory from user.

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
    spec_source: str,
    selected_categories: List[str],
    skill_name: str,
    output_dir: str
) -> bool:
    """
    Generate skill with selected categories.

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*60)
    print("⚙️  Generating Skill")
    print("="*60 + "\n")

    # Parse OpenAPI spec
    parser = OpenAPIParser(spec_source)
    if not parser.load_spec():
        return False

    parser.extract_categories()
    all_categories = parser.get_all_categories_list()

    # Validate selections
    if not all(cat in all_categories for cat in selected_categories):
        print("❌ Invalid category selection")
        return False

    # Generate skill
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
        print("Usage: python3 swagger2skill_claude.py <openapi-url-or-file>")
        sys.exit(1)

    spec_source = sys.argv[1]
    print(f"📦 Using OpenAPI source: {spec_source}\n")

    # Step 1: Extract categories
    categories_data = extract_categories_via_script(spec_source)
    if not categories_data:
        sys.exit(1)

    display_categories(categories_data)

    # Step 2: Ask for selection (all or custom)
    selection_choice = ask_for_category_selection(categories_data)

    # In interactive mode, get selection from user
    if selection_choice == "all":
        selected_categories = [cat['name'] for cat in categories_data['categories']]
        print(f"\n✅ Selected all {len(selected_categories)} categories")
    elif selection_choice == "custom":
        selected_categories = get_custom_selection(categories_data)
        print(f"\n✅ Selected {len(selected_categories)} categories:")
        for cat in selected_categories:
            print(f"   • {cat}")
    else:
        # Interactive fallback
        choice_input = input("\n👉 Select [all] or [custom]: ").strip().lower()
        if choice_input == "all":
            selected_categories = [cat['name'] for cat in categories_data['categories']]
            print(f"\n✅ Selected all {len(selected_categories)} categories")
        elif choice_input == "custom":
            selected_categories = get_custom_selection(categories_data)
            print(f"\n✅ Selected {len(selected_categories)} categories:")
            for cat in selected_categories:
                print(f"   • {cat}")
        else:
            print("❌ Invalid choice")
            sys.exit(1)

    # Step 3: Get skill details
    skill_name, output_dir = get_skill_details()

    # Step 4: Generate skill
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
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
