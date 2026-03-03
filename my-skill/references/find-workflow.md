# Find Workflow - Enhanced Skill Research

This workflow provides a structured process for discovering, evaluating, and documenting agent skills with comprehensive research and analysis.

## Purpose

When users need to find the best skill for a specific task, this workflow:
- Searches ClawHub for relevant skills
- Compares multiple candidates systematically
- Evaluates pros/cons/risks for each option
- Generates detailed reports
- Archives findings to personal knowledge base

## When to Use This Workflow

Use this workflow when:
- User wants to find the best skill for a specific task
- Need to compare multiple skill options systematically
- Researching skills requires detailed evaluation (pros/cons/risks)
- Results should be documented in personal knowledge base
- User says "深入研究 skills", "对比分析 skills", "find-skill-plus"

## Workflow Steps

### Step 1: Input Target Goal

Ask the user to clarify the target requirement:
- What problem needs to be solved?
- What domain or technology?
- Any specific constraints or preferences?

Example questions:
```
What capability are you looking for?
Domain: (e.g., GitHub automation, data analysis, web scraping)
Specific requirements: (e.g., must support Python, CLI-based)
```

### Step 2: Search with find-skills

Use the find-skills skill or clawhub CLI to search:

```bash
# Search ClawHub
clawhub search <query>

# Or use npx skills
npx skills find <query>
```

Extract results including:
- Skill names
- Repository sources
- Brief descriptions
- Install commands

### Step 3: Identify Top Candidates

From search results, identify the top 3-5 most relevant skills based on:
- Relevance to user's goal
- Popularity/stars
- Recent updates
- Comprehensive descriptions

List candidates for user review:
```
Found 5 relevant skills:
1. owner/repo@skill-name-1 - Description...
2. owner/repo@skill-name-2 - Description...
...

Proceeding to deep analysis of top 3 candidates.
```

### Step 4: Deep Comparative Analysis

For each top candidate, read the SKILL.md file and extract:

#### 4.1 Core Information
- **技术方案** (Technical Approach): How does it work? What tools/APIs does it use?
- **简介** (Overview): What does this skill do? Core functionality?
- **优势** (Advantages): What makes it good? Unique features?
- **劣势** (Disadvantages): Limitations, missing features, complexity?
- **风险** (Risks): Dependencies, maintenance status, compatibility issues?

#### Research Process

For each skill:

```bash
# Install temporarily to read SKILL.md
clawhub get <owner/repo@skill-name> --path /tmp/skill-analysis

# Or if already installed locally
cat ~/.agents/skills/<skill-name>/SKILL.md
```

Analyze SKILL.md for:
- Frontmatter metadata (name, description, context, agent)
- Usage instructions and examples
- Tool/CLI dependencies
- Workflow complexity
- Edge cases and limitations

### Step 5: Generate Comparative Report

Create a markdown report with the following structure:

**CRITICAL: All reports MUST include YAML frontmatter for Obsidian metadata management.**

```markdown
---
create_date: YYYY-MM-DD
update_date: YYYY-MM-DD
tags:
  - skills-research
  - <domain-tag>
  - <technology-tag>
description: Skills 研究报告 - <目标需求简述>
brief: 对比分析了 <N> 个 skills，推荐使用 <recommended-skill>
---

# Skills 研究报告: <目标需求>

**研究日期**: YYYY-MM-DD
**研究目标**: <用户的具体需求>

---

## 候选 Skills 概览

| Skill Name | Source | Stars | Last Update |
|------------|--------|-------|-------------|
| skill-1    | repo-1 | ⭐️123 | 2024-01-15  |
| skill-2    | repo-2 | ⭐️89  | 2024-01-10  |
| skill-3    | repo-3 | ⭐️56  | 2023-12-20  |

---

## Skill 1: <skill-name>

### 简介
<What it does, core purpose>

### 技术方案
<How it works, tools used, architecture>

### 优势
- ✅ Advantage 1
- ✅ Advantage 2
- ✅ Advantage 3

### 劣势
- ❌ Limitation 1
- ❌ Limitation 2

### 风险
- ⚠️ Risk 1 (e.g., unmaintained dependency)
- ⚠️ Risk 2 (e.g., requires paid API)

### 安装命令
\`\`\`bash
clawhub get <owner/repo@skill-name>
\`\`\`

---

## Skill 2: <skill-name>

[Repeat same structure]

---

## Skill 3: <skill-name>

[Repeat same structure]

---

## 综合对比

| 维度 | Skill 1 | Skill 2 | Skill 3 |
|------|---------|---------|---------|
| 易用性 | ⭐️⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️ |
| 功能完整度 | ⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️ |
| 维护状态 | 活跃 | 活跃 | 较旧 |
| 依赖复杂度 | 低 | 中 | 高 |

---

## 推荐结论

**推荐选择**: Skill 1

**理由**:
- <Primary reason>
- <Secondary reason>
- <Additional considerations>

**替代方案**:
- 如果需要 <specific feature>, 考虑 Skill 2
- 如果 <specific constraint>, Skill 3 也可以

---

## 参考链接

- [Skill 1 - ClawHub](https://clawhub.com/...)
- [Skill 2 - ClawHub](https://clawhub.com/...)
- [Skill 3 - ClawHub](https://clawhub.com/...)
```

### Step 6: Archive to Knowledge Base

Save the report to Obsidian vault with proper YAML frontmatter:

```bash
# Generate filename with timestamp
TOPIC="<sanitized-topic-name>"
DATE=$(date +%Y%m%d)
REPORT_FILE="/Users/ppsteven/Documents/obsidian/minions/00.工作区/02.技术研究/Skills研究-${TOPIC}-${DATE}.md"

# Write report with YAML frontmatter
cat > "$REPORT_FILE" << 'EOF'
---
create_date: $(date +%Y-%m-%d)
update_date: $(date +%Y-%m-%d)
tags:
  - skills-research
  - <domain-tag>
  - <technology-tag>
description: Skills 研究报告 - <目标需求简述>
brief: 对比分析了 <N> 个 skills，推荐使用 <recommended-skill>
---

[Generated markdown report content]
EOF

echo "✅ Report saved to: $REPORT_FILE"
```

**YAML Frontmatter Fields:**

- `create_date`: Report creation date (YYYY-MM-DD format)
- `update_date`: Last modification date (initially same as create_date)
- `tags`: Array of relevant tags:
  - Always include `skills-research`
  - Add domain tags (e.g., `github`, `data-analysis`, `automation`)
  - Add technology tags (e.g., `python`, `cli`, `api`)
- `description`: One-line description of the research goal
- `brief`: Executive summary - what was analyzed and what's recommended

**Tag Examples:**

```yaml
# GitHub automation research
tags:
  - skills-research
  - github
  - automation
  - ci-cd

# Data analysis research
tags:
  - skills-research
  - data-analysis
  - python
  - visualization

# Web scraping research
tags:
  - skills-research
  - web-scraping
  - crawler
  - data-extraction
```

Confirm with user:
```
✅ Research report saved to:
/Users/ppsteven/Documents/obsidian/minions/00.工作区/02.技术研究/Skills研究-<topic>-YYYYMMDD.md

Metadata:
- Tags: skills-research, <domain>, <technology>
- Created: YYYY-MM-DD
- Brief: <summary>

Open in Obsidian to review the detailed comparison and recommendations.
```

## Example Usage

### User Request
```
我想找一个处理 GitHub PR review 的 skill，帮我深入研究一下
```

### Agent Response Workflow

**Step 1: Clarify goal**
```
目标确认：
- 功能：自动化 GitHub PR review 流程
- 需求：支持代码质量检查、自动评论、批准流程
- 约束：需要与 gh CLI 集成

开始搜索...
```

**Step 2: Search**
```bash
clawhub search "github pr review"
```

**Step 3: Top candidates**
```
找到 5 个相关 skills，筛选出 top 3：
1. vercel-labs/agent-skills@github-pr-reviewer
2. anthropic/agent-skills@code-review
3. community/gh-review-automation

开始深入分析...
```

**Step 4: Analyze each SKILL.md**
```bash
clawhub get vercel-labs/agent-skills@github-pr-reviewer --path /tmp/analysis-1
cat /tmp/analysis-1/SKILL.md
# Repeat for each candidate
```

**Step 5: Generate report**
```markdown
---
create_date: 2024-01-15
update_date: 2024-01-15
tags:
  - skills-research
  - github
  - pr-review
  - automation
description: Skills 研究报告 - GitHub PR 自动化 review 工具
brief: 对比分析了 3 个 GitHub PR review skills，推荐使用 vercel-labs/agent-skills@github-pr-reviewer
---

# Skills 研究报告: GitHub PR Review

[Create comprehensive markdown with all 5 sections per skill]
```

**Step 6: Save to knowledge base**
```bash
/Users/ppsteven/Documents/obsidian/minions/00.工作区/02.技术研究/Skills研究-GitHub-PR-Review-20240115.md
```

## Important Notes

### Research Quality

- **Be thorough**: Read entire SKILL.md, not just frontmatter
- **Be critical**: Note both strengths and weaknesses
- **Be practical**: Consider real-world usage, not just features

### Report Writing

- **YAML frontmatter is mandatory**: Every report must start with valid YAML metadata
- **Use clear structure**: Follow the template structure strictly
- **Be objective**: Present facts, then give recommendation
- **Include examples**: Show concrete use cases when possible
- **Cite sources**: Link to ClawHub, GitHub repos, SKILL.md files
- **Tag appropriately**: Include domain-specific tags for Obsidian search/filtering

### Knowledge Base Integration

- **YAML frontmatter required**: All reports must include create_date, update_date, tags, description, brief
- **Consistent naming**: Use format `Skills研究-<主题>-<日期>.md`
- **Proper location**: Always save to `00.工作区/02.技术研究/`
- **Verify write**: Confirm file was written successfully before finishing
- **Date format**: Use ISO 8601 (YYYY-MM-DD) for all dates
- **Tags format**: YAML array with meaningful, searchable tags

## Troubleshooting

### Skill not found in search
- Try alternative keywords
- Search directly on clawhub.com
- Check if skill is in local `~/.agents/skills/`

### Cannot read SKILL.md
- Use `clawhub get` to download temporarily
- Check if skill is properly installed
- Verify file path exists

### Report save fails
- Verify Obsidian vault path exists
- Check write permissions
- Create directory if missing: `mkdir -p "<path>"`

---

**Workflow Summary:**
Input Goal → Search → Top 3-5 → Deep Analysis (方案/优劣/风险) → Report → Archive to Obsidian
