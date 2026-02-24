# GitHub Repository Init Skill

## Quick Start

This skill automates the complete workflow for pushing a new local git repository to GitHub.

### Installation

The skill is already installed at:
```
~/.claude/skills/github-repo-init/
```

### Usage

**Interactive mode:**
```bash
/Users/ppsteven/.claude/skills/github-repo-init/github-repo-init.sh
```

**Quick mode (with all details):**
```bash
/Users/ppsteven/.claude/skills/github-repo-init/github-repo-init.sh \
  -n my-project \
  -d "Brief description" \
  -t "tag1,tag2,tag3"
```

**Auto mode (uses defaults):**
```bash
/Users/ppsteven/.claude/skills/github-repo-init/github-repo-init.sh --auto
```

## What It Does

The skill automates these 7 phases:

1. **Phase 1: Validate Prerequisites**
   - Check GitHub authentication
   - Verify git repository exists
   - Ensure at least one commit
   - Verify required tools (jq, curl)

2. **Phase 2: Collect Metadata**
   - Repository name
   - Description
   - Topics (tags)
   - Homepage URL (optional)
   - Visibility (public/private)

3. **Phase 3: Generate README.md**
   - Creates professional README if none exists
   - Includes installation, usage, contributing sections
   - Automatically populated with project metadata

4. **Phase 4: Create GitHub Repository**
   - Uses `gh repo create` to push to GitHub
   - Configures remote and branch tracking
   - Pushes all local commits

5. **Phase 5: Configure About Section**
   - Sets repository description
   - Configures homepage URL
   - Adds topics/tags

6. **Phase 6: Verify Success**
   - Checks remote repository
   - Confirms branch tracking
   - Validates README is visible
   - Verifies About section

7. **Phase 7: Display Summary**
   - Shows repository URL
   - Provides next steps

## Features

✅ Automatic README.md generation  
✅ GitHub About section configuration  
✅ Topics/tags management  
✅ One command replaces 5+ manual steps  
✅ Clear colored output with progress  
✅ Flexible input modes (auto, quick, interactive)  
✅ Comprehensive error handling  
✅ Success verification  

## Requirements

- GitHub account with `gh` CLI authenticated
- Local git repository with at least one commit
- `jq` installed (for JSON processing)
- `curl` installed (for verification)

## Examples

### Example 1: Create a JavaScript project
```bash
cd my-js-app
git init && git add . && git commit -m "initial"
/Users/ppsteven/.claude/skills/github-repo-init/github-repo-init.sh \
  -n my-js-app \
  -d "A React application" \
  -t "javascript,react,frontend"
```

### Example 2: Create a Python library
```bash
cd my-python-lib
git init && git add . && git commit -m "initial"
/Users/ppsteven/.claude/skills/github-repo-init/github-repo-init.sh \
  -n my-python-lib \
  -d "Utility library for data processing" \
  -t "python,utilities,data"
```

### Example 3: Use auto mode
```bash
cd my-project
/Users/ppsteven/.claude/skills/github-repo-init/github-repo-init.sh --auto
```

## File Structure

```
~/.claude/skills/github-repo-init/
├── SKILL.md                  # Complete skill reference
├── github-repo-init.sh       # Main implementation script
└── README.md                 # This file
```

## Support

For issues or improvements, refer to SKILL.md for the complete skill reference.
