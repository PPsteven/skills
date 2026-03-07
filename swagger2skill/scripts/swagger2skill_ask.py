#!/usr/bin/env python3
"""
Swagger to Skill Generator - Claude Code Integration with AskUserQuestion

This script provides Claude Code integration using the AskUserQuestion tool.
It should be invoked from Claude Code environment.

Usage:
    When in Claude Code, invoke this script with the OpenAPI URL:
    python3 swagger2skill_ask.py <openapi-url>

    The script will:
    1. Extract categories from the OpenAPI spec
    2. Use AskUserQuestion to ask for user preferences
    3. Generate the skill based on user selections
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from openapi_parser import OpenAPIParser
from skill_generator import SkillGenerator


def extract_categories(spec_source: str) -> Dict:
    """Extract categories by running extract_categories.py."""
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
    except Exception as e:
        print(f"❌ Error extracting categories: {e}", file=sys.stderr)
        return None


def display_categories(categories_data: Dict):
    """Display extracted categories."""
    print("\n" + "="*60)
    print("📖 OpenAPI Categories Extracted")
    print("="*60 + "\n")

    print(f"✅ Found {categories_data['total']} API categories:\n")
    for i, cat_info in enumerate(categories_data['categories'], 1):
        print(f"   {i}. {cat_info['name']} ({cat_info['endpoint_count']} endpoints)")


def ask_user_question_via_tool(categories_data: Dict) -> List[str]:
    """
    Use Claude Code's AskUserQuestion tool to get user selections.

    This function returns the tool data structure that Claude Code's Skill tool
    should handle. The actual user interaction happens via the tool.

    Returns:
        List of selected category names (or None if this is first invocation)
    """
    print("\n" + "="*60)
    print("🎯 Category Selection (via AskUserQuestion)")
    print("="*60 + "\n")

    categories_list = [cat['name'] for cat in categories_data['categories']]

    # Build options for custom selection if user chooses that
    # Format categories nicely for display
    categories_str = "\n".join([
        f"   {i}. {cat_info['name']} ({cat_info['endpoint_count']} endpoints)"
        for i, cat_info in enumerate(categories_data['categories'], 1)
    ])

    # This would be handled by Claude Code's Skill system
    # For now, provide structured output that shows what we need

    tool_request = {
        "tool": "AskUserQuestion",
        "questions": [
            {
                "question": f"How would you like to select API categories? ({categories_data['total']} total)",
                "header": "Category Selection",
                "multiSelect": False,
                "options": [
                    {
                        "label": "All categories",
                        "description": f"Include all {categories_data['total']} categories in the skill"
                    },
                    {
                        "label": "Custom selection",
                        "description": "Choose specific categories to include"
                    }
                ]
            }
        ]
    }

    print("Requesting user input via AskUserQuestion tool...")
    print("\nAvailable categories:")
    print(categories_str)
    print("\n" + json.dumps(tool_request, indent=2))

    return None  # Indicates that user input is needed


def process_user_selection(selection: str, categories_data: Dict) -> List[str]:
    """
    Process user selection (either 'all' or custom list).

    Args:
        selection: Either "all" or comma-separated category names/numbers

    Returns:
        List of selected category names
    """
    categories_list = [cat['name'] for cat in categories_data['categories']]

    if selection.lower() == "all":
        return categories_list

    # Parse comma-separated selection
    selections = [s.strip() for s in selection.split(",")]
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


def get_skill_name_and_dir() -> tuple:
    """Get skill name and output directory from environment or prompt."""
    # Try to get from environment variables first (set by Claude Code)
    skill_name = os.environ.get("SWAGGER2SKILL_NAME")
    output_dir = os.environ.get("SWAGGER2SKILL_OUTPUT_DIR")

    # If not set, prompt for them
    if not skill_name:
        skill_name = input("👉 Skill name (kebab-case, e.g., 'airflow-api'): ").strip().lower()
        if not skill_name:
            print("❌ Skill name cannot be empty")
            sys.exit(1)

    if not output_dir:
        default_dir = "/Users/ppsteven/projects/skills"
        output_dir = input(f"👉 Output directory (default: {default_dir}): ").strip()
        if not output_dir:
            output_dir = default_dir

    return skill_name, output_dir


def generate_skill(
    spec_source: str,
    selected_categories: List[str],
    skill_name: str,
    output_dir: str
) -> bool:
    """Generate skill with selected categories."""
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
    print("🚀 Swagger to Skill Generator (Claude Code Integration)")
    print("="*60 + "\n")

    if len(sys.argv) < 2:
        print("❌ OpenAPI source is required")
        print("Usage: python3 swagger2skill_ask.py <openapi-url-or-file>")
        sys.exit(1)

    spec_source = sys.argv[1]
    print(f"📦 Using OpenAPI source: {spec_source}\n")

    # Step 1: Extract categories
    categories_data = extract_categories(spec_source)
    if not categories_data:
        sys.exit(1)

    display_categories(categories_data)

    # Step 2: Ask for category selection using AskUserQuestion
    # (This is handled by Claude Code's tool system)
    ask_user_question_via_tool(categories_data)

    # For now, provide fallback if not in Claude Code environment
    import os
    user_selection = os.environ.get("SWAGGER2SKILL_SELECTION", "").strip()

    if not user_selection:
        print("\n👉 Enter selection (e.g., 'all' or '1,2,3' or 'Config,DAG,Variable'): ")
        user_selection = input().strip()

    if not user_selection:
        print("❌ No selection provided")
        sys.exit(1)

    selected_categories = process_user_selection(user_selection, categories_data)
    print(f"\n✅ Selected {len(selected_categories)} categories:")
    for cat in selected_categories:
        print(f"   • {cat}")

    # Step 3: Get skill name and output directory
    skill_name, output_dir = get_skill_name_and_dir()

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
    import os
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
