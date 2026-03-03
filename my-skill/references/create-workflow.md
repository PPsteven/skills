# Create Workflow - Skill Deployment

This workflow documents the complete process for creating and deploying new skills to the centralized skills repository.

## Purpose

When users need to create a new skill, this workflow:
- Syncs with remote repository to avoid conflicts
- Invokes skill-creator for guidance
- Sets up proper directory structure
- Creates symlinks for tool availability
- Verifies deployment
- Commits changes to repository

## When to Use This Workflow

Use this workflow when:
- Creating a new skill for the skills repository
- Setting up a skill in the proper deployment directory structure
- Configuring symlinks for skill availability across tools (Claude Code, Cline)
- Verifying that a skill is properly deployed and discoverable

## Initial Repository Sync

**CRITICAL:** Before starting skill creation, synchronize with the remote repository:

```bash
cd /Users/ppsteven/projects/skills
git pull origin main
```

This ensures:
- You have the latest skills and updates
- Avoid merge conflicts when committing new skills
- All team members are working with current code

## Skill Creation Trigger Rules

**CRITICAL:** Always invoke the `skill-creator` skill BEFORE any other action when:
- Creating a new skill
- Adding functionality via a new skill
- Extending capabilities through skill development
- Asked to create or add a new skill in any language (including "新增技能" in Chinese)

This is mandatory and non-negotiable. The `skill-creator` skill provides the complete guidance for skill anatomy, YAML frontmatter configuration, inline vs. fork context decisions, and best practices.

## Deployment Directory Structure

All skills must be created in the centralized repository:

```
/Users/ppsteven/projects/skills/
├── skill-name-1/
│   ├── SKILL.md                 # Required skill metadata and instructions
│   ├── scripts/                 # Optional: Executable code (Python/Bash/etc.)
│   ├── references/              # Optional: Documentation and reference materials
│   └── assets/                  # Optional: Output templates, icons, boilerplate
│
├── skill-name-2/
│   └── SKILL.md
│
└── new-skill/
    └── SKILL.md                 # This skill
```

**Key principles:**
- Use kebab-case for directory names (lowercase with hyphens)
- SKILL.md is always required
- Resource directories (scripts/, references/, assets/) are optional
- No spaces or special characters in skill directory names

## Symlink Setup After Creation

After creating a skill in `/Users/ppsteven/projects/skills/<skill-name>`, create symlinks to make it available to Claude Code, Cline, and OpenClaw:

### Link to Claude Code

```bash
ln -s /Users/ppsteven/projects/skills/<skill-name> ~/.claude/skills/<skill-name>
```

### Link to Cline

```bash
ln -s /Users/ppsteven/projects/skills/<skill-name> ~/.cline/skills/<skill-name>
```

### Link to OpenClaw

```bash
ln -s /Users/ppsteven/projects/skills/<skill-name> ~/.openclaw/workspace/skills/<skill-name>
```

### Verification

Verify all three symlinks were created correctly:

```bash
# Check Claude Code symlink
ls -l ~/.claude/skills/<skill-name>

# Check Cline symlink
ls -l ~/.cline/skills/<skill-name>

# Check OpenClaw symlink
ls -l ~/.openclaw/workspace/skills/<skill-name>

# Verify symlinks point to the correct source
readlink ~/.claude/skills/<skill-name>
readlink ~/.cline/skills/<skill-name>
readlink ~/.openclaw/workspace/skills/<skill-name>
```

All three should output `/Users/ppsteven/projects/skills/<skill-name>`.

## Complete Workflow Example

### Scenario: Create a new skill for Python dependency management

**Step 0: Sync repository**
```bash
cd /Users/ppsteven/projects/skills
git pull origin main
```
Always sync first to avoid merge conflicts.

**Step 1: Invoke skill-creator (MANDATORY)**
```
Invoke the skill-creator skill with appropriate task description
```

**Step 2: Create skill directory**
```bash
mkdir -p /Users/ppsteven/projects/skills/python-dependency-manager
```

**Step 3: Generate SKILL.md**
Following skill-creator guidance, create SKILL.md with:
- YAML frontmatter (name, description, optional context/agent)
- Clear documentation of what the skill does
- Instructions for how Claude should use the skill
- References to any bundled resources (scripts/, references/, assets/)

**Step 4: Add reusable resources** (as needed)
- `scripts/` - For Python scripts or utility code
- `references/` - For documentation, best practices, schema definitions
- `assets/` - For templates, boilerplate code, or sample projects

**Step 5: Create symlinks**
```bash
ln -s /Users/ppsteven/projects/skills/python-dependency-manager \
      ~/.claude/skills/python-dependency-manager

ln -s /Users/ppsteven/projects/skills/python-dependency-manager \
      ~/.cline/skills/python-dependency-manager

ln -s /Users/ppsteven/projects/skills/python-dependency-manager \
      ~/.openclaw/workspace/skills/python-dependency-manager
```

**Step 6: Verify deployment**
```bash
# Verify symlink targets exist
test -f ~/.claude/skills/python-dependency-manager/SKILL.md && echo "Claude Code OK" || echo "FAILED"
test -f ~/.cline/skills/python-dependency-manager/SKILL.md && echo "Cline OK" || echo "FAILED"
test -f ~/.openclaw/workspace/skills/python-dependency-manager/SKILL.md && echo "OpenClaw OK" || echo "FAILED"

# Verify skill is discoverable
ls -l ~/.claude/skills/ | grep python-dependency-manager
ls -l ~/.openclaw/workspace/skills/ | grep python-dependency-manager
```

**Step 7: Test the skill**
Invoke the skill to verify it loads correctly and functions as intended.

**Step 8: Commit and Push to Repository** (if skill is complete)
After all verification passes, ask the user for confirmation before committing:

```
Are you ready to commit and push this new skill to the repository?
Commit message: feat(new-skill): Add python-dependency-manager skill
```

If user confirms:
```bash
cd /Users/ppsteven/projects/skills
git add python-dependency-manager/
git commit -m "feat(new-skill): Add python-dependency-manager skill"
git push origin main
```

If user declines, keep the skill local without pushing to remote.

## Critical Deployment Rules

### DO ✅

- Always execute `git pull` before starting skill creation
- Always invoke `skill-creator` skill first when creating skills
- Deploy to `/Users/ppsteven/projects/skills/<skill-name>`
- Create symlinks to all three tools: `~/.claude/skills/`, `~/.cline/skills/`, and `~/.openclaw/workspace/skills/`
- Use kebab-case for skill directory names
- Verify symlinks after creation with `readlink` command
- Follow skill-creator guidance for SKILL.md format and content
- Store skill source in the centralized repository (not in symlink targets)
- Ask user confirmation before committing changes
- Use conventional commit messages: `feat(new-skill): Add <skill-name> skill`

### DON'T ❌

- Create skills directly in `~/.claude/skills/`, `~/.cline/skills/`, or `~/.openclaw/workspace/skills/`
- Skip the `skill-creator` skill invocation
- Create skills in arbitrary locations
- Use spaces or special characters in skill directory names
- Edit skills in `~/.claude/plugins/cache/` (that's a read-only cache)
- Forget to create symlinks for any of the three tools (Claude Code, Cline, OpenClaw)
- Store skill implementations in symlink directories
- Commit changes without user confirmation
- Push to repository without verifying skill completion and testing
- Skip `git pull` at the beginning of skill creation workflow

## Post-Deployment Verification Checklist

After creating a new skill, verify all these points:

**Before Starting:**
- [ ] Executed `git pull` to sync latest repository state

**During Development:**
- [ ] skill-creator skill was invoked before any implementation
- [ ] Skill created in `/Users/ppsteven/projects/skills/<skill-name>/`
- [ ] SKILL.md exists with proper YAML frontmatter (name and description)
- [ ] SKILL.md frontmatter contains appropriate fields (context, agent if needed)
- [ ] Symlink created at `~/.claude/skills/<skill-name>`
- [ ] Symlink created at `~/.cline/skills/<skill-name>`
- [ ] Symlink created at `~/.openclaw/workspace/skills/<skill-name>`
- [ ] All three symlinks verified with `readlink` to point to correct source
- [ ] Skill is discoverable when checking available skills
- [ ] Skill invocation works and content loads correctly
- [ ] All resource directories (scripts/, references/, assets/) are optional but named correctly
- [ ] No sensitive information in SKILL.md (no absolute paths, usernames, API keys)

**Before Committing:**
- [ ] All tests and verifications pass
- [ ] User confirms readiness to commit
- [ ] Git status shows only new skill files (no unintended changes)
- [ ] Commit message follows convention: `feat(new-skill): Add <skill-name> skill`
- [ ] Changes pushed to remote main branch successfully

## Important Notes

### About Skills

Skills are modular packages that extend Claude's capabilities by providing:
1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats
3. Domain expertise - Knowledge and best practices
4. Bundled resources - Scripts, references, and assets for repeated tasks

### YAML Frontmatter Reference

Essential fields in SKILL.md:

```yaml
---
name: skill-name                          # Required: lowercase, hyphens, max 64 chars
description: What this skill does and... # Required: when to use it
context: fork                             # Optional: runs as subagent (fork) or inline
agent: general-purpose                   # Optional: subagent type (Explore, Plan, general-purpose)
disable-model-invocation: false          # Optional: prevent auto-invocation
---
```

**Key decision:** Set `context: fork` if the skill needs to call other skills or use the Task tool for parallel operations. Otherwise, leave unset for inline execution.

### Inline vs. Fork Context

- **Inline (default)**: Runs in main conversation context; can call other skills and use all tools
- **Fork (context: fork)**: Runs in isolated subagent context; cannot call other skills but provides clean execution environment

Choose inline for orchestration skills, fork for specialized execution skills.

## Related Documentation

- **skill-creator skill**: Comprehensive guidance on skill creation, anatomy, best practices
- **Skills directory**: `/Users/ppsteven/projects/skills/`
- **Project rules**: `~/.claude/rules/project-documentation-rules.md`
- **CLAUDE.md**: Project-specific development guidance at `/Users/ppsteven/projects/skills/.claude/CLAUDE.md`
