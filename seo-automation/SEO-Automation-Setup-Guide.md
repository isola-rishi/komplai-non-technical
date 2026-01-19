# SEO Content Automation Setup Guide

Complete guide to set up your automated SEO content pipeline: Keywords → Claude AI → Google Sheets → WordPress

## Overview

**Workflow**: You input keywords → Claude generates SEO content → Stored in Google Sheets → Auto-posts to WordPress

## Step 1: Create Google Sheet

1. Create a new Google Sheet
2. Add these column headers in Row 1:

| A | B | C | D | E | F | G | H | I | J | K | L |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Keyword | Secondary Keywords | Search Intent | Target Word Count | Generated Title | H1 | H2s | Content | Meta Description | Status | WordPress URL | Backlinks Added |

### Column Explanations:
- **Keyword**: Your primary target keyword/phrase (you fill this)
- **Secondary Keywords**: Additional related keywords to incorporate (you fill this, optional - comma-separated)
- **Search Intent**: informational/transactional/navigational (you fill this, optional)
- **Target Word Count**: Desired article length (you fill this, defaults to 1500)
- **Generated Title**: Auto-filled by script
- **H1**: Auto-filled by script
- **H2s**: Auto-filled by script (line-separated)
- **Content**: Full HTML content (auto-filled)
- **Meta Description**: SEO meta description (auto-filled)
- **Status**: Tracks progress (auto-updated)
- **WordPress URL**: Link to published post (auto-filled)
- **Backlinks Added**: Shows internal linking status (auto-filled)

## Step 2: Set Up Google Apps Script

1. In your Google Sheet, go to **Extensions → Apps Script**
2. Delete any existing code
3. Copy the entire content from `seo-automation-script.gs`
4. Paste into the script editor
5. Click **Save** (disk icon)
6. Name your project: "SEO Content Automation"

## Step 3: Get Claude API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-...`)
6. **Important**: Store this securely - you won't see it again

## Step 4: Get WordPress Application Password

1. Log into your WordPress site
2. Go to **Users → Profile**
3. Scroll to **Application Passwords** section
4. Enter name: "SEO Automation"
5. Click **Add New Application Password**
6. Copy the generated password (format: `xxxx xxxx xxxx xxxx xxxx xxxx`)

**Note**: If you don't see Application Passwords:
- Make sure you're using HTTPS
- Update WordPress to latest version
- Check if your hosting blocks this feature

## Step 5: Configure Script Properties

1. In Apps Script editor, click **Project Settings** (gear icon on left)
2. Scroll to **Script Properties**
3. Click **Add script property** and add these 4 properties:

| Property | Value | Example |
|----------|-------|---------|
| `ANTHROPIC_API_KEY` | Your Claude API key | `sk-ant-api03-xxx...` |
| `WORDPRESS_SITE_URL` | Your site URL (no trailing slash) | `https://yoursite.com` |
| `WORDPRESS_USERNAME` | Your WP username | `admin` |
| `WORDPRESS_APP_PASSWORD` | Application password | `xxxx xxxx xxxx xxxx xxxx xxxx` |

4. Click **Save script properties**

## Step 6: Authorize & Test

1. In Apps Script editor, select `setup` from the function dropdown
2. Click **Run**
3. Grant permissions when prompted:
   - Click **Review Permissions**
   - Select your Google account
   - Click **Advanced** → **Go to [Project Name] (unsafe)**
   - Click **Allow**

4. Go back to your Google Sheet
5. Refresh the page
6. You should see new menu: **SEO Automation**
7. Click **SEO Automation → Setup & Test Connection**

## Step 7: Usage

### Generate Content

1. Fill in keywords in your sheet:

| Keyword | Secondary Keywords | Search Intent | Target Word Count |
|---------|-------------------|---------------|-------------------|
| best running shoes for beginners | running shoes, beginner runners, athletic footwear | informational | 2000 |
| how to tie shoelaces properly | shoe lacing, tying techniques | informational | 1200 |
| buy nike air max online | nike shoes, air max collection | transactional | 1500 |

2. Select the rows you want to generate (or leave blank for all pending)
3. Click **SEO Automation → Generate Content for Selected Rows**
4. Wait for generation (30-60 seconds per article)
5. Content will populate automatically

### Post to WordPress

1. After content is generated (Status = "Generated")
2. Select rows to post
3. Click **SEO Automation → Post Selected to WordPress**
4. Articles will be created as **drafts** in WordPress
5. WordPress URL will appear in column J

### Batch Operations

- **Generate All Pending**: Generates content for all rows with "Pending" status
- **Post All Generated to WordPress**: Posts all rows with "Generated" status

## Step 8: Customize (Optional)

### Change Post Status to Auto-Publish

In `seo-automation-script.gs`, line ~280:
```javascript
status: 'draft', // Change to 'publish' to auto-publish
```

### Adjust Claude Model

Line ~163:
```javascript
model: 'claude-sonnet-4-5-20250929', // Change to claude-opus-4-5 for higher quality
```

### Add Custom Prompting

Modify the `prompt` variable in `generateSEOContent()` function (starting line ~145)

## Content Features (Updated December 2025)

The automation now generates **premium, data-rich content** with:

### Sophisticated Layout
- Clear visual hierarchy with generous spacing between sections
- Numbered H2 headings for better scannability
- Short paragraphs (2-3 sentences) for easy scanning
- Professional gradient callout boxes for key information

### Data-Driven Content
- **Key Statistics callout box** prominently featured early in each article
- Statistics, percentages, and research findings from 2025 or late 2024
- Inline source citations with footnote format
- Dedicated "Sources & References" section at the end
- All content automatically reflects the current year (2025)

### Visual Elements
- WordPress Gutenberg-formatted hero images from Unsplash
- Related articles section (text links without thumbnails)
- Duplicate image prevention across posts
- Gradient-styled statistics boxes with shadow effects

### SEO Optimization
- Numbered H2 headings (e.g., "1. Introduction", "2. Key Benefits")
- Justified text alignment for professional appearance
- Frequent bullet points for readability
- Internal linking opportunities marked as [INTERNAL: anchor text]
- Meta descriptions optimized for UK English
- Current year references throughout (2025)

## Pricing Estimates

### Claude API Costs
- Sonnet 4.5: ~$0.10-0.30 per 1500-word article
- Opus 4.5: ~$0.50-1.00 per article (higher quality)

### Tips to Reduce Costs
- Use Sonnet for most content (current default)
- Reserve Opus for high-value cornerstone content
- Batch generate during off-peak times

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
- Check Script Properties are saved correctly
- Make sure key starts with `sk-ant-`

### "WordPress API error"
- Verify site URL has no trailing slash
- Confirm Application Password is correct (with spaces removed or included as copied)
- Test WordPress REST API: `yoursite.com/wp-json/wp/v2/posts`

### "Could not parse JSON from Claude response"
- Claude occasionally returns malformed JSON
- Try running again
- If persistent, increase max_tokens in the API call

### "Authorization failed"
- Regenerate WordPress Application Password
- Use admin-level WordPress account

## Advanced: Add SEO Plugins Integration

### Yoast SEO
Modify the WordPress post payload to include:
```javascript
meta: {
  _yoast_wpseo_focuskw: keyword,
  _yoast_wpseo_metadesc: metaDesc
}
```

### Rank Math
```javascript
meta: {
  rank_math_focus_keyword: keyword,
  rank_math_description: metaDesc
}
```

## Workflow Tips

1. **Keyword Research First**: Use Ahrefs, SEMrush, or Google Keyword Planner
2. **Batch Input**: Fill 10-20 keywords at once
3. **Review Before Publishing**: Generated content is in drafts - review and edit
4. **Add Images**: The script doesn't add images - do this manually in WordPress
5. **Internal Linking**: Claude marks opportunities as `[INTERNAL: anchor text]` - replace with actual links

## Support

For issues with:
- **Google Apps Script**: Check execution logs (View → Logs)
- **Claude API**: Check https://status.anthropic.com/
- **WordPress API**: Check your site's REST API at `/wp-json/`

---

**Ready to automate!** Start by filling in your first keyword and clicking "Generate Content for Selected Rows"
