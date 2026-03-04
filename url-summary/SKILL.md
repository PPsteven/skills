---
name: url-summary
description: Save web articles to personal knowledge base with intelligent summaries. Use when user provides a URL and wants to save, summarize, or archive web content to their notes. Triggers on phrases like "保存这个链接", "总结这篇文章", "save this article to my notes", "summarize this URL", or whenever a user shares a URL and mentions their knowledge base, Obsidian, or note-taking.
---

# URL Summary - Web Content to Knowledge Base

This skill fetches web articles, generates intelligent summaries, and saves them to your personal knowledge base with proper formatting and metadata.

## When to Use This Skill

Use this skill when the user:
- Provides a URL and wants it summarized or saved
- Says "保存这个链接到我的知识库" or "save this article to my notes"
- Mentions summarizing web content for later reference
- Wants to archive articles, documentation, or blog posts
- Needs to extract key information from online content

## Workflow

### Step 1: Identify Knowledge Base Location

**Check context first**: Look in the current conversation for mentions of:
- Personal knowledge base path
- Obsidian vault location
- Note directory or documentation folder
- Any previous references to where notes are stored

**If location is found in context**: Use that path directly.

**If NOT found in context**: Ask the user:
```
I'll help you save this article to your knowledge base. Where would you like me to save it?

Please provide the directory path (e.g., ~/Documents/obsidian/articles/ or ~/notes/)
```

Wait for their response before proceeding.

### Step 2: Fetch Article Content

**Priority order** for fetching content:

**1. Browser tool - Independent browser mode (PREFERRED)**:
Always try browser first for best compatibility with modern websites:

```
1. Open URL with browser tool using profile="openclaw":
   browser(action="open", profile="openclaw", targetUrl="<url>")

2. Wait 2-3 seconds for page to load:
   exec("sleep 3")

3. Capture content with snapshot:
   browser(action="snapshot", profile="openclaw", targetId="<targetId>")

4. Close browser when done:
   browser(action="close", profile="openclaw", targetId="<targetId>")
```

**Why browser mode is preferred:**
- `profile="openclaw"` runs a standalone headless browser - no Chrome extension needed
- Handles JavaScript rendering (WeChat, social media, modern SPAs)
- Works with sites that block web scrapers
- Most reliable method for content extraction

**2. WebFetch tool (fallback)**:
If browser is unavailable or fails, try WebFetch:
```
Use web_fetch tool with the URL to extract readable content.
```

**3. curl/wget (last resort)**:
If both browser and WebFetch fail, try curl:
```bash
curl -L -A "Mozilla/5.0" "<url>" > /tmp/article_content.html
```
Then extract text content from the HTML.

**Error handling**: If all methods fail, inform the user and ask if they'd like to paste the content manually.

### Step 3: Determine Content Type

Analyze the fetched content to determine the article type:

- **Technical content**: Contains code examples, technical documentation, API references, architecture diagrams, system design
- **Research/Academic**: Contains abstract, methodology, citations, academic language, paper structure
- **General article**: Blog posts, news articles, opinion pieces, tutorials, general content

### Step 4: Select Appropriate Template

Based on content type, use the corresponding template:

| Content Type | Template File | When to Use |
|--------------|---------------|-------------|
| General article | `references/default-template.md` | Default for most web content |
| Technical content | `references/technical-template.md` | Documentation, tutorials, technical blogs |
| Research paper | `references/research-template.md` | Academic papers, research articles |

Read the appropriate template file and follow its structure.

### Step 5: Generate Summary

Follow the selected template to create a structured summary. Key principles:

1. **YAML frontmatter (REQUIRED)**: Every generated document MUST start with YAML frontmatter containing:
   ```yaml
   ---
   title: <article title>
   author: <author name or source>
   date: <publication date in YYYY-MM-DD format>
   source: <original URL>
   tags: [<relevant>, <topic>, <tags>]
   created: <YYYY-MM-DD current date>
   ---
   ```
   - **title**: Extract from article or page title
   - **author**: Extract from article metadata, or use source name (e.g., "扬子晚报")
   - **date**: Publication date in YYYY-MM-DD format (if available, else use current date)
   - **source**: Full original URL (critical for reference)
   - **tags**: 3-5 relevant topic tags (e.g., [新闻, 银行, 金融, 系统故障])
   - **created**: Current date in YYYY-MM-DD format (when saved to knowledge base)

2. **Create executive summary**: 1-3 paragraphs capturing the essence

3. **Extract key points**: Bullet list of main takeaways

4. **Preserve important details**:
   - For technical content: Include code snippets, diagrams (as Mermaid), architecture notes
   - For research: Include methodology, findings, conclusions
   - For general: Include interesting insights, quotes, actionable advice

### Step 6: Generate Filename

Create filename using format: `YYYY-MM-DD-sanitized-title.md`

**Steps**:
1. Get current date in YYYY-MM-DD format
2. Take article title and sanitize:
   - Convert to lowercase
   - Replace spaces with hyphens
   - Remove special characters except hyphens and underscores
   - Limit to 50 characters
3. Combine: `2026-03-04-how-to-build-llm-agents.md`

### Step 7: Save to Knowledge Base

Write the formatted summary to the knowledge base directory:

```
<knowledge_base_path>/<YYYY-MM-DD-sanitized-title.md>
```

Confirm with the user:
```
✓ Article saved to: <full_path>
📄 <article_title>
🔗 <original_url>
📝 <word_count> words | <section_count> sections
```

## Template Reference

Templates are stored in `references/` and provide structure for different content types. Each template defines:

- YAML frontmatter format (title, author, date, source, tags)
- Section structure (summary, key points, detailed notes)
- Special elements (code blocks, diagrams, citations)

Templates can be extended over time. If you encounter content that doesn't fit existing templates, use the default template and suggest a new template type to the user.

## Error Handling

**Browser fetch fails**:
```
Browser couldn't load the page. Trying WebFetch as fallback...
```
→ Automatically switch to web_fetch tool

**Content extraction fails (all methods)**:
```
I tried multiple methods but couldn't extract readable content. The page might be:
- Behind a login or paywall
- Requires user interaction (captcha, cookies)
- Not article content (e.g., video, image gallery)

Would you like to paste the content manually, or try a different URL?
```

**Knowledge base path not writable**:
```
I don't have permission to write to: <path>

Please check:
1. The directory exists
2. You have write permissions
3. The path is correct
```

## Examples

**Example 1: WeChat article**
```
User: "保存这个链接到我的知识库: https://mp.weixin.qq.com/s/xxxxx"
Context: Knowledge base at ~/Documents/obsidian/minions/

Action:
1. Knowledge base found: ~/Documents/obsidian/minions/00.工作区/02.技术研究/
2. Open URL with browser (profile="openclaw")
3. Wait 3 seconds for page load
4. Snapshot to extract full content
5. Close browser
6. Detect content type (general news article)
7. Use default-template.md
8. Generate summary with YAML frontmatter
9. Save as: ~/Documents/obsidian/minions/00.工作区/02.技术研究/2026-03-04-article-title.md
```

**Example 2: Technical article**
```
User: "保存这个链接到我的 Obsidian: https://example.com/how-llm-agents-work"
Context: Obsidian vault at ~/Documents/obsidian/

Action:
1. Knowledge base found: ~/Documents/obsidian/
2. Fetch article with browser (profile="openclaw") - most reliable method
3. Detect technical content (contains code, architecture)
4. Use technical-template.md
5. Generate summary with Mermaid diagrams
6. Save as: ~/Documents/obsidian/2026-03-04-how-llm-agents-work.md
```

**Example 3: General article, no context**
```
User: "Summarize this and save to my notes: https://blog.example.com/productivity-tips"
Context: No knowledge base mentioned

Action:
1. No knowledge base in context - ask user for location
2. User responds: "~/notes/articles/"
3. Fetch article with browser (profile="openclaw")
4. Detect general content
5. Use default-template.md
6. Save as: ~/notes/articles/2026-03-04-productivity-tips.md
```

**Example 4: Batch processing**
```
User: "Save all these to my research folder at ~/Documents/research/:
- https://arxiv.org/paper1
- https://arxiv.org/paper2
- https://example.com/article3"

Action:
1. Knowledge base specified: ~/Documents/research/
2. Process each URL sequentially
3. Detect research papers for first two (use research-template.md)
4. Detect general article for third (use default-template.md)
5. Save all three with appropriate formatting
```

## Important Notes

- **YAML frontmatter is mandatory** - Every document MUST include complete YAML frontmatter with title, author, date, source, tags, and created fields
- **Always preserve the source URL** in the metadata - it's crucial for verification and follow-up
- **Use YYYY-MM-DD date format** consistently in both `date` and `created` fields
- **Browser mode is default**: Always try `profile="openclaw"` browser first for best compatibility
- **Don't over-summarize technical content** - keep important details, code, and diagrams
- **Ask before overwriting** - if a file with the same name exists, ask the user first
- **Handle non-English content** - preserve the original language in summaries
- **Respect rate limits** - if processing multiple URLs, add small delays between requests
- **Clean up browser sessions** - always close browser tabs when done to free resources

## Related Skills

- **obsidian**: For advanced Obsidian vault operations (linking, tagging, templates)
- **deepwiki**: For fetching repository documentation when URL is a GitHub repo

---

**Extending Templates**: Users can request new template types for specific content categories (e.g., podcast transcripts, video summaries, tweet threads). When this happens, suggest creating a new template file and offer to add it to the references/ directory.