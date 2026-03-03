# Manage Workflow - Skill Maintenance

This workflow provides tools for maintaining and inspecting installed skills.

## Purpose

When users need to manage their installed skills, this workflow:
- Lists all installed skills with status information
- Removes unwanted skills and their symlinks
- Performs health checks to verify skill integrity

## When to Use This Workflow

Use this workflow when:
- User wants to see all installed skills
- User needs to remove/uninstall a skill
- User wants to verify that skills are properly configured
- User says "list skills", "show my skills", "删除 skill", "check skill health"

## Subcommands

### 1. list - List All Installed Skills

**Purpose**: Display all installed skills with their metadata and status

**Command format**:
```
my-skill manage list
```

**What it does**:
1. Scans `~/.claude/skills/` for all symlinks
2. For each skill, extracts:
   - Skill name (from SKILL.md frontmatter)
   - Description (truncated to 80 chars)
   - Source path (where the symlink points)
   - Symlink status (both Claude Code and Cline)
3. Displays results in a formatted table

**Implementation**:

```bash
# List all skills in Claude Code directory
for skill_link in ~/.claude/skills/*; do
  if [ -L "$skill_link" ]; then
    SKILL_NAME=$(basename "$skill_link")
    SOURCE_PATH=$(readlink "$skill_link")

    # Check if SKILL.md exists
    if [ -f "$SOURCE_PATH/SKILL.md" ]; then
      # Extract name and description from YAML frontmatter
      NAME=$(grep '^name:' "$SOURCE_PATH/SKILL.md" | cut -d':' -f2- | xargs)
      DESC=$(grep '^description:' "$SOURCE_PATH/SKILL.md" | cut -d':' -f2- | xargs | cut -c1-80)

      # Check Cline symlink status
      if [ -L ~/.cline/skills/"$SKILL_NAME" ]; then
        CLINE_STATUS="✅"
      else
        CLINE_STATUS="❌"
      fi

      echo "$NAME | $DESC... | $SOURCE_PATH | ✅ | $CLINE_STATUS"
    else
      echo "$SKILL_NAME | [No SKILL.md] | $SOURCE_PATH | ⚠️ | N/A"
    fi
  fi
done
```

**Output format**:

```
Installed Skills:

| Name               | Description                                          | Source Path                                  | Claude | Cline |
|--------------------|------------------------------------------------------|----------------------------------------------|--------|-------|
| my-skill           | Unified skill management tool for finding, creating...| /Users/ppsteven/projects/skills/my-skill     | ✅     | ✅    |
| akshare-data       | Chinese financial market data (stocks, bonds...)     | /Users/ppsteven/projects/skills/akshare-data | ✅     | ✅    |
| skill-creator      | Create new skills and iteratively improve them       | ~/.claude/skills/skill-creator               | ✅     | ❌    |

Legend:
✅ = Symlink exists and points to valid directory
❌ = Symlink missing or broken
⚠️ = SKILL.md missing or invalid
```

**Important notes**:
- Only scan `~/.claude/skills/` as the source of truth (avoid duplicates)
- Check corresponding Cline symlink for each skill
- Truncate long descriptions to keep table readable
- Flag skills with missing or invalid SKILL.md files

---

### 2. remove - Remove Skill and Symlinks

**Purpose**: Delete a skill and its symlinks from both Claude Code and Cline

**Command format**:
```
my-skill manage remove <skill-name>
```

**What it does**:
1. Confirms with user before deletion
2. Optionally removes the source directory
3. Removes symlinks from `~/.claude/skills/` and `~/.cline/skills/`
4. Verifies deletion was successful

**Implementation**:

**Step 1: Confirm with user**
```
You're about to remove skill: <skill-name>

This will:
- Remove symlink at ~/.claude/skills/<skill-name>
- Remove symlink at ~/.cline/skills/<skill-name>
- Remove symlink at ~/.openclaw/workspace/skills/<skill-name>

Do you also want to delete the source directory?
Source: <path>

[Yes, delete source / No, keep source / Cancel]
```

**Step 2: Remove symlinks**
```bash
# Remove Claude Code symlink
if [ -L ~/.claude/skills/<skill-name> ]; then
  rm ~/.claude/skills/<skill-name>
  echo "✅ Removed Claude Code symlink"
else
  echo "⚠️ Claude Code symlink not found"
fi

# Remove Cline symlink
if [ -L ~/.cline/skills/<skill-name> ]; then
  rm ~/.cline/skills/<skill-name>
  echo "✅ Removed Cline symlink"
else
  echo "⚠️ Cline symlink not found"
fi

# Remove OpenClaw symlink
if [ -L ~/.openclaw/workspace/skills/<skill-name> ]; then
  rm ~/.openclaw/workspace/skills/<skill-name>
  echo "✅ Removed OpenClaw symlink"
else
  echo "⚠️ OpenClaw symlink not found"
fi
```

**Step 3: Remove source directory (if user confirmed)**
```bash
# Only if user chose "Yes, delete source"
if [ -d "$SOURCE_PATH" ]; then
  rm -rf "$SOURCE_PATH"
  echo "✅ Removed source directory: $SOURCE_PATH"
else
  echo "⚠️ Source directory not found: $SOURCE_PATH"
fi
```

**Step 4: Verify removal**
```bash
# Verify symlinks are gone
test ! -e ~/.claude/skills/<skill-name> && echo "✅ Claude Code symlink removed" || echo "❌ Failed to remove Claude Code symlink"
test ! -e ~/.cline/skills/<skill-name> && echo "✅ Cline symlink removed" || echo "❌ Failed to remove Cline symlink"
test ! -e ~/.openclaw/workspace/skills/<skill-name> && echo "✅ OpenClaw symlink removed" || echo "❌ Failed to remove OpenClaw symlink"

# Verify source directory (if deleted)
if [[ $DELETE_SOURCE == true ]]; then
  test ! -d "$SOURCE_PATH" && echo "✅ Source directory removed" || echo "❌ Failed to remove source directory"
fi
```

**Output example**:
```
Removing skill: obsolete-skill

✅ Removed Claude Code symlink
✅ Removed Cline symlink
✅ Removed OpenClaw symlink
✅ Removed source directory: /Users/ppsteven/projects/skills/obsolete-skill

Verification:
✅ Claude Code symlink removed
✅ Cline symlink removed
✅ Source directory removed

Skill 'obsolete-skill' has been successfully removed.
```

**Important notes**:
- Always ask for confirmation before deleting
- Distinguish between symlink removal (safe) and source deletion (permanent)
- Default to keeping source directory unless user explicitly confirms deletion
- Verify all operations completed successfully
- If skill is in `/Users/ppsteven/projects/skills/`, remind user to commit removal to git

---

### 3. health-check - Verify Skill Integrity

**Purpose**: Check that all installed skills are properly configured and functional

**Command format**:
```
my-skill manage health-check
```

**What it does**:
1. Scans all skills in `~/.claude/skills/`
2. For each skill, checks:
   - Symlink integrity (points to valid directory)
   - SKILL.md exists
   - YAML frontmatter is valid
   - Required fields (name, description) are present
3. Reports issues and provides recommendations

**Implementation**:

```bash
#!/bin/bash

echo "Running health check on all installed skills..."
echo ""

TOTAL=0
HEALTHY=0
ISSUES=0

for skill_link in ~/.claude/skills/*; do
  if [ -L "$skill_link" ]; then
    TOTAL=$((TOTAL + 1))
    SKILL_NAME=$(basename "$skill_link")
    SOURCE_PATH=$(readlink "$skill_link")

    echo "Checking: $SKILL_NAME"

    SKILL_HEALTHY=true

    # Check 1: Symlink points to valid directory
    if [ ! -d "$SOURCE_PATH" ]; then
      echo "  ❌ Symlink broken: points to non-existent directory"
      echo "     Path: $SOURCE_PATH"
      SKILL_HEALTHY=false
    else
      echo "  ✅ Symlink valid"
    fi

    # Check 2: SKILL.md exists
    if [ ! -f "$SOURCE_PATH/SKILL.md" ]; then
      echo "  ❌ SKILL.md not found"
      SKILL_HEALTHY=false
    else
      echo "  ✅ SKILL.md exists"

      # Check 3: YAML frontmatter present
      if ! grep -q '^---$' "$SOURCE_PATH/SKILL.md"; then
        echo "  ❌ YAML frontmatter missing"
        SKILL_HEALTHY=false
      else
        echo "  ✅ YAML frontmatter present"

        # Check 4: Required fields (name, description)
        if ! grep -q '^name:' "$SOURCE_PATH/SKILL.md"; then
          echo "  ❌ Required field 'name' missing"
          SKILL_HEALTHY=false
        else
          echo "  ✅ Field 'name' present"
        fi

        if ! grep -q '^description:' "$SOURCE_PATH/SKILL.md"; then
          echo "  ❌ Required field 'description' missing"
          SKILL_HEALTHY=false
        else
          echo "  ✅ Field 'description' present"
        fi
      fi
    fi

    # Check 5: Cline symlink exists
    if [ ! -L ~/.cline/skills/"$SKILL_NAME" ]; then
      echo "  ⚠️  Cline symlink missing (skill only available in Claude Code)"
      # This is a warning, not a failure
    else
      # Verify Cline symlink points to same source
      CLINE_SOURCE=$(readlink ~/.cline/skills/"$SKILL_NAME")
      if [ "$CLINE_SOURCE" != "$SOURCE_PATH" ]; then
        echo "  ⚠️  Cline symlink points to different source"
        echo "     Expected: $SOURCE_PATH"
        echo "     Actual: $CLINE_SOURCE"
      else
        echo "  ✅ Cline symlink valid"
      fi
    fi

    # Check 6: OpenClaw symlink exists
    if [ ! -L ~/.openclaw/workspace/skills/"$SKILL_NAME" ]; then
      echo "  ⚠️  OpenClaw symlink missing (skill not available in OpenClaw)"
      # This is a warning, not a failure
    else
      # Verify OpenClaw symlink points to same source
      OPENCLAW_SOURCE=$(readlink ~/.openclaw/workspace/skills/"$SKILL_NAME")
      if [ "$OPENCLAW_SOURCE" != "$SOURCE_PATH" ]; then
        echo "  ⚠️  OpenClaw symlink points to different source"
        echo "     Expected: $SOURCE_PATH"
        echo "     Actual: $OPENCLAW_SOURCE"
      else
        echo "  ✅ OpenClaw symlink valid"
      fi
    fi

    if [ "$SKILL_HEALTHY" = true ]; then
      HEALTHY=$((HEALTHY + 1))
      echo "  ✅ Overall: Healthy"
    else
      ISSUES=$((ISSUES + 1))
      echo "  ❌ Overall: Issues found"
    fi

    echo ""
  fi
done

echo "========================================"
echo "Health Check Summary"
echo "========================================"
echo "Total skills: $TOTAL"
echo "Healthy: $HEALTHY"
echo "With issues: $ISSUES"
echo ""

if [ $ISSUES -gt 0 ]; then
  echo "Recommendations:"
  echo "- For broken symlinks: Remove with 'my-skill manage remove <name>'"
  echo "- For missing SKILL.md: Verify skill installation or reinstall"
  echo "- For invalid frontmatter: Edit SKILL.md to add required fields"
  echo "- For missing Cline symlinks: Create with 'ln -s <source> ~/.cline/skills/<name>'"
  echo "- For missing OpenClaw symlinks: Create with 'ln -s <source> ~/.openclaw/workspace/skills/<name>'"
fi
```

**Output example**:
```
Running health check on all installed skills...

Checking: my-skill
  ✅ Symlink valid
  ✅ SKILL.md exists
  ✅ YAML frontmatter present
  ✅ Field 'name' present
  ✅ Field 'description' present
  ✅ Cline symlink valid
  ✅ Overall: Healthy

Checking: broken-skill
  ❌ Symlink broken: points to non-existent directory
     Path: /tmp/deleted-skill
  ✅ Overall: Issues found

Checking: incomplete-skill
  ✅ Symlink valid
  ✅ SKILL.md exists
  ❌ YAML frontmatter missing
  ⚠️ Cline symlink missing (skill only available in Claude Code)
  ❌ Overall: Issues found

========================================
Health Check Summary
========================================
Total skills: 3
Healthy: 1
With issues: 2

Recommendations:
- For broken symlinks: Remove with 'my-skill manage remove <name>'
- For missing SKILL.md: Verify skill installation or reinstall
- For invalid frontmatter: Edit SKILL.md to add required fields
- For missing Cline symlinks: Create with 'ln -s <source> ~/.cline/skills/<name>'
```

**Important notes**:
- Non-critical issues (missing Cline symlink, mismatched paths) should be warnings, not failures
- Provide actionable recommendations for each type of issue
- Consider creating a repair mode that fixes common issues automatically
- Run health check after installing new skills to catch setup problems early

---

## Best Practices

### When to List Skills
- Before removing a skill (to verify it exists)
- After installing new skills (to confirm availability)
- When troubleshooting skill-related issues
- Periodically to review installed skills

### When to Remove Skills
- Skill is no longer needed
- Skill is superseded by a better alternative
- Skill is causing conflicts or errors
- Cleaning up test/experimental skills

### When to Run Health Check
- After batch installing multiple skills
- When skills stop working unexpectedly
- After system updates or migrations
- Before committing skill changes to repository
- Periodically (e.g., monthly maintenance)

## Troubleshooting

### Symlink Issues
**Problem**: Symlink broken or pointing to wrong location
**Solution**:
1. Remove broken symlink: `rm ~/.claude/skills/<skill-name>`
2. Recreate symlink: `ln -s <correct-source> ~/.claude/skills/<skill-name>`
3. Verify: `readlink ~/.claude/skills/<skill-name>`

### SKILL.md Format Issues
**Problem**: YAML frontmatter invalid or missing required fields
**Solution**:
1. Open SKILL.md in editor
2. Ensure frontmatter starts/ends with `---`
3. Add missing fields:
   ```yaml
   ---
   name: skill-name
   description: What the skill does and when to use it
   ---
   ```
4. Validate with health check

### Cline Symlink Missing
**Problem**: Skill works in Claude Code but not in Cline
**Solution**:
```bash
# Find source path
SOURCE=$(readlink ~/.claude/skills/<skill-name>)

# Create Cline symlink
ln -s "$SOURCE" ~/.cline/skills/<skill-name>

# Verify
ls -l ~/.cline/skills/<skill-name>
```

### OpenClaw Symlink Missing
**Problem**: Skill works in Claude Code/Cline but not in OpenClaw
**Solution**:
```bash
# Find source path
SOURCE=$(readlink ~/.claude/skills/<skill-name>)

# Create OpenClaw symlink
ln -s "$SOURCE" ~/.openclaw/workspace/skills/<skill-name>

# Verify
ls -l ~/.openclaw/workspace/skills/<skill-name>
```

---

## Related Operations

- Use **list** before **remove** to confirm skill exists
- Run **health-check** after bulk installations
- Combine with **find workflow** to discover replacement skills
- Use **create workflow** to add new skills after cleanup
