---
name: komplai-insights
description: Generate LinkedIn post topics and insights from client conversation transcripts
---

# Komplai Insights from Client Conversations

Generate LinkedIn post topics and insights from client conversation transcripts.

## Description

This skill analyzes client conversation transcripts stored as Google Docs to extract insights and generate compelling LinkedIn post topics for Komplai. It maintains a running log of processed conversations and an insights document that accumulates learnings over time.

## Prerequisites

- Google Docs MCP server must be configured and running (run `/mcp` to verify connection)
- Conversations stored in `/Users/rishi/Documents/Komplai/Client Conversations/` as `.gdoc` files
- Komplai context file available at `/Users/rishi/Documents/Komplai/Client Conversations/Komplai_Context_Canonical.md`

## Technical Notes & Common Mistakes to Avoid

### Google Docs MCP Connection
- **Always verify MCP is connected** before starting - run `/mcp` to check status
- If connection fails, check `~/.claude/debug/latest` for error logs
- Common issues:
  - `fastmcp` version mismatch: Run `npm update` in `~/mcp-googledocs-server`
  - Missing credentials: Ensure `credentials.json` exists in `~/mcp-googledocs-server/node_modules/@xalia/mcp-googledocs-server/`
  - Expired token: Re-authenticate by running `node -e "require('@xalia/mcp-googledocs-server')"` in the server directory

### Reading .gdoc Files
- `.gdoc` files are JSON pointers, NOT the actual content
- Extract the `doc_id` field from the JSON: `{"doc_id": "1abc123..."}`
- Use `mcp__google-docs__readGoogleDoc` with the `doc_id` to fetch actual content
- Request format as `text` for cleaner output

### Processing Efficiency
- Read multiple .gdoc files in parallel to extract doc_ids
- Batch Google Docs MCP calls (up to 6 in parallel) to speed up retrieval
- Prioritize recent conversations (last 3 months) but include older ones for patterns

## Instructions

When this skill is invoked, follow these steps:

### Step 1: Load Context

1. Read the Komplai context file at `/Users/rishi/Documents/Komplai/Client Conversations/Komplai_Context_Canonical.md`
2. Read the existing insights file at `/Users/rishi/Documents/Komplai/Client Conversations/Komplai_Insights.md` (create if doesn't exist)
3. Read the processing log at `/Users/rishi/Documents/Komplai/Client Conversations/.komplai_processing_log.json` (create if doesn't exist)

### Step 2: Identify Conversations to Analyze

1. Find all `.gdoc` files in `/Users/rishi/Documents/Komplai/Client Conversations/` recursively (India/, US/, Middle East/, Pilot/ subfolders)
2. For each `.gdoc` file, extract the `doc_id` from the JSON content
3. Check the processing log to identify:
   - New conversations (never processed)
   - Updated conversations (modified since last processing)
4. Prioritize newer conversations but also re-scan older ones for fresh perspective

### Step 3: Read Conversations via Google Docs MCP

For each conversation document:
1. Use the `readGoogleDoc` MCP tool with the extracted `doc_id`
2. Request content in plain text or markdown format
3. Store the content for analysis

### Step 4: Extract Insights (Build, Don't Repeat)

**CRITICAL: Review previous insights first.** Before extracting new insights:
1. Read the existing `Komplai_Insights.md` thoroughly
2. Note which pain points, FAQs, and trends have already been documented
3. Focus on NEW angles, deeper evidence, or emerging patterns not yet captured

**When you find a previously documented insight:**
- Don't repeat it verbatim
- Instead, ADD to it: new quotes, stronger evidence, different industry angle
- Note if the insight is strengthening (more prospects mention it) or evolving

**Look for these categories:**

**Pain Points:**
- What NEW problems are prospects describing?
- What frustrations haven't been captured yet?
- Are there industry-specific variations of known pain points?

**Frequently Asked Questions:**
- What NEW questions are prospects asking?
- Are there patterns in HOW questions are phrased that reveal deeper concerns?

**Objections & Hesitations:**
- What NEW concerns are emerging?
- How are objections evolving as AI becomes more mainstream?

**Success Stories & Outcomes:**
- What NEW success metrics are prospects hoping for?
- Are there specific ROI expectations being mentioned?

**Industry Trends:**
- What NEW patterns are emerging across conversations?
- Are there shifts in tech stack preferences, team structures, or priorities?

**Emerging Topics (flag for future focus):**
- Topics mentioned by 2+ prospects that aren't yet a clear pattern
- New use cases or feature requests that keep appearing

### Step 5: Update Insights Document

Append new insights to `/Users/rishi/Documents/Komplai/Client Conversations/Komplai_Insights.md` with:
- Date of analysis
- Source conversations (anonymized - use company type/size, not names)
- Categorized insights
- Notable quotes (anonymized)

### Step 6: Generate LinkedIn Post Topics (Fresh Angles Only)

**Before generating topics:**
1. Review previous `.txt` summary files to see what topics have been generated before
2. Check the processing log to understand which conversations informed previous topics
3. Aim for FRESH angles - don't regenerate the same topics with different words

**Topic freshness strategies:**
- If a pain point was covered before, find a NEW angle (different industry, different persona, contrarian take)
- Combine multiple insights into a single topic for depth
- Look for "second-order" insights - what does a pattern IMPLY about the market?
- Consider timely hooks (end of quarter, audit season, budget planning cycles)

Generate exactly **3 LinkedIn post topic ideas** following this format for each:

```
---
## Topic [N]: [Title]

**Core Insight:**
[The underlying insight from conversations that makes this relevant]

**Suggested Hook/Opening Line:**
[A compelling first line that stops the scroll - can be a question, bold statement, or relatable scenario]

**Key Talking Points:**
- [Point 1]
- [Point 2]
- [Point 3]

**Data Points/Quotes (anonymized):**
- "[Quote or statistic from conversations]"

**Target Audience:**
[CFO / Controller / Business Operator] at [company profile]

**Suggested Post Format:**
[Story / List / Question / Contrarian take / Before-After / Case study teaser]

**Komplai Connection (subtle):**
[How this naturally connects to what Komplai solves - for reference, don't make post too salesy]
---
```

### Step 7: Update Processing Log

Update `/Users/rishi/Documents/Komplai/Client Conversations/.komplai_processing_log.json` with:
- List of processed doc_ids
- Processing timestamps
- Last run date

### Step 8: Save Summary Report

Save the complete summary as a `.txt` file in the Client Conversations folder:
- Filename format: `komplai_insights_YYYY-MM-DD.txt` (using the current date)
- Include:
  - Conversations analyzed (count by region)
  - Key insights discovered
  - All 3 LinkedIn post topics with full details
  - List of files updated

## Style Guidelines

Reference the tone and approach of:
- **CFO Secrets** (cfosecrets.io): "From the trenches, not textbooks" - make complex simple, concise, mix of educational and relatable
- **CFO Office** (cfooffice.io): Direct, no BS, problem-solution framing, evidence-based, actionable

**Post Characteristics:**
- Storytelling + data-driven
- Thought leadership style
- Problem-focused (lead with the pain)
- Case study approach when possible
- Target: CFOs, Controllers, Business Operators at $50M+ ARR SaaS companies (15+ person finance teams)
- Secondary industries: manufacturing, logistics, ecommerce, consumer brands

**Avoid:**
- Generic advice
- Overly promotional content
- Vague claims without backing
- Marketing speak or influencer tone
- Naming competitors negatively

## Output

After running, display:
1. Summary of conversations analyzed (count, new vs. revisited)
2. Key insights discovered this run
3. The 3 LinkedIn post topics with full details
4. Confirmation that log, insights, and summary files were updated

## Files Maintained

| File | Purpose |
|------|---------|
| `Komplai_Insights.md` | Cumulative insights document, updated each run |
| `.komplai_processing_log.json` | Tracks which docs were processed and when |
| `komplai_insights_YYYY-MM-DD.txt` | Summary report for each run, named by date |
| `Komplai_Context_Canonical.md` | Reference for Komplai positioning (read-only) |

## Quality Checklist (Before Completing Run)

Before finalizing, verify:

- [ ] **MCP connected** - Google Docs were successfully read (not just .gdoc JSON files)
- [ ] **New insights added** - At least some insights are genuinely new, not rehashes
- [ ] **Quotes are anonymized** - No company names, individual names, or identifiable details
- [ ] **Topics are fresh** - LinkedIn topics cover different ground from previous runs
- [ ] **Files updated** - All three output files created/updated
- [ ] **Processing log accurate** - Doc IDs logged with correct timestamps

## Iteration & Improvement

After multiple runs, patterns will emerge:
- **Strengthen high-frequency insights** with more evidence and quotes
- **Retire stale insights** that aren't appearing in new conversations
- **Track insight evolution** - how are pain points changing over time?
- **Note seasonal patterns** - do certain topics spike during audit/close seasons?

The goal is a living knowledge base that gets sharper with each run, not a repetitive dump of the same observations.
