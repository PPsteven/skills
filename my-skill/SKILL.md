---
name: my-skill
description: Unified skill management tool for finding, creating, and managing agent skills. Use when user needs to discover skills with deep research (find), create new skills with proper deployment (create), or manage installed skills (list/remove/health-check). Trigger on phrases like 'my-skill find/create/manage', 'find a skill for X', 'create a new skill', 'list all skills', 'check skill health', or any skill-related operations including skill discovery, creation, listing, removal, or health checking.
---

# My Skill - Unified Skill Management

This skill provides a complete toolkit for managing agent skills throughout their lifecycle: discovering existing skills, creating new ones, and maintaining installed skills.

## Overview

**my-skill** consolidates three essential skill management workflows:

1. **find** - Discover and research skills with deep comparative analysis
2. **create** - Create new skills with proper deployment and symlink configuration
3. **manage** - Maintain installed skills (list, remove, health-check)

## How This Skill Works

This skill acts as a router that delegates to specialized workflows based on the user's intent:

### Explicit Subcommands

When the user explicitly requests a subcommand:
- `my-skill find <query>` → Triggers find workflow
- `my-skill create <skill-name>` → Triggers create workflow
- `my-skill manage list` → Lists all installed skills
- `my-skill manage remove <skill-name>` → Removes a skill
- `my-skill manage health-check` → Checks skill health

### Smart Intent Detection

When the user's request implies skill management without explicit subcommands:

**Find workflow triggers:**
- "找一个 GitHub 相关的 skill"
- "search for data analysis skills"
- "compare skills for web scraping"
- "深入研究 PDF processing skills"

**Create workflow triggers:**
- "创建一个新的 skill"
- "create a skill for database management"
- "我想添加一个 skill"
- "build a new skill"

**Manage workflow triggers:**
- "list all my skills"
- "show installed skills"
- "删除 obsolete-skill"
- "check if my skills are working correctly"
- "verify skill health"

## Routing Logic

**Step 1: Identify User Intent**

Analyze the user's request to determine which workflow to invoke:

```
IF user says "my-skill find" OR request contains ("find skill", "search skill", "discover skill", "compare skills", "研究 skill"):
    → Load references/find-workflow.md

ELSE IF user says "my-skill create" OR request contains ("create skill", "new skill", "创建 skill", "添加 skill"):
    → Load references/create-workflow.md

ELSE IF user says "my-skill manage" OR request contains ("list skills", "remove skill", "check skill", "health", "删除 skill"):
    → Load references/manage-workflow.md

ELSE:
    → Ask user to clarify which operation they want: find, create, or manage
```

**Step 2: Load Appropriate Workflow**

Once the intent is identified, read the corresponding workflow file:

- **Find workflow**: Read `references/find-workflow.md` and follow its instructions
- **Create workflow**: Read `references/create-workflow.md` and follow its instructions
- **Manage workflow**: Read `references/manage-workflow.md` and follow its instructions

**Step 3: Execute Workflow**

Follow the instructions in the loaded workflow file to complete the user's request.

## Workflow Summaries

### Find Workflow

**Purpose**: Discover and deeply research skills with comparative analysis

**Key steps**:
1. Clarify user's goal and requirements
2. Search ClawHub for relevant skills
3. Identify top 3-5 candidates
4. Analyze each candidate (技术方案/优势/劣势/风险)
5. Generate comparative report with recommendations
6. Save report to Obsidian with YAML frontmatter

**Output**: Markdown research report saved to `~/Documents/obsidian/minions/00.工作区/02.技术研究/`

### Create Workflow

**Purpose**: Create new skills with proper deployment and configuration

**Key steps**:
1. Sync repository with `git pull`
2. Invoke skill-creator skill for guidance
3. Create skill directory structure
4. Write SKILL.md with proper YAML frontmatter
5. Create symlinks for Claude Code and Cline
6. Verify deployment
7. Commit and push to repository (with user confirmation)

**Output**: New skill deployed at `/Users/ppsteven/projects/skills/<skill-name>` with symlinks

### Manage Workflow

**Purpose**: Maintain and inspect installed skills

**Subcommands**:
- **list**: Display all installed skills with name, description, source path, and symlink status
- **remove**: Delete a skill and its symlinks from both Claude Code and Cline
- **health-check**: Verify symlinks, SKILL.md format, and required fields for all skills

**Output**: Status reports, skill listings, or health check results

## When to Use This Skill

Use **my-skill** whenever you need to:

- **Research skills**: Find the best skill for a specific task with detailed comparison
- **Create skills**: Build new skills following proper deployment practices
- **Manage skills**: List, inspect, or remove installed skills

## Important Notes

### Skill Locations

- **Source repository**: `/Users/ppsteven/projects/skills/`
- **Claude Code symlinks**: `~/.claude/skills/`
- **Cline symlinks**: `~/.cline/skills/`

### Dependencies

- **find**: Requires `clawhub` CLI or `npx skills` for searching
- **create**: Requires `skill-creator` skill for guidance
- **manage**: No external dependencies

### Best Practices

1. Always invoke the appropriate workflow - don't try to improvise or combine workflows
2. For find: Take time to thoroughly analyze each candidate skill
3. For create: Always sync repository first and verify deployment after
4. For manage: Check health before removing skills to understand impact

## Related Skills

- **skill-creator**: Provides detailed guidance for creating new skills
- **find-skills**: Basic skill discovery (my-skill find extends this with deep research)
- **obsidian**: Manage Obsidian vault and notes (used by find workflow)

---

**Next Steps**: Read the appropriate workflow file from `references/` based on user intent, then follow its instructions exactly.
