---
name: github-repo-init
description: Use when pushing a new local git repository to GitHub with automatic README generation, metadata configuration, and verification
---

# GitHub Repository Initialization

## Overview

Automate the complete workflow for pushing a new local git repository to GitHub with intelligent defaults and configuration. This skill handles repository creation, README.md auto-generation, About section configuration, and success verification in a single unified process.

**Core principle:** One command replaces manual multi-step workflows involving gh CLI, file creation, and configuration.

---

## When to Use

**Triggering conditions:**
- Have a local git repository (initialized but not pushed)
- Want to push to GitHub with professional defaults
- Need automatic README.md generation with project metadata
- Want to configure repository About section automatically
- Working with PPsteven or similar GitHub accounts

**When NOT to use:**
- Repository already exists on GitHub
- Want fine-grained control over every step (use gh CLI directly)
- README needs complex custom structure
- Repository requires private/organizational setup beyond basics

---

## Core Workflow

```
Local Git Repo
    ↓
Verify Prerequisites (gh auth, git, jq)
    ↓
Collect Project Metadata (name, description, topics, homepage)
    ↓
Generate README.md (if not exists)
    ↓
Create GitHub Repository (gh repo create)
    ↓
Configure About Section (description, topics, homepage)
    ↓
Verify Success (remote check, branch tracking)
    ↓
Display Summary & URLs
```

---

## Prerequisites Check

**Required tools:**
- `gh` CLI (GitHub CLI v2.0+)
- `git` (any modern version)
- `jq` (JSON processor, used for API responses)

**Required state:**
- GitHub account authenticated with `gh auth login`
- Local git repository initialized with at least one commit
- Current directory is the repository root

**Check status:**
```bash
gh auth status          # Verify authentication
git log -1 --oneline    # Verify git repository
which jq                # Verify jq installed
```

If any check fails, the skill should exit with clear error messaging.

---

## Metadata Collection

Gather project information to populate README and repository configuration:

**Essential metadata:**
- Repository name (from directory name or user input)
- Description (1-2 sentence project summary)
- Topics (3-5 tags: language, purpose, category)
- Homepage URL (optional: project website, docs, etc.)
- Visibility (public or private)

**Collection strategy:**
- Use sensible defaults from directory name
- Ask for confirmation before proceeding
- Validate inputs (no special characters in name, topics < 30 chars each)
- Allow quick entry: `-n repo-name -d "description" -t tag1,tag2`

---

## README.md Auto-Generation

Generate professional README.md with:

**Standard sections:**
1. **Title** - Repository name from metadata
2. **Description** - Project purpose (2-3 sentences)
3. **Features** - Key capabilities (bulleted list)
4. **Installation** - Setup instructions (language-specific)
5. **Usage** - Quick start example
6. **Configuration** - How to configure (if applicable)
7. **Testing** - How to run tests (if applicable)
8. **Contributing** - Contribution guidelines
9. **License** - License declaration
10. **Links** - Homepage, issues, discussions

**Adaptive generation:**
- Detect project type from files (.ts/.tsx → TypeScript, .py → Python, etc.)
- Include language-specific installation/usage examples
- Add build/run commands based on package managers found
- Reference existing test files if present

**Respect existing files:**
- If README.md already exists, don't overwrite (skip generation)
- If other docs exist (CONTRIBUTING.md, CHANGELOG.md), reference them

---

## GitHub Repository Creation

Use `gh repo create` with intelligent defaults:

```bash
gh repo create <repo-name> \
  --description "<description>" \
  --public|--private \
  --source=. \
  --remote=origin \
  --push
```

**Configuration:**
- `--public` by default (can be overridden to `--private`)
- `--source=.` uses current directory as source
- `--push` automatically pushes all local commits
- Sets `origin` as remote and tracks `main` branch

**Error handling:**
- Repository name conflicts (already exists)
- Authentication failures (not logged in)
- Network errors during creation
- Git permissions issues

---

## About Section Configuration

Configure GitHub's repository About section automatically:

**Available fields:**
- Description (max 200 chars)
- Website/Homepage URL
- Topics (up to 30, comma-separated)
- Visibility (shown in settings)

**Configuration method:**
```bash
gh repo edit <owner>/<repo> \
  --description "<text>" \
  --homepage "<url>"
```

**Topics setup** (if GitHub API supports):
```bash
# Using gh API for topics (if available in gh version)
gh api repos/<owner>/<repo> -X PUT -f topics='["topic1","topic2"]'
```

**Fallback:** If API method fails, provide manual configuration link

---

## Success Verification

After push completes, verify all operations succeeded:

**Verification checks:**
1. Remote repository exists (`git remote -v` shows origin)
2. Branch tracking configured (`git branch -vv`)
3. GitHub page is accessible (`gh repo view --web` or HTTP request)
4. README.md visible on repository main page
5. About section populated correctly

**Output summary:**
```
✓ Repository created: https://github.com/<owner>/<repo>
✓ Code pushed: main branch with X commits
✓ About section configured
✓ README generated with Y sections
✓ Subscribe/watch at: [URL]
```

---

## Quick Reference

**Installation command:**
```bash
source <(curl -s https://example.com/github-repo-init.sh)
```

**Usage variants:**

Interactive mode (asks for everything):
```bash
github-repo-init
```

Quick mode (provide all details):
```bash
github-repo-init \
  -n my-project \
  -d "Brief project description" \
  -t "javascript,nodejs,automation" \
  -p public
```

Minimal mode (uses directory name and defaults):
```bash
github-repo-init --auto
```

**Common tasks:**

Create public repo with auto README:
```bash
github-repo-init --auto --public
```

Create private repo with custom description:
```bash
github-repo-init -n my-lib -d "Internal library" -p private
```

Push with homepage URL:
```bash
github-repo-init -n project -d "My project" -H https://myproject.dev
```

---

## Implementation Checklist

**File structure:**
- `~/.claude/skills/github-repo-init/SKILL.md` (this file)
- `~/.claude/skills/github-repo-init/github-repo-init.sh` (main script)

**Script responsibilities:**

**Phase 1: Validation**
- [ ] Check gh authentication
- [ ] Verify git repository exists
- [ ] Confirm at least one commit
- [ ] Check required tools (jq, curl)

**Phase 2: Metadata Collection**
- [ ] Parse command-line arguments
- [ ] Prompt for missing information
- [ ] Validate inputs
- [ ] Show confirmation summary

**Phase 3: File Generation**
- [ ] Generate README.md (skip if exists)
- [ ] Stage generated files
- [ ] Create initial commit if needed

**Phase 4: Repository Creation**
- [ ] Create GitHub repository
- [ ] Add remote and push
- [ ] Configure branch tracking
- [ ] Handle creation errors

**Phase 5: Configuration**
- [ ] Set description
- [ ] Set homepage URL
- [ ] Configure topics
- [ ] Add GitHub Actions badges (optional)

**Phase 6: Verification**
- [ ] Check remote repository exists
- [ ] Verify branch tracking
- [ ] Confirm README visible
- [ ] Validate About section

**Phase 7: Summary**
- [ ] Display success message
- [ ] Show repository URL
- [ ] Provide next steps
- [ ] Display important links

---

## Error Handling

| Error | Symptom | Recovery |
|-------|---------|----------|
| Not authenticated | `gh auth status` fails | Run `gh auth login` |
| No git repository | `git log` returns nothing | Initialize: `git init && git add . && git commit -m "initial"` |
| Repository exists | `Repository already exists` error | Choose different name or use existing repo |
| Network error | Timeout during push | Check connection, retry with `git push -u origin main` |
| Missing metadata | Empty description or topics | Prompt user again, validate before proceeding |
| jq not installed | `jq: command not found` | Install: `brew install jq` |
| Invalid topics | Topics with invalid chars | Filter/validate before API call |

---

## Common Mistakes

**❌ Skipping authentication check**
- Problem: Proceeds to create repo then fails
- Fix: Always check `gh auth status` first

**❌ Using existing README without checking**
- Problem: Overwrites custom README with generated one
- Fix: Check if README exists before generation

**❌ Not validating metadata inputs**
- Problem: Creates repository with invalid topics/description
- Fix: Validate each field before API calls

**❌ Assuming successful push without verification**
- Problem: Shows success but repository is empty
- Fix: Always run verification checks

**❌ Hardcoding paths or usernames**
- Problem: Fails for different users or systems
- Fix: Use `$(whoami)` and dynamic paths

---

## Example Output

```
🚀 GitHub Repository Initialization
═════════════════════════════════════════════════════

📋 Metadata Summary:
  Repository: my-awesome-project
  Description: A blazing-fast utility for automating Git workflows
  Topics: automation, git, utility
  Visibility: Public
  Homepage: https://github.com/PPsteven/my-awesome-project

✓ Phase 1: Prerequisites verified
  ✓ GitHub authenticated as PPsteven
  ✓ Git repository found with 5 commits
  ✓ Required tools available (gh, git, jq)

✓ Phase 2: README.md generated
  ✓ Created with 8 sections
  ✓ Includes installation, usage, contributing
  ✓ Staged for commit

✓ Phase 3: Repository created on GitHub
  ✓ https://github.com/PPsteven/my-awesome-project
  ✓ Set to Public
  ✓ All 5 commits pushed

✓ Phase 4: Configuration applied
  ✓ Description updated
  ✓ Topics: automation, git, utility
  ✓ Homepage configured

✓ Phase 5: Verification complete
  ✓ Remote repository accessible
  ✓ Branch tracking configured
  ✓ README visible on main page
  ✓ About section populated

═════════════════════════════════════════════════════
✅ Success! Your repository is ready.

📍 Repository: https://github.com/PPsteven/my-awesome-project
📖 README: https://github.com/PPsteven/my-awesome-project#readme
⭐ Star & Watch: https://github.com/PPsteven/my-awesome-project

Next steps:
  1. Visit the repository to verify everything looks good
  2. Share with your team or community
  3. Set up CI/CD with GitHub Actions (optional)
```

---

## Integration Notes

**Pairs with:**
- **gh CLI** - GitHub command-line interface for repository management
- **git** - Local version control operations

**Complements:**
- **github-actions-setup** - CI/CD pipeline automation (future skill)
- **readme-template-picker** - Advanced README customization (future skill)

**Alternative approaches:**
- Manual `gh repo create` - requires separate README and About configuration
- GitHub web UI - slow and error-prone for repetitive setup
- GitHub API directly - requires authentication token management

This skill automates and standardizes the workflow that would otherwise require 5+ separate commands.
