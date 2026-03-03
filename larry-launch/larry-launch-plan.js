const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak
} = require("docx");

// ============================================================
// COLOR PALETTE & CONSTANTS
// ============================================================
const COLORS = {
  primary: "1B2A4A",      // Deep navy
  accent: "E85D26",       // Komplai orange
  darkGray: "333333",
  medGray: "666666",
  lightGray: "F5F5F5",
  tableHeader: "1B2A4A",
  tableHeaderText: "FFFFFF",
  tableAlt: "F0F4FA",
  red: "CC3333",
  green: "2D7D46",
  yellow: "D4A017",
  white: "FFFFFF",
};

const CONTENT_WIDTH = 9360; // US Letter 1" margins
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

// ============================================================
// HELPER FUNCTIONS
// ============================================================
function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200 },
    children: [new TextRun({ text, bold: true, size: 36, font: "Arial", color: COLORS.primary })],
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 160 },
    children: [new TextRun({ text, bold: true, size: 28, font: "Arial", color: COLORS.primary })],
  });
}

function heading3(text) {
  return new Paragraph({
    spacing: { before: 200, after: 120 },
    children: [new TextRun({ text, bold: true, size: 24, font: "Arial", color: COLORS.accent })],
  });
}

function para(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 160, line: 276 },
    ...opts,
    children: [new TextRun({ text, size: 22, font: "Arial", color: opts.color || COLORS.darkGray })],
  });
}

function boldPara(boldText, normalText, opts = {}) {
  return new Paragraph({
    spacing: { after: 160, line: 276 },
    ...opts,
    children: [
      new TextRun({ text: boldText, bold: true, size: 22, font: "Arial", color: opts.color || COLORS.darkGray }),
      new TextRun({ text: normalText, size: 22, font: "Arial", color: opts.color || COLORS.darkGray }),
    ],
  });
}

function bulletItem(text, reference = "bullets", level = 0) {
  return new Paragraph({
    numbering: { reference, level },
    spacing: { after: 80, line: 276 },
    children: [new TextRun({ text, size: 22, font: "Arial", color: COLORS.darkGray })],
  });
}

function boldBulletItem(boldText, normalText, reference = "bullets", level = 0) {
  return new Paragraph({
    numbering: { reference, level },
    spacing: { after: 80, line: 276 },
    children: [
      new TextRun({ text: boldText, bold: true, size: 22, font: "Arial", color: COLORS.darkGray }),
      new TextRun({ text: normalText, size: 22, font: "Arial", color: COLORS.darkGray }),
    ],
  });
}

function numItem(text, reference = "numbers1", level = 0) {
  return new Paragraph({
    numbering: { reference, level },
    spacing: { after: 80, line: 276 },
    children: [new TextRun({ text, size: 22, font: "Arial", color: COLORS.darkGray })],
  });
}

function boldNumItem(boldText, normalText, reference = "numbers1", level = 0) {
  return new Paragraph({
    numbering: { reference, level },
    spacing: { after: 80, line: 276 },
    children: [
      new TextRun({ text: boldText, bold: true, size: 22, font: "Arial", color: COLORS.darkGray }),
      new TextRun({ text: normalText, size: 22, font: "Arial", color: COLORS.darkGray }),
    ],
  });
}

function calloutBox(title, bodyText) {
  const cellWidth = CONTENT_WIDTH;
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [cellWidth],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            width: { size: cellWidth, type: WidthType.DXA },
            borders: {
              top: { style: BorderStyle.SINGLE, size: 2, color: COLORS.accent },
              bottom: { style: BorderStyle.SINGLE, size: 2, color: COLORS.accent },
              left: { style: BorderStyle.SINGLE, size: 6, color: COLORS.accent },
              right: { style: BorderStyle.SINGLE, size: 2, color: COLORS.accent },
            },
            shading: { fill: "FFF5F0", type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 200, right: 200 },
            children: [
              new Paragraph({
                spacing: { after: 80 },
                children: [new TextRun({ text: title, bold: true, size: 22, font: "Arial", color: COLORS.accent })],
              }),
              new Paragraph({
                spacing: { after: 0 },
                children: [new TextRun({ text: bodyText, size: 20, font: "Arial", color: COLORS.darkGray })],
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

function tableRow(cells, isHeader = false) {
  const colWidth = Math.floor(CONTENT_WIDTH / cells.length);
  return new TableRow({
    children: cells.map((text, i) =>
      new TableCell({
        width: { size: i === cells.length - 1 ? CONTENT_WIDTH - colWidth * (cells.length - 1) : colWidth, type: WidthType.DXA },
        borders,
        shading: { fill: isHeader ? COLORS.tableHeader : "FFFFFF", type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        verticalAlign: "center",
        children: [
          new Paragraph({
            spacing: { after: 0 },
            children: [
              new TextRun({
                text,
                bold: isHeader,
                size: 20,
                font: "Arial",
                color: isHeader ? COLORS.tableHeaderText : COLORS.darkGray,
              }),
            ],
          }),
        ],
      })
    ),
  });
}

function simpleTable(headers, rows) {
  const colWidth = Math.floor(CONTENT_WIDTH / headers.length);
  const colWidths = headers.map((_, i) => i === headers.length - 1 ? CONTENT_WIDTH - colWidth * (headers.length - 1) : colWidth);
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      tableRow(headers, true),
      ...rows.map((r) => tableRow(r, false)),
    ],
  });
}

function spacer(pts = 120) {
  return new Paragraph({ spacing: { after: pts }, children: [] });
}

// ============================================================
// DOCUMENT
// ============================================================
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Arial", size: 22 } },
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: COLORS.primary },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 },
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: COLORS.primary },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 },
      },
    ],
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
          { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
        ],
      },
      {
        reference: "numbers1",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
      },
      {
        reference: "numbers2",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
      },
      {
        reference: "numbers3",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
      },
      {
        reference: "numbers4",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
      },
      {
        reference: "numbers5",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
      },
      {
        reference: "numbers6",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
      },
      {
        reference: "numbers7",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
      },
      {
        reference: "numbers8",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
      },
      {
        reference: "numbers9",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
      },
    ],
  },
  sections: [
    // ============================================================
    // TITLE PAGE
    // ============================================================
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      children: [
        spacer(2400),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "PROJECT HAIL MARY", size: 56, bold: true, font: "Arial", color: COLORS.primary })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [new TextRun({ text: "Larry Self-Serve Launch Plan", size: 36, font: "Arial", color: COLORS.accent })],
        }),
        spacer(200),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "April 1, 2026", size: 28, font: "Arial", color: COLORS.medGray })],
        }),
        spacer(600),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Prepared: February 14, 2026", size: 22, font: "Arial", color: COLORS.medGray })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Classification: Internal / Confidential", size: 22, font: "Arial", color: COLORS.medGray })],
        }),
        spacer(800),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 0 },
          children: [new TextRun({ text: "This document is a critical assessment.", size: 20, italics: true, font: "Arial", color: COLORS.medGray })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "It prioritizes honesty over optimism.", size: 20, italics: true, font: "Arial", color: COLORS.medGray })],
        }),
      ],
    },

    // ============================================================
    // MAIN CONTENT
    // ============================================================
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      headers: {
        default: new Header({
          children: [
            new Paragraph({
              alignment: AlignmentType.RIGHT,
              children: [new TextRun({ text: "KOMPLAI | Project Hail Mary | Confidential", size: 16, font: "Arial", color: COLORS.medGray, italics: true })],
            }),
          ],
        }),
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [
                new TextRun({ text: "Page ", size: 18, font: "Arial", color: COLORS.medGray }),
                new TextRun({ children: [PageNumber.CURRENT], size: 18, font: "Arial", color: COLORS.medGray }),
              ],
            }),
          ],
        }),
      },
      children: [
        // ============================================================
        // SECTION 0: EXECUTIVE SUMMARY
        // ============================================================
        heading1("Executive Summary"),

        para("This plan addresses three questions: how to execute the Larry self-serve launch on April 1 without catastrophic failure, how to build a realistic path toward $1M in revenue over the following 6 months, and what mistakes would kill the launch before it starts."),

        calloutBox(
          "The Hard Truth Up Front",
          "Your current plan, as documented in Project Hail Mary, will not generate $1M in 6 months through self-serve alone. The math does not support it at the projected conversion rates, traffic volumes, and budget constraints. This is not a reason to abandon the launch. It is a reason to restructure expectations and build a plan that actually works: one where self-serve revenue is one of three revenue streams, not the only one."
        ),
        spacer(120),

        para("The recommended approach uses Larry as the top-of-funnel wedge (as intended), but restructures the revenue target across three streams: self-serve subscriptions ($150K-$250K), sales-assisted Growth/Enterprise deals ($400K-$600K), and partner-channel revenue ($150K-$250K). This gives you a credible path to $700K-$1.1M without depending on any single channel to perform miraculously."),

        // ============================================================
        // SECTION 1: THE REVENUE MATH
        // ============================================================
        heading1("Part 1: The Revenue Math (Why Your Current Plan Falls Short)"),

        para("Before building a plan, you need to confront the numbers. The current Project Hail Mary document projects 500-750 free signups in Phase 1, with 5% converting to Scaling ($199/mo) and 2% converting to Growth ($499/mo). Let us trace what that actually produces."),

        heading2("Current-Plan Revenue Projection"),

        simpleTable(
          ["Metric", "Optimistic", "Conservative"],
          [
            ["Website visitors (6 months)", "30,000", "15,000"],
            ["Free signups (3-5% of visitors)", "1,500", "450"],
            ["ERP connection rate (50%)", "750", "225"],
            ["Activated users (Larry engaged)", "525", "158"],
            ["Free to Scaling (5%)", "37", "11"],
            ["Free to Growth (2%)", "15", "4"],
            ["MRR at end of month 6", "$12,863", "$3,155"],
            ["Cumulative revenue (6 months)*", "$48,000-$65,000", "$12,000-$18,000"],
          ]
        ),
        spacer(80),

        para("*Assumes gradual sign-up ramp, not all at once. Even the optimistic scenario produces roughly 5% of the $1M target. The reason is straightforward: $7,200 in paid marketing budget cannot generate the traffic volume needed for a self-serve SaaS funnel to produce $1M. Industry benchmarks for B2B finance software show $15-$40 cost-per-click on Google, meaning your entire 6-month ad budget buys 180-480 clicks total."),

        heading2("The Three-Stream Revenue Model"),

        para("The only way to credibly approach $1M is to treat Larry self-serve as one of three revenue engines, not the only one. Here is the restructured model:"),

        simpleTable(
          ["Revenue Stream", "6-Month Target", "Mechanism", "Confidence"],
          [
            ["Self-serve (Scaling + Growth)", "$150K-$250K", "PLG funnel, organic + paid", "Medium"],
            ["Sales-assisted deals", "$400K-$600K", "Enterprise handoff from Larry + outbound", "Medium-High"],
            ["Partner / channel", "$150K-$250K", "Accounting firm partnerships, referrals", "Low-Medium"],
            ["TOTAL", "$700K-$1.1M", "", ""],
          ]
        ),
        spacer(80),

        para("Self-serve revenue of $150K-$250K requires reaching approximately 200-400 paying subscribers across Scaling and Growth tiers by month 6. This is aggressive but achievable if organic channels (LinkedIn, SEO, community) deliver the majority of traffic and your activation rate exceeds 60%. The sales-assisted stream is where the real money is: 10-15 Enterprise deals at $20K-$40K each, sourced from Larry usage signals and direct outbound."),

        // ============================================================
        // SECTION 2: THE PLAN
        // ============================================================
        heading1("Part 2: The Detailed Launch Plan"),

        heading2("Phase 0: Pre-Launch (Now through March 31)"),
        para("You have 6.5 weeks. Every day matters. Here is what must happen before April 1, in priority order."),

        heading3("1. Nail the Self-Serve Onboarding (Highest Priority)"),
        para("The single biggest risk to this launch is not marketing. It is the moment between signup and first value. If a user signs up, connects their ERP, and Larry does not deliver a meaningful insight within 5 minutes, you lose them permanently. B2B self-serve products live and die on time-to-value."),

        boldPara("What to build before April 1:", ""),
        boldBulletItem("Pre-built first questions: ", "When the ERP connects and data syncs, Larry should immediately suggest 3-5 high-value queries specific to the user's data. Not generic suggestions. If they have overdue receivables, Larry's first suggestion should reference those overdue amounts. If their burn rate spiked last month, surface that."),
        boldBulletItem("The 'wow moment' email: ", "After the ERP sync completes (15-30 minutes), send an automated email with 2-3 actual insights from their data. 'Larry found $47K in receivables over 90 days across 10 invoices. Click to see the full analysis.' This email is the most important piece of marketing you will produce."),
        boldBulletItem("Guided walkthrough: ", "A 3-step interactive tour (not a video) that walks users through their first query, their first chart, and their first download attempt (which gates on Scaling tier). This tour should take under 2 minutes."),
        boldBulletItem("Error handling: ", "If the ERP sync fails, if data is incomplete, if Larry cannot answer a query, the fallback experience must be graceful. A generic error page will kill conversion. Build specific error states with recovery paths."),

        heading3("2. Instrument Everything (Second Priority)"),
        para("You cannot optimize what you do not measure. Before launch, wire up tracking for every critical step in the funnel. This is not optional."),

        boldBulletItem("Funnel events to track: ", "Website visit, signup initiated, signup completed, ERP connection started, ERP connection completed, first Larry query, first chart generated, upgrade prompt shown, upgrade initiated, upgrade completed."),
        boldBulletItem("Engagement metrics: ", "Questions asked per session, questions asked per day, return rate (Day 1, Day 3, Day 7), feature usage distribution (Analyze vs. Explain vs. Search vs. Identify)."),
        boldBulletItem("Sales trigger events: ", "User hits 10-question daily limit, user asks about multi-entity, user's Close Tracker shows bottlenecks, user's company matches ICP (Series B+, 10+ finance team). Each of these should fire a notification to your sales workflow."),
        boldBulletItem("Tool stack: ", "Mixpanel or Amplitude for product analytics. Segment (or equivalent) for event routing. A simple CRM (even a well-structured spreadsheet initially) for sales handoff tracking."),

        heading3("3. Build the Sales Handoff Pipeline"),
        para("Larry is a product wedge. It generates enterprise leads. But leads without a sales process are wasted. Before launch:"),

        boldBulletItem("Define the handoff criteria: ", "Which Larry signals trigger a sales conversation? Codify the 5 triggers from your plan (question limit hit, multi-entity request, bottleneck signals, ICP match, explicit Book Close interest) and build automated notifications for each."),
        boldBulletItem("Prepare the sales motion: ", "When a user triggers a handoff, what happens? Who reaches out? Within what timeframe? What does the first message say? Draft these templates now. The message should reference their actual Larry usage ('I noticed you've been analyzing receivables aging across your entities. We've helped similar companies cut that analysis from days to minutes with our full close platform.')"),
        boldBulletItem("Staff the motion: ", "With 10 active pilots and a launch coming, who is handling inbound sales conversations? If the answer is 'Rishi does everything,' that is a bottleneck that will kill conversion on your highest-value deals."),

        heading3("4. Pricing Page and Upgrade Flow"),
        para("Your pricing needs to be crystal clear on the website and inside the product. Ambiguity kills self-serve conversion."),

        boldBulletItem("In-product upgrade prompts: ", "When users hit the free tier limits (10 questions/day, no downloads, 7-day history), the upgrade prompt must show exactly what they unlock, at what price, with a 1-click upgrade path. Do not redirect to a separate pricing page. The upgrade should happen in context."),
        boldBulletItem("Annual vs. monthly: ", "Offer both with a clear annual discount (2 months free, i.e., $199/mo or $1,990/year). Annual plans improve cash flow and reduce churn. Show the annual savings prominently."),
        boldBulletItem("India vs. US pricing: ", "Geo-detect and show the right price automatically. Do not show both prices on the same page. This creates confusion and invites arbitrage."),

        heading3("5. Pre-Launch Content Blitz (March 15-31)"),
        para("Your LinkedIn content plan is solid for weeks 1-6. The Phase 3 content (weeks 7-9) is where the launch energy lives. The adjustments I would make:"),

        boldBulletItem("The 'Roast My Ledger' post (Mar 17): ", "This is your best lead-gen idea. Make it real. Commit to personally running 10-20 of these audits. Each one becomes a warm lead and a potential case study. But only do this if you can deliver insights within 24 hours. A week-long wait kills the momentum."),
        boldBulletItem("The launch day post (Apr 1): ", "Do not bury the CTA. The post should be: here is the problem (latency), here is what we built (Larry), here is how to try it right now (link to signup). No manifesto. No philosophy. Direct, actionable, with a clear path from post to product."),
        boldBulletItem("Amplification: ", "Reach out to 5-10 finance influencers and newsletter operators NOW (not launch week) and offer them early access. Ask them to try Larry on their own books. Authentic reactions from real finance professionals are worth more than any ad spend."),

        new Paragraph({ children: [new PageBreak()] }),

        // ============================================================
        // Phase 1
        // ============================================================
        heading2("Phase 1: Launch Month (April 1-30)"),
        para("The first 30 days determine whether this launch has legs. Your goal is not revenue. It is activation and retention."),

        heading3("Week 1: Controlled Launch (April 1-7)"),
        boldBulletItem("Soft launch to warm audience: ", "Your 10 pilot customers, LinkedIn followers, email list, finance community connections. Do NOT turn on paid ads yet. Let the first 50-100 users go through the funnel. Watch where they drop off. Fix what breaks."),
        boldBulletItem("Daily monitoring: ", "Every morning, review: how many signups, how many ERP connections, how many first queries, how many return visits. If ERP connection rate is below 40%, there is a UX problem. If first-query rate is below 60% of connected users, the onboarding is broken. Fix these before scaling traffic."),
        boldBulletItem("Personal outreach: ", "Message every single user who signs up in week 1. Ask them: what brought you here, what did you try, what worked, what didn't? This qualitative data is worth more than any analytics dashboard."),

        heading3("Weeks 2-3: Iterate and Scale (April 8-21)"),
        boldBulletItem("Turn on paid acquisition cautiously: ", "Allocate only Rs. 40,000 ($480) for April. Start with Google AdWords on branded terms (Komplai, Larry AI finance) and high-intent long-tail keywords (MIS automation, AI finance assistant). Do NOT bid on expensive category terms yet."),
        boldBulletItem("LinkedIn organic acceleration: ", "Continue the 3x/week content cadence. Post 27 (launch post) should already be live. Now shift content from educational to 'here is what Larry found' posts. Share anonymized insights from real user data (with permission). Show Larry's answers, charts, and analysis in action."),
        boldBulletItem("SEO content: ", "Your blog has an impressions-but-no-clicks problem (your own optimization guide identifies this). Before publishing more articles, fix the existing ones: rewrite titles using your new CTR formula (benefit + timeframe), update meta descriptions, add schema markup. 20 optimized existing articles will outperform 20 new mediocre ones."),

        heading3("Week 4: First Conversion Push (April 22-30)"),
        boldBulletItem("Upgrade nudge campaign: ", "For users who signed up in weeks 1-2 and have used Larry 5+ times, trigger an email sequence: Day 1: 'You've asked Larry 47 questions this month. Scaling plan gives you unlimited.' Day 3: 'Your team could save [X hours] based on the queries you're running.' Day 7: Direct upgrade offer with annual discount."),
        boldBulletItem("Close Tracker launch nudge: ", "If month-end close data is available, surface Close Tracker insights proactively: 'Your April close is 30% complete. At current pace, you'll finish on Day 9.' The Close Tracker is the wedge into paid because the free tier only shows basic progress."),

        calloutBox(
          "April Success Metrics (Phase 1 Targets)",
          "Signups: 200-400 | ERP connections: 120-240 (60%+) | Active Larry users: 80-160 | Questions asked: 2,000+ | First paid conversions: 10-25 | MRR: $2,000-$7,000 | Sales-qualified leads generated: 15-30"
        ),
        spacer(120),

        // ============================================================
        // Phase 2
        // ============================================================
        heading2("Phase 2: Growth Month (May 1-31)"),
        para("May is when you shift from 'does this work?' to 'how do we scale what works?' The Growth tier ($499/mo) also goes live, adding JV automation, bank recon, and email sync."),

        heading3("Channel Strategy for May"),
        boldBulletItem("Double down on what converted: ", "By May 1, you will know which channels produced signups and which produced activated users. These are often different. A channel that produces lots of signups but low activation is a vanity metric. Focus spend on channels where users actually connect their ERP and ask Larry questions."),
        boldBulletItem("Google AdWords expansion: ", "Increase to Rs. 60,000 ($720) for May. Add competitor keywords ('Numeric alternatives,' 'FloQast alternative for startups') which are low-competition per your competitive intel. Create dedicated landing pages for each comparison query."),
        boldBulletItem("Community plays: ", "Start engaging in r/accounting, r/CFO, finance Slack communities (not with ads, with genuine value). Answer questions about month-end close, reconciliation, variance analysis. Include your experience building Komplai when relevant. This is slow-burn but produces the highest-quality leads."),
        boldBulletItem("Partner outreach: ", "Approach 5-10 accounting firms that serve Series A-C companies. Offer: 'We'll give your clients free access to Larry. When they need close automation, you get the implementation fees.' This is the partner-channel revenue stream."),

        heading3("Sales Motion Activation"),
        para("By May, your Larry user base should be generating sales signals. This is where the real revenue lives."),

        boldBulletItem("Warm outbound from Larry data: ", "Users who hit question limits, explore multi-entity features, or show consistent bottlenecks in Close Tracker get a personalized outreach. Reference their actual usage. This is not cold email; it is informed, contextual selling."),
        boldBulletItem("Target: 5-8 enterprise conversations in May ", "from Larry-generated signals. Even if none close in May, these are pipeline for June-September."),
        boldBulletItem("Direct outbound to ICP: ", "In parallel, begin targeted outbound to Series A-C CFOs/Controllers at US companies with 10+ finance team members. Use the 'Roast My Ledger' concept as the hook: 'We'll run an AI audit of your close process for free.'"),

        calloutBox(
          "May Success Metrics (Phase 2 Targets)",
          "Cumulative signups: 600-1,000 | New paid Scaling: 25-50 | New paid Growth: 5-15 | MRR: $8,000-$18,000 | Cumulative revenue: $10,000-$25,000 | Enterprise pipeline: $200K-$400K | Partner conversations: 5-10"
        ),
        spacer(120),

        // ============================================================
        // Phase 3
        // ============================================================
        heading2("Phase 3: Acceleration (June - September)"),
        para("Phases 1-2 are about proving the model. Phase 3 is about compounding it. By June, you should have case studies, refined messaging, a working sales motion, and data on which channels convert."),

        heading3("Revenue Acceleration Levers"),

        boldNumItem("Enterprise deals close: ", "The pipeline built in April-May starts converting. Target 2-3 Enterprise deals per month at $20K-$30K each. This is $40K-$90K/month from enterprise alone.", "numbers2"),
        boldNumItem("Self-serve compounds: ", "As SEO content matures (3-6 month lag), organic traffic increases. LinkedIn content has built an audience. Word-of-mouth from early users kicks in. Self-serve MRR should be growing 20-40% month-over-month.", "numbers2"),
        boldNumItem("Partner channel delivers: ", "Accounting firms who started referring in May begin producing qualified leads. Even 2-3 referral deals per month at $10K-$20K adds meaningfully.", "numbers2"),
        boldNumItem("Growth tier upsells: ", "Scaling users who've been using Larry for 2-3 months and are now approaching close periods will see the value of JV automation and bank recon. Target 10-15% Scaling-to-Growth upgrade rate.", "numbers2"),

        heading3("6-Month Cumulative Revenue Projection"),
        simpleTable(
          ["Month", "Self-Serve MRR", "Enterprise Deals", "Partner Revenue", "Monthly Total"],
          [
            ["April", "$3K-$7K", "$0", "$0", "$3K-$7K"],
            ["May", "$8K-$18K", "$0", "$0", "$8K-$18K"],
            ["June", "$15K-$30K", "$40K-$60K", "$0", "$55K-$90K"],
            ["July", "$22K-$42K", "$60K-$90K", "$10K-$20K", "$92K-$152K"],
            ["August", "$30K-$55K", "$60K-$90K", "$20K-$30K", "$110K-$175K"],
            ["September", "$40K-$70K", "$80K-$120K", "$30K-$50K", "$150K-$240K"],
            ["6-Mo Total", "$118K-$222K", "$240K-$360K", "$60K-$100K", "$418K-$682K"],
          ]
        ),
        spacer(80),

        para("The realistic range is $420K-$680K. To hit $1M, you would need the optimistic end of every stream plus faster-than-expected enterprise deal velocity. That is possible but not plannable. A stretch target of $750K is more honest and still represents remarkable traction for a self-serve launch in its first 6 months."),

        new Paragraph({ children: [new PageBreak()] }),

        // ============================================================
        // SECTION 3: BUDGET ALLOCATION
        // ============================================================
        heading1("Part 3: Budget Allocation (Rs. 6,00,000 / ~$7,200)"),

        para("With $7,200 for 6 months, every rupee must be deployed with surgical precision. Here is the revised allocation, prioritizing channels that compound over time rather than those that stop when budget stops."),

        simpleTable(
          ["Channel", "Allocation", "Amount", "Rationale"],
          [
            ["SEO + content optimization", "35%", "Rs. 2,10,000", "Fix existing articles for CTR, create 5-8 new high-intent pages. Compounds over time."],
            ["Google AdWords (branded + long-tail)", "25%", "Rs. 1,50,000", "Branded terms + competitor terms only. No expensive category bids."],
            ["Launch event + Product Hunt", "15%", "Rs. 90,000", "One-time amplification: webinar, PH launch, influencer early access."],
            ["LinkedIn retargeting", "15%", "Rs. 90,000", "Retarget website visitors with CFO/Controller job titles only."],
            ["Community + partnerships", "10%", "Rs. 60,000", "Event sponsorships, accounting firm outreach, community tools."],
          ]
        ),
        spacer(80),

        calloutBox(
          "Critical Budget Decision",
          "Do NOT spread thin across all channels simultaneously. In April, spend 80% of the month's budget on launch event and Google branded terms. In May, shift to SEO and retargeting. By June, your data will tell you where to concentrate. Kill channels that are not producing activated users (not just signups)."
        ),
        spacer(120),

        heading2("Free / Low-Cost Channels (Where Most Growth Will Come From)"),

        para("Given the budget constraint, your primary growth will come from channels that cost time, not money:"),

        boldNumItem("LinkedIn organic (Rishi's profile): ", "Your content plan is strong. The 3x/week cadence with utility-first content positions you as an expert, not a vendor. This is your single most important channel. Protect this time ruthlessly.", "numbers3"),
        boldNumItem("SEO blog (existing 125+ articles): ", "You have a content base. The problem is CTR, not ranking. Fix the titles and meta descriptions of your top-50 articles by impressions. This is the highest-ROI marketing activity available to you right now.", "numbers3"),
        boldNumItem("Product Hunt launch: ", "Time it for the second week of April (not April 1). Let week 1 users validate the product first. PH can deliver 500-2,000 signups in a single day if you prepare properly: teaser posts, hunter lined up, first-hour voting brigade from your network.", "numbers3"),
        boldNumItem("Finance community engagement: ", "Reddit, Slack groups, LinkedIn groups, accounting forums. Be a genuine participant, not a marketer. Answer questions. Share frameworks. Mention Komplai only when directly relevant.", "numbers3"),
        boldNumItem("Referral from existing pilots: ", "Your 10 active pilot customers are your best salespeople. Ask each one to refer 2-3 CFO/Controller peers. Offer them 3 months of Scaling for free for every referral that converts. This costs you nothing but deferred revenue.", "numbers3"),

        new Paragraph({ children: [new PageBreak()] }),

        // ============================================================
        // SECTION 4: WHAT NOT TO DO
        // ============================================================
        heading1("Part 4: What NOT To Do (The Kill List)"),

        para("This section is as important as the plan itself. These are the mistakes that would waste your limited resources or actively damage the launch."),

        heading2("1. Do Not Chase Vanity Metrics"),
        para("Signups that do not connect an ERP are worthless. Website visits that do not convert are noise. LinkedIn impressions that do not drive traffic are ego metrics. The only numbers that matter in April are: ERP connections, Larry questions asked per user, and return visits on Day 3 and Day 7. If you find yourself celebrating signup numbers while activation is below 50%, you are losing."),

        heading2("2. Do Not Launch with a Broken Onboarding"),
        para("If the ERP connection flow has bugs, if the data sync takes hours instead of minutes, if Larry's first response is generic or wrong, delay the launch. A bad first impression in self-serve SaaS is a death sentence. Users will not come back. They will not give you a second chance. They will tell their CFO friends it did not work. Get the first 5 minutes right or do not launch."),

        heading2("3. Do Not Spend Money on Expensive Keywords"),
        para("'Close management software' and 'automated reconciliation software' are $20-$40 per click. With $7,200 total budget, you cannot compete on these terms. Do not try. Instead, own the long-tail: 'why does month end close take so long' (low competition, high intent), 'MIS automation' (your differentiator), 'AI finance assistant for CFOs.' These are cheaper and attract more qualified users."),

        heading2("4. Do Not Ignore the Enterprise Handoff"),
        para("Larry's biggest value is not the $199/month subscription. It is the enterprise deal it generates. If a CFO at a Series B company with a 15-person finance team is using Larry and hitting limitations, that is a $20K-$30K/year deal waiting to happen. If you do not have a process to identify and engage these users within 48 hours of the signal, you are leaving the most valuable revenue on the table."),

        heading2("5. Do Not Build Features Nobody Asked For"),
        para("Between now and April 1, the temptation will be to add 'one more feature' to Larry. Resist this. The features in your Phase 1 scope (ERP integration, Larry insights/reports, basic Close Tracker, Starter and Scaling tiers) are sufficient for launch. Feature creep is the most common cause of missed launch dates in startups. Ship what you have. Iterate based on user feedback."),

        heading2("6. Do Not Treat India and US as the Same Market"),
        para("The pricing ($199 US / $99 India) reflects different markets. The messaging, channels, and conversion patterns will also differ. Indian finance teams may adopt Larry for MIS automation (a strong local pain point). US teams will adopt for CFO visibility and close speed. Your LinkedIn content should primarily target US (higher ARPU, matches ICP). Do not dilute the messaging trying to serve both markets with the same content."),

        heading2("7. Do Not Offer Discounts in the First 60 Days"),
        para("If users are not converting at $199/month, the problem is value perception, not price. Discounting signals desperation and sets a precedent that erodes LTV. Instead of discounting, offer extended free trials (14 days of Scaling features) or add a limited-time perk (free onboarding call, custom MIS template setup). These add value without destroying pricing integrity."),

        heading2("8. Do Not Forget Retention After Conversion"),
        para("A paying user who churns in month 2 is worse than a free user who never converted (because the paying user tells people the product was not worth it). In weeks 3-4 post-conversion, check in with every paying user. Ask: 'Is Larry saving you time? What would make it more useful?' These conversations prevent churn and generate product insights simultaneously."),

        heading2("9. Do Not Publish SEO Content Without Fixing Existing CTR"),
        para("Your SEO optimization guide correctly identifies that your articles rank but do not get clicks. Publishing 20 more articles with the same title formula will produce more impressions with no clicks. Fix the top 50 existing articles first: rewrite titles using the benefit + timeframe formula, update meta descriptions with proof points, add structured data markup. Then publish new content using the improved formula."),

        heading2("10. Do Not Run the Launch Solo"),
        para("Even if you are the only person doing marketing, sales, and product simultaneously, you need at least 2-3 people helping during launch week. Someone to monitor the product for bugs. Someone to respond to support queries within 1 hour. Someone to manage the community reaction. If a user tweets 'I tried Komplai and my ERP connection failed' and nobody responds for 6 hours, that is a reputational wound that paid marketing cannot heal."),

        new Paragraph({ children: [new PageBreak()] }),

        // ============================================================
        // SECTION 5: WEEK-BY-WEEK
        // ============================================================
        heading1("Part 5: Week-by-Week Execution (Feb 14 - April 30)"),

        heading2("Weeks 1-2 (Feb 14-28): Foundation"),
        simpleTable(
          ["Task", "Owner", "Outcome"],
          [
            ["Finalize self-serve onboarding flow", "Product", "User signup > ERP connect > first insight in < 5 min"],
            ["Instrument funnel tracking", "Engineering", "All 10 funnel events tracked in analytics"],
            ["Build sales handoff notifications", "Engineering", "5 trigger events auto-notify sales"],
            ["Prepare 'wow moment' email template", "Marketing", "Automated email with real data insights"],
            ["Draft pricing page (in-product + website)", "Product + Design", "Clear tiers, 1-click upgrade"],
            ["Reach out to 10 finance influencers", "Rishi", "5+ confirmed for early access"],
            ["Continue LinkedIn posts (Week 3-4 of plan)", "Rishi", "3 posts/week, engagement tracked"],
            ["Rewrite top 20 SEO article titles", "Marketing", "CTR-optimized titles and metas live"],
          ]
        ),
        spacer(80),

        heading2("Weeks 3-4 (Mar 1-14): Build and Test"),
        simpleTable(
          ["Task", "Owner", "Outcome"],
          [
            ["Internal QA of full self-serve flow", "Product + Eng", "10 test users complete full flow without issues"],
            ["Prepare Google AdWords campaigns", "Marketing", "Branded + long-tail keywords ready to activate"],
            ["Draft Product Hunt listing", "Marketing", "Teaser, screenshots, tagline, first-day plan"],
            ["Build comparison landing pages", "Marketing", "Komplai vs Numeric, vs FloQast, vs BlackLine"],
            ["Set up LinkedIn retargeting pixel", "Marketing", "Pixel installed, audience building"],
            ["Prepare launch-week email sequence", "Marketing", "3-email sequence: announcement, features, CTA"],
            ["Begin partner outreach (5 accounting firms)", "Rishi", "Intro calls scheduled for April"],
            ["LinkedIn Phase 2 content (Weeks 5-6)", "Rishi", "3 posts/week continues"],
          ]
        ),
        spacer(80),

        heading2("Weeks 5-6 (Mar 15-31): Final Prep and Soft Launch"),
        simpleTable(
          ["Task", "Owner", "Outcome"],
          [
            ["Run 'Roast My Ledger' campaign (Post 19)", "Rishi", "10-20 ledger audits committed"],
            ["Launch early access to influencers", "Marketing", "5+ influencers testing Larry on their data"],
            ["Final product testing with real ERP data", "Product + Eng", "Zero critical bugs in signup > insight flow"],
            ["Prepare launch day social + email", "Marketing", "All launch assets ready"],
            ["LinkedIn Phase 3 content (Weeks 7-8)", "Rishi", "Larry revealed, CTA-driven posts"],
            ["Confirm Product Hunt launch date", "Marketing", "Hunter confirmed, voting plan set"],
            ["Prepare support escalation process", "Support", "1-hour response SLA for launch week"],
            ["Brief anyone helping with launch week", "Rishi", "Roles assigned: product, support, marketing"],
          ]
        ),
        spacer(80),

        heading2("Weeks 7-8 (Apr 1-14): Launch and Monitor"),
        simpleTable(
          ["Task", "Owner", "Outcome"],
          [
            ["April 1: Launch post + email blast", "Marketing", "Launch live, CTA drives to signup"],
            ["April 1: Activate Google branded ads", "Marketing", "Branded terms live ($200 weekly budget)"],
            ["Daily monitoring: signup > ERP > Larry metrics", "Product", "Dashboard reviewed every morning"],
            ["Personal outreach to every week-1 user", "Rishi", "30+ conversations with early users"],
            ["Product Hunt launch (Week 2)", "Marketing", "500+ upvotes target"],
            ["Fix any onboarding friction identified", "Engineering", "< 24-hour fix cycle"],
            ["First sales outreach from Larry signals", "Sales", "5+ enterprise conversations initiated"],
            ["Publish 'what Larry found' LinkedIn content", "Rishi", "Real data examples (anonymized)"],
          ]
        ),
        spacer(80),

        heading2("Weeks 9-10 (Apr 15-30): First Conversions"),
        simpleTable(
          ["Task", "Owner", "Outcome"],
          [
            ["Trigger upgrade email sequence", "Marketing", "Users with 5+ sessions get upgrade nudge"],
            ["Month-end: Surface Close Tracker insights", "Product", "Proactive close progress notifications"],
            ["Compile first case study from early adopter", "Marketing", "1 case study draft ready"],
            ["Review funnel data, identify bottlenecks", "Product + Marketing", "Clear picture of where users drop off"],
            ["Activate LinkedIn retargeting", "Marketing", "Website visitors see targeted ads"],
            ["Plan May content and channel adjustments", "Marketing", "Data-driven channel allocation"],
            ["Continue enterprise outreach", "Sales", "10+ conversations in pipeline"],
            ["Month-end review: revenue, metrics, learnings", "Rishi", "Documented learnings, adjusted targets"],
          ]
        ),

        new Paragraph({ children: [new PageBreak()] }),

        // ============================================================
        // SECTION 6: RISK REGISTER
        // ============================================================
        heading1("Part 6: Risk Register"),

        simpleTable(
          ["Risk", "Likelihood", "Impact", "Mitigation"],
          [
            ["ERP connection failures at scale", "Medium", "Critical", "Load test all 4 integrations with 100+ concurrent users. Have fallback manual upload path."],
            ["Larry gives wrong/misleading answers", "Medium", "Critical", "Add confidence disclaimers. Build manual override. Quality-test against 50 real datasets."],
            ["Low ERP connection rate (<40%)", "Medium", "High", "Simplify OAuth flow. Add video walkthrough. Offer live setup help for first 100 users."],
            ["Paid marketing burns budget with no conversions", "High", "Medium", "Start with $480/month. Only scale what converts to activated users, not just signups."],
            ["Competitor launches Larry-equivalent", "Low (6-mo)", "High", "Move fast. Memory and institutional knowledge create moat. Ship Close Tracker faster."],
            ["Free tier abuse (users never convert)", "High", "Medium", "Daily question limit + 7-day history creates friction. Track power users for sales outreach."],
            ["Enterprise deals take longer than expected", "High", "High", "Build pipeline early (May). Do not count on June closes. Budget for 90-day sales cycle."],
            ["Team bandwidth bottleneck (Rishi does everything)", "Very High", "Critical", "Hire/contract 1 person for marketing operations before launch. Delegate post scheduling, ad management, email sequences."],
          ]
        ),

        new Paragraph({ children: [new PageBreak()] }),

        // ============================================================
        // SECTION 7: THE 5 THINGS THAT DETERMINE SUCCESS
        // ============================================================
        heading1("Part 7: The 5 Things That Will Determine Whether This Works"),

        para("If you only read one section of this document, read this one. Hundreds of tactical decisions will follow, but these five structural factors will determine whether the launch succeeds or fails."),

        heading2("1. Time-to-First-Value Under 5 Minutes"),
        para("The moment a user connects their ERP and Larry delivers a real, specific, valuable insight from their actual data, you have them. Every minute of friction before that moment reduces your activation rate. If this number is above 10 minutes, the self-serve model will not work. Measure it obsessively. Optimize it ruthlessly."),

        heading2("2. The Enterprise Handoff Must Be Operational by Day 30"),
        para("Self-serve subscriptions at $199-$499/month are meaningful but cannot carry a $1M target alone. The enterprise deals sourced from Larry usage are where the revenue math works. If your sales handoff process is not operational by the end of April, you lose 2-3 months of pipeline development that you cannot recover."),

        heading2("3. Content Must Convert, Not Just Educate"),
        para("Your LinkedIn plan and SEO content are well-structured for education and brand building. But education without conversion is a branding exercise, not a growth engine. Every piece of content from April 1 onwards must include a clear path to Larry. Not a soft CTA buried at the bottom. A direct, in-context link: 'Run this analysis on your own data in 30 seconds. Connect your ERP to Larry.'"),

        heading2("4. You Need at Least One More Person"),
        para("You cannot be the CEO, product manager, marketer, salesperson, and customer support agent simultaneously during a product launch. You will drop balls. The highest-impact hire or contractor before April 1 is a marketing operations person who can manage ad campaigns, schedule social posts, set up email sequences, and handle support tickets. Budget $2,000-$3,000/month for this. It will pay for itself in the first enterprise deal you close because you had time to actually sell."),

        heading2("5. Kill Your Darlings Quickly"),
        para("If a channel is not working after 30 days, kill it. If a feature is not being used, deprioritize it. If a pricing tier is not converting, experiment. The worst thing you can do with limited resources is continue investing in something that the data says is not working because you hoped it would. Check the data every week. Make decisions every two weeks. Be willing to be wrong fast."),

        spacer(400),

        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "---", size: 28, font: "Arial", color: COLORS.medGray })],
        }),
        spacer(200),

        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "This plan is a living document.", italics: true, size: 22, font: "Arial", color: COLORS.medGray })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Revisit weekly. Update with data. Do not treat it as scripture.", italics: true, size: 22, font: "Arial", color: COLORS.medGray })],
        }),
      ],
    },
  ],
});

// Generate the document
Packer.toBuffer(doc).then((buffer) => {
  const outputPath = "/sessions/funny-stoic-pascal/mnt/komplai-non-technical/Larry-Launch-Plan-Feb2026.docx";
  fs.writeFileSync(outputPath, buffer);
  console.log(`Document saved to: ${outputPath}`);
  console.log(`Size: ${(buffer.length / 1024).toFixed(1)} KB`);
});
