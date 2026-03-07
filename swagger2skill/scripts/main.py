#!/usr/bin/env python3
"""
Swagger to Skill Generator - Main Entry Point for Claude Code

Simple, clean workflow:
1. Receive OpenAPI URL
2. Extract and display categories
3. Use AskUserQuestion for selection (handled by Claude Code)
4. Generate skill based on selection
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from openapi_parser import OpenAPIParser
from skill_generator import SkillGenerator


def extract_categories(spec_source: str) -> Optional[Dict]:
    """Extract categories from OpenAPI spec."""
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
        print(f"❌ Error: {e}", file=sys.stderr)
        return None


def print_categories(categories_data: Dict):
    """Pretty print categories list."""
    print("\n" + "="*60)
    print("📖 OpenAPI Categories")
    print("="*60 + "\n")

    print(f"✅ Found {categories_data['total']} API categories:\n")
    for i, cat_info in enumerate(categories_data['categories'], 1):
        print(f"   {i}. {cat_info['name']} ({cat_info['endpoint_count']} endpoints)")

    # Output as JSON for potential machine parsing
    print("\n📋 JSON Output:")
    print(json.dumps(categories_data, indent=2))


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
    print("🚀 Swagger to Skill Generator")
    print("="*60 + "\n")

    # Step 1: Get OpenAPI URL
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <openapi-url>")
        print("   or: python3 main.py <openapi-url> --extract-only")
        sys.exit(1)

    spec_source = sys.argv[1]
    extract_only = "--extract-only" in sys.argv

    print(f"📦 OpenAPI source: {spec_source}\n")

    # Step 2: Extract categories
    categories_data = extract_categories(spec_source)
    if not categories_data:
        sys.exit(1)

    # Step 3: Display categories
    print_categories(categories_data)

    # If extract-only mode, stop here
    if extract_only:
        print("\n✅ Categories extraction complete (extract-only mode)")
        sys.exit(0)

    # Step 4: Get selection from user
    print("\n" + "="*60)
    print("🎯 Category Selection")
    print("="*60 + "\n")

    print("Select categories:")
    print("1. All categories")
    print("2. Custom selection (enter numbers or names)\n")

    choice = input("👉 Your choice (1 or 2): ").strip()

    categories_list = [cat['name'] for cat in categories_data['categories']]

    if choice == "1":
        selected_categories = categories_list
        print(f"\n✅ Selected all {len(selected_categories)} categories")
    elif choice == "2":
        selection_str = input("👉 Enter category numbers/names (comma-separated, e.g., '1,2,3' or 'dag,variable'): ").strip()
        selections = [s.strip() for s in selection_str.split(",")]
        selected_categories = []

        for sel in selections:
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(categories_list):
                    selected_categories.append(categories_list[idx])
                else:
                    print(f"⚠️  Skipping invalid index: {sel}")
            except ValueError:
                if sel.lower() in [c.lower() for c in categories_list]:
                    # Find exact match (case-insensitive)
                    selected_categories.append(next(c for c in categories_list if c.lower() == sel.lower()))
                else:
                    print(f"⚠️  Skipping unknown category: {sel}")

        if not selected_categories:
            print("❌ No valid categories selected")
            sys.exit(1)

        print(f"\n✅ Selected {len(selected_categories)} categories:")
        for cat in selected_categories:
            print(f"   • {cat}")
    else:
        print("❌ Invalid choice")
        sys.exit(1)

    # Step 5: Get skill details
    print("\n" + "="*60)
    print("💾 Skill Details")
    print("="*60 + "\n")

    skill_name = input("👉 Skill name (kebab-case, e.g., 'airflow-api'): ").strip().lower()
    if not skill_name:
        print("❌ Skill name cannot be empty")
        sys.exit(1)

    default_dir = "/Users/ppsteven/projects/skills"
    output_dir = input(f"👉 Output directory (default: {default_dir}): ").strip()
    if not output_dir:
        output_dir = default_dir

    output_path = Path(output_dir)
    if not output_path.exists():
        print(f"❌ Directory does not exist: {output_dir}")
        sys.exit(1)

    # Step 6: Generate skill
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
