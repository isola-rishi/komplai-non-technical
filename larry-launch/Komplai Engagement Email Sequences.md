# Komplai Email Sequences — Larry Launch (April 1, 2026)

**Last Updated:** February 23, 2026
**Sender:** Rishi Isola (rishi@komplai.com)
**Persona:** CFO / Controller / CEO (when no CFO exists)
**Markets:** US + India (unified sequence)
**Core Value Pillars:** MIS automation, custom reporting, proactive alerts, budgeting, close tracking

---

## Voice & Tone Guide

**Sound like:** A sharp controller talking to a peer over coffee. Numbers-first, direct, slightly understated. Someone who's been in the trenches and built something to fix what frustrated them.

**Never sound like:** A SaaS marketing team. No "exciting new features," no "we're thrilled," no "unlock the power of." No exclamation marks in subject lines.

**Rules:**
- Every email references a tangible outcome (a report, a number, a deliverable) — never a capability
- From Rishi, written as Rishi. First person singular. "I built" not "we launched"
- One CTA per email. Specific and concrete. "See your cash flow analysis" not "Learn more"
- Short paragraphs. 2-3 sentences max. Finance people skim
- No images in the first 3 outbound emails (deliverability)

---

# SEQUENCE 1: OUTBOUND (Cold → Signup)

## Strategy

**Narrative arc:** Each email leads with a business decision the CFO/CEO needs to make *this week* — and the data gap that's slowing them down. These are not accounting process problems. They're "how do I run this business" problems that happen to require financial data the recipient can't access fast enough.

**Core insight:** CFOs who think like CEOs don't care about faster reconciliation for its own sake. They care about being able to answer "can we afford to hire?" in 30 seconds instead of 3 hours. Larry's value isn't that it automates finance processes — it's that it makes business decisions faster.

**Pain Point → Email Mapping:**

| Pain Point | Email | Why It Works |
|------------|-------|-------------|
| "Can we afford to hire 2 more people?" — the resource allocation decision that stalls because nobody can model the impact fast enough | Email 1 | Every growing company faces this weekly. The CFO knows directionally but can't give a confident answer without hours of work. The decision stalls or gets made on gut feel. |
| "Which customers are actually making us money?" — revenue looks healthy but profitability is a black box | Email 2 | Hits a nerve because everyone suspects the answer but nobody has the data to prove it. Late-paying customers still getting serviced. Discounted deals eating margin. |
| "What do I tell the board on Thursday?" — the reporting burden reframed as a business communication problem | Email 3 | First product mention. Not about formatting a template — about walking into a room with a clear, data-backed narrative. Larry is introduced as the thing that gives you the story. |
| "How long does our runway last at current burn?" — the number running in the back of every CFO's head that drives every other decision | Email 4 | Social proof email. Universal across company stages. The CFO who can answer this confidently — and model scenarios against it in real time — makes better decisions about everything else. |
| "Where is the money actually going?" — strategic spend visibility, not line-item accounting | Email 5 | Final email. Combines the spend blindness problem with the Monday morning data pull. Hybrid CTA. |

**Journey mapping:** Unaware → "That decision stalled last week because of exactly this" → "Wait, something fixes this?" → "It works for companies like mine" → Decision

**Escalation logic:** Emails 1-2 are pure business decision problems (no product). Email 3 introduces Larry through the board reporting problem (most relatable to senior finance leaders). Email 4 shows proof via cash runway/burn. Email 5 is the personal ask anchored on spend visibility.

**Exit condition:** Recipient signs up for Komplai (detected via email match) OR books a demo call. Remove from sequence immediately.

**Suppression rules:** Do not send if recipient is already a Komplai user, has unsubscribed, or has an open support ticket.

---

## Personalization Requirements

**Email 1 must open with a personalized sentence about the recipient.** This is the single highest-leverage change for cold email performance. Generic openers get deleted. A sentence that proves you've done 60 seconds of research gets read. Emails 2-5 don't repeat the personalization — by then, the thread and Rishi's name provide continuity.

**What `{{personalization_sentence}}` should contain (pick ONE per email):**

| Source | Example | When to Use |
|--------|---------|-------------|
| LinkedIn activity | "I saw your post about consolidating your reporting stack — that's exactly the gap I keep hearing about." | Recipient is active on LinkedIn |
| Company news | "Congrats on the Series B — scaling the finance team after a raise is where the data gaps hit hardest." | Recent funding, acquisition, or expansion |
| Role/career context | "Going from Big 4 audit to running controllership at a 200-person startup is a specific kind of chaos — I hear it a lot." | Clear career trajectory visible |
| Industry pain point | "Healthcare SaaS companies hit the multi-entity reporting wall faster than most — it usually starts around your stage." | Industry is identifiable and relevant |
| Mutual connection or event | "I was at SaaStr last week and your CFO's panel on close automation came up in three separate conversations." | Genuine connection exists |
| Company financial signal | "I noticed {{company_name}} has been hiring aggressively across engineering — that's usually when the 'can we afford this?' question starts coming up daily." | Job postings, headcount growth visible |

**Research workflow (for SDR or automation tool):**
1. Check LinkedIn profile — recent posts, job history, skills endorsed
2. Check company news — Crunchbase, press releases, job postings
3. Check industry — vertical-specific pain points from the pain point table above
4. Write ONE sentence (under 20 words) that connects your research to the email's pain point
5. The sentence must feel like an observation, not flattery. Never say "I love what you're doing at..."

**Tone rules for personalization:**
- Observational, not complimentary ("I noticed..." not "I admire...")
- Specific, not generic ("your Series B" not "your company's growth")
- Connected to the email's theme, not random ("consolidating reporting" for Email 3, not "great company culture")
- One sentence only — the personalization opens the door, the pain point keeps them reading

---

## Sequence Overview

| # | Email | Pain Point | Timing | Primary CTA |
|---|-------|-----------|--------|-------------|
| 1 | "Can we afford to hire?" | Resource allocation decisions that stall because the data takes too long to assemble | Day 0 | Reply to engage |
| 2 | "Which customers actually make us money?" | Revenue concentration and profitability blindness — the numbers everyone suspects but nobody can prove | Day 3 | Reply to engage |
| 3 | "What do I tell the board?" | The board meeting is Thursday and you don't have the narrative yet — MIS/reporting as a business communication problem | Day 7 | Try Larry free |
| 4 | "How long does our runway last?" | Cash runway at current burn — the number behind every hiring, investment, and fundraising decision | Day 12 | Try Larry free |
| 5 | "Where is the money actually going?" | Strategic spend visibility + the Monday data pull that starts every week | Day 18 | Signup or book 15 min |

---

## Email 1: "Can We Afford to Hire?"

**Pain point:** A business decision — hiring, a new vendor contract, a marketing budget increase — requires the CFO to model the financial impact. But assembling the data (current burn, committed expenses, projected revenue, AR collection rates, cash position) takes hours or a full day. Meanwhile, the decision stalls. The CEO gets impatient. The hire doesn't happen for another 2 weeks. Or worse — it happens based on gut feel and the cash position turns out to be tighter than anyone thought.

**Purpose:** Surface the *business* cost of slow financial data. Not "your ERP is hard to use" but "your company makes slower, worse decisions because the data isn't available when the question is asked." No product mention.

**Subject line options:**
- "Can we afford to hire two more engineers?"
- "The decision that's been sitting on your desk for a week"
- "How long does a headcount decision take at {{company_name}}?"

**Preview text:** "Most CFOs I talk to can't answer this question same-day."

**Body:**

Hi {{first_name}},

{{personalization_sentence}}

It made me think of a moment I keep hearing from CFOs — see if it lands.

Someone on your leadership team asks: "Can we afford to hire two more engineers this quarter? What's the impact on our runway?"

You know the answer directionally. But a confident number means pulling together cash, committed expenses, projected revenue, AR collection rates, and payroll impact. That takes hours. Sometimes a full day if the data lives in multiple places.

So the decision stalls. Or it gets made on gut feel. Two months later, the cash position is tighter than anyone expected. Or worse — the CEO stops asking you and just makes the call, and finance isn't at the table.

I've talked to dozens of CFOs about this exact gap — between when a business question gets asked and when finance can give a confident answer. It's the most expensive problem nobody tracks.

How often does a business decision at {{company_name}} wait on financial data?

— Rishi
Founder, Komplai

**CTA:** Reply (conversational, no button)

**Timing:** Day 0

**Segment notes:** Send to all prospects. No conditions. No product mention — only Rishi's title establishes the connection. The framing is deliberately about business decisions, not finance operations.

---

## Email 2: "Which Customers Actually Make Us Money?"

**Pain point:** Revenue looks healthy at the top line. But if you asked the CFO "which of your top 10 customers are actually profitable after accounting for payment delays, support costs, discounts, and credit terms?" — most can't answer without building a spreadsheet. Meanwhile, the sales team is chasing renewal on a customer who pays 90 days late and negotiated a 30% discount. And a smaller customer who pays on time and uses no support resources is getting the same level of attention. The business is optimising for revenue, not profitability, because the profitability data doesn't exist in a usable format.

**Purpose:** Different nerve from Email 1. This is about the business running on incomplete information — not because nobody cares, but because the data to make better decisions isn't accessible. Still no product mention.

**Subject line options:**
- "Your top customer might be your worst"
- "Revenue isn't profit — but does your team know the difference?"
- "Which of your customers should you fire?"

**Preview text:** "Most finance teams can't answer this without a spreadsheet project."

**Body:**

Hi {{first_name}},

Here's a question I've started asking every CFO I meet: "Of your top 10 customers by revenue, which ones are actually profitable?"

The usual answer is a pause, followed by "I'd have to pull that together." And they're right — the data exists in the ERP, but it's not assembled in a way that answers the question.

Revenue is easy to see. But profitability at the customer level — after you factor in payment terms (some customers pay in 30 days, others stretch to 90), discounts and credits, support or service costs, and the opportunity cost of AR sitting overdue — is a different picture entirely.

One finance leader I talked to ran this analysis and found that their third-largest customer by revenue was actually cash-negative when you factored in 90-day payment terms and the credit notes they issued every quarter. Meanwhile, four smaller customers who paid on time and required zero support were getting less attention from the sales team.

The business was optimising for revenue. Not for profitability. Not because anyone decided to — but because the profitability data wasn't visible where decisions were being made.

I suspect this isn't unique to that company. At {{company_name}}, has the customer picture ever looked different once you actually dug into the numbers?

— Rishi

**CTA:** Reply (conversational)

**Timing:** Day 3

**Segment notes:** Send to all remaining. If they replied to Email 1, Rishi responds personally and pauses the sequence for 5 days before resuming. This email deliberately avoids mentioning "close" or "reconciliation" — it's framed entirely as a business intelligence gap.

---

## Email 3: "What Do I Tell the Board on Thursday?"

**Pain point:** The board meeting is Thursday. The CFO needs a clear, data-backed narrative: where the business stands, what changed, what's at risk, what needs a decision. The *data* exists in the ERP. But the *story* — the MIS report, the charts, the variance explanations, the forward-looking projections — doesn't exist yet. It's going to take 3-5 days of pulling data, formatting templates, checking numbers, and building slides. And it's Wednesday. This is the MIS automation pain point, but reframed from "the template is tedious" to "I can't walk into the most important room of the month with confidence."

**Purpose:** First product introduction. Larry is introduced not as "an MIS automation tool" but as "the thing that gives you the board narrative instantly." The differentiator from the Hail Mary doc (MIS automation) is positioned as a business communication solution, not an accounting efficiency.

**Subject line options:**
- "Your board meeting is Thursday. Do you have the story?"
- "The 3 days between your data and your narrative"
- "What if your board report wrote itself from your ERP?"

**Preview text:** "Your data is in the ERP. Your narrative isn't. That gap costs you 3-5 days every month."

**Body:**

Hi {{first_name}},

In my last two emails I talked about the decisions that stall because financial data takes too long to assemble — hiring, customer profitability, resource allocation.

There's one moment where all of those converge: the board meeting.

The board meeting is Thursday. You need a clear narrative: where the business stands financially, what changed since last month, what's at risk, and what needs a decision. The data exists in your ERP. But the story — the MIS report with the right charts, the variance explanations, the forward-looking projections — doesn't exist yet. That takes 3-5 days of pulling, formatting, checking, and rebuilding.

And you've done this exact exercise every month for years. The template barely changes. The process never gets faster. It's not analysis — it's assembly.

I built something to eliminate that gap. It's called Larry — an AI finance assistant that connects to your ERP (QuickBooks, Xero, Zoho Books, or ERPNext) and gives you the narrative instantly.

Upload your MIS template, and Larry generates the report from live data — formatting, charts, period comparisons, variance highlights. No template? Larry generates one. Three minutes instead of three days.

But the board report is just the starting point. Once Larry has your ERP data, you can ask it the questions from my previous emails:

- "Can we afford to hire two more engineers?" — answered in 30 seconds, with the cash flow impact modelled
- "Which customers are actually profitable after payment terms and credits?" — broken down with the numbers
- "What's our burn rate trend over the last 6 months?" — with the chart ready to drop into your deck

Free tier. 10 questions a day. No credit card. Takes 5 minutes to connect your ERP.

→ {{signup_link}}

— Rishi

**CTA:** Sign up free → {{signup_link}}

**Timing:** Day 7

**Segment notes:** Send to all who haven't signed up. If they replied to previous emails, personalise the opening to reference their reply. This email deliberately closes the loop on Emails 1 and 2 — the reader should feel "oh, the same tool that solves the board reporting problem also solves the other two things he mentioned."

---

## Email 4: "How Long Does Our Runway Last?"

**Pain point:** Every CFO and CEO carries a number in the back of their head: how long does our runway last at current burn? It's the number behind every other decision — whether to hire, whether to invest, when to fundraise, whether to renew that vendor contract. But the "confident" version of that number (not the directional guess) requires modelling current cash, committed expenses, projected revenue, and AR collection patterns. Most CFOs update this monthly, during close. Between updates, decisions are made against a number that's 2-4 weeks stale. Larry makes runway a live, always-current answer.

**Purpose:** Social proof email anchored on the single number that drives every business decision. Shows Larry in action with a scenario that every CFO/CEO will recognise — not as a crisis situation, but as the constant background calculation that every finance leader runs.

**Subject line options:**
- "How long does your runway last at current burn?"
- "The number in the back of every CFO's head"
- "She got her runway answer in 10 seconds"

**Preview text:** "At current burn, with your actual collection rates, how many months do you have?"

**Body:**

Hi {{first_name}},

There's a number every CFO carries in the back of their head: how long does our runway last at current burn?

It's not a crisis question. It's the background calculation that drives everything else. Can we hire? Depends on runway. Should we renew that vendor? Depends on runway. When do we start fundraising? Depends on runway.

The problem is that the "confident" version of that number — not the rough estimate, but the precise answer based on current cash, committed expenses, projected revenue, and actual AR collection patterns — is expensive to produce. Most CFOs I talk to update their runway model monthly, usually during close. Between updates, the number in everyone's head is 2-4 weeks stale. Decisions get made against last month's picture.

A CFO I work with used to spend half a day every two weeks rebuilding her runway model from scratch. Current cash position, AR aging patterns, committed payroll and vendor costs, stress-testing 2-3 scenarios. By the time she presented it, her CEO had already been making decisions based on the old number.

She connected her Xero account to Larry and asked: "At our current burn rate, adjusted for actual AR collection patterns, how long does our runway last?"

Larry answered in 10 seconds. Based on live ERP data, with every assumption visible. She followed up: "What happens to runway if we hire 3 engineers at $150K loaded cost?" Larry modelled the scenario instantly.

Now she has a live number. Hiring decisions that used to take 2 weeks of back-and-forth happen in a single meeting. Budget conversations start with "here's our current runway at three different burn scenarios" instead of "let me pull that together and get back to you."

→ See what Larry finds in your data: {{signup_link}}

— Rishi

**CTA:** Sign up free → {{signup_link}}

**Timing:** Day 12

**Segment notes:** Send to all who haven't signed up. If they clicked the signup link from Email 3 but didn't complete, send a "finish your signup" nudge on Day 10 instead, then resume with this email on Day 14. The social proof in this email should be updated with real customer data once available — the scenario above is illustrative.

---

## Email 5: "Where Is the Money Actually Going?"

**Pain point:** Two related business problems. (1) Strategic spend visibility — the CFO knows total expenses, but can't quickly answer "where has our spend shifted in the last quarter?" at a strategic level. Which departments are over budget? Where are costs creeping up without anyone approving the increase? This is not about line-item review — it's about the business's spending pattern changing without anyone noticing until it's too late. (2) The Monday morning question — every week the CEO or leadership team needs a picture of where the business stands. Revenue movement, cash position, key customer changes, spend trends. Assembling this picture is a manual ritual that takes hours and produces a snapshot that's already stale.

**Purpose:** Final email. Anchors on the "I can't see where the business is going" problem. Hybrid CTA: self-serve signup or 15-minute call.

**Subject line options:**
- "Your spending pattern changed last quarter. Did you notice?"
- "Where the money goes when nobody's watching"
- "One last question, then I'll stop"

**Preview text:** "This is my last email. One question: do you know where your spend shifted last quarter?"

**Body:**

Hi {{first_name}},

Last email — I promise. One more problem I wanted to surface, because it compounds silently.

**The spend shift nobody approved.**

Every company's spending pattern drifts over time. Vendor costs creep up as auto-renewals hit at higher rates. Departments add tools without central approval. Contractors get extended month after month. None of it shows up as a single alarming line item — but in aggregate, your cost structure has shifted from what the board approved in the budget.

Most CFOs I talk to discover this during budget season or annual planning. By then, 6-12 months of drift has accumulated. They end up doing a forensic exercise to understand "how did we get here?" when the answer is: slowly, one untracked change at a time.

Larry watches for this in real time. Every Monday morning, Larry sends you a brief: what changed in your financials this week, which spending categories shifted, which vendors are new, which customers' payment patterns changed, and where your close process stands. It reads like a briefing from a senior analyst who's been watching your numbers all week — not a dashboard you have to go look at.

Two paths forward:

**Option A:** Sign up free and connect your ERP. Five minutes. Larry will show you where your spend has shifted and what's worth investigating. → {{signup_link}}

**Option B:** If you'd rather see it with a demo dataset first, I have 15-minute slots here. No pitch — just a look at what Larry surfaces for someone in your role. → {{calendar_link}}

And if none of these emails hit the mark — I respect that. Reply "not relevant" and I'll take you off the list. No hard feelings.

— Rishi

**CTA:** Dual — {{signup_link}} and {{calendar_link}}

**Timing:** Day 18

**Segment notes:** Final email in outbound sequence. Non-responders exit and move to a long-term nurture list (monthly content email, not product emails). Include the explicit opt-out ("reply not relevant") to maintain list hygiene and sender reputation.

---

## Outbound Sequence Flow

```
[Prospect enters sequence]
        |
        v
    Email 1 (Day 0) — "Can we afford to hire?"
    Pain: Resource decisions stall on slow data
        |
    Replied? ──Yes──> Rishi responds personally, pause 5 days then resume
        |
        No
        v
    Email 2 (Day 3) — "Which customers make us money?"
    Pain: Revenue ≠ profitability, but the data doesn't exist
        |
    Replied? ──Yes──> Rishi responds personally, pause 5 days then resume
        |
        No
        v
    Email 3 (Day 7) — "What do I tell the board?" [FIRST PRODUCT MENTION]
    Pain: Board narrative takes 3-5 days to assemble
    Larry introduced as the solution to Emails 1, 2, AND 3
        |
    Signed up? ──Yes──> [EXIT → Enter Engagement Sequence]
        |
        No
        |
    Clicked signup link? ──Yes──> "Finish your signup" nudge (Day 10)
        |                              |
        No                         Signed up? ──Yes──> [EXIT]
        v                              |
    Email 4 (Day 12) — "How long does runway last?"    No ──> Continue
    Pain: Runway at current burn — the number behind every decision
        |
    Signed up? ──Yes──> [EXIT → Enter Engagement Sequence]
        |
        No
        v
    Email 5 (Day 18) — "Where is the money going?"
    Pain: Spend drift + the Monday data pull
    CTA: Signup OR book 15-min call
        |
    Signed up OR booked call? ──Yes──> [EXIT]
        |
        No
        v
    [EXIT → Move to monthly nurture list]
```

---

# SEQUENCE 2: POST-SIGNUP ENGAGEMENT (Signup → Activation → Conversion)

## Strategy

**Narrative arc:** Welcome + first value → Deepen engagement → Show what they're missing → Convert or enterprise handoff

**Journey mapping:** This sequence is primarily **behavior-triggered**, not calendar-driven. Time-based emails exist as fallbacks when no behavioral trigger fires.

**Key principle:** Every email shows their data, not our features. Every email references something Larry actually found or did.

**Email classification:**
- E1 is **transactional** (ERP sync confirmation) — exempt from the 2/week marketing email cap
- All other emails (E2–E10) are **marketing/engagement** — subject to the 2/week cap
- Minimum 72 hours between marketing emails in Week 1 to prevent back-to-back sends

**Revised time-based cadence (typical user):**
- Day 0: E1 (transactional, exempt)
- Day 1: E2 (marketing slot 1, Week 1)
- Day 4: E3 (marketing slot 2, Week 1)
- Day 8+: E4 first weekly brief (marketing slot 1, Week 2)
- Day 8–9: E5 MIS nudge (marketing slot 2, Week 2, 48hrs after E4)

**Exit conditions:**
- Upgrades to any paid tier → exit engagement sequence, enter post-conversion onboarding
- Triggers enterprise sales handoff signal → exit sequence, enter sales-touched cadence
- Churns (no login for 21+ days) → exit sequence, enter re-engagement/win-back

**Suppression rules:**
- Never send an engagement email within 24 hours of the user's last session (they're already active)
- Never send upgrade emails to users in active sales conversations
- Max 2 marketing emails per week regardless of triggers (E1 is transactional and exempt)
- Minimum 72 hours between marketing emails during Week 1

---

## Sequence Overview

| # | Email | Trigger | Timing | Purpose |
|---|-------|---------|--------|---------|
| E1 | Larry is ready | ERP sync completes | Immediate (transactional, exempt from 2/week cap) | First value moment — drive back to product |
| E2 | What Larry found | 24hrs after ERP sync, user hasn't returned | Day 1 (marketing slot 1, Week 1) | Re-engagement hook with real data insight |
| E3 | Your close snapshot | User asked 3+ questions OR Day 4, AND 72hrs since last marketing email | Day 4 (marketing slot 2, Week 1) | Introduce Close Tracker with their data |
| E4 | Your first weekly brief | Monday after signup (earliest Day 8) | Weekly (Monday AM, starting Week 2) | Recurring engagement — CFO briefing style |
| E5 | MIS ready for you | User hasn't tried MIS feature by Day 8–9, 48hrs after E4 | Day 8–9 (marketing slot 2, Week 2) | Drive MIS adoption — key differentiator |
| E6 | You're hitting the ceiling | User hits daily question cap | Behavioral | Upgrade nudge — show what they're missing |
| E7 | Rishi's personal note | User asked 30+ questions total | Behavioral | Personal upgrade email from Rishi |
| E8 | Enterprise signal | User asks about multi-entity, consolidation, or Book Close | Behavioral | Warm handoff to sales conversation |
| E9 | We noticed you've been quiet | No login for 7 days | Day 7 of inactivity | Re-engagement with a fresh insight |
| E10 | Last insight from Larry | No login for 14 days after E9 | Day 14 of inactivity | Final re-engagement attempt |

---

## Email E1: Larry Is Ready

**Trigger:** ERP sync completes successfully
**Classification:** Transactional (exempt from 2/week marketing email cap)

**Purpose:** Get the user back into the product immediately. This is the moment Larry has something to show — the email should create urgency to see it. Classified as transactional because the user just connected their ERP and expects confirmation — standard practice for SaaS onboarding.

**Subject line options:**
- "Larry found {{insight_count}} things in your {{erp_name}} data"
- "Your {{erp_name}} data is ready — here's what Larry sees"
- "Larry's first take on your financials"

**Preview text:** "Larry has already spotted some patterns worth discussing."

**Body:**

Hi {{first_name}},

Larry just finished analyzing your {{erp_name}} data. Here's where things stand.

---

<!-- VISUAL: Setup Completeness Bar (Courier HTML block) -->
<!-- Horizontal progress bar showing data readiness. Green fill = % complete. -->
<!-- Example: ████████████░░░░ 78% Data Ready -->

**YOUR DATA AT A GLANCE**

| | |
|---|---|
| Data completeness | **{{data_completeness_pct}}%** |
| Accounts synced | **{{accounts_synced}}** of {{accounts_total}} |
| Transactions analyzed | **{{transactions_analyzed}}** |
| Date range covered | **{{date_range_start}}** — **{{date_range_end}}** |

---

**WHAT LARRY FOUND**

<!-- VISUAL: Insight Cards (Courier HTML block) -->
<!-- 2-3 stacked cards, each with a colored left border: -->
<!-- - Amber border = Needs attention -->
<!-- - Blue border = Informational -->
<!-- - Red border = Risk/anomaly -->
<!-- Each card: Icon + headline + one-liner + severity tag -->

**{{insight_1_headline}}** — {{insight_1_one_liner}}
{{#if insight_1_severity_high}}⚠ Needs attention{{/if}}

{{#if insight_2_headline}}**{{insight_2_headline}}** — {{insight_2_one_liner}}{{/if}}

Larry flagged **{{insight_count}}** patterns total. {{remaining_insight_teaser}}.

→ Ask Larry about it: {{app_link}}

— Rishi

---

### Good to Have

Surface these if the data supports it — they increase click-through by showing breadth of analysis:

- **Top vendor by spend** — "Your largest vendor is {{top_vendor}} at {{top_vendor_amount}}/mo"
- **AR aging snapshot** — "{{ar_overdue_count}} invoices are overdue, totaling {{ar_overdue_amount}}"
- **Cash position indicator** — "Current cash: {{cash_position}} ({{cash_trend}} vs. last month)"
- **Anomaly count** — "Larry spotted {{anomaly_count}} unusual transactions worth reviewing"

### Risks / Needs Oversight

These are red flags Larry should surface proactively in the email. If any are true, add a "Needs Your Attention" section above the insights:

- **Incomplete sync** — Data completeness below 80%. Message: "Larry is still pulling some data — {{missing_data_description}}. Your analysis will update as more data flows in."
- **Missing bank accounts** — No bank account connected. Message: "Larry can't run cash analysis yet. Connect your bank accounts to unlock cash flow insights." (This is the #1 blocker from the Inflect data — "Blocked on Add Bank Accounts")
- **Stale data** — Most recent transaction is >7 days old. Message: "Your most recent transaction is from {{last_txn_date}}. If your ERP is current, Larry may need a re-sync."
- **Single-entity limitation** — Only one entity detected but company profile suggests multi-entity. Message: "Larry found data for one entity. If you have others, connect them for consolidated analysis."

### Key Metrics to Track

**Customer-facing (embedded in email):**
- Data completeness % (progress bar)
- Accounts synced (X of Y)
- Insight count (number of patterns found)
- Transaction volume analyzed

**Internal (email performance + trial health):**
- Open rate (target: 70%+ — this is transactional, should be high)
- Click-through to app (target: 40%+)
- Time from email open → first app session
- % of users who return to app within 2 hours of this email
- Data completeness at time of send (flag users below 80% for CS follow-up)

### Visual Design (Courier Template Specs)

**1. Data Readiness Bar**
- Type: HTML table-based progress bar
- Width: 100% of content area
- Height: 24px
- Fill color: #22C55E (green) for complete, #F59E0B (amber) for 50-79%, #EF4444 (red) for <50%
- Label: "{{data_completeness_pct}}% Data Ready" right-aligned
- Courier implementation: Custom HTML block with Handlebars conditional for color

**2. Insight Cards**
- Type: Stacked card layout (HTML table rows)
- Left border: 4px solid, color varies by severity (Red = risk, Amber = attention, Blue = informational)
- Background: #F9FAFB (light gray)
- Padding: 16px
- Content: Bold headline, one-line description, severity tag (colored pill)
- Max 3 cards in email, "See {{remaining_count}} more" link below

**3. Data Summary Table**
- Type: 2-column HTML table
- Left column: Metric label (gray text, 14px)
- Right column: Value (black, bold, 16px)
- Row separator: 1px #E5E7EB bottom border
- No outer border

**CTA:** "Ask Larry about it" → {{app_link}}

**Timing:** Immediate on sync completion

**Segment notes:** Requires ERP connection. If sync fails, send a different email (troubleshooting + offer to help). If data completeness is below 50%, delay this email until sync catches up — send a "still syncing" placeholder instead.

**Personalization required:** {{erp_name}}, {{data_completeness_pct}}, {{accounts_synced}}, {{accounts_total}}, {{transactions_analyzed}}, {{date_range_start}}, {{date_range_end}}, {{insight_1_headline}}, {{insight_1_one_liner}}, {{insight_1_severity_high}}, {{insight_2_headline}}, {{insight_2_one_liner}}, {{insight_count}}, {{remaining_insight_teaser}} — all pulled from Larry's initial analysis engine via API.

---

## Email E2: What Larry Found

**Trigger:** 24 hours after ERP sync AND user hasn't returned to the app

**Purpose:** The re-engagement hook. Uses real data to create a reason to come back. This is the critical Day 1 retention email. The Inflect data shows that users who don't return within 24 hours have a significantly higher churn risk — this email must make the data feel too interesting to ignore.

**Subject line options:**
- "{{primary_insight_headline}}"
- "{{dollar_amount}} — Larry found something in your {{erp_name}}"
- "Your {{category}} spend shifted {{percent}}% last quarter"

**Preview text:** "Your data kept updating. Here's what changed."

**Body:**

Hi {{first_name}},

You connected your {{erp_name}} yesterday. Larry has been analyzing overnight. Here's the headline:

---

<!-- VISUAL: Primary Insight Card (Courier HTML block) -->
<!-- Large card with colored top border based on severity -->
<!-- Contains: headline, dollar amount (large font), trend arrow, detail text -->

**{{primary_insight_headline}}**

<!-- VISUAL: Metric Callout -->
<!-- Large number in bold (32px), with trend arrow (↑ red or ↓ green) and % change -->
<!-- Example: $42,300  ↑ 18% vs. last quarter -->

**{{primary_metric_value}}** {{primary_metric_trend_direction}} **{{primary_metric_change_pct}}%** vs. {{comparison_period}}

{{primary_insight_detail — 2-3 sentences with specific numbers, each under 15 words}}

---

<!-- VISUAL: Three-Column Quick Stats (Courier HTML block) -->
<!-- Three stat boxes side by side, each with: small label, large number, trend indicator -->

| What Larry checked | Status |
|---|---|
| Transactions scanned | **{{transactions_scanned}}** |
| Vendors analyzed | **{{vendors_analyzed}}** |
| Anomalies flagged | **{{anomalies_flagged}}** |

---

{{#if secondary_insight_headline}}
Larry also noticed: **{{secondary_insight_headline}}**. {{secondary_insight_teaser}}.
{{/if}}

The full breakdown is ready — including which vendors are driving the change and how this compares to your previous quarter.

→ See the full analysis: {{app_link}}

— Rishi

---

### Good to Have

Include these if available — they add specificity that drives clicks:

- **Vendor concentration risk** — "{{top_vendor_pct}}% of your spend goes to {{top_3_vendors}}. If any one vendor raises prices, it's material."
- **Payment pattern anomaly** — "{{late_payment_count}} invoices were paid late last quarter, costing an estimated {{late_fee_amount}} in penalties or lost discounts."
- **Recurring charge drift** — "Larry found {{new_recurring_count}} new recurring charges since {{date}} that weren't in your prior quarter."
- **Revenue vs. collection gap** — "You invoiced {{invoiced_amount}} last month but collected {{collected_amount}} — a {{collection_gap_pct}}% gap."

### Risks / Needs Oversight

Red flags to surface directly in the email — these replace the generic insight if detected:

- **Spend spike (>15% QoQ in any category)** — Headline the email with this. Message: "Your {{category}} spend jumped {{pct}}% quarter-over-quarter. The top 3 drivers: {{driver_1}}, {{driver_2}}, {{driver_3}}."
- **Vendor added without pattern** — A new vendor appears with >$5K in charges and no prior history. Message: "New vendor alert: {{vendor_name}} — {{amount}} in charges. Larry hasn't seen this vendor in your prior data."
- **AR aging deterioration** — Average days-to-pay increased. Message: "Your customers are paying slower. Average collection time went from {{old_days}} to {{new_days}} days."
- **Cash position decline** — Cash dropped >10% month-over-month. Message: "Your cash position declined {{decline_pct}}% since last month. Current: {{cash_position}}."
- **Duplicate or unusual transactions** — Message: "Larry flagged {{dup_count}} transactions that may be duplicates or need review, totaling {{dup_amount}}."

### Key Metrics to Track

**Customer-facing (embedded in email):**
- Primary insight with dollar amount and % change (the hook)
- Transactions scanned / vendors analyzed (shows depth of analysis)
- Anomaly count (creates urgency to investigate)
- Trend direction with comparison period

**Internal (email performance + trial health):**
- Click-through rate (target: 20%+ — this is the highest-leverage engagement email)
- Time from email open → app session (target: <1 hour)
- % of users who ask a follow-up question about the emailed insight (measures if the insight resonated)
- Correlation between insight severity and CTR (calibrate which insight types to lead with)
- Non-return rate after this email (users who don't click = high churn risk, trigger CS outreach)

### Visual Design (Courier Template Specs)

**1. Primary Insight Card**
- Type: Full-width card with 4px top border
- Top border color: Conditional — #EF4444 (red) for risk/anomaly, #F59E0B (amber) for attention, #3B82F6 (blue) for informational
- Background: #FFFFFF with 1px #E5E7EB border
- Padding: 24px
- Headline: 18px bold, #111827
- Detail text: 14px, #6B7280

**2. Metric Callout**
- Type: Inline HTML
- Primary number: 32px bold, #111827
- Trend arrow: Inline SVG or Unicode ↑/↓
- Arrow color: #EF4444 for unfavorable trends, #22C55E for favorable
- Change %: 16px bold, same color as arrow
- Comparison text: 14px, #9CA3AF

**3. Quick Stats Row**
- Type: 3-column HTML table (stacks on mobile)
- Each cell: Centered, 100px min-width
- Label: 12px uppercase, #9CA3AF
- Value: 24px bold, #111827
- Bottom border: 2px solid, color matches insight severity

**CTA:** "See the full analysis" → {{app_link}}

**Timing:** 24 hours post-ERP sync (skip if user has logged back in)

**Segment notes:** Only send to users who connected ERP but haven't returned. If user returned and engaged, skip this email entirely. The insight chosen for the headline should be the highest-severity finding — prioritize risks over informational patterns.

**Personalization required:** {{erp_name}}, {{primary_insight_headline}}, {{primary_metric_value}}, {{primary_metric_trend_direction}}, {{primary_metric_change_pct}}, {{comparison_period}}, {{primary_insight_detail}}, {{transactions_scanned}}, {{vendors_analyzed}}, {{anomalies_flagged}}, {{secondary_insight_headline}}, {{secondary_insight_teaser}} — all from Larry's analysis API.

---

## Email E3: Your Close Snapshot

**Trigger:** User has asked 3+ Larry questions OR it's Day 4 post-signup (whichever comes first) AND at least 72 hours since last marketing email

**Purpose:** Introduce Close Tracker using their actual data. Plant the seed for the paid feature without making it feel like a pitch. The 72hr minimum gap from the last marketing email prevents back-to-back sends in Week 1. This email should feel like a CFO's close status report — not a product tour.

**Subject line options:**
- "Your close: {{reconciled_pct}}% reconciled, {{pace_assessment}}"
- "Your bank recon is {{bottleneck_days}} days behind pace"
- "Where your {{current_month}} close stands right now"

**Preview text:** "Larry tracked your close phases from your ERP activity."

**Body:**

Hi {{first_name}},

Larry has been tracking your close from your {{erp_name}} activity. Here's where your {{current_month}} close stands.

---

<!-- VISUAL: Close Progress Tracker (Courier HTML block) -->
<!-- Horizontal multi-phase progress bar showing close stages -->
<!-- Each phase: colored segment (green = done, amber = in progress, gray = not started, red = behind) -->
<!-- Labels below each segment: Bank Recon | Sub-ledger | Journal Entries | Review | Reporting -->

**CLOSE PROGRESS**

<!-- VISUAL: Phase Bar -->
<!-- ████████░░░░░░░░░░░░░░░░ -->
<!-- Bank Recon ✓ | Sub-ledger ● | JEs ○ | Review ○ | Reporting ○ -->

| Close Phase | Status | Progress |
|---|---|---|
| Bank reconciliation | {{bank_recon_status}} | {{bank_recon_pct}}% |
| Sub-ledger reconciliation | {{subledger_status}} | {{subledger_pct}}% |
| Journal entries | {{je_status}} | {{je_count}} of ~{{je_expected}} posted |
| Review & adjustments | {{review_status}} | {{review_pct}}% |
| Reporting | {{reporting_status}} | {{reporting_status_label}} |

---

<!-- VISUAL: Three Key Metrics (Courier HTML block) -->
<!-- Three stat boxes: Reconciled %, Estimated Days to Close, Bottleneck -->

| Reconciled | Est. Days to Close | Pace |
|---|---|---|
| **{{reconciled_pct}}%** | **{{est_days_to_close}}** | **{{pace_assessment}}** |

---

{{#if bottleneck_detected}}
<!-- VISUAL: Bottleneck Alert Card (Courier HTML block) -->
<!-- Card with red left border, warning icon -->
**⚠ BOTTLENECK DETECTED**

Your slowest step is **{{bottleneck_name}}** — averaging **{{bottleneck_days}} days** vs. **{{benchmark_days}} days** for similar companies. This is adding **{{bottleneck_impact_days}} days** to your close.

{{#if bottleneck_root_cause}}Larry's assessment: {{bottleneck_root_cause}}.{{/if}}
{{/if}}

{{#if ahead_of_pace}}
**Your close is running {{days_ahead}} days ahead of last month.** {{pace_positive_note}}.
{{/if}}

This is Larry's Close Tracker — close visibility from your ERP activity, without the spreadsheet.

→ See your full close dashboard: {{app_link_close_tracker}}

— Rishi

---

### Good to Have

Surface these if the data supports it — they deepen the close visibility story:

- **Month-over-month comparison** — "Last month you closed in {{last_close_days}} days. At current pace, this month is tracking to {{current_pace_days}} days."
- **Unreconciled items count** — "{{unreconciled_count}} transactions remain unreconciled, totaling {{unreconciled_amount}}."
- **JE patterns** — "You've posted {{je_count}} journal entries. {{je_recurring_count}} are recurring entries Larry can auto-detect next month."
- **Close calendar position** — "If your close deadline is {{close_deadline}}, you're {{days_remaining}} days away with {{remaining_tasks}} tasks remaining."
- **Peer benchmark** — "Companies your size typically close in {{benchmark_days}} days. You're currently at {{current_pace_days}}."

### Risks / Needs Oversight

Flags to surface directly in the email — these appear in the "Bottleneck" section or as a separate "Needs Attention" block:

- **Bank recon stalled** — No recon activity in >3 days while other close phases are progressing. Message: "Your bank reconciliation hasn't moved since {{last_recon_date}}. This is typically the longest phase — starting it earlier can shave {{potential_save_days}} days off your close."
- **JE count anomaly** — Significantly fewer JEs posted than expected based on historical pattern. Message: "You've posted {{je_count}} journal entries this period vs. {{je_historical_avg}} average. {{je_count_diff}} entries may still be pending."
- **Close pace deteriorating** — Close is tracking slower than last month. Message: "At Day {{close_day}}, you're {{pct_behind}}% behind last month's pace. Key gap: {{gap_phase}}."
- **Missing sub-ledger data** — Sub-ledger reconciliation can't run due to missing data. Message: "Larry can't reconcile your {{missing_subledger}} sub-ledger — this data source may need to be connected or re-synced."
- **Review bottleneck** — Multiple items flagged for review but none resolved. Message: "{{pending_review_count}} items are waiting for review. The oldest has been pending {{oldest_review_days}} days."

### Key Metrics to Track

**Customer-facing (embedded in email):**
- Close phase progress (per-phase % and status)
- Overall reconciliation %
- Estimated days to close
- Pace assessment (ahead/on track/behind)
- Bottleneck identification with impact quantification

**Internal (email performance + trial health):**
- Click-through to Close Tracker dashboard (target: 25%+ — this is the conversion hook for paid tier)
- % of users who visit Close Tracker for the first time from this email
- Correlation between bottleneck detection and CTR (do alerts drive more engagement?)
- Close Tracker return rate (do users come back to Close Tracker in the next 7 days?)
- Feature adoption: % of E3 recipients who later use Close Tracker at least 3x (leading indicator for upgrade)

### Visual Design (Courier Template Specs)

**1. Close Phase Progress Bar**
- Type: Multi-segment horizontal bar (HTML table with colored cells)
- Total width: 100% of content area
- Segments: 5 phases, proportional width based on typical close duration
- Segment colors: #22C55E (complete), #F59E0B (in progress), #E5E7EB (not started), #EF4444 (behind/blocked)
- Phase labels: Below each segment, 12px, #6B7280
- Status icons: ✓ (complete), ● (in progress), ○ (not started), ⚠ (behind)

**2. Key Metrics Row**
- Type: 3-column HTML table
- Each cell: Centered, equal width
- Label: 12px uppercase, #9CA3AF
- Value: 28px bold, color-coded (green for good, amber for watch, red for behind)
- Bottom accent: 3px solid bar matching value color

**3. Bottleneck Alert Card**
- Type: Full-width card with 4px left border
- Border color: #EF4444 (red)
- Background: #FEF2F2 (light red tint)
- Icon: ⚠ warning triangle
- Headline: 16px bold, #991B1B
- Body: 14px, #7F1D1D
- Only renders if {{bottleneck_detected}} is true (Courier conditional block)

**4. Ahead-of-Pace Card** (alternative to bottleneck)
- Type: Full-width card with 4px left border
- Border color: #22C55E (green)
- Background: #F0FDF4 (light green tint)
- Headline: 16px bold, #166534
- Only renders if {{ahead_of_pace}} is true

**CTA:** "See your full close dashboard" → {{app_link_close_tracker}}

**Timing:** Behavioral (3+ questions) or Day 4 fallback, with 72hr minimum gap from last marketing email

**Segment notes:** Only for users with connected ERP. Close Tracker data must have populated — if insufficient ERP activity, delay this email. If close activity is minimal (e.g., very early in the month with <10% of expected activity), consider delaying until more data is available.

**Personalization required:** {{erp_name}}, {{current_month}}, {{bank_recon_status}}, {{bank_recon_pct}}, {{subledger_status}}, {{subledger_pct}}, {{je_status}}, {{je_count}}, {{je_expected}}, {{review_status}}, {{review_pct}}, {{reporting_status}}, {{reporting_status_label}}, {{reconciled_pct}}, {{est_days_to_close}}, {{pace_assessment}}, {{bottleneck_detected}}, {{bottleneck_name}}, {{bottleneck_days}}, {{benchmark_days}}, {{bottleneck_impact_days}}, {{bottleneck_root_cause}}, {{ahead_of_pace}}, {{days_ahead}}, {{pace_positive_note}} — from Larry's Close Tracker engine.

---

## Email E4: Weekly Brief (Recurring)

**Trigger:** Every Monday at 8 AM local time, starting the first Monday after signup (minimum Day 8)

**Purpose:** Recurring engagement. Should feel like a CFO briefing, not a product notification. This is the primary retention mechanism through the Day 7–14 drop-off window. Starting in Week 2 (not Week 1) prevents the weekly brief from competing with onboarding emails E2 and E3, and lands right when the drop-off risk peaks. This email should feel like it was written by a senior analyst on the user's team — not by a product.

**Subject line options:**
- "Week of {{date}}: {{headline_change}}"
- "{{company_name}} weekly: {{change_count}} things shifted"
- "Your Monday brief — {{primary_alert_headline}}"

**Preview text:** "New vendors, expense shifts, and your close status."

**Body:**

<!-- VISUAL: Weekly Brief Header Bar (Courier HTML block) -->
<!-- Dark banner (#111827) with white text, company name, date range -->
<!-- Looks like a professional report header -->

**{{company_name}} — Weekly Financial Brief**
Week of {{week_start_date}} | Prepared by Larry

---

<!-- VISUAL: Health Dashboard — Three Traffic Light Indicators (Courier HTML block) -->
<!-- Three side-by-side boxes, each with a colored dot (green/amber/red) + label + value -->
<!-- Modeled on the Inflect "health score" concept but customer-facing -->

| Spend Trend | Cash Position | Close Status |
|---|---|---|
| {{spend_trend_indicator}} | {{cash_position_indicator}} | {{close_status_indicator}} |
| {{spend_trend_label}} | {{cash_position_label}} | {{close_status_label}} |

<!-- Indicator colors: 🟢 = stable/healthy, 🟡 = watch, 🔴 = needs attention -->

---

**WHAT CHANGED THIS WEEK**

<!-- VISUAL: Change Cards (Courier HTML block) -->
<!-- Stacked cards, each with: severity dot (left), headline, detail, $ impact -->
<!-- Sorted by severity: red first, then amber, then blue -->

{{#each weekly_changes}}
<!-- Card with {{this.severity}} left border -->
**{{this.headline}}**
{{this.detail}}
{{#if this.dollar_impact}}Impact: **{{this.dollar_impact}}**{{/if}}

{{/each}}

---

{{#if risks_detected}}
**⚠ NEEDS YOUR ATTENTION**

<!-- VISUAL: Risk Alert Section (Courier HTML block) -->
<!-- Red-tinted background section (#FEF2F2) -->

{{#each risks}}
- **{{this.title}}**: {{this.description}}
{{/each}}
{{/if}}

---

**CLOSE STATUS**

<!-- VISUAL: Mini Close Progress Bar (same design as E3, but compact) -->
<!-- Single-line progress indicator with phase dots -->

{{close_status_detail}}

| Phase | Status |
|---|---|
| Bank recon | {{bank_recon_indicator}} {{bank_recon_pct}}% |
| Journal entries | {{je_indicator}} {{je_count}}/{{je_expected}} |
| Overall pace | {{pace_indicator}} {{pace_label}} |

---

**WORTH ASKING LARRY**

<!-- VISUAL: Question Cards (Courier HTML block) -->
<!-- Clickable cards with question text, each linking to app with pre-loaded question -->

→ "{{suggested_question_1}}" — {{question_1_context}}
→ "{{suggested_question_2}}" — {{question_2_context}}

---

→ Open Larry: {{app_link}}

— Rishi

---

### Good to Have

Include these sections when data supports them — they make the brief feel comprehensive:

- **New vendors this week** — "{{new_vendor_count}} new vendors appeared: {{new_vendor_list}} (total: {{new_vendor_spend}}). None were in your prior quarter data."
- **AR aging movement** — "{{ar_aging_improvement_or_decline}}: {{ar_over_90_count}} invoices over 90 days ({{ar_over_90_total}}), {{ar_movement_vs_last_week}}."
- **Budget vs. actual snapshot** — "MTD spend: {{mtd_spend}} vs. {{mtd_budget}} budget ({{budget_variance_pct}}% {{over_under}})."
- **Upcoming commitments** — "{{upcoming_payments_count}} payments due this week totaling {{upcoming_payments_total}}. Largest: {{largest_upcoming_vendor}} ({{largest_upcoming_amount}})."
- **Usage stats** — "You asked Larry {{questions_this_week}} questions this week. Top topic: {{top_topic}}." (Reinforces engagement)

### Risks / Needs Oversight

These should surface in the "Needs Your Attention" section with red-tinted background. Show a maximum of 3 risks per brief to avoid alarm fatigue:

- **Spend anomaly (>15% WoW increase in any category)** — "Your {{category}} spend is up {{pct}}% vs. last week. Top driver: {{driver}}."
- **New unauthorized vendor** — "{{vendor_name}} appeared with {{amount}} in charges. This vendor has no prior history in your data."
- **AR deterioration** — "{{count}} invoices are now past 90 days (up from {{prior_count}} last week). Largest: {{customer_name}} ({{amount}})."
- **Close behind pace** — "Your close is {{days_behind}} days behind last month's pace. Bottleneck: {{bottleneck_phase}}."
- **Cash runway alert** — "At current burn, your runway is {{runway_months}} months. This is {{runway_change}} from last week's estimate."
- **Duplicate/unusual transactions** — "Larry flagged {{flag_count}} transactions for review this week ({{flag_total}})."
- **Recurring charge increase** — "{{vendor_name}} auto-renewed at {{new_amount}} (was {{old_amount}} — {{increase_pct}}% increase)."

### Key Metrics to Track

**Customer-facing (embedded in email):**
- Three health indicators (Spend Trend, Cash Position, Close Status) — traffic light format
- Week-over-week changes with dollar impact
- Close progress (phase-level)
- Risk/attention items (capped at 3)
- Suggested questions with context

**Internal (email performance + trial health):**
- Weekly brief open rate over time (target: 40%+ sustained; declining open rate = churn signal)
- Click-through rate by section (which section drives the most clicks?)
- Correlation between risk alerts and CTR (do alerts drive more engagement?)
- Weeks of consecutive opens (engagement streak — users with 4+ week streaks are high-conversion candidates)
- Weekly brief → question asked within 24hrs (measures if the brief triggers product usage)
- Unsubscribe rate per weekly brief (target: <0.5%; rising rate = content quality issue)

### Visual Design (Courier Template Specs)

**1. Report Header Bar**
- Type: Full-width dark banner
- Background: #111827
- Text: White, 18px bold (company name), 14px normal (date range)
- Padding: 16px 24px
- "Prepared by Larry" in 12px, #9CA3AF

**2. Health Dashboard (Traffic Lights)**
- Type: 3-column HTML table
- Each cell: 120px min-width, centered
- Indicator dot: 12px circle, inline — #22C55E (green), #F59E0B (amber), #EF4444 (red)
- Label: 14px bold, #111827
- Sublabel: 12px, #6B7280
- Courier implementation: Handlebars conditional for color based on health thresholds

**3. Change Cards**
- Type: Stacked list items with left-border severity indicator
- Left border: 4px solid (red/amber/blue based on severity)
- Background: White with subtle #F9FAFB alternating rows
- Headline: 14px bold, #111827
- Detail: 14px, #6B7280
- Dollar impact: 14px bold, color matches severity
- Max 5 changes displayed; "See {{remaining}} more in Larry" link if >5

**4. Risk Alert Section**
- Type: Full-width section with background tint
- Background: #FEF2F2 (red tint) if risks present
- Border: 1px #FECACA
- Items: Bulleted list, 14px, #991B1B
- Only renders if {{risks_detected}} is true

**5. Mini Close Progress Bar**
- Type: Compact version of E3's close tracker
- Single horizontal bar, 16px height
- Phase indicators: Dots or segments
- Labels: Below bar, 11px

**6. Question Cards**
- Type: Clickable blocks with right arrow →
- Background: #F3F4F6 on hover (if supported), #FFFFFF default
- Question text: 14px, #111827
- Context: 12px, #6B7280
- Each links to {{app_link}}?q={{url_encoded_question}} (pre-loads the question in Larry)

**CTA:** "Open Larry" → {{app_link}}

**Timing:** Weekly, Monday 8 AM local, starting first Monday on or after Day 8. Recurring until user churns, upgrades, or unsubscribes.

**Segment notes:** All active free-tier users with connected ERP. Suppress if user logged in within the last 24 hours. The brief should feel progressively more useful — Week 1 may have limited WoW comparison data, so the first brief should lead with absolute metrics and note "Next week, Larry will show you how these numbers changed."

**Personalization required:** {{company_name}}, {{week_start_date}}, {{spend_trend_indicator}}, {{spend_trend_label}}, {{cash_position_indicator}}, {{cash_position_label}}, {{close_status_indicator}}, {{close_status_label}}, {{weekly_changes[]}} (array of change objects with headline, detail, dollar_impact, severity), {{risks_detected}}, {{risks[]}} (array of risk objects), {{close_status_detail}}, {{bank_recon_pct}}, {{je_count}}, {{je_expected}}, {{pace_label}}, {{suggested_question_1}}, {{question_1_context}}, {{suggested_question_2}}, {{question_2_context}} — all from Larry's weekly analysis job.

---

## Email E5: MIS Ready for You

**Trigger:** Day 8–9 post-signup AND user hasn't used the MIS feature (send 48 hours after E4 or Day 9, whichever is later)

**Purpose:** Drive adoption of the key differentiator. MIS automation is called out as "non-negotiable" in the Hail Mary doc — if users don't try it, they're missing the core wedge. Moved from Day 7 to Day 8–9 to prevent collision with the first weekly brief (E4). Unlike the other emails which show insights, this one needs to sell a *workflow* — the user has to take an action (upload a template or generate from scratch).

**Subject line options:**
- "Your {{current_month}} MIS report — ready in 3 minutes"
- "Larry already has the data for your board report"
- "3-5 days of reporting vs. 3 minutes — your call"

**Preview text:** "Your {{erp_name}} data is connected. The MIS report is one click away."

**Body:**

Hi {{first_name}},

You've been using Larry for {{days_since_signup}} days. You've asked {{total_questions}} questions and explored your {{erp_name}} data across {{topics_explored_count}} areas.

One thing you haven't tried yet: the MIS report.

---

<!-- VISUAL: Before/After Comparison (Courier HTML block) -->
<!-- Two-column layout showing manual vs. Larry process -->
<!-- Left column (gray/muted): "The Manual Way" -->
<!-- Right column (highlighted/green): "With Larry" -->

| Without Larry | With Larry |
|---|---|
| Pull data from ERP | ✓ Already connected |
| Format template | ✓ Upload yours or use ours |
| Build charts | ✓ Auto-generated |
| Period comparisons | ✓ Auto-calculated |
| Variance commentary | ✓ Larry drafts it |
| **3–5 days** | **~3 minutes** |

---

<!-- VISUAL: Feature Adoption Tracker (Courier HTML block) -->
<!-- Modeled on Inflect's feature adoption concept -->
<!-- Shows which Larry features the user has tried vs. hasn't -->

**YOUR LARRY USAGE**

| Feature | Status |
|---|---|
| {{#each features}}{{this.name}} | {{this.status_icon}} {{this.status_label}} |{{/each}}

<!-- Status icons: ✅ Used | ⬜ Not tried yet | 🔒 Paid tier -->
<!-- MIS row should be highlighted/emphasized since that's the CTA -->

---

{{#if has_board_meeting_soon}}
<!-- VISUAL: Urgency Card (Courier HTML block) -->
<!-- Amber card if board meeting detected within 14 days -->
**📅 Your next reporting period ends {{period_end_date}}.**
Larry already has your data through {{data_current_date}}. Generate the report before the rush.
{{/if}}

Here's how it works:

**Option A:** Upload the MIS template your board or management uses. Larry maps your ERP data to it — formatting, charts, period comparisons, variance highlights. Done.

**Option B:** No template? Larry generates one in Komplai's format. You can customize it later.

→ Generate your MIS report: {{app_link_mis}}

— Rishi

---

### Good to Have

Include these to increase urgency and specificity:

- **Data readiness confirmation** — "Larry has {{months_of_data}} months of your {{erp_name}} data. That's enough for period comparisons going back to {{earliest_comparison_period}}."
- **Estimated report contents** — "Based on your data, Larry can generate: P&L, balance sheet, cash flow statement, AR aging summary, and {{custom_section_count}} custom sections."
- **Peer social proof** — "Controllers using Larry's MIS feature save an average of {{avg_hours_saved}} hours per month on reporting."
- **Template gallery preview** — "Not sure what format to use? Larry has {{template_count}} templates for {{industry}} companies."
- **Sample output teaser** — "Here's a preview of what your P&L section looks like with live data:" (followed by a mini snapshot — 3-4 rows of actual P&L data from their ERP)

### Risks / Needs Oversight

These flags indicate the user may be at risk of not adopting the core differentiator:

- **Low engagement overall** — User has asked <5 questions in 8 days. This email alone won't save them. Internal flag: trigger CS outreach alongside the email. Message in email: Keep it soft — don't reference low usage. Focus on the value proposition.
- **Data gaps for MIS** — Larry doesn't have enough data for a complete MIS (e.g., missing balance sheet accounts, no prior period for comparison). Message: "Larry can generate a partial report with what's connected. For a complete MIS, you may need to connect {{missing_data_source}}."
- **Feature drop-off pattern** — User explored Larry in Week 1 but hasn't returned since. The Inflect data shows this as "champion inactive" risk. Message: Don't acknowledge the gap — instead, create urgency with the board meeting/reporting deadline angle.
- **No ERP connected** — User signed up but never connected ERP (edge case — E1-E4 should have caught this). Don't send E5. Instead send: "Larry needs your ERP data to generate MIS reports. Connect your {{suggested_erp}} in 5 minutes: {{erp_connect_link}}"

### Key Metrics to Track

**Customer-facing (embedded in email):**
- Days since signup and questions asked (engagement context)
- Feature adoption tracker (which features used vs. not)
- Before/after time comparison (3-5 days vs. 3 minutes)
- Data readiness for MIS generation
- Reporting period urgency (if applicable)

**Internal (email performance + trial health):**
- Click-through to MIS generation page (target: 15%+ — lower than other emails because it requires effort)
- MIS feature adoption rate within 48hrs of email (target: 8-10%)
- Template upload vs. auto-generate split (informs product — do users have templates or need ours?)
- Correlation between questions asked (engagement) and MIS adoption (do engaged users convert to MIS faster?)
- MIS adoption → paid conversion correlation (this is the "non-negotiable" feature — users who try MIS should convert at 2-3x the base rate)
- Non-adoption after E5 = high churn signal (flag for CS intervention)

### Visual Design (Courier Template Specs)

**1. Before/After Comparison**
- Type: 2-column HTML table
- Left column header: "Without Larry" — background #F3F4F6, text #6B7280 (muted)
- Right column header: "With Larry" — background #F0FDF4, text #166534 (green emphasis)
- Left column rows: Plain text, 14px, with strikethrough styling
- Right column rows: ✓ prefix, 14px bold, #166534
- Bottom row (time): Larger text (18px bold), left column #EF4444 ("3–5 days"), right column #22C55E ("~3 minutes")

**2. Feature Adoption Tracker**
- Type: Vertical list with status indicators
- Modeled on Inflect's feature adoption grid
- Each row: Feature name (14px, #111827) + status icon + status label
- Status icons: ✅ (green checkmark) for used, ⬜ (empty box) for not tried, 🔒 (lock) for paid tier
- MIS row: Highlighted with amber background (#FFFBEB) and "← Try this" arrow label
- Courier implementation: Loop through {{features}} array with conditional icon rendering

**3. Urgency Card**
- Type: Full-width card, conditional render
- Background: #FFFBEB (amber tint)
- Border: 1px #FDE68A
- Icon: 📅 calendar
- Text: 14px bold, #92400E
- Only renders if {{has_board_meeting_soon}} is true (detected from close tracker or calendar integration)

**4. Sample P&L Preview** (Good to Have)
- Type: Mini data table
- 4-5 rows of actual P&L data (Revenue, COGS, Gross Margin, OpEx, Net Income)
- Current period vs. prior period columns
- Variance column with green/red coloring
- Watermark overlay: "Preview — Generate full report →"
- Courier implementation: Pre-compute from ERP data, render as HTML table

**CTA:** "Generate your MIS report" → {{app_link_mis}}

**Timing:** Day 8–9, or 48 hours after E4, whichever is later (skip if user has already used MIS feature)

**Segment notes:** Only for users who haven't generated an MIS report. If they have, skip entirely. This is the most important adoption email — MIS is the core differentiator. If the user doesn't try MIS within 3 days of receiving this email, flag for CS follow-up.

**Personalization required:** {{days_since_signup}}, {{total_questions}}, {{erp_name}}, {{topics_explored_count}}, {{features[]}} (array with name, status_icon, status_label), {{has_board_meeting_soon}}, {{period_end_date}}, {{data_current_date}}, {{months_of_data}}, {{earliest_comparison_period}} — from Larry's usage tracking and analysis engine.

---

## Email E6: You're Hitting the Ceiling

**Trigger:** User hits the 10-question daily cap

**Purpose:** Upgrade nudge at the moment of maximum frustration/desire. Show what they're missing, not what you're blocking.

**Subject line options:**
- "Larry found {{x}} more things worth discussing"
- "You asked 10 questions today — here's what's next"
- "Your questions are getting sharper"

**Preview text:** "Unlock unlimited questions and full close tracking."

**Body:**

Hi {{first_name}},

You've asked Larry 10 questions today. That tells me you're finding it useful — and Larry has more to share.

With Scaling ($199/mo), you get:
- **Unlimited questions** — no daily cap
- **Full Close Tracker** — timeline predictions, bottleneck analysis, historical trend comparisons
- **MIS downloads** — export your reports as PDFs
- **Unlimited history** — every conversation preserved

You've asked {{total_questions}} questions since signing up. Here are {{x}} more things Larry found that are worth exploring → {{app_link_upgrade}}

— Rishi

**CTA:** "See what you're missing" → {{app_link_upgrade}}

**Timing:** Immediate on hitting daily cap (max once per week)

**Segment notes:** Free-tier users only. Do not send if user has already seen this email in the past 7 days. Do not send if user is in an active sales conversation.

---

## Email E7: Rishi's Personal Note

**Trigger:** User has asked 30+ total questions (cumulative, any number of sessions)

**Purpose:** Personal upgrade email. The onboarding doc specifies this should reference specific usage data. This is the highest-converting email in the sequence.

**Subject line options:**
- "You've asked Larry {{count}} questions"
- "A note about your Komplai usage"
- "You're one of our most active users"

**Preview text:** "Here's what you'd unlock with Scaling."

**Body:**

Hi {{first_name}},

I wanted to reach out personally. You've asked Larry {{total_questions}} questions since you signed up {{days_since_signup}} days ago. That puts you in the top {{percentile}}% of our users.

Based on what you've been asking about — {{top_topics}} — I think you'd get a lot out of the Scaling tier. Specifically:

- **Timeline predictions** for your close process (you've been tracking close progress — this adds forecasting)
- **Downloadable MIS reports** (you've generated {{mis_count}} reports but can't export them yet)
- **Full conversation history** (you're losing context every 7 days right now)

It's $199/month. One-click upgrade, no sales call required: {{upgrade_link}}

But if you'd rather talk through whether it makes sense, I'm happy to do a quick call: {{calendar_link}}

— Rishi

**CTA:** Dual — {{upgrade_link}} and {{calendar_link}}

**Timing:** Behavioral (30+ cumulative questions). Send once only.

**Segment notes:** Free-tier users only. Suppress if already upgraded or in sales conversation. This email sends once — never repeat.

---

## Email E8: Enterprise Signal

**Trigger:** User asks about multi-entity consolidation, maker-checker workflows, Book Close automation, or matches ICP signals (Series B+, 10+ finance team)

**Purpose:** Warm handoff from self-serve to sales. The Hail Mary doc says enterprise outreach should happen within 48 hours of signal.

**Subject line options:**
- "I noticed something about how you're using Larry"
- "Larry flagged something I wanted to discuss"
- "Quick thought on {{topic_they_asked_about}}"

**Preview text:** "This is exactly what our Book Close module handles."

**Body:**

Hi {{first_name}},

I saw that you asked Larry about {{specific_topic}} — {{specific_question_paraphrase}}.

That's a pattern I see with finance teams that are running into the limits of manual processes. {{Specific_insight_about_their_situation — e.g., "Your intercompany reconciliation complexity suggests you're managing multiple entities, and Larry's Close Tracker is showing consistent bottlenecks in bank recon."}}.

This is exactly the problem our full Book Close module solves — automated JV processing, AI-assisted bank recon, and maker-checker workflows. It's what our enterprise customers use to cut their close from 12+ days to 5.

Would it be helpful to walk through how that would work with your specific setup? I have 15-minute slots here: {{calendar_link}}

No pressure — but I think the conversation would be valuable even if you stay on Scaling.

— Rishi

**CTA:** "Book 15 minutes" → {{calendar_link}}

**Timing:** Within 48 hours of trigger signal

**Segment notes:** Immediately suppress all automated upgrade emails (E6, E7). User enters sales-touched cadence. This email sends once — follow-up is manual from Rishi.

---

## Email E9: Re-engagement (7 Days Inactive)

**Trigger:** No login for 7 consecutive days

**Purpose:** Bring them back with a fresh insight they haven't seen. The onboarding doc notes that Day 7-14 is the critical drop-off window.

**Subject line options:**
- "Larry found something while you were away"
- "{{x}} things changed in your financials this week"
- "Your {{erp_name}} data updated — Larry has notes"

**Preview text:** "Your data kept flowing. Larry kept watching."

**Body:**

Hi {{first_name}},

It's been a week since you last checked in with Larry. In the meantime, your {{erp_name}} data has been updating, and Larry flagged a few things:

{{fresh_insight_1}}
{{fresh_insight_2}}

Your close status also shifted: {{close_status_update}}.

→ See what's new: {{app_link}}

— Rishi

**CTA:** "See what's new" → {{app_link}}

**Timing:** 7 days of inactivity

**Segment notes:** Active free or paid users who haven't logged in. Skip if user already unsubscribed from engagement emails. Requires ERP to still be connected (if disconnected, send a different "reconnect" email).

---

## Email E10: Last Insight from Larry

**Trigger:** 14 days of inactivity after E9 was sent (21 total days of inactivity)

**Purpose:** Final re-engagement attempt. Acknowledge they may have moved on, but leave the door open.

**Subject line options:**
- "Larry's still watching your data"
- "One last thing before I stop emailing"
- "Your financials in 30 seconds"

**Preview text:** "Quick summary of what Larry would tell you if you logged in."

**Body:**

Hi {{first_name}},

I realize Larry might not have been the right fit, or maybe the timing wasn't right. Either way, I wanted to share one last thing before I stop sending these:

**Your quick financial snapshot (as of {{date}}):**
{{snapshot_summary — 3-4 bullet points of key financial state}}

If you ever want to pick it back up, your account and ERP connection are still active. Larry will be here.

And if you have feedback on what would have made Komplai more useful, I'd genuinely appreciate hearing it — just reply to this email.

— Rishi

**CTA:** "Log back in" → {{app_link}} (soft) + "Share feedback" (reply)

**Timing:** 14 days after E9 (21 days total inactivity)

**Segment notes:** Final email in the re-engagement path. If no response, move to quarterly check-in list. Do not send further automated emails.

---

## Engagement Sequence Flow

```
[User signs up and connects ERP]
        |
        v
    E1: "Larry is ready" (immediate on sync, TRANSACTIONAL — exempt from cap)
        |
    User returns? ──Yes──> Continue to E3 trigger
        |
        No (24hrs)
        v
    E2: "What Larry found" (Day 1, marketing slot 1 of Week 1)
        |
        v
    User asked 3+ questions AND 72hrs since E2? OR Day 4?
        |──Yes──> E3: "Your close snapshot" (Day 4, marketing slot 2 of Week 1)
        |
        v
    [Monday, Day 8+] ──> E4: Weekly Brief (recurring every Monday, starts Week 2)
        |
    Day 8-9 (48hrs after E4), MIS not used? ──> E5: "MIS ready for you"
        |
        v
    ┌─────────────────────────────────────────────┐
    │         BEHAVIORAL TRIGGERS                  │
    │                                              │
    │  Hit daily cap ──> E6: "Hitting the ceiling" │
    │  30+ total Qs  ──> E7: "Rishi's personal"   │
    │  Enterprise signal ──> E8: "Enterprise"      │
    │    (suppresses E6 + E7 permanently)          │
    └─────────────────────────────────────────────┘
        |
    No login 7 days ──> E9: "We noticed you've been quiet"
        |
    No login 14 more days ──> E10: "Last insight from Larry"
        |
    [EXIT → Quarterly check-in list]

    ──────────────────────────────────────────
    EXIT CONDITIONS (apply at any point):
    - Upgrades to paid tier → Post-conversion onboarding sequence
    - Enterprise handoff triggered → Sales-touched cadence
    - Unsubscribes → Stop all
    - 21+ days inactive after E10 → Quarterly list
    ──────────────────────────────────────────
```

---

## Branching Logic Summary

| Condition | Action |
|-----------|--------|
| User signs up from outbound sequence | Exit outbound → Enter engagement at E1 |
| ERP sync fails | Send troubleshooting email (not in this sequence) instead of E1 |
| User returns within 24hrs of ERP sync | Skip E2, proceed to E3 trigger |
| User replies to any outbound email | Rishi responds personally, pause sequence |
| User hits question cap | Send E6 (max once per 7 days) |
| User reaches 30+ questions | Send E7 (once only, ever) |
| Enterprise signal fires | Send E8, suppress E6/E7 permanently, exit automated sequence |
| User upgrades | Exit engagement → Enter post-conversion onboarding |
| User inactive 7 days | Send E9 |
| User inactive 21 days (post E9) | Send E10, then exit to quarterly list |
| User active in last 24hrs | Suppress any scheduled engagement email |
| User in active sales conversation | Suppress all upgrade emails (E6, E7) |
| Max 2 marketing emails per week | Queue excess emails for next available slot (E1 is transactional, exempt) |
| Less than 72hrs since last marketing email (Week 1) | Delay next marketing email until 72hr gap is met |

---

## Performance Benchmarks

### Outbound Sequence (Cold)

| Metric | Target | Industry Benchmark |
|--------|--------|--------------------|
| Open rate | 35-45% | 20-30% for cold B2B |
| Reply rate | 8-12% | 3-5% for cold B2B |
| Click-through rate (Email 3-5) | 5-8% | 2-4% for cold B2B |
| Sequence → Signup conversion | 3-5% | 1-2% for B2B SaaS |
| Sequence → Demo booked | 2-3% | 1-2% for B2B SaaS |

Higher targets justified by: highly targeted persona list, founder-led personal tone, genuine value in email content (not just pitch).

### Engagement Sequence (Post-Signup)

| Metric | Target | Industry Benchmark |
|--------|--------|--------------------|
| E1 open rate | 65-80% | 50-70% for onboarding |
| E2 click-through rate | 15-25% | 10-20% for onboarding |
| Day 3 return rate | 40-50% | 30-40% for B2B SaaS |
| Weekly brief open rate | 40-50% | 25-35% for recurring |
| Free → Scaling conversion (30 days) | 5-8% | 3-5% for freemium B2B |
| E7 (personal note) conversion rate | 10-15% | 5-8% for personalized upgrade |
| E8 → Enterprise conversation rate | 25-35% | 15-20% for warm outreach |

---

## A/B Test Recommendations

### Test 1: Outbound Email 1 Subject Line
- **Variant A:** "Your MIS report takes how long?" (curiosity + pain)
- **Variant B:** "Quick question about your monthly reporting" (conversational)
- **Metric:** Open rate
- **Split:** 50/50
- **Sample needed:** 200+ per variant for significance

### Test 2: Engagement E6 — Show Value vs. Show Comparison
- **Variant A:** Current copy (lists what they'd unlock)
- **Variant B:** Side-by-side comparison table: "What you have now vs. what Scaling gives you"
- **Metric:** Upgrade conversion rate
- **Split:** 50/50

### Test 3: Weekly Brief Format — Summary vs. Questions
- **Variant A:** Current format (changes + status + suggested questions)
- **Variant B:** Just 3 questions Larry wants to discuss: "Larry has 3 questions about your financials this week" — creates curiosity without giving away the answers
- **Metric:** Click-through rate and return-to-app rate

### Test 4: E7 Timing — 30 Questions vs. 20 Questions
- **Variant A:** Trigger at 30 cumulative questions
- **Variant B:** Trigger at 20 cumulative questions
- **Metric:** Conversion rate (is earlier better, or does it feel premature?)

---

## Implementation Checklist

1. **Email platform setup** — configure automation triggers for behavioral events (question cap, question count, login activity, ERP sync status, feature usage)
2. **Data pipeline** — Larry's analysis engine must expose: top insights, question counts, close status, MIS usage, and enterprise signal flags via API for email personalization
3. **Suppression logic** — build the suppression rules (24hr activity, sales conversation flag, max 2/week) before launching
4. **Rishi's reply workflow** — outbound replies route to Rishi's inbox with context. He needs a playbook for common reply types
5. **Weekly brief generation** — automated Monday AM job that pulls fresh data per user and populates E4 template
6. **Enterprise signal detection** — instrument Larry conversations to flag keywords (multi-entity, consolidation, Book Close, automation) and ICP match
7. **Unsubscribe handling** — separate unsubscribe for outbound vs. engagement vs. weekly brief. Users should be able to keep the weekly brief but stop upgrade emails
