#!/usr/bin/env python3
"""
Swagger2Skill Main Entry Point

Orchestrates the complete workflow:
1. Parse OpenAPI specification
2. Extract categories
3. Display to user
4. Get category selection
5. Generate skill
"""

import sys
import json
from pathlib import Path
from typing import List

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from openapi_parser import OpenAPIParser
from skill_generator import SkillGenerator


def prompt_category_selection(parser: OpenAPIParser) -> List[str]:
    """
    Display categories and prompt user for selection.

    Returns:
        List of selected category names
    """
    categories = parser.get_all_categories_list()

    if not categories:
        print("❌ No categories found in specification")
        return []

    print("\n" + "="*60)
    print("🎯 Select Categories to Include in Generated Skill")
    print("="*60 + "\n")

    # Display all categories with numbers
    for i, category in enumerate(categories, 1):
        endpoint_count = len(parser.get_category_details(category))
        print(f"{i}. {category} ({endpoint_count} endpoints)")

    print("\n" + "-"*60)
    print("Enter the numbers of categories to include (comma-separated)")
    print("Example: 1,2,4  (to select 1st, 2nd, and 4th categories)")
    print("-"*60 + "\n")

    while True:
        try:
            user_input = input("👉 Your selection: ").strip()

            if not user_input:
                print("❌ Please enter at least one category number")
                continue

            # Parse user input
            selected_indices = [int(x.strip()) - 1 for x in user_input.split(',')]

            # Validate indices
            if any(idx < 0 or idx >= len(categories) for idx in selected_indices):
                print("❌ Invalid category numbers. Please try again.")
                continue

            # Check for duplicates
            selected_indices = list(set(selected_indices))

            # Get selected category names
            selected = [categories[idx] for idx in selected_indices]

            print(f"\n✅ Selected {len(selected)} categories:")
            for cat in selected:
                print(f"   • {cat}")

            # Confirm
            confirm = input("\n👉 Confirm selection? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                return selected

        except ValueError:
            print("❌ Invalid input. Please enter numbers separated by commas.")
            continue
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            return []


def prompt_skill_name() -> str:
    """
    Prompt user for generated skill name.

    Returns:
        Skill name in kebab-case format
    """
    print("\n" + "="*60)
    print("💾 Generated Skill Name")
    print("="*60 + "\n")
    print("Enter the name for the generated skill.")
    print("(Use lowercase with hyphens, e.g., 'airflow-api', 'my-api-tool')\n")

    while True:
        name = input("👉 Skill name: ").strip().lower()

        # Validate skill name
        if not name:
            print("❌ Skill name cannot be empty")
            continue

        if not all(c.isalnum() or c == '-' for c in name):
            print("❌ Skill name can only contain lowercase letters, numbers, and hyphens")
            continue

        if name.startswith('-') or name.endswith('-'):
            print("❌ Skill name cannot start or end with a hyphen")
            continue

        print(f"\n✅ Skill name: {name}")
        confirm = input("👉 Confirm? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            return name


def prompt_output_directory() -> str:
    """
    Prompt user for output directory.

    Returns:
        Path to output directory
    """
    print("\n" + "="*60)
    print("📁 Output Directory")
    print("="*60 + "\n")
    print("Where should the skill be created?")
    print(f"Default: /Users/ppsteven/projects/skills\n")

    while True:
        output_dir = input("👉 Output directory (or press Enter for default): ").strip()

        if not output_dir:
            output_dir = "/Users/ppsteven/projects/skills"

        output_path = Path(output_dir)

        if not output_path.exists():
            print(f"❌ Directory does not exist: {output_dir}")
            create = input("Create it? (yes/no): ").strip().lower()
            if create in ['yes', 'y']:
                try:
                    output_path.mkdir(parents=True)
                    print(f"✅ Created directory: {output_dir}")
                    return output_dir
                except Exception as e:
                    print(f"❌ Error creating directory: {e}")
                continue
        else:
            print(f"✅ Output directory: {output_dir}")
            return output_dir


def main():
    """Main workflow."""
    print("\n" + "="*60)
    print("🚀 Swagger to Skill Generator")
    print("="*60 + "\n")

    # Step 1: Get OpenAPI source from user
    if len(sys.argv) > 1:
        spec_source = sys.argv[1]
        print(f"Using OpenAPI source from argument: {spec_source}\n")
    else:
        print("Provide an OpenAPI specification URL or file path.")
        print("Example: https://api.example.com/openapi.json")
        print("Example: ./openapi.json\n")
        spec_source = input("👉 OpenAPI source: ").strip()

        if not spec_source:
            print("❌ OpenAPI source is required")
            sys.exit(1)

    # Step 2: Parse OpenAPI specification
    print("\n" + "="*60)
    parser = OpenAPIParser(spec_source)

    if not parser.load_spec():
        sys.exit(1)

    parser.extract_categories()

    # Step 3: Display categories and get selection
    parser.display_categories()
    selected_categories = prompt_category_selection(parser)

    if not selected_categories:
        print("❌ No categories selected")
        sys.exit(1)

    # Step 4: Get skill name and output directory
    skill_name = prompt_skill_name()
    output_dir = prompt_output_directory()

    # Step 5: Generate skill
    print("\n" + "="*60)
    print("⚙️  Generating Skill")
    print("="*60 + "\n")

    generator = SkillGenerator(
        skill_name,
        output_dir,
        parser.categories,
        selected_categories,
        parser.get_all_categories_list()
    )

    if not generator.generate():
        sys.exit(1)

    # Step 6: Success summary
    print("\n" + "="*60)
    print("✅ Skill Generation Complete!")
    print("="*60)
    print(f"\n📍 Skill location: {generator.skill_dir}\n")
    print("📋 Next Steps:")
    print(f"   1. Review the generated files:")
    print(f"      - SKILL.md (Skill documentation)")
    print(f"      - scripts/cli_tool.py (CLI implementation)")
    print(f"      - references/api_endpoints.md (API reference)")
    print(f"\n   2. Implement the CLI commands in scripts/cli_tool.py")
    print(f"      - Replace TODO markers with actual API calls")
    print(f"      - Add authentication if needed")
    print(f"\n   3. Test the CLI tool locally")
    print(f"\n   4. Create symlink to ~/.claude/skills/ for use:")
    print(f"      ln -s {generator.skill_dir} ~/.claude/skills/{skill_name}")
    print(f"\n   5. Commit to repository:")
    print(f"      cd {output_dir}")
    print(f"      git add {skill_name}/")
    print(f"      git commit -m 'feat: Add {skill_name} skill'")
    print(f"      git push origin main")
    print()


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
