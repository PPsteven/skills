#!/bin/bash
# github-repo-init.sh - Initialize and push a local git repository to GitHub
# Usage: github-repo-init [OPTIONS]
# Options:
#   -n, --name NAME              Repository name
#   -d, --description DESC       Project description
#   -t, --topics TOPICS          Comma-separated topics (tag1,tag2,tag3)
#   -H, --homepage URL           Homepage URL
#   -p, --private                Create private repository (default: public)
#   --auto                       Use defaults (directory name as repo name)
#   -h, --help                   Show this help message

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Defaults
REPO_NAME=""
REPO_DESC=""
REPO_TOPICS=""
REPO_HOMEPAGE=""
REPO_PRIVATE=false
AUTO_MODE=false

# Functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

log_section() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
}

show_help() {
    cat << EOF
Usage: github-repo-init [OPTIONS]

Initialize and push a local git repository to GitHub with automatic README
generation and About section configuration.

OPTIONS:
    -n, --name NAME              Repository name (defaults to directory name)
    -d, --description DESC       Project description (max 200 chars)
    -t, --topics TOPICS          Comma-separated topics (tag1,tag2,tag3)
    -H, --homepage URL           Homepage URL
    -p, --private                Create private repository (default: public)
    --auto                       Use defaults (skip prompts)
    -h, --help                   Show this help message

EXAMPLES:
    # Interactive mode (asks for everything)
    github-repo-init

    # Quick mode with all options
    github-repo-init -n my-project -d "My awesome project" -t "javascript,nodejs"

    # Auto mode (uses directory name, skips prompts)
    github-repo-init --auto

    # With private repo and homepage
    github-repo-init -p -H https://myproject.dev

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--name)
            REPO_NAME="$2"
            shift 2
            ;;
        -d|--description)
            REPO_DESC="$2"
            shift 2
            ;;
        -t|--topics)
            REPO_TOPICS="$2"
            shift 2
            ;;
        -H|--homepage)
            REPO_HOMEPAGE="$2"
            shift 2
            ;;
        -p|--private)
            REPO_PRIVATE=true
            shift
            ;;
        --auto)
            AUTO_MODE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# ============================================================================
# Phase 1: Validation
# ============================================================================

log_section "Phase 1: Validating Prerequisites"

# Check gh authentication
if ! gh auth status > /dev/null 2>&1; then
    log_error "GitHub authentication failed"
    echo "Run 'gh auth login' to authenticate with GitHub"
    exit 1
fi

# Get GitHub username from API
GH_USER=$(gh api user --jq '.login' 2>/dev/null)
if [ -z "$GH_USER" ] || [ "$GH_USER" = "null" ]; then
    log_error "Could not retrieve GitHub username"
    exit 1
fi
log_success "GitHub authenticated as $GH_USER"

# Check git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log_error "Not a git repository"
    echo "Initialize with: git init && git add . && git commit -m 'initial'"
    exit 1
fi
log_success "Git repository found"

# Check for at least one commit
if ! git log -1 --oneline > /dev/null 2>&1; then
    log_error "No commits found in repository"
    echo "Create initial commit with: git add . && git commit -m 'initial'"
    exit 1
fi
COMMIT_COUNT=$(git rev-list --count HEAD)
log_success "Git repository has $COMMIT_COUNT commit(s)"

# Check required tools
for tool in jq curl; do
    if ! command -v $tool &> /dev/null; then
        log_error "$tool is not installed"
        exit 1
    fi
done
log_success "Required tools available (jq, curl)"

# ============================================================================
# Phase 2: Metadata Collection
# ============================================================================

log_section "Phase 2: Collecting Project Metadata"

# Get repository name from directory if not provided
if [ -z "$REPO_NAME" ]; then
    REPO_NAME=$(basename "$(pwd)")
fi

# In auto mode, skip prompts
if [ "$AUTO_MODE" = true ]; then
    log_success "Using auto mode with defaults"
    [ -z "$REPO_DESC" ] && REPO_DESC="A new repository"
    [ -z "$REPO_TOPICS" ] && REPO_TOPICS="project"
else
    # Interactive mode
    read -p "Repository name [$REPO_NAME]: " input
    [ -n "$input" ] && REPO_NAME="$input"

    read -p "Description: " input
    [ -n "$input" ] && REPO_DESC="$input"

    read -p "Topics (comma-separated): " input
    [ -n "$input" ] && REPO_TOPICS="$input"

    read -p "Homepage URL (optional): " input
    [ -n "$input" ] && REPO_HOMEPAGE="$input"

    read -p "Create as private repository? (y/N): " input
    [[ "$input" =~ ^[Yy]$ ]] && REPO_PRIVATE=true
fi

# Validate repository name
if [[ ! "$REPO_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    log_error "Invalid repository name: $REPO_NAME"
    echo "Repository names can only contain letters, numbers, hyphens, and underscores"
    exit 1
fi

log_success "Repository name: $REPO_NAME"
log_success "Description: ${REPO_DESC:0:60}..."
log_success "Topics: $REPO_TOPICS"
[ -n "$REPO_HOMEPAGE" ] && log_success "Homepage: $REPO_HOMEPAGE"
log_success "Visibility: $([ "$REPO_PRIVATE" = true ] && echo "Private" || echo "Public")"

# ============================================================================
# Phase 3: README Generation
# ============================================================================

log_section "Phase 3: Generating README.md"

if [ -f "README.md" ]; then
    log_info "README.md already exists, skipping generation"
else
    cat > README.md << EOF
# $REPO_NAME

$REPO_DESC

## Features

- Easy to use
- Well documented
- Actively maintained

## Installation

\`\`\`bash
# Installation instructions here
\`\`\`

## Usage

\`\`\`bash
# Usage examples here
\`\`\`

## Configuration

Create a configuration file or set environment variables:

\`\`\`bash
# Configuration details here
\`\`\`

## Testing

Run the test suite:

\`\`\`bash
# Test command here
\`\`\`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Links

- [Issues](https://github.com/$GH_USER/$REPO_NAME/issues)
- [Discussions](https://github.com/$GH_USER/$REPO_NAME/discussions)
EOF

    git add README.md
    if git status --porcelain | grep -q README.md; then
        if git diff --cached --name-only | grep -q README.md; then
            git commit -m "docs: add auto-generated README.md" 2>/dev/null || true
        fi
    fi
    log_success "README.md generated and committed"
fi

# ============================================================================
# Phase 4: Repository Creation
# ============================================================================

log_section "Phase 4: Creating GitHub Repository"

VISIBILITY_FLAG=$([ "$REPO_PRIVATE" = true ] && echo "--private" || echo "--public")

if gh repo create "$REPO_NAME" \
    --description "$REPO_DESC" \
    $VISIBILITY_FLAG \
    --source=. \
    --remote=origin \
    --push 2>/dev/null; then
    log_success "Repository created and code pushed"
    REPO_URL="https://github.com/$GH_USER/$REPO_NAME"
else
    log_error "Failed to create repository"
    exit 1
fi

# ============================================================================
# Phase 5: Configure About Section
# ============================================================================

log_section "Phase 5: Configuring Repository About Section"

# Set description and homepage using gh repo edit
if gh repo edit "$REPO_NAME" \
    --description "$REPO_DESC" \
    ${REPO_HOMEPAGE:+--homepage "$REPO_HOMEPAGE"} \
    2>/dev/null; then
    log_success "Repository metadata updated"
else
    log_error "Warning: Could not update repository metadata with gh repo edit"
fi

# Configure topics using GitHub API
if [ -n "$REPO_TOPICS" ]; then
    # Convert comma-separated topics to JSON array using jq
    TOPICS_JSON=$(echo "$REPO_TOPICS" | jq -R 'split(",") | map(gsub("^\\s+|\\s+$";"")) | unique')

    if gh api "repos/$GH_USER/$REPO_NAME" \
        --input - \
        -X PUT \
        <<< "{\"topics\": $TOPICS_JSON}" \
        > /dev/null 2>&1; then
        log_success "Topics configured: $REPO_TOPICS"
    else
        log_info "Could not set topics via API (this is optional)"
    fi
fi

# ============================================================================
# Phase 6: Verification
# ============================================================================

log_section "Phase 6: Verifying Success"

# Check remote
if git remote -v | grep -q "origin"; then
    log_success "Remote repository configured"
else
    log_error "Warning: Remote repository not properly configured"
fi

# Check branch tracking
if git branch -vv | grep -q "origin/main\|origin/master"; then
    log_success "Branch tracking configured"
else
    log_error "Warning: Branch tracking may not be configured"
fi

# Check repository is accessible
REPO_CHECK=$(curl -s -o /dev/null -w "%{http_code}" "$REPO_URL")
if [ "$REPO_CHECK" = "200" ]; then
    log_success "Repository is accessible online"
else
    log_info "Repository may still be initializing, check again in a moment"
fi

# ============================================================================
# Phase 7: Summary
# ============================================================================

log_section "Success! Repository is Ready"

echo ""
echo -e "${GREEN}📍 Repository:${NC} $REPO_URL"
echo -e "${GREEN}📖 README:${NC} $REPO_URL#readme"
if [ "$REPO_PRIVATE" = false ]; then
    echo -e "${GREEN}⭐ Star & Watch:${NC} $REPO_URL"
fi
echo ""
echo "Next steps:"
echo "  1. Visit the repository to verify everything looks good"
echo "  2. Share with your team or community"
echo "  3. Set up CI/CD with GitHub Actions (optional)"
echo ""
