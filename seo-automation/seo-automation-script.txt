/**
 * SEO Content Automation Tool
 * Google Apps Script for generating SEO-optimized content and posting to WordPress
 *
 * Setup Instructions:
 * 1. Create a Google Sheet with columns: Keyword, Search Intent, Target Word Count, Generated Title, H1, H2s, Content, Meta Description, Status, WordPress URL
 * 2. Go to Extensions > Apps Script and paste this code
 * 3. Set up Script Properties: File > Project properties > Script properties
 *    - ANTHROPIC_API_KEY: Your Claude API key
 *    - WORDPRESS_SITE_URL: Your WordPress site URL (e.g., https://yoursite.com)
 *    - WORDPRESS_USERNAME: Your WordPress username
 *    - WORDPRESS_APP_PASSWORD: WordPress Application Password (create at Users > Profile)
 * 4. Run setup() once to authorize permissions
 */

// Column indices (adjust if your sheet structure differs)
const COLS = {
  KEYWORD: 1,
  SECONDARY_KEYWORDS: 2,
  SEARCH_INTENT: 3,
  TARGET_WORD_COUNT: 4,
  GENERATED_TITLE: 5,
  H1: 6,
  H2S: 7,
  CONTENT: 8,
  META_DESC: 9,
  STATUS: 10,
  WP_URL: 11,
  BACKLINKS_ADDED: 12
};

const STATUS = {
  PENDING: 'Pending',
  GENERATING: 'Generating...',
  GENERATED: 'Generated',
  POSTING: 'Posting to WP...',
  PUBLISHED: 'Published',
  ERROR: 'Error'
};

// Komplai company context for content alignment
const KOMPLAI_CONTEXT = {
  companyDescription: 'Komplai is an AI-powered accounting automation platform for mid-market finance teams',
  clientPainPoints: [
    'Multi-entity consolidation with currency conversion and tight month-end deadlines',
    'Consultant dependency for finance teams (institutional knowledge walks out the door when people leave)',
    'Manual reconciliation across 10-15 bank accounts and payment systems',
    'ERP limitations (QuickBooks cannot scale, SAP is overkill for mid-market)',
    '"Show me 50% value and I\'ll pilot" mentality from busy CFOs'
  ],
  targetAudience: {
    revenueRange: '$5-50M revenue companies',
    teamSize: '2-8 person finance teams',
    roles: ['CFOs', 'Controllers', 'Finance Directors', 'VP Finance']
  },
  valuePropositions: [
    'AI-powered automation that learns your accounting patterns over time',
    'Continuous close (not just faster month-end, but real-time financial visibility)',
    'Knowledge stays in the system, not with consultants who leave'
  ]
};

/**
 * Creates custom menu in Google Sheets
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('SEO Automation')
    .addItem('Generate Content for Selected Rows', 'generateContentForSelected')
    .addItem('Generate All Pending', 'generateAllPending')
    .addSeparator()
    .addItem('Post Selected to WordPress', 'postSelectedToWordPress')
    .addItem('Post All Generated to WordPress', 'postAllGeneratedToWordPress')
    .addSeparator()
    .addItem('Add Backlinks for Selected Row', 'addBacklinksForSelected')
    .addSeparator()
    .addSubMenu(SpreadsheetApp.getUi().createMenu('⏰ Daily Trigger')
      .addItem('Install Daily 11 AM Trigger', 'installDailyTrigger')
      .addItem('Remove Daily Trigger', 'removeDailyTriggerWithConfirm')
      .addItem('Check Trigger Status', 'checkTriggerStatus'))
    .addSeparator()
    .addItem('🧪 Run Comprehensive Sanity Tests', 'runSanityTests')
    .addItem('⚡ Quick Test (API Keys Only)', 'quickTest')
    .addItem('Setup & Test Connection', 'testConnections')
    .addToUi();
}

/**
 * Setup function - run once to authorize and install trigger
 */
function setup() {
  // This authorizes the script and installs the onOpen trigger
  onOpen(); // This will create the menu
  Logger.log('Setup complete. Please refresh your spreadsheet to see the SEO Automation menu.');
  Logger.log('Also configure Script Properties with your API keys.');
}

/**
 * Install daily trigger to run at 11 AM every weekday
 * Run this function once to set up the automated schedule
 */
function installDailyTrigger() {
  // Remove any existing daily triggers first to avoid duplicates
  removeDailyTrigger();

  // Create new trigger for 11 AM daily
  ScriptApp.newTrigger('scheduledDailyRun')
    .timeBased()
    .atHour(11)
    .everyDays(1)
    .create();

  Logger.log('Daily trigger installed. Will run at 11 AM and check for weekdays.');

  // Show confirmation if called from UI
  try {
    SpreadsheetApp.getUi().alert('Success', 'Daily 11 AM trigger installed!\n\nThe script will automatically run generateAllPending() at 11 AM on weekdays (Monday-Friday).', SpreadsheetApp.getUi().ButtonSet.OK);
  } catch (e) {
    // Not running from UI context, just log
  }
}

/**
 * Remove all daily triggers for this script
 */
function removeDailyTrigger() {
  const triggers = ScriptApp.getProjectTriggers();
  let removed = 0;

  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'scheduledDailyRun') {
      ScriptApp.deleteTrigger(trigger);
      removed++;
    }
  });

  if (removed > 0) {
    Logger.log(`Removed ${removed} existing trigger(s).`);
  }

  return removed;
}

/**
 * Scheduled function called by the daily trigger
 * Checks if it's a weekday before running generateAllPending()
 */
function scheduledDailyRun() {
  const today = new Date();
  const dayOfWeek = today.getDay(); // 0 = Sunday, 6 = Saturday

  // Only run on weekdays (Monday=1 through Friday=5)
  if (dayOfWeek >= 1 && dayOfWeek <= 5) {
    Logger.log(`Running scheduled content generation on ${today.toDateString()}`);

    try {
      // Run the content generation for all pending rows
      const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
      const lastRow = sheet.getLastRow();

      let generated = 0;
      for (let row = 2; row <= lastRow; row++) {
        const status = sheet.getRange(row, COLS.STATUS).getValue();
        if (status === STATUS.PENDING || status === '') {
          generateContentForRow(sheet, row);
          generated++;
        }
      }

      Logger.log(`Scheduled run complete. Generated content for ${generated} rows.`);
    } catch (e) {
      Logger.log(`Scheduled run error: ${e.toString()}`);
    }
  } else {
    Logger.log(`Skipping scheduled run - today is ${today.toDateString()} (weekend)`);
  }
}

/**
 * Remove daily trigger with confirmation dialog
 */
function removeDailyTriggerWithConfirm() {
  const ui = SpreadsheetApp.getUi();
  const response = ui.alert(
    'Remove Trigger',
    'Are you sure you want to remove the daily 11 AM trigger?\n\nThe automated content generation will stop.',
    ui.ButtonSet.YES_NO
  );

  if (response === ui.Button.YES) {
    const removed = removeDailyTrigger();
    if (removed > 0) {
      ui.alert('Removed', `Removed ${removed} trigger(s). Automated scheduling is now disabled.`, ui.ButtonSet.OK);
    } else {
      ui.alert('No Trigger Found', 'There was no active daily trigger to remove.', ui.ButtonSet.OK);
    }
  }
}

/**
 * Check the status of the daily trigger
 */
function checkTriggerStatus() {
  const triggers = ScriptApp.getProjectTriggers();
  let found = false;

  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'scheduledDailyRun') {
      found = true;
      Logger.log(`Trigger found: runs ${trigger.getHandlerFunction()} - ${trigger.getTriggerSource()}`);
    }
  });

  const message = found
    ? 'Daily 11 AM trigger is ACTIVE.\n\nIt will run generateAllPending() on weekdays (Mon-Fri).'
    : 'No daily trigger found.\n\nUse "Install Daily 11 AM Trigger" to set it up.';

  try {
    SpreadsheetApp.getUi().alert('Trigger Status', message, SpreadsheetApp.getUi().ButtonSet.OK);
  } catch (e) {
    Logger.log(message);
  }

  return found;
}

/**
 * Test API connections
 */
function testConnections() {
  const ui = SpreadsheetApp.getUi();

  // Test Claude API
  try {
    const apiKey = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');
    if (!apiKey) {
      ui.alert('Error', 'ANTHROPIC_API_KEY not set in Script Properties', ui.ButtonSet.OK);
      return;
    }
    ui.alert('Success', 'Claude API key found. Ready to generate content.', ui.ButtonSet.OK);
  } catch (e) {
    ui.alert('Error', 'Failed to test connections: ' + e.toString(), ui.ButtonSet.OK);
  }
}

/**
 * Generate content for selected rows
 */
function generateContentForSelected() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const selection = sheet.getActiveRange();
  const startRow = selection.getRow();
  const numRows = selection.getNumRows();

  for (let i = 0; i < numRows; i++) {
    const row = startRow + i;
    generateContentForRow(sheet, row);
  }

  SpreadsheetApp.getUi().alert('Content generation complete!');
}

/**
 * Generate content for all pending rows
 */
function generateAllPending() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const lastRow = sheet.getLastRow();

  let generated = 0;
  for (let row = 2; row <= lastRow; row++) {
    const status = sheet.getRange(row, COLS.STATUS).getValue();
    if (status === STATUS.PENDING || status === '') {
      generateContentForRow(sheet, row);
      generated++;
    }
  }

  SpreadsheetApp.getUi().alert(`Generated content for ${generated} rows!`);
}

/**
 * Generate SEO content for a single row using Claude API
 */
function generateContentForRow(sheet, row) {
  try {
    // Get input data first to validate
    const keyword = sheet.getRange(row, COLS.KEYWORD).getValue();
    const secondaryKeywords = sheet.getRange(row, COLS.SECONDARY_KEYWORDS).getValue() || '';
    const searchIntent = sheet.getRange(row, COLS.SEARCH_INTENT).getValue() || 'informational';
    const targetWordCount = sheet.getRange(row, COLS.TARGET_WORD_COUNT).getValue() || 1500;

    if (!keyword) {
      sheet.getRange(row, COLS.STATUS).setValue(STATUS.ERROR + ': No keyword');
      return;
    }

    // Step 1: Fetching existing WordPress articles
    sheet.getRange(row, COLS.STATUS).setValue('📚 Step 1/5: Fetching existing WordPress articles...');
    SpreadsheetApp.flush();

    const existingPosts = fetchAllWordPressPosts();

    // Extract used images to avoid repetition
    const usedImages = getUsedImages(existingPosts);

    // Step 2: Research and planning
    sheet.getRange(row, COLS.STATUS).setValue('🔍 Step 2/5: Researching topic and planning content...');
    SpreadsheetApp.flush();

    const researchPlan = createContentPlan(keyword, secondaryKeywords, searchIntent, targetWordCount, existingPosts);

    // Step 3: Calling Claude API to generate content
    sheet.getRange(row, COLS.STATUS).setValue('🤖 Step 3/5: Claude AI generating content...');
    SpreadsheetApp.flush();

    // Generate content using Claude with research plan and used images
    const content = generateSEOContent(keyword, secondaryKeywords, searchIntent, targetWordCount, researchPlan, usedImages, sheet, row);

    // Step 4: Processing response
    sheet.getRange(row, COLS.STATUS).setValue('⚙️ Step 4/5: Processing content...');
    SpreadsheetApp.flush();

    // Convert [INTERNAL: ...] placeholders to actual links
    let htmlContent = convertInternalPlaceholdersToLinks(content.htmlContent, researchPlan);

    // Add related articles carousel with links
    htmlContent = addRelatedArticles(htmlContent, existingPosts, keyword);

    // Step 5: Saving to sheet
    sheet.getRange(row, COLS.STATUS).setValue('💾 Step 5/5: Saving to sheet...');
    SpreadsheetApp.flush();

    // Parse and populate results
    sheet.getRange(row, COLS.GENERATED_TITLE).setValue(content.title);
    sheet.getRange(row, COLS.H1).setValue(content.h1);
    sheet.getRange(row, COLS.H2S).setValue(content.h2s.join('\n'));

    // Check content length - Google Sheets has a 50,000 character limit per cell
    const MAX_CELL_CHARS = 50000;
    if (htmlContent.length > MAX_CELL_CHARS) {
      Logger.log(`Warning: Content is ${htmlContent.length} characters, exceeds ${MAX_CELL_CHARS} limit. Truncating...`);
      // Truncate content and add a note about truncation
      htmlContent = htmlContent.substring(0, MAX_CELL_CHARS - 100) + '\n\n<!-- CONTENT TRUNCATED: Original was ' + htmlContent.length + ' characters. Reduce word count target. -->';
    }

    sheet.getRange(row, COLS.CONTENT).setValue(htmlContent);
    sheet.getRange(row, COLS.META_DESC).setValue(content.metaDescription);

    // Final status: Complete!
    sheet.getRange(row, COLS.STATUS).setValue('✅ ' + STATUS.GENERATED);
    SpreadsheetApp.flush();

  } catch (e) {
    sheet.getRange(row, COLS.STATUS).setValue(STATUS.ERROR + ': ' + e.message);
    Logger.log('Error generating content for row ' + row + ': ' + e.toString());
  }
}

/**
 * Retry wrapper for API calls with exponential backoff
 * Helps handle temporary network issues
 */
function callAnthropicAPIWithRetry(payload, maxRetries = 3) {
  const apiKey = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const options = {
        method: 'post',
        contentType: 'application/json',
        headers: {
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01'
        },
        payload: JSON.stringify(payload),
        muteHttpExceptions: true
      };

      const response = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', options);
      const responseData = JSON.parse(response.getContentText());

      if (responseData.error) {
        Logger.log(`Claude API error (attempt ${attempt}/${maxRetries}): ${responseData.error.message}`);
        if (attempt === maxRetries) {
          throw new Error(`Claude API error: ${responseData.error.message}`);
        }
        // Wait before retrying on API errors
        Utilities.sleep(1000 * attempt);
        continue;
      }

      return responseData;

    } catch (e) {
      Logger.log(`API call failed (attempt ${attempt}/${maxRetries}): ${e.toString()}`);

      if (attempt === maxRetries) {
        throw new Error(`Failed after ${maxRetries} attempts: ${e.toString()}`);
      }

      // Exponential backoff: 2s, 4s, 8s
      const waitTime = 2000 * Math.pow(2, attempt - 1);
      Logger.log(`Waiting ${waitTime}ms before retry...`);
      Utilities.sleep(waitTime);
    }
  }
}

/**
 * Create a content plan by researching existing articles and identifying backlinking opportunities
 */
function createContentPlan(keyword, secondaryKeywords, searchIntent, targetWordCount, existingPosts) {
  // Limit to top 20 posts for analysis
  const postsToAnalyze = existingPosts.slice(0, 20);

  // Create a summary of existing posts
  const existingPostsSummary = postsToAnalyze.map((post, idx) =>
    `[${idx}] "${post.title}" - ${post.url}\nTopics covered: ${post.excerpt || 'N/A'}`
  ).join('\n\n');

  const secondaryKeywordsText = secondaryKeywords ? `\nSECONDARY KEYWORDS: ${secondaryKeywords}` : '';

  const prompt = `You are an SEO content strategist. Create a detailed content plan for a new blog post.

TARGET KEYWORD: "${keyword}"${secondaryKeywordsText}
SEARCH INTENT: ${searchIntent}
TARGET WORD COUNT: ${targetWordCount} words

EXISTING ARTICLES ON THE BLOG:
${existingPostsSummary || 'No existing articles yet.'}

YOUR TASK:
Analyze the existing articles and create a comprehensive content plan that:

1. IDENTIFIES BACKLINKING OPPORTUNITIES: You MUST find AT LEAST 3-5 existing articles to link to. This is MANDATORY, not optional.

   EVEN IF the topic seems unrelated, be creative and find connections:
   - If writing about "continuous close", link to articles about "financial close", "automation", "accounting", "month-end", "reporting", etc.
   - If writing about "anomaly detection", link to articles about "AI", "financial close", "data analysis", "automation", etc.
   - If writing about anything financial, link to other financial articles about processes, tools, or related concepts

   For each backlinking opportunity, specify:
   - Which article to link to (by index number from the list below)
   - Where in the new content the link would fit naturally (be specific: "in the introduction", "when discussing benefits", "in the implementation section")
   - What anchor text to use (5-10 words from the new content that naturally connects)

   CRITICAL: Return AT LEAST 3 backlinking opportunities. Do not return an empty array. Look at EVERY article and find ANY possible connection, no matter how indirect.

2. AVOIDS REPETITION: Identify topics already covered in existing articles so we can reference them (via backlinks) rather than repeating the same information.

3. FINDS UNIQUE ANGLES: Suggest fresh perspectives or aspects of the topic that haven't been covered yet.

4. GATHERS KEY FACTS: List 5-7 important statistics, data points, or facts about the topic from 2025 or late 2024 (use realistic examples - you can indicate where to find real data).

5. SUGGESTS SOURCES: Recommend reputable sources for citations (industry reports, research studies, government data, etc.).

6. PLANS STRUCTURE: Outline the main H2 sections that would comprehensively cover the topic.

Return ONLY valid JSON in this exact format:
{
  "backlinkingOpportunities": [
    {
      "articleIndex": 0,
      "articleTitle": "title of existing article",
      "suggestedAnchorText": "natural anchor text",
      "placementContext": "where/why this link fits naturally"
    }
  ],
  "topicsToAvoid": ["topic 1 already covered", "topic 2 already covered"],
  "uniqueAngles": ["fresh angle 1", "fresh angle 2"],
  "keyFacts": [
    {
      "fact": "statistic or data point",
      "suggestedSource": "source type or name"
    }
  ],
  "suggestedH2s": ["H2 1", "H2 2", "H2 3"]
}`;

  const payload = {
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4000,
    messages: [{
      role: 'user',
      content: prompt
    }]
  };

  try {
    // Use retry wrapper for better reliability
    const responseData = callAnthropicAPIWithRetry(payload);

    const contentText = responseData.content[0].text;

    // Extract JSON from response
    const jsonMatch = contentText.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      Logger.log('No valid JSON found in planning response');
      return null;
    }

    const plan = JSON.parse(jsonMatch[0]);

    // Add the actual post objects to backlinking opportunities
    if (plan.backlinkingOpportunities) {
      plan.backlinkingOpportunities = plan.backlinkingOpportunities.map(opp => {
        return {
          ...opp,
          articleUrl: postsToAnalyze[opp.articleIndex]?.url || ''
        };
      });
    }

    return plan;

  } catch (e) {
    Logger.log('Error creating content plan: ' + e.toString());
    return null;
  }
}

/**
 * Call Claude API to generate SEO-optimized content
 */
function generateSEOContent(keyword, secondaryKeywords, searchIntent, targetWordCount, researchPlan, usedImages, sheet, row) {
  const apiKey = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');

  if (!apiKey) {
    throw new Error('ANTHROPIC_API_KEY not found in Script Properties. Please configure it in Project Settings.');
  }

  // Build secondary keywords section
  const secondaryKeywordsText = secondaryKeywords ? `SECONDARY KEYWORDS: ${secondaryKeywords} (naturally incorporate these throughout the content where relevant)` : '';

  // Get current year for content freshness
  const currentYear = new Date().getFullYear();

  // Build research plan section
  let researchPlanText = '';
  if (researchPlan) {
    researchPlanText = `
RESEARCH PLAN (use this to guide your content creation):

BACKLINKING OPPORTUNITIES:
${researchPlan.backlinkingOpportunities?.map(opp =>
  `- Link to "${opp.articleTitle}" (${opp.articleUrl})
   Anchor text: "${opp.suggestedAnchorText}"
   Context: ${opp.placementContext}
   Add this as: [INTERNAL: ${opp.suggestedAnchorText}]`
).join('\n') || 'No existing articles to link to yet.'}

TOPICS TO AVOID (already covered in existing articles):
${researchPlan.topicsToAvoid?.map(topic => `- ${topic}`).join('\n') || 'None'}

UNIQUE ANGLES TO FOCUS ON:
${researchPlan.uniqueAngles?.map(angle => `- ${angle}`).join('\n') || 'None'}

KEY FACTS TO INCLUDE:
${researchPlan.keyFacts?.map(fact => `- ${fact.fact} (Source: ${fact.suggestedSource})`).join('\n') || 'None'}

SUGGESTED H2 STRUCTURE:
${researchPlan.suggestedH2s?.map((h2, idx) => `${idx + 1}. ${h2}`).join('\n') || 'Use your judgment'}
`;
  }

  const prompt = `You are an SEO content writer. Generate a comprehensive, SEO-optimized blog post with the following specifications. Today's date is ${new Date().toISOString().split('T')[0]} and the current year is ${currentYear}.

TARGET KEYWORD: "${keyword}"
${secondaryKeywordsText}
SEARCH INTENT: ${searchIntent}

TARGET WORD COUNT: ${targetWordCount} words (THIS IS MANDATORY - SEE REQUIREMENTS BELOW)

═══════════════════════════════════════════════════════════════════════════════
MANDATORY REQUIREMENTS - READ THESE FIRST - YOUR ARTICLE WILL BE REJECTED IF NOT MET
═══════════════════════════════════════════════════════════════════════════════

REQUIREMENT 1: WORD COUNT (STRICTLY ENFORCED)
- Your article MUST be EXACTLY between ${Math.round(targetWordCount * 0.95)} and ${Math.round(targetWordCount * 1.05)} words
- Target: ${targetWordCount} words | Acceptable: ${Math.round(targetWordCount * 0.95)}-${Math.round(targetWordCount * 1.05)} words
- COUNT YOUR WORDS before submitting - this is verified automatically
- If too short: add more detail, examples, statistics, or expand explanations
- If too long: trim unnecessary words, combine sentences, remove redundancy

REQUIREMENT 2: NO CONSECUTIVE SENTENCES WITH SAME STARTING WORD
- ZERO consecutive sentences may start with the same word
- Every single sentence must start with a DIFFERENT word than the previous sentence
- BAD: "This helps... This also..." (REJECTED - both start with "This")
- GOOD: "This helps... Additionally, it also..." (ACCEPTED - different starting words)
- CHECK EVERY SENTENCE PAIR in your article before submitting
- Common violations: "The... The...", "This... This...", "It... It...", "They... They..."

REQUIREMENT 3: TRANSITION WORDS (MINIMUM 30% - AIM FOR 40%)
- AT LEAST 30% of sentences MUST start with transition words
- Aim for 40% to ensure you pass the 30% threshold
- EVERY 2-3 SENTENCES, one must start with a transition word
- Transition words: However, Additionally, Furthermore, Moreover, Therefore, Consequently, Meanwhile, First, Second, Next, Finally, For example, In addition, As a result, Nevertheless, Indeed, Specifically, Importantly, Similarly, Conversely, Subsequently, Accordingly, Thus, Hence, Overall, Ultimately, Currently, Previously, Initially, Notably, Certainly, Clearly
- COUNT your transition sentences: (transition sentences ÷ total sentences) × 100 = must be ≥30%

═══════════════════════════════════════════════════════════════════════════════
${researchPlanText}

KOMPLAI COMPANY CONTEXT (use this to align content with our positioning):
${buildKomplaiContextSection()}

IMPORTANT REQUIREMENTS:

0. WRITING STYLE - STORY-DRIVEN & RELATABLE (like cfooffice/cfosecrets):
   - Write as if you're a seasoned finance professional sharing real experiences
   - Use "I've been there" moments: "If you've ever stayed late reconciling bank accounts..."
   - Include behind-the-scenes finance team struggles: "We all know that feeling when the month-end crunch hits..."
   - Reference real frustrations CFOs feel: consultant dependency, Excel hell, the "we've always done it this way" resistance
   - AVOID corporate jargon - write conversationally: "Let's be honest..." / "Here's the thing..." / "The truth is..."
   - Use specific, relatable scenarios: "Picture this: It's day 5 of close, your controller just resigned, and half your processes lived in their head"
   - Include empathetic acknowledgments: "Yes, your team is already stretched thin. Yes, implementing something new sounds exhausting."
   - Make it personal with phrases like: "I've seen this pattern dozens of times..." / "What most finance leaders don't realise is..."

1. Use UK English spelling and grammar throughout (e.g., "optimise" not "optimize", "colour" not "color", "analysing" not "analyzing")
2. ALL monetary amounts MUST be formatted with the $ symbol (e.g., "$50,000", "$2.5 million", "$100")
3. SENTENCE LENGTH: Keep sentences SHORT and punchy. Maximum 20 words per sentence. At least 65% of sentences MUST be under 20 words. Break long sentences into multiple shorter ones.
4. PUNCTUATION: DO NOT use em-dashes (—) or en-dashes (–) anywhere in the content. Use commas, periods, or split into separate sentences instead.
5. VOCABULARY SIMPLICITY (CRITICAL): Write for a broad audience:
   - Use common, everyday words instead of complex alternatives
   - Prefer 1-2 syllable words where possible (e.g., "use" not "utilise", "help" not "facilitate")
   - If technical terms are necessary, explain them immediately in simple terms
   - Target reading level: Year 9 (age 13-14) comprehension
   - Avoid: jargon, corporate-speak, unnecessarily long words
   - Examples of what to use: "start" not "commence", "end" not "terminate", "buy" not "purchase", "get" not "obtain", "show" not "demonstrate", "need" not "require"
6. SENTENCE VARIETY (SEE REQUIREMENT 2 ABOVE - ZERO CONSECUTIVE SAME-WORD STARTS):
   - NO consecutive sentences may start with the same word - not even 2 in a row
   - Every sentence must begin with a DIFFERENT word than the sentence before it
   - After writing each sentence, check: does it start with the same word as the previous sentence? If yes, REWRITE it
   - Use varied openers: transition words (40% of sentences), different subjects, questions, imperatives
   - BAD: "This helps. This also reduces..." → REWRITE to: "This helps. Additionally, it reduces..."
   - BAD: "The team benefits. The process improves..." → REWRITE to: "The team benefits. Meanwhile, the process improves..."
7. Create an engaging, SEO-friendly title (50-60 characters)
8. Create an H1 tag (can be same as title or slightly different)
9. Generate 5-8 H2 subheadings that cover the topic comprehensively
10. Write full HTML content with SOPHISTICATED LAYOUT and CLEAR VISUAL HIERARCHY:
   - Hero section with featured image using WordPress figure block format:
     <!-- wp:image {"sizeSlug":"large","linkDestination":"none"} -->
     <figure class="wp-block-image size-large"><img src="https://images.unsplash.com/photo-PHOTO_ID_HERE?w=1600&h=900&fit=crop" alt="[Relevant alt text based on keyword]"/></figure>
     <!-- /wp:image -->

     CRITICAL IMAGE REQUIREMENTS:
     * Replace PHOTO_ID_HERE with a valid Unsplash photo ID (format: numbers and letters, e.g., "1557804506-069f1546344a" or "1454165804606-c3d57bc86b40")
     * Choose a photo ID relevant to the keyword topic
     * Valid example IDs you can use:
       - Business/finance: 1454165804606-c3d57bc86b40, 1557804506-069f1546344a, 1460925895917-afdab827c52f
       - Technology: 1518770660439-4636190af475, 1526374965881-54f90c92f5ba, 1484480974693-6ca0a78fb36b
       - Office/work: 1497366216902-e8f0c0c5c1b8, 1486406146357-2295cb0f1e52, 1497366811353-6870744d04b2
     ${usedImages && usedImages.length > 0 ? `* DO NOT USE these photo IDs (already used): ${Array.from(usedImages).join(', ')}` : ''}
     * Choose a DIFFERENT photo ID from the examples above or use your own valid Unsplash photo ID
     * NEVER leave "PHOTO_ID_HERE" as-is - always replace with actual photo ID
   - NUMBER all H2 headings (e.g., "1. Introduction", "2. Key Benefits", etc.)
   - KEYPHRASE IN SUBHEADINGS (CRITICAL - MANDATORY FOR SEO):
     * H2 REQUIREMENT: At least 50% of H2 subheadings MUST contain the target keyword or a very close synonym
       - If you have 6 H2s, at least 3 MUST include the keyphrase
       - Use the EXACT keyword in at least 2 H2s, synonyms in others
       - Example: If keyword is "continuous close", use "Continuous Close Benefits", "How Continuous Close Works", etc.
     * H3 REQUIREMENT: At least 40% of H3 subheadings MUST contain the keyword or synonym
     * BEFORE FINALIZING: Count your H2s and H3s and verify the keyword percentage
     * Use natural variations to avoid repetition while maintaining SEO value
     * This is NON-NEGOTIABLE: Subheadings without keyphrases FAIL Yoast SEO checks
   - CRITICAL: Add H3 subheadings every 200-300 words to break up long sections. NO section should exceed 300 words without a subheading
   - ALL paragraphs must use justified text alignment: <p style="text-align: justify;">content here</p>
   - TRANSITION WORDS (SEE REQUIREMENT 3 ABOVE - MINIMUM 30%, AIM FOR 40%):
     * AT LEAST 30% of ALL sentences MUST begin with transition words - AIM FOR 40%
     * If your article has 100 sentences, at least 40 should start with transition words
     * PATTERN TO FOLLOW: Sentence 1 (any start) → Sentence 2 (transition word) → Sentence 3 (any start) → Sentence 4 (transition word)
     * USE THESE TRANSITION WORDS LIBERALLY: However, Additionally, Furthermore, Moreover, Therefore, Consequently, Meanwhile, First, Second, Next, Finally, For example, In addition, As a result, Nevertheless, Indeed, Specifically, Importantly, Similarly, Subsequently, Thus, Hence, Overall, Currently, Previously, Initially, Notably, Certainly
   - Use bullet points (HTML <ul> and <li> tags) frequently where appropriate - for lists, benefits, steps, features, comparisons, etc.
   - DATA-DRIVEN CONTENT: Include relevant statistics, percentages, and research findings from ${currentYear} or late ${currentYear - 1} with inline source citations in footnote format
   - MANDATORY: Include a "Key Statistics" or "Quick Facts" callout box early in the content (within first 30% of article) using this format:
     <div style="background: #f9f9f9; border-left: 4px solid #333; padding: 20px; margin: 30px 0;">
       <h3 style="margin-top: 0;">Key Statistics</h3>
       <ul style="margin: 15px 0; padding-left: 20px;">
         <li><strong>[Percentage or number]</strong>: [Brief statistic with context]</li>
         <li><strong>[Percentage or number]</strong>: [Brief statistic with context]</li>
         <li><strong>[Percentage or number]</strong>: [Brief statistic with context]</li>
       </ul>
       <p style="margin-bottom: 0; font-size: 0.9em;"><em>Sources: [Brief source citations]</em></p>
     </div>
   - In the middle of the content (around 50% through), include a "Related Articles" section using this EXACT format:
     <div style="background: #f5f5f5; padding: 20px; margin: 30px 0; border-radius: 8px;">
       <h3 style="margin-top: 0;">Related Articles</h3>
       <p>[RELATED_ARTICLE_PLACEHOLDER_1]</p>
       <p>[RELATED_ARTICLE_PLACEHOLDER_2]</p>
     </div>

     CRITICAL PLACEHOLDER REQUIREMENTS:
     * Use EXACTLY "[RELATED_ARTICLE_PLACEHOLDER_1]" and "[RELATED_ARTICLE_PLACEHOLDER_2]" - do not modify these strings
     * DO NOT write article descriptions, titles, or any text in place of the placeholders
     * DO NOT write things like "Discover how to..." or "Learn strategies..." - just use the exact placeholder strings
     * These will be automatically populated with links to related articles
     * Example of CORRECT usage: <p>[RELATED_ARTICLE_PLACEHOLDER_1]</p>
     * Example of INCORRECT usage: <p>Discover how to design comprehensive controls...</p>
   - Proper heading hierarchy (numbered H2s, H3 where needed) with generous spacing between sections
   - Add a "Sources & References" section at the VERY END (after the conclusion and CTA) with numbered footnotes linking to all cited statistics and data
   - Short paragraphs (2-3 sentences) for easy scanning
   - Natural keyword integration (avoid keyword stuffing)${secondaryKeywords ? '\n   - Naturally incorporate secondary keywords where relevant' : ''}
   - INTERNAL LINKING - MANDATORY: You MUST include ALL backlinking opportunities from the research plan above.
     * Use the [INTERNAL: anchor text] format exactly as shown in the research plan
     * Place each link in the context specified in the research plan
     * If the research plan shows 5 backlinking opportunities, your content MUST include all 5 [INTERNAL: ...] markers
     * This is NOT optional - every backlinking opportunity MUST appear in your content
   - AVOID repeating topics already covered in existing articles - reference them via internal links instead
   - FOCUS on the unique angles identified in the research plan
   - Strong opening hook and conclusion with CTA
   - SOCIAL MEDIA OPTIMISATION: Write content that is easily extractable for Twitter, Quora, and Reddit:
     * Include quotable statistics and insights that can be tweeted (under 280 characters)
     * Write self-contained paragraphs that can answer common questions (for Quora)
     * Use conversational tone with practical examples (for Reddit)
     * Include actionable takeaways and specific tips throughout
   - Focus on answering specific questions users might search for on Google, ask on Quora, or discuss on Reddit
   - ACTION PLAN ELEMENTS - MANDATORY: Every article MUST include these three types of actionable content:

     1. INLINE ACTIONABLE TAKEAWAYS: Weave actionable advice throughout the article. At least every 2-3 paragraphs, include phrases like:
        * "Here's what you should do..."
        * "Your next step is..."
        * "Take action by..."
        * "Start by..."
        * "The key move here is..."

     2. CHECKLIST CALLOUT BOXES: Include 2-3 checklist boxes throughout the article using this exact format:
        <div style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 20px; margin: 30px 0;">
          <h3 style="margin-top: 0; color: #2e7d32;">Action Checklist: [Topic Name]</h3>
          <ul style="margin: 15px 0; padding-left: 20px; list-style-type: none;">
            <li style="margin-bottom: 10px;">&#9744; <strong>[Specific action item]</strong></li>
            <li style="margin-bottom: 10px;">&#9744; <strong>[Specific action item]</strong></li>
            <li style="margin-bottom: 10px;">&#9744; <strong>[Specific action item]</strong></li>
          </ul>
        </div>

     3. ACTION STEPS SECTION: Include a "What To Do Next" or "Your Action Plan" section near the end (before the conclusion) using this exact format:
        <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 20px; margin: 30px 0;">
          <h3 style="margin-top: 0; color: #e65100;">What To Do Next</h3>
          <ol style="margin: 15px 0; padding-left: 20px;">
            <li style="margin-bottom: 15px;"><strong>Step 1:</strong> [Specific actionable step with detail]</li>
            <li style="margin-bottom: 15px;"><strong>Step 2:</strong> [Specific actionable step with detail]</li>
            <li style="margin-bottom: 15px;"><strong>Step 3:</strong> [Specific actionable step with detail]</li>
            <li style="margin-bottom: 15px;"><strong>Step 4:</strong> [Specific actionable step with detail]</li>
            <li style="margin-bottom: 15px;"><strong>Step 5:</strong> [Specific actionable step with detail]</li>
          </ol>
        </div>
   - SEO OPTIMIZATION (ALL ITEMS BELOW ARE MANDATORY - FAILURE TO COMPLY WILL RESULT IN SEO FAILURE):

     * KEYPHRASE IN INTRODUCTION (CRITICAL - FIRST PRIORITY):
       - The EXACT target keyword "${keyword}" MUST appear in the FIRST PARAGRAPH (first 2-3 sentences)
       - This is the MOST IMPORTANT SEO requirement - search engines weight the first paragraph heavily
       - Also include a synonym or variation of the keyword in the first paragraph
       - Example: If keyword is "continuous close accounting", the first paragraph MUST contain "continuous close accounting" verbatim
       - DO NOT start writing until you have verified the keyword appears in your opening paragraph

     * KEYPHRASE DENSITY (CRITICAL - MINIMUM 11 OCCURRENCES):
       - The EXACT target keyword "${keyword}" must appear AT LEAST 11-15 times throughout the article
       - Distribution requirements:
         * First paragraph: 1-2 times (MANDATORY - see above)
         * H2 subheadings: 2-3 times (in at least 50% of H2s - use exact match or close synonyms)
         * H3 subheadings: 1-2 times
         * Body paragraphs: 5-7 times (spread evenly, roughly once per 150 words)
         * Conclusion paragraph: 1-2 times (exact match required)
         * Image alt text: 1 time
       - COUNT your keyword usage before finalizing - if fewer than 11 occurrences, add more naturally
       - Use BOTH exact match AND natural variations (synonyms, related phrases)
       - This is NON-NEGOTIABLE: Articles with fewer than 11 keyword occurrences FAIL SEO checks

     * Include LSI keywords (semantically related terms) naturally
     * Answer "what", "why", "how", "when" questions related to the topic
     * Include "People Also Ask" style sections with clear Q&A format where appropriate
     * Naturally reference pain points your target audience experiences (multi-entity consolidation, consultant dependency, ERP limitations)
     * Position solutions around continuous close and AI-powered pattern learning where relevant to the topic
     * Speak to 2-8 person finance teams at $5-50M revenue companies - they're your readers
11. ALL CTAs must link to: https://calendar.google.com/calendar/u/0/appointments/schedules/AcZssZ13_PU25qP6mHW9P6VCKYXD9vRfwvxQDP8ZlxUJD1Un4mC20CLjx0zag4E9-oPAYaqjxMlGhN29
   - Use calendar-appropriate language (e.g., "Book a consultation", "Schedule a call", "Book your free demo")
12. META DESCRIPTION (CRITICAL - MANDATORY FOR SEO):
   - YOU MUST PROVIDE A META DESCRIPTION - this field cannot be empty or omitted
   - MUST be exactly 150-160 characters (count carefully - not shorter, not longer)
   - MUST include the EXACT target keyword "${keyword}" within the FIRST 60 characters
   - Must be compelling and action-oriented with a clear value proposition
   - Write in UK English
   - Format: Start with the keyword, then describe the benefit/value
   - Example format: "[Keyword] helps finance teams [benefit]. Learn [what they'll discover] in this guide."
   - VERIFY your meta description contains the keyword before submitting
   - This is NON-NEGOTIABLE: Articles without a proper meta description FAIL SEO checks
13. All content must reflect ${currentYear} - DO NOT reference outdated years like 2024 or earlier unless citing historical context

FINAL CHECKLIST BEFORE SUBMITTING (VERIFY ALL - ARTICLE WILL BE REJECTED IF ANY FAIL):
□ Word count is EXACTLY ${Math.round(targetWordCount * 0.95)}-${Math.round(targetWordCount * 1.05)} words (target: ${targetWordCount}) - COUNT THEM
□ Keyword "${keyword}" appears 11+ times throughout article
□ Keyword appears in FIRST PARAGRAPH (first 2-3 sentences)
□ Keyword appears in 50%+ of H2 subheadings
□ Meta description is 150-160 characters and contains the keyword in first 60 chars
□ ZERO consecutive sentences start with the same word (every sentence starts differently from the previous one)
□ AT LEAST 30% of sentences start with transition words (aim for 40% - count: transitions ÷ total sentences ≥ 0.30)

Return ONLY valid JSON in this exact format:
{
  "title": "SEO-optimized title here",
  "h1": "H1 tag here",
  "h2s": ["1. First H2", "2. Second H2", "3. Third H2", ...],
  "htmlContent": "<full HTML content here - MUST be ${Math.round(targetWordCount * 0.9)}-${Math.round(targetWordCount * 1.1)} words>",
  "metaDescription": "150-160 chars with keyword in first 60 chars"
}`;

  const payload = {
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 16000, // Increased for longer content with styling and citations
    messages: [{
      role: 'user',
      content: prompt
    }]
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01'
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  // Show "thinking" indicator during API call
  if (sheet && row) {
    sheet.getRange(row, COLS.STATUS).setValue('🤖 Step 3/5: Claude AI thinking... (30-60s)');
    SpreadsheetApp.flush();
  }

  const response = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', options);
  const responseData = JSON.parse(response.getContentText());

  if (responseData.error) {
    throw new Error('Claude API error: ' + responseData.error.message);
  }

  // Update status: parsing response
  if (sheet && row) {
    sheet.getRange(row, COLS.STATUS).setValue('🤖 Step 3/5: Parsing AI response...');
    SpreadsheetApp.flush();
  }

  // Extract JSON from Claude's response
  const contentText = responseData.content[0].text;

  // Strategy 1: Try to extract JSON from code blocks first
  const codeBlockMatch = contentText.match(/```json\s*(\{[\s\S]*?\})\s*```/);
  if (codeBlockMatch) {
    try {
      return JSON.parse(codeBlockMatch[1]);
    } catch (e) {
      Logger.log('Failed to parse JSON from code block: ' + e.toString());
    }
  }

  // Strategy 2: Find the first { and last } to extract complete JSON
  const firstBrace = contentText.indexOf('{');
  const lastBrace = contentText.lastIndexOf('}');

  if (firstBrace === -1 || lastBrace === -1 || firstBrace >= lastBrace) {
    throw new Error('Could not find valid JSON structure in Claude response');
  }

  const jsonString = contentText.substring(firstBrace, lastBrace + 1);

  // Try to parse the extracted JSON
  try {
    return JSON.parse(jsonString);
  } catch (parseError) {
    Logger.log('Standard JSON parse failed: ' + parseError.toString());

    // Strategy 3: Extract fields individually using regex (more robust for malformed JSON)
    try {
      Logger.log('Attempting field-by-field extraction...');

      // Extract title
      const titleMatch = jsonString.match(/"title"\s*:\s*"([^"]*(?:\\.[^"]*)*)"/);
      const title = titleMatch ? titleMatch[1].replace(/\\"/g, '"') : 'Untitled';

      // Extract h1
      const h1Match = jsonString.match(/"h1"\s*:\s*"([^"]*(?:\\.[^"]*)*)"/);
      const h1 = h1Match ? h1Match[1].replace(/\\"/g, '"') : title;

      // Extract h2s array
      const h2sMatch = jsonString.match(/"h2s"\s*:\s*\[([\s\S]*?)\]/);
      let h2s = [];
      if (h2sMatch) {
        const h2sContent = h2sMatch[1];
        const h2Matches = h2sContent.match(/"([^"]*(?:\\.[^"]*)*)"/g);
        if (h2Matches) {
          h2s = h2Matches.map(h => h.replace(/^"|"$/g, '').replace(/\\"/g, '"'));
        }
      }

      // Extract metaDescription
      const metaMatch = jsonString.match(/"metaDescription"\s*:\s*"([^"]*(?:\\.[^"]*)*)"/);
      const metaDescription = metaMatch ? metaMatch[1].replace(/\\"/g, '"') : '';

      // Extract htmlContent - this is the tricky one
      // Find the start of htmlContent value
      const htmlStartMatch = jsonString.match(/"htmlContent"\s*:\s*"/);
      if (!htmlStartMatch) {
        throw new Error('Could not find htmlContent field');
      }

      const htmlStartIndex = jsonString.indexOf(htmlStartMatch[0]) + htmlStartMatch[0].length;

      // Find the end by looking for the pattern that ends the htmlContent field
      // Look for ",\n  "metaDescription" or similar patterns
      let htmlEndIndex = jsonString.length - 1;

      // Try to find where htmlContent ends (before metaDescription or end of object)
      const metaDescPattern = /",\s*"metaDescription"/;
      const metaDescMatch = jsonString.substring(htmlStartIndex).match(metaDescPattern);
      if (metaDescMatch) {
        htmlEndIndex = htmlStartIndex + jsonString.substring(htmlStartIndex).indexOf(metaDescMatch[0]);
      } else {
        // If no metaDescription after, look for closing pattern
        const closingPattern = /"\s*\}\s*$/;
        const closingMatch = jsonString.substring(htmlStartIndex).match(closingPattern);
        if (closingMatch) {
          htmlEndIndex = htmlStartIndex + jsonString.substring(htmlStartIndex).lastIndexOf(closingMatch[0]);
        }
      }

      let htmlContent = jsonString.substring(htmlStartIndex, htmlEndIndex);
      // Unescape the HTML content
      htmlContent = htmlContent
        .replace(/\\n/g, '\n')
        .replace(/\\t/g, '\t')
        .replace(/\\"/g, '"')
        .replace(/\\\\/g, '\\');

      Logger.log('Field extraction successful!');
      Logger.log(`Title: ${title.substring(0, 50)}...`);
      Logger.log(`H2s count: ${h2s.length}`);
      Logger.log(`HTML content length: ${htmlContent.length}`);
      Logger.log(`Meta description: ${metaDescription.substring(0, 50)}...`);

      return {
        title: title,
        h1: h1,
        h2s: h2s,
        htmlContent: htmlContent,
        metaDescription: metaDescription
      };

    } catch (extractError) {
      Logger.log('Field extraction also failed: ' + extractError.toString());
      Logger.log('JSON string length: ' + jsonString.length);
      Logger.log('First 500 chars: ' + jsonString.substring(0, 500));
      Logger.log('Last 500 chars: ' + jsonString.substring(Math.max(0, jsonString.length - 500)));

      // Check if response was truncated
      if (responseData.stop_reason === 'max_tokens') {
        throw new Error('Claude response was truncated due to length. The content is too long. Try reducing target word count or simplifying requirements.');
      }

      throw new Error('Could not parse JSON from Claude response: ' + parseError.message + '. This may indicate the response was malformed or incomplete.');
    }
  }
}

/**
 * Build the Komplai context section for the content generation prompt
 * This injects company positioning, target audience, and pain points
 */
function buildKomplaiContextSection() {
  return `
ABOUT KOMPLAI (the company publishing this content):
${KOMPLAI_CONTEXT.companyDescription}

TARGET AUDIENCE:
- ${KOMPLAI_CONTEXT.targetAudience.revenueRange}
- ${KOMPLAI_CONTEXT.targetAudience.teamSize}
- Key roles: ${KOMPLAI_CONTEXT.targetAudience.roles.join(', ')}

PAIN POINTS YOUR READERS EXPERIENCE (reference these naturally when relevant):
${KOMPLAI_CONTEXT.clientPainPoints.map((p, i) => `${i + 1}. ${p}`).join('\n')}

VALUE PROPOSITIONS TO WEAVE IN (when naturally relevant to the topic):
${KOMPLAI_CONTEXT.valuePropositions.map(v => `- ${v}`).join('\n')}

NOTE: Do NOT turn this into a sales pitch. Reference these pain points and solutions only when they naturally fit the topic. The goal is authentic, helpful content that resonates with finance leaders.`;
}

/**
 * Post selected rows to WordPress
 */
function postSelectedToWordPress() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const selection = sheet.getActiveRange();
  const startRow = selection.getRow();
  const numRows = selection.getNumRows();

  for (let i = 0; i < numRows; i++) {
    const row = startRow + i;
    postToWordPress(sheet, row);
  }

  SpreadsheetApp.getUi().alert('WordPress posting complete!');
}

/**
 * Post all generated content to WordPress
 */
function postAllGeneratedToWordPress() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const lastRow = sheet.getLastRow();

  let posted = 0;
  for (let row = 2; row <= lastRow; row++) {
    const status = sheet.getRange(row, COLS.STATUS).getValue();
    if (status.includes(STATUS.GENERATED)) {
      postToWordPress(sheet, row);
      posted++;
    }
  }

  SpreadsheetApp.getUi().alert(`Posted ${posted} articles to WordPress!`);
}

/**
 * Post content to WordPress using REST API
 */
function postToWordPress(sheet, row) {
  try {
    // Step 1: Preparing
    sheet.getRange(row, COLS.STATUS).setValue('📤 Step 1/2: Preparing post...');
    SpreadsheetApp.flush();

    // Get data
    const title = sheet.getRange(row, COLS.GENERATED_TITLE).getValue();
    const content = sheet.getRange(row, COLS.CONTENT).getValue();
    const metaDesc = sheet.getRange(row, COLS.META_DESC).getValue();
    const keyword = sheet.getRange(row, COLS.KEYWORD).getValue();

    if (!title || !content) {
      sheet.getRange(row, COLS.STATUS).setValue(STATUS.ERROR + ': Missing content');
      return;
    }

    // Get WordPress credentials
    const wpUrl = PropertiesService.getScriptProperties().getProperty('WORDPRESS_SITE_URL');
    const wpUser = PropertiesService.getScriptProperties().getProperty('WORDPRESS_USERNAME');
    const wpPass = PropertiesService.getScriptProperties().getProperty('WORDPRESS_APP_PASSWORD');

    if (!wpUrl || !wpUser || !wpPass) {
      throw new Error('WordPress credentials not configured in Script Properties');
    }

    // Remove spaces from Application Password (WordPress.com format)
    const cleanPassword = wpPass.replace(/\s+/g, '');

    // Create post
    const postData = {
      title: title,
      content: content,
      status: 'draft', // Change to 'publish' to auto-publish
      excerpt: metaDesc
      // Note: tags removed - WordPress REST API requires tag IDs, not names
      // You can add tags manually in WordPress after posting
    };

    const options = {
      method: 'post',
      contentType: 'application/json',
      headers: {
        'Authorization': 'Basic ' + Utilities.base64Encode(wpUser + ':' + cleanPassword)
      },
      payload: JSON.stringify(postData),
      muteHttpExceptions: true
    };

    // Step 2: Publishing to WordPress
    sheet.getRange(row, COLS.STATUS).setValue('📤 Step 2/2: Publishing to WordPress...');
    SpreadsheetApp.flush();

    const response = UrlFetchApp.fetch(wpUrl + '/wp-json/wp/v2/posts', options);
    const responseData = JSON.parse(response.getContentText());

    if (response.getResponseCode() === 201) {
      // Success
      sheet.getRange(row, COLS.WP_URL).setValue(responseData.link);
      sheet.getRange(row, COLS.STATUS).setValue('✅ ' + STATUS.PUBLISHED);
    } else {
      throw new Error('WordPress API error: ' + (responseData.message || 'Unknown error'));
    }

  } catch (e) {
    sheet.getRange(row, COLS.STATUS).setValue(STATUS.ERROR + ': ' + e.message);
    Logger.log('Error posting to WordPress for row ' + row + ': ' + e.toString());
  }
}

/**
 * Optional: Add SEO analysis function
 */
function analyzeSEO(content, keyword) {
  const wordCount = content.split(/\s+/).length;
  const keywordCount = (content.toLowerCase().match(new RegExp(keyword.toLowerCase(), 'g')) || []).length;
  const keywordDensity = ((keywordCount / wordCount) * 100).toFixed(2);

  return {
    wordCount: wordCount,
    keywordCount: keywordCount,
    keywordDensity: keywordDensity + '%'
  };
}

/**
 * BACKLINKING AUTOMATION
 * Adds internal backlinks TO new content (not FROM old articles to new)
 * Internal links are added during content generation
 */

/**
 * Count links in HTML content
 */
function countLinks(html) {
  const matches = html.match(/<a\s+[^>]*href=/gi);
  return matches ? matches.length : 0;
}

/**
 * Convert [INTERNAL: ...] placeholders to actual links
 */
function convertInternalPlaceholdersToLinks(content, researchPlan) {
  if (!researchPlan || !researchPlan.backlinkingOpportunities) {
    return content;
  }

  let updatedContent = content;
  let linksAdded = 0;

  // Convert each [INTERNAL: anchor text] to an actual <a href> link
  researchPlan.backlinkingOpportunities.forEach(opp => {
    const placeholder = `[INTERNAL: ${opp.suggestedAnchorText}]`;
    const actualLink = `<a href="${opp.articleUrl}">${opp.suggestedAnchorText}</a>`;

    if (updatedContent.includes(placeholder)) {
      updatedContent = updatedContent.replace(placeholder, actualLink);
      linksAdded++;
    }
  });

  Logger.log(`Converted ${linksAdded} [INTERNAL: ...] placeholders to actual links`);
  return updatedContent;
}

/**
 * Add internal links to new content during generation
 */
function addInternalLinksToContent(newTitle, newKeyword, newContent, existingPosts) {
  const apiKey = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');

  // Limit to analyzing top 20 posts for cost efficiency
  const postsToAnalyze = existingPosts.slice(0, 20);

  const postsContext = postsToAnalyze.map((post, idx) =>
    `[${idx}] Title: ${post.title}\nURL: ${post.url}`
  ).join('\n');

  const prompt = `You are an SEO specialist adding internal links to a new blog post.

NEW ARTICLE:
Title: ${newTitle}
Keyword: ${newKeyword}
Content: ${newContent.substring(0, 2000)}...

EXISTING ARTICLES TO LINK TO:
${postsContext}

Task: Find 3-5 places in the NEW article where you should add natural internal links to EXISTING articles.

For each opportunity:
1. Find specific text in the new article that naturally relates to an existing article
2. The link should feel organic, not forced
3. Use relevant anchor text (5-10 words from the existing content)

Return ONLY valid JSON array:
[
  {
    "postIndex": 0,
    "anchorText": "exact text from new article to link",
    "reason": "why this is relevant"
  }
]

If no good opportunities exist, return empty array: []`;

  const payload = {
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 2000,
    messages: [{
      role: 'user',
      content: prompt
    }]
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01'
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', options);
  const responseData = JSON.parse(response.getContentText());

  if (responseData.error) {
    Logger.log('Claude API error in internal linking: ' + responseData.error.message);
    return newContent;
  }

  const contentText = responseData.content[0].text;
  const jsonMatch = contentText.match(/\[[\s\S]*\]/);

  if (!jsonMatch) {
    return newContent;
  }

  const suggestions = JSON.parse(jsonMatch[0]);

  if (suggestions.length === 0) {
    return newContent;
  }

  // Add links to the content
  let updatedContent = newContent;

  for (const suggestion of suggestions) {
    const targetPost = postsToAnalyze[suggestion.postIndex];
    if (!targetPost) continue;

    // Find and replace the anchor text with a link
    const anchorText = suggestion.anchorText;
    const linkedText = `<a href="${targetPost.url}">${anchorText}</a>`;

    // Only replace first occurrence to avoid over-linking
    updatedContent = updatedContent.replace(anchorText, linkedText);
  }

  return updatedContent;
}

/**
 * Remove any remaining placeholders from content
 * This ensures no placeholder text appears in the final published content
 */
function cleanupInternalPlaceholders(content) {
  let cleanedContent = content;

  // Remove [INTERNAL: anchor text] patterns
  cleanedContent = cleanedContent.replace(/\[INTERNAL:\s*[^\]]+\]/gi, '');

  // If there are unreplaced related article placeholders, remove the entire related articles section
  if (cleanedContent.includes('[RELATED_ARTICLE_PLACEHOLDER_')) {
    // Remove the entire related articles div if placeholders weren't replaced
    cleanedContent = cleanedContent.replace(/<div style="background: #f5f5f5;[^>]*>[\s\S]*?<\/div>/gi, '');
  }

  // Remove empty <p> tags that may be left after placeholder removal
  cleanedContent = cleanedContent.replace(/<p>\s*<\/p>/gi, '');

  return cleanedContent;
}

/**
 * Extract all image URLs from content
 */
function extractImageUrls(content) {
  const imgRegex = /<img[^>]+src="([^">]+)"/g;
  const urls = [];
  let match;

  while ((match = imgRegex.exec(content)) !== null) {
    urls.push(match[1]);
  }

  return urls;
}

/**
 * Get all used images from existing WordPress posts
 * Returns a Set of Unsplash photo IDs (not full URLs)
 */
function getUsedImages(existingPosts) {
  const usedPhotoIds = new Set();

  existingPosts.forEach(post => {
    const images = extractImageUrls(post.content);
    images.forEach(imgUrl => {
      // Extract photo ID from Unsplash URL
      // Example: https://images.unsplash.com/photo-1557804506-069f1546344a?w=1600...
      // Extract: 1557804506-069f1546344a
      const photoIdMatch = imgUrl.match(/photo-([^?&]+)/);
      if (photoIdMatch) {
        usedPhotoIds.add(photoIdMatch[1]);
      }
    });
  });

  return usedPhotoIds;
}

/**
 * Populate related articles section with actual WordPress posts (text links only)
 */
function addRelatedArticles(content, existingPosts, currentKeyword) {
  // Check if content has the related articles placeholders
  if (!content.includes('[RELATED_ARTICLE_PLACEHOLDER_1]')) {
    return content;
  }

  // Get the first 2 most relevant posts based on title similarity
  const relatedPosts = existingPosts.slice(0, 2);

  let updatedContent = content;

  if (relatedPosts.length === 0) {
    // If no posts available, show a placeholder message instead of removing the section
    const placeholderMessage = `<p style="color: #666; font-style: italic;">More articles coming soon! Subscribe to stay updated with our latest insights.</p>`;
    updatedContent = updatedContent.replace('[RELATED_ARTICLE_PLACEHOLDER_1]', placeholderMessage);
    updatedContent = updatedContent.replace('<p>[RELATED_ARTICLE_PLACEHOLDER_2]</p>', '');
    return updatedContent;
  }

  // Create text links with descriptions for related articles
  relatedPosts.forEach((post, index) => {
    const placeholderNum = index + 1;
    const placeholder = `[RELATED_ARTICLE_PLACEHOLDER_${placeholderNum}]`;

    // Extract first sentence or first 150 characters from post excerpt/title as description
    let description = '';
    if (post.excerpt) {
      // Remove HTML tags from excerpt
      description = post.excerpt.replace(/<[^>]*>/g, '').trim();
      // Get first sentence or first 150 chars
      const firstSentence = description.match(/^[^.!?]+[.!?]/);
      description = firstSentence ? firstSentence[0] : description.substring(0, 150) + '...';
    } else {
      // Generate a description from the title
      description = `Learn more about ${post.title.toLowerCase()}.`;
    }

    // Create hyperlinked title with description
    const articleBlock = `<a href="${post.url}" style="font-weight: bold; color: #0066cc; text-decoration: underline;">${post.title}</a>
${description}`;

    updatedContent = updatedContent.replace(placeholder, articleBlock);
  });

  // If only one post, remove the second placeholder
  if (relatedPosts.length === 1) {
    updatedContent = updatedContent.replace('<p>[RELATED_ARTICLE_PLACEHOLDER_2]</p>', '');
  }

  return updatedContent;
}

/**
 * Add internal links to selected row (BEFORE publishing to WordPress)
 * This updates the content in the sheet with links to existing articles
 */
function addBacklinksForSelected() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const row = sheet.getActiveRange().getRow();

  if (row < 2) {
    SpreadsheetApp.getUi().alert('Please select a content row (not the header)');
    return;
  }

  const status = sheet.getRange(row, COLS.STATUS).getValue();

  // Check if content has been generated (check if status contains "Generated" or "Published")
  if (!status.includes(STATUS.GENERATED) && !status.includes(STATUS.PUBLISHED)) {
    SpreadsheetApp.getUi().alert('Error', 'Content must be generated first. Run "Generate Content" before adding backlinks.', SpreadsheetApp.getUi().ButtonSet.OK);
    return;
  }

  // Get the generated content
  const title = sheet.getRange(row, COLS.GENERATED_TITLE).getValue();
  const keyword = sheet.getRange(row, COLS.KEYWORD).getValue();
  const currentContent = sheet.getRange(row, COLS.CONTENT).getValue();

  if (!title || !currentContent) {
    SpreadsheetApp.getUi().alert('Error', 'No generated content found for this row.', SpreadsheetApp.getUi().ButtonSet.OK);
    return;
  }

  try {
    // Step 1: Fetching WordPress posts
    sheet.getRange(row, COLS.STATUS).setValue('🔗 Step 1/3: Fetching WordPress posts...');
    SpreadsheetApp.flush();

    // Fetch existing WordPress posts
    const existingPosts = fetchAllWordPressPosts();

    if (existingPosts.length === 0) {
      sheet.getRange(row, COLS.BACKLINKS_ADDED).setValue('No existing posts found');
      sheet.getRange(row, COLS.STATUS).setValue(STATUS.GENERATED);
      SpreadsheetApp.getUi().alert('No existing WordPress posts found to link to.');
      return;
    }

    // Step 2: Adding internal links
    sheet.getRange(row, COLS.STATUS).setValue('🔗 Step 2/3: Adding internal links...');
    SpreadsheetApp.flush();

    // Add internal links to the content
    let updatedContent = addInternalLinksToContent(
      title,
      keyword,
      currentContent,
      existingPosts
    );

    // Step 3: Adding related articles
    sheet.getRange(row, COLS.STATUS).setValue('🔗 Step 3/3: Adding related articles...');
    SpreadsheetApp.flush();

    // Add related articles section with thumbnails
    updatedContent = addRelatedArticles(updatedContent, existingPosts, keyword);

    // Clean up any remaining [INTERNAL: ...] placeholders
    updatedContent = cleanupInternalPlaceholders(updatedContent);

    const linksAdded = countLinks(updatedContent) - countLinks(currentContent);

    // Check content length - Google Sheets has a 50,000 character limit per cell
    const MAX_CELL_CHARS = 50000;
    if (updatedContent.length > MAX_CELL_CHARS) {
      Logger.log(`Warning: Content is ${updatedContent.length} characters, exceeds ${MAX_CELL_CHARS} limit. Truncating...`);
      updatedContent = updatedContent.substring(0, MAX_CELL_CHARS - 100) + '\n\n<!-- CONTENT TRUNCATED: Original was ' + updatedContent.length + ' characters. -->';
    }

    // Update the sheet with new content containing links and related articles
    sheet.getRange(row, COLS.CONTENT).setValue(updatedContent);
    sheet.getRange(row, COLS.BACKLINKS_ADDED).setValue(`Added ${linksAdded} internal links + related articles`);
    sheet.getRange(row, COLS.STATUS).setValue('✅ ' + STATUS.GENERATED);

    SpreadsheetApp.getUi().alert(
      'Success!',
      `Added ${linksAdded} internal links and related articles carousel to your content.\n\nThe content in Column H has been updated.\n\nReview the content, then click "Post to WordPress" when ready.`,
      SpreadsheetApp.getUi().ButtonSet.OK
    );

  } catch (e) {
    sheet.getRange(row, COLS.BACKLINKS_ADDED).setValue('Error: ' + e.message);
    sheet.getRange(row, COLS.STATUS).setValue(STATUS.GENERATED);
    SpreadsheetApp.getUi().alert('Error', 'Failed to add internal links: ' + e.message, SpreadsheetApp.getUi().ButtonSet.OK);
    Logger.log('Error adding internal links for row ' + row + ': ' + e.toString());
  }
}

/**
 * Main backlinking function
 */
function addBacklinks(sheet, row) {
  try {
    // Update status
    const currentStatus = sheet.getRange(row, COLS.STATUS).getValue();
    sheet.getRange(row, COLS.STATUS).setValue('Adding backlinks...');
    SpreadsheetApp.flush();

    // Get new article details
    const newArticleTitle = sheet.getRange(row, COLS.GENERATED_TITLE).getValue();
    const newArticleUrl = sheet.getRange(row, COLS.WP_URL).getValue();
    const newArticleKeyword = sheet.getRange(row, COLS.KEYWORD).getValue();
    const newArticleContent = sheet.getRange(row, COLS.CONTENT).getValue();

    // Extract post ID from URL
    const postId = extractPostIdFromUrl(newArticleUrl);

    // Fetch all existing WordPress posts
    const existingPosts = fetchAllWordPressPosts();

    if (existingPosts.length === 0) {
      sheet.getRange(row, COLS.BACKLINKS_ADDED).setValue('No existing posts found');
      sheet.getRange(row, COLS.STATUS).setValue(currentStatus);
      return;
    }

    // Use Claude to find best articles to add backlinks from
    const backlinkSuggestions = findBacklinkOpportunities(
      newArticleTitle,
      newArticleKeyword,
      newArticleContent,
      existingPosts,
      postId
    );

    // Add backlinks to those articles
    const updatedArticles = [];
    for (const suggestion of backlinkSuggestions) {
      const success = addBacklinkToPost(
        suggestion.postId,
        suggestion.anchorText,
        newArticleUrl,
        suggestion.insertionPoint
      );

      if (success) {
        updatedArticles.push(suggestion.postTitle);
      }
    }

    // Update sheet with results
    if (updatedArticles.length > 0) {
      sheet.getRange(row, COLS.BACKLINKS_ADDED).setValue(
        `Added to ${updatedArticles.length} posts: ${updatedArticles.join(', ')}`
      );
    } else {
      sheet.getRange(row, COLS.BACKLINKS_ADDED).setValue('No suitable backlink opportunities found');
    }

    sheet.getRange(row, COLS.STATUS).setValue(currentStatus);

  } catch (e) {
    sheet.getRange(row, COLS.BACKLINKS_ADDED).setValue('Error: ' + e.message);
    Logger.log('Error adding backlinks for row ' + row + ': ' + e.toString());
  }
}

/**
 * Fetch all posts from WordPress
 */
function fetchAllWordPressPosts() {
  const wpUrl = PropertiesService.getScriptProperties().getProperty('WORDPRESS_SITE_URL');
  const wpUser = PropertiesService.getScriptProperties().getProperty('WORDPRESS_USERNAME');
  const wpPass = PropertiesService.getScriptProperties().getProperty('WORDPRESS_APP_PASSWORD');
  const cleanPassword = wpPass.replace(/\s+/g, '');

  const allPosts = [];
  let page = 1;
  let hasMore = true;

  while (hasMore && page <= 10) { // Limit to 10 pages (100 posts per page = 1000 posts max)
    const options = {
      method: 'get',
      headers: {
        'Authorization': 'Basic ' + Utilities.base64Encode(wpUser + ':' + cleanPassword)
      },
      muteHttpExceptions: true
    };

    const response = UrlFetchApp.fetch(
      wpUrl + '/wp-json/wp/v2/posts?per_page=100&page=' + page + '&status=publish',
      options
    );

    if (response.getResponseCode() === 200) {
      const posts = JSON.parse(response.getContentText());

      if (posts.length === 0) {
        hasMore = false;
      } else {
        allPosts.push(...posts.map(post => ({
          id: post.id,
          title: post.title.rendered,
          content: post.content.rendered,
          url: post.link
        })));
        page++;
      }
    } else {
      hasMore = false;
    }
  }

  return allPosts;
}

/**
 * Use Claude to find best backlink opportunities
 */
function findBacklinkOpportunities(newTitle, newKeyword, newContent, existingPosts, excludePostId) {
  const apiKey = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');

  // Limit to analyzing top 20 most recent posts for cost efficiency
  const postsToAnalyze = existingPosts
    .filter(post => post.id !== excludePostId)
    .slice(0, 20);

  const postsContext = postsToAnalyze.map((post, idx) =>
    `[${idx}] Title: ${post.title}\nURL: ${post.url}\nExcerpt: ${post.content.substring(0, 500)}...`
  ).join('\n\n');

  const prompt = `You are an SEO specialist analyzing internal linking opportunities.

NEW ARTICLE:
Title: ${newTitle}
Keyword: ${newKeyword}
Content excerpt: ${newContent.substring(0, 800)}...

EXISTING ARTICLES:
${postsContext}

Find the 3-5 BEST existing articles that should link to this new article. For each:
1. It should be topically relevant
2. The backlink should feel natural, not forced
3. Suggest specific anchor text (5-10 words)
4. Suggest where in the content to insert it (beginning, middle, or end)

Return ONLY valid JSON array:
[
  {
    "postIndex": 0,
    "postTitle": "Article title",
    "anchorText": "suggested anchor text here",
    "insertionPoint": "middle",
    "relevanceReason": "brief reason why this is a good match"
  }
]

If no good opportunities exist, return empty array: []`;

  const payload = {
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 2000,
    messages: [{
      role: 'user',
      content: prompt
    }]
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01'
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', options);
  const responseData = JSON.parse(response.getContentText());

  if (responseData.error) {
    throw new Error('Claude API error: ' + responseData.error.message);
  }

  const contentText = responseData.content[0].text;
  const jsonMatch = contentText.match(/\[[\s\S]*\]/);

  if (!jsonMatch) {
    return [];
  }

  const suggestions = JSON.parse(jsonMatch[0]);

  // Map back to actual post IDs
  return suggestions.map(sugg => ({
    postId: postsToAnalyze[sugg.postIndex].id,
    postTitle: sugg.postTitle,
    anchorText: sugg.anchorText,
    insertionPoint: sugg.insertionPoint
  }));
}

/**
 * Add a backlink to an existing WordPress post
 */
function addBacklinkToPost(postId, anchorText, targetUrl, insertionPoint) {
  try {
    const wpUrl = PropertiesService.getScriptProperties().getProperty('WORDPRESS_SITE_URL');
    const wpUser = PropertiesService.getScriptProperties().getProperty('WORDPRESS_USERNAME');
    const wpPass = PropertiesService.getScriptProperties().getProperty('WORDPRESS_APP_PASSWORD');
    const cleanPassword = wpPass.replace(/\s+/g, '');

    // Fetch the existing post
    const fetchOptions = {
      method: 'get',
      headers: {
        'Authorization': 'Basic ' + Utilities.base64Encode(wpUser + ':' + cleanPassword)
      },
      muteHttpExceptions: true
    };

    const fetchResponse = UrlFetchApp.fetch(
      wpUrl + '/wp-json/wp/v2/posts/' + postId,
      fetchOptions
    );

    if (fetchResponse.getResponseCode() !== 200) {
      return false;
    }

    const post = JSON.parse(fetchResponse.getContentText());
    let content = post.content.rendered;

    // Create the backlink HTML
    const backlinkHtml = `<a href="${targetUrl}">${anchorText}</a>`;

    // Insert the backlink based on insertion point
    const paragraphs = content.split('</p>');
    let insertIndex;

    if (insertionPoint === 'beginning') {
      insertIndex = 1; // After first paragraph
    } else if (insertionPoint === 'end') {
      insertIndex = paragraphs.length - 2; // Before last paragraph
    } else { // middle
      insertIndex = Math.floor(paragraphs.length / 2);
    }

    // Insert a new paragraph with the backlink
    paragraphs.splice(insertIndex, 0, `<p>Related: ${backlinkHtml}</p>`);
    const updatedContent = paragraphs.join('</p>');

    // Update the post
    const updateData = {
      content: updatedContent
    };

    const updateOptions = {
      method: 'post',
      contentType: 'application/json',
      headers: {
        'Authorization': 'Basic ' + Utilities.base64Encode(wpUser + ':' + cleanPassword)
      },
      payload: JSON.stringify(updateData),
      muteHttpExceptions: true
    };

    const updateResponse = UrlFetchApp.fetch(
      wpUrl + '/wp-json/wp/v2/posts/' + postId,
      updateOptions
    );

    return updateResponse.getResponseCode() === 200;

  } catch (e) {
    Logger.log('Error adding backlink to post ' + postId + ': ' + e.toString());
    return false;
  }
}

/**
 * Extract post ID from WordPress URL
 */
function extractPostIdFromUrl(url) {
  // Try to extract from URL patterns
  const match = url.match(/\/(\d+)\/?$/);
  if (match) {
    return parseInt(match[1]);
  }

  // For WordPress.com, fetch the post by slug
  const wpUrl = PropertiesService.getScriptProperties().getProperty('WORDPRESS_SITE_URL');
  const wpUser = PropertiesService.getScriptProperties().getProperty('WORDPRESS_USERNAME');
  const wpPass = PropertiesService.getScriptProperties().getProperty('WORDPRESS_APP_PASSWORD');
  const cleanPassword = wpPass.replace(/\s+/g, '');

  const slug = url.split('/').filter(part => part).pop();

  const options = {
    method: 'get',
    headers: {
      'Authorization': 'Basic ' + Utilities.base64Encode(wpUser + ':' + cleanPassword)
    },
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(
    wpUrl + '/wp-json/wp/v2/posts?slug=' + slug,
    options
  );

  if (response.getResponseCode() === 200) {
    const posts = JSON.parse(response.getContentText());
    if (posts.length > 0) {
      return posts[0].id;
    }
  }

  return null;
}

/**
 * ==========================================
 * COMPREHENSIVE TESTING & VALIDATION
 * ==========================================
 * Run these tests before generating content
 */

/**
 * Run all sanity checks before content generation
 * Tests API connections, WordPress setup, and content validation
 */
function runSanityTests() {
  const ui = SpreadsheetApp.getUi();
  const results = [];
  let allPassed = true;

  // Test 1: Check Script Properties
  results.push('\n📋 TEST 1: Script Properties');
  const apiKey = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');
  const wpUrl = PropertiesService.getScriptProperties().getProperty('WORDPRESS_SITE_URL');
  const wpUser = PropertiesService.getScriptProperties().getProperty('WORDPRESS_USERNAME');
  const wpPass = PropertiesService.getScriptProperties().getProperty('WORDPRESS_APP_PASSWORD');

  if (!apiKey) {
    results.push('❌ ANTHROPIC_API_KEY is missing');
    allPassed = false;
  } else {
    results.push('✅ ANTHROPIC_API_KEY is set');
  }

  if (!wpUrl) {
    results.push('❌ WORDPRESS_SITE_URL is missing');
    allPassed = false;
  } else {
    results.push(`✅ WORDPRESS_SITE_URL: ${wpUrl}`);
  }

  if (!wpUser) {
    results.push('❌ WORDPRESS_USERNAME is missing');
    allPassed = false;
  } else {
    results.push('✅ WORDPRESS_USERNAME is set');
  }

  if (!wpPass) {
    results.push('❌ WORDPRESS_APP_PASSWORD is missing');
    allPassed = false;
  } else {
    results.push('✅ WORDPRESS_APP_PASSWORD is set');
  }

  // Test 2: Claude API Connection
  results.push('\n🤖 TEST 2: Claude API Connection');
  if (apiKey) {
    try {
      const testPayload = {
        model: 'claude-sonnet-4-5-20250929',
        max_tokens: 50,
        messages: [{
          role: 'user',
          content: 'Reply with just the word "success"'
        }]
      };

      const options = {
        method: 'post',
        contentType: 'application/json',
        headers: {
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01'
        },
        payload: JSON.stringify(testPayload),
        muteHttpExceptions: true
      };

      const response = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', options);
      const responseData = JSON.parse(response.getContentText());

      if (responseData.error) {
        results.push(`❌ Claude API Error: ${responseData.error.message}`);
        allPassed = false;
      } else {
        results.push('✅ Claude API connection successful');
      }
    } catch (e) {
      results.push(`❌ Claude API connection failed: ${e.toString()}`);
      if (e.toString().includes('Address unavailable')) {
        results.push('   💡 This error means Google Apps Script cannot reach api.anthropic.com');
        results.push('   Try these solutions:');
        results.push('   1. Wait a few minutes and try again (temporary network issue)');
        results.push('   2. Check if you can access https://api.anthropic.com in your browser');
        results.push('   3. Re-authorize the script (Extensions > Apps Script > Run > setup)');
        results.push('   4. This may be a temporary Google Apps Script outage');
      }
      allPassed = false;
    }
  } else {
    results.push('⚠️ Skipped (no API key)');
  }

  // Test 3: WordPress API Connection
  results.push('\n🌐 TEST 3: WordPress API Connection');
  if (wpUrl && wpUser && wpPass) {
    try {
      const cleanPassword = wpPass.replace(/\s+/g, '');
      const authHeader = 'Basic ' + Utilities.base64Encode(wpUser + ':' + cleanPassword);

      const options = {
        method: 'get',
        headers: {
          'Authorization': authHeader
        },
        muteHttpExceptions: true
      };

      const response = UrlFetchApp.fetch(
        wpUrl.replace(/\/$/, '') + '/wp-json/wp/v2/posts?per_page=1',
        options
      );

      const responseCode = response.getResponseCode();
      if (responseCode === 200) {
        results.push('✅ WordPress API connection successful');
        const posts = JSON.parse(response.getContentText());
        results.push(`   Found ${posts.length > 0 ? 'existing posts' : 'no posts yet'}`);
      } else if (responseCode === 401) {
        results.push('❌ WordPress authentication failed (401)');
        results.push('   Check your username and application password');
        allPassed = false;
      } else {
        results.push(`❌ WordPress API returned status ${responseCode}`);
        allPassed = false;
      }
    } catch (e) {
      results.push(`❌ WordPress connection failed: ${e.toString()}`);
      allPassed = false;
    }
  } else {
    results.push('⚠️ Skipped (WordPress credentials missing)');
  }

  // Test 4: Sheet Structure Validation
  results.push('\n📊 TEST 4: Sheet Structure');
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const headers = sheet.getRange(1, 1, 1, 12).getValues()[0];

  const expectedHeaders = {
    1: 'Keyword',
    2: 'Secondary Keywords',
    3: 'Search Intent',
    4: 'Word Count',
    5: 'Category',
    6: 'Generated Title',
    7: 'H1',
    8: 'Content',
    9: 'Meta Description',
    10: 'WP URL',
    11: 'Backlinks Added',
    12: 'Status'
  };

  let headersCorrect = true;
  for (const [col, expectedHeader] of Object.entries(expectedHeaders)) {
    const actualHeader = headers[col - 1];
    if (actualHeader !== expectedHeader) {
      results.push(`❌ Column ${col}: Expected "${expectedHeader}", found "${actualHeader}"`);
      headersCorrect = false;
      allPassed = false;
    }
  }

  if (headersCorrect) {
    results.push('✅ All column headers are correct');
  }

  // Test 5: Content Validation (if rows exist)
  results.push('\n🔍 TEST 5: Content Validation');
  const lastRow = sheet.getLastRow();
  let content = ''; // Declare content outside the block so Test 6 can access it
  let postUrl = ''; // WordPress post URL from the sheet (different from wpUrl which is the site URL)

  if (lastRow > 1) {
    // Check first content row
    const testRow = 2;
    const keyword = sheet.getRange(testRow, COLS.KEYWORD).getValue();
    content = sheet.getRange(testRow, COLS.CONTENT).getValue();
    postUrl = sheet.getRange(testRow, COLS.WP_URL).getValue();

    if (keyword) {
      results.push(`✅ Found test data in row ${testRow}: "${keyword}"`);

      if (content) {
        // Validate placeholder conversion
        if (content.includes('[INTERNAL:')) {
          results.push(`⚠️ Warning: Content contains unconverted [INTERNAL:...] placeholders`);
        } else {
          results.push('✅ No [INTERNAL:...] placeholders found');
        }

        // Validate Related Articles placeholders
        if (content.includes('[RELATED_ARTICLE_PLACEHOLDER_')) {
          results.push('⚠️ Warning: Content contains unconverted [RELATED_ARTICLE_PLACEHOLDER_...] placeholders');
        } else {
          results.push('✅ No [RELATED_ARTICLE_PLACEHOLDER_...] placeholders found');
        }

        // Check for actual links
        const linkMatches = content.match(/<a href=/g);
        if (linkMatches) {
          results.push(`✅ Found ${linkMatches.length} hyperlinks in content`);
        } else {
          results.push('⚠️ Warning: No hyperlinks found in content');
        }

        // Check sentence length (sample first 500 words)
        const textContent = content.replace(/<[^>]*>/g, ' ').substring(0, 2000);
        const sentences = textContent.split(/[.!?]+/).filter(s => s.trim().length > 0);
        const longSentences = sentences.filter(s => s.split(/\s+/).length > 20);
        const longSentencePercent = (longSentences.length / sentences.length * 100).toFixed(1);

        if (longSentencePercent > 35) {
          results.push(`⚠️ Warning: ${longSentencePercent}% of sentences are over 20 words (should be <35%)`);
        } else {
          results.push(`✅ Sentence length good: ${longSentencePercent}% over 20 words`);
        }

        // Check for em-dashes
        if (content.includes('—') || content.includes('–')) {
          results.push('⚠️ Warning: Content contains em-dashes or en-dashes');
        } else {
          results.push('✅ No em-dashes found');
        }
      }

      if (postUrl) {
        results.push(`✅ WordPress URL: ${postUrl}`);
      }
    } else {
      results.push('ℹ️ No test data found (sheet is empty)');
    }
  } else {
    results.push('ℹ️ No content rows to validate');
  }

  // Test 6: Image Validation
  results.push('\n🖼️ TEST 6: Image Validation');
  if (content && content.includes('images.unsplash.com')) {
    const imgMatches = content.match(/images\.unsplash\.com\/photo-([^?]+)/g);
    if (imgMatches) {
      results.push(`✅ Found ${imgMatches.length} Unsplash image(s)`);

      // Check for placeholder photo IDs
      if (content.includes('PHOTO_ID_HERE') || content.includes('[SPECIFIC_PHOTO_ID]')) {
        results.push('❌ ERROR: Content contains placeholder photo ID - not replaced!');
        allPassed = false;
      } else {
        results.push('✅ No placeholder photo IDs found');
      }

      // Extract and display photo IDs
      const photoIds = [];
      imgMatches.forEach(match => {
        const idMatch = match.match(/photo-([^?]+)/);
        if (idMatch) {
          photoIds.push(idMatch[1]);
        }
      });
      results.push(`   Photo IDs: ${photoIds.join(', ')}`);
    }
  } else {
    results.push('ℹ️ No images to validate');
  }

  // Final Summary
  results.push('\n' + '='.repeat(50));
  if (allPassed) {
    results.push('✅ ALL TESTS PASSED - Safe to generate content!');
  } else {
    results.push('❌ SOME TESTS FAILED - Fix issues before generating content');
  }
  results.push('='.repeat(50));

  // Display results
  const resultText = results.join('\n');
  Logger.log(resultText);

  // Show in UI dialog
  const htmlOutput = HtmlService.createHtmlOutput(`
    <div style="font-family: monospace; white-space: pre-wrap; padding: 15px; font-size: 12px;">
${resultText}
    </div>
  `)
    .setWidth(700)
    .setHeight(600);

  ui.showModalDialog(htmlOutput, 'Sanity Test Results');

  return allPassed;
}

/**
 * Quick test - just validates API keys and WordPress connection
 */
function quickTest() {
  const ui = SpreadsheetApp.getUi();
  const results = [];

  // Test Claude API
  const apiKey = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');
  if (!apiKey) {
    results.push('❌ ANTHROPIC_API_KEY is missing');
  } else {
    results.push('✅ Claude API key is set');
  }

  // Test WordPress
  const wpUrl = PropertiesService.getScriptProperties().getProperty('WORDPRESS_SITE_URL');
  const wpUser = PropertiesService.getScriptProperties().getProperty('WORDPRESS_USERNAME');
  const wpPass = PropertiesService.getScriptProperties().getProperty('WORDPRESS_APP_PASSWORD');

  if (!wpUrl || !wpUser || !wpPass) {
    results.push('❌ WordPress credentials incomplete');
  } else {
    results.push('✅ WordPress credentials are set');
  }

  ui.alert('Quick Test Results', results.join('\n'), ui.ButtonSet.OK);
}
