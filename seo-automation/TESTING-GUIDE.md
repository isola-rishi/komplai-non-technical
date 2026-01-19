# SEO Automation Testing Guide

## Overview

This guide explains how to use the comprehensive testing features to validate your SEO automation setup before generating content.

---

## Quick Reference

| Test Type | Menu Location | Duration | Purpose |
|-----------|--------------|----------|---------|
| **Comprehensive Sanity Tests** | SEO Automation > 🧪 Run Comprehensive Sanity Tests | ~30 seconds | Full validation of setup, APIs, content quality |
| **Quick Test** | SEO Automation > ⚡ Quick Test (API Keys Only) | ~2 seconds | Fast API key validation |
| **Setup & Test Connection** | SEO Automation > Setup & Test Connection | ~5 seconds | Basic WordPress connection test |

---

## Comprehensive Sanity Tests

**When to run**: Before generating content for the first time, or after making changes to the script/configuration.

**What it tests**:

### 1. Script Properties Validation
- ✅ ANTHROPIC_API_KEY is set
- ✅ WORDPRESS_SITE_URL is set
- ✅ WORDPRESS_USERNAME is set
- ✅ WORDPRESS_APP_PASSWORD is set

### 2. Claude API Connection
- Tests actual connection to Anthropic API
- Verifies API key is valid
- Checks for API errors or rate limits

### 3. WordPress API Connection
- Tests WordPress REST API authentication
- Verifies application password works
- Checks if WordPress site is accessible
- Lists number of existing posts

### 4. Sheet Structure Validation
- Verifies all 12 column headers are correct
- Checks column names match expected format
- Ensures proper spreadsheet setup

### 5. Content Validation (if content exists)
Tests existing content in row 2 for:
- ✅ No unconverted `[INTERNAL:...]` placeholders
- ✅ No unconverted `[RELATED_ARTICLE_PLACEHOLDER_...]` placeholders
- ✅ Contains hyperlinks (`<a href=...>`)
- ✅ Sentence length (checks % of sentences over 20 words)
- ✅ No em-dashes (—) or en-dashes (–)
- ✅ WordPress URL is populated

### 6. Image Validation
- ✅ Unsplash images are present
- ✅ No placeholder photo IDs (PHOTO_ID_HERE)
- ✅ Shows actual photo IDs being used
- ✅ Validates image deduplication

---

## Test Results

### All Tests Passed
```
==================================================
✅ ALL TESTS PASSED - Safe to generate content!
==================================================
```

**What to do**: Proceed with content generation confidently!

### Some Tests Failed
```
==================================================
❌ SOME TESTS FAILED - Fix issues before generating content
==================================================
```

**What to do**:
1. Review the specific failures in the test results
2. Fix the issues (see Troubleshooting below)
3. Re-run the tests
4. Only generate content when all tests pass

---

## Common Test Failures & Solutions

### ❌ ANTHROPIC_API_KEY is missing
**Solution**:
1. Go to Apps Script > ⚙️ Project Settings
2. Scroll to "Script Properties"
3. Click "Add script property"
4. Property: `ANTHROPIC_API_KEY`
5. Value: Your Claude API key from https://console.anthropic.com
6. Save

### ❌ Claude API Error: authentication_error
**Solution**:
- Your API key is invalid or expired
- Get a new API key from https://console.anthropic.com
- Update the Script Property

### ❌ WordPress authentication failed (401)
**Solution**:
1. Verify WordPress username is correct (usually your admin username)
2. Regenerate Application Password:
   - WordPress Admin > Users > Profile
   - Scroll to "Application Passwords"
   - Create new password
   - Copy the password (with or without spaces)
   - Update WORDPRESS_APP_PASSWORD Script Property

### ❌ WordPress API returned status 404
**Solution**:
- Your WORDPRESS_SITE_URL is incorrect
- Should be: `https://yourdomain.com` (no trailing slash)
- Should NOT include `/wp-admin` or `/wp-json`

### ⚠️ Content contains unconverted [INTERNAL:...] placeholders
**Solution**:
- This indicates the `convertInternalPlaceholdersToLinks()` function isn't working
- The issue should be fixed in the latest version
- Regenerate the content to apply the fix

### ⚠️ Content contains unconverted [RELATED_ARTICLE_PLACEHOLDER_...] placeholders
**Solution**:
- This means Claude generated descriptions instead of using exact placeholders
- The latest version has stricter prompt requirements
- Regenerate the content to apply the fix

### ❌ ERROR: Content contains placeholder photo ID
**Solution**:
- Claude didn't replace PHOTO_ID_HERE with actual ID
- The latest version provides example photo IDs
- Regenerate the content to apply the fix

### ⚠️ Sentence length: 45% over 20 words (should be <35%)
**Solution**:
- Content has too many long sentences
- The latest version enforces 20-word maximum
- Regenerate the content to apply the fix

### ⚠️ Content contains em-dashes or en-dashes
**Solution**:
- The latest version prohibits em-dashes
- Regenerate the content to apply the fix

---

## Best Practices

### Before First Use
1. Run **Comprehensive Sanity Tests** to validate setup
2. Fix any failures
3. Generate content for one test keyword
4. Run **Comprehensive Sanity Tests** again to validate content
5. If all tests pass, proceed with bulk generation

### Regular Usage
1. Run **Quick Test** before each content generation session
2. Run **Comprehensive Sanity Tests** weekly to catch content quality issues
3. Run **Comprehensive Sanity Tests** after script updates

### After Script Updates
1. Refresh Google Apps Script editor
2. Run **Comprehensive Sanity Tests**
3. Verify all tests pass
4. Generate test content for one keyword
5. Review content quality manually

---

## Testing Workflow

```
┌─────────────────────────────────────┐
│ 1. Run Comprehensive Sanity Tests   │
└──────────────┬──────────────────────┘
               │
               ├─ All Pass ─────────────┐
               │                        │
               ├─ Some Fail             │
               │   └─> Fix Issues       │
               │       └─> Retry Tests ─┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. Generate Test Content (1 row)   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 3. Run Comprehensive Sanity Tests   │
│    (validates generated content)    │
└──────────────┬──────────────────────┘
               │
               ├─ All Pass ─────────────┐
               │                        │
               ├─ Some Fail             │
               │   └─> Fix Issues       │
               │       └─> Regenerate ──┘
               │
               ▼
┌─────────────────────────────────────┐
│ 4. Proceed with Bulk Generation     │
└─────────────────────────────────────┘
```

---

## Interpreting Test Results

### Green Checkmarks (✅)
- Feature is working correctly
- No action needed

### Yellow Warnings (⚠️)
- Feature works but quality could be improved
- Content may still be usable
- Consider fixing for better results

### Red X Marks (❌)
- Critical failure
- **Must** be fixed before proceeding
- Content generation may fail or produce bad results

### Blue Info (ℹ️)
- Informational message
- Not a failure
- Example: "No content rows to validate" (expected for empty sheet)

---

## Quick Test vs Comprehensive Tests

| Feature | Quick Test | Comprehensive Tests |
|---------|-----------|---------------------|
| Duration | 2 seconds | 30 seconds |
| API Key Check | ✅ | ✅ |
| WordPress Credentials Check | ✅ | ✅ |
| **Claude API Connection** | ❌ | ✅ |
| **WordPress API Connection** | ❌ | ✅ |
| **Sheet Structure Validation** | ❌ | ✅ |
| **Content Quality Validation** | ❌ | ✅ |
| **Image Validation** | ❌ | ✅ |
| **Placeholder Validation** | ❌ | ✅ |
| **Sentence Length Check** | ❌ | ✅ |
| When to Use | Daily quick check | Weekly or before important runs |

---

## FAQ

**Q: How often should I run tests?**
A: Run Quick Test daily, Comprehensive Tests weekly or after updates.

**Q: Can I generate content if some tests fail?**
A: Only if failures are warnings (⚠️). Never proceed if critical tests (❌) fail.

**Q: Why do I need to test content validation if I haven't generated content yet?**
A: The test will show "No content rows to validate" - that's expected and not a failure.

**Q: The tests take 30 seconds. Can I skip them?**
A: The 30 seconds can save hours of debugging later. Highly recommended to run regularly.

**Q: What if Claude API test passes but content generation fails?**
A: Check your API balance at https://console.anthropic.com. You may be out of credits.

**Q: What if WordPress test passes but posting fails?**
A: Check WordPress error logs. You may have plugin conflicts or permission issues.

---

## Support

If tests consistently fail after following troubleshooting steps:
1. Check Apps Script execution logs (View > Executions)
2. Look for detailed error messages
3. Verify all script properties are exactly correct (no extra spaces)
4. Try regenerating Application Password in WordPress

---

**Version:** 2.0
**Last Updated:** January 2026
**Created by:** Claude Code
