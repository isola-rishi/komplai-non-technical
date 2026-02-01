# Page-Specific FAQ Recommendations

*Generated: January 31, 2026*

This document contains 5-7 recommended FAQs for each product page. Questions are designed to address common buyer objections, clarify product capabilities, and reduce friction in the decision-making process.

---

## Homepage FAQs

**Target audience:** CFOs, Controllers, and Finance Leaders evaluating Komplai

### 1. What is Komplai and how does it help finance teams?
Komplai is an AI-powered continuous close platform that automates tedious bookkeeping work—like reconciliation, journal entries, and accruals—so finance teams can close faster and focus on analysis. Our AI agent, Larry, learns from how your financials have been maintained, your team's ongoing actions and handles the repetitive 90% of close work.

### 2. How long does it take to implement Komplai?
Most teams are live in 30 minutes to 2 hours. We connect to your existing ERP (QuickBooks, Xero, Zoho Books, or ERPNext) via secure OAuth, sync your historical data, and start matching transactions immediately. There's no multi-month implementation project.

### 3. Will Komplai replace my finance team?
No. Komplai uses a maker-checker workflow: Larry handles the tedious creation work (matching, data entry, voucher generation), and your team reviews and approves. You maintain full control while cutting preparation time by 65%.

### 4. How does the AI learn our specific accounting practices?
Larry builds "memory" from how your financials have been maintained and your team's ongoing actions. When your team classifies an invoice or approves a match, Larry remembers that decision and applies it to similar future transactions. The more you use Komplai, the smarter it gets.

### 5. What if the AI makes a mistake?
Every AI decision includes confidence scores and match reasoning. Low-confidence items get flagged for human review, and exceptions are routed to the right team member. Your team approves everything before it hits the books. Fixing errors also teaches Larry to be more accurate.

### 6. Which ERPs does Komplai integrate with?
We currently integrate with Zoho Books, QuickBooks, Xero, and ERPNext. NetSuite and Dynamics 365 integrations are planned. 

### 7. How much does Komplai cost?
Pricing depends on your team size and modules needed. Reach out to our team for more information. 

---

## Journal Automation FAQs

**Target audience:** Controllers and Accountants managing recurring journal entries

### 1. How does Larry know which GL accounts to use?
Larry uses "Memory Lookup" to match entries against historical patterns and your specific Chart of Accounts. When a new invoice arrives, Larry finds similar past invoices and checks how they were classified—showing you the consensus percentage and confidence level.

### 2. Can we review journals before they're posted to our ERP?
Absolutely. We use a Maker-Checker workflow where Larry drafts the journal entry and your team provides the final approval. Nothing is posted automatically without human sign-off.

### 3. Does this handle complex accruals and reversals?
Yes. Larry identifies recurring schedules and automatically drafts accrual entries and their subsequent reversals. When actuals differ from estimates, Larry suggests true-up entries with clear supporting documentation.

### 4. What happens if an invoice doesn't match any historical pattern?
Larry flags it as an exception for manual review. You'll see why it was flagged (new vendor, unusual amount, no pattern match) and can classify it manually. Larry then remembers your decision for future similar invoices—no "black box" classifications.

### 5. How do you handle new vendors or new GL accounts?
When Larry encounters an unmapped vendor or account, it flags it during validation and prompts you to create the mapping. Once mapped, Larry remembers and applies that classification automatically going forward.

### 6. What journal entry sources can Komplai automate?
Larry can generate journals from multiple sources: invoices (AP/AR), payroll exports (Gusto, ADP, Rippling, Paychex), bank transactions, recurring expense schedules, and manual triggers. Each entry includes the source data, approval logs, and edit history for audit readiness.

### 7. How much time can we save on journal prep?
Typical teams see 50–80% reduction in journal preparation time. Instead of manually creating entries each period, your team reviews Larry's drafts and approves or adjusts as needed.

---

## Bank Reconciliation FAQs

**Target audience:** Controllers and Staff Accountants handling reconciliations

### 1. How does Larry match bank transactions to ledger entries?
Larry uses advanced rules and historical patterns to suggest matches. Each match shows a confidence score (e.g., "EXACT MATCH, SCORE: 100%") with human-readable reasoning (e.g., "Matched on vendor and amount 89,100"). You can approve, reject, or manually override any match.

### 2. Does this support multi-currency bank accounts?
Yes. Komplai automatically pulls current mid-market rates to reconcile transactions across different currencies and suggests appropriate GL coding for FX differences.

### 3. Can we connect multiple banks and payment gateways?
Absolutely. Komplai identifies and consolidated feeds from multiple bank accounts and payment gateways (Stripe, PayPal, Razorpay, etc.) into one unified view. Messy payment provider statements become one explainable, balanced match.

### 4. How does the AI handle duplicate transactions from the bank feed?
Larry flags duplicates instantly and allows you to merge or dismiss them with a single click, preventing double-counting. You'll see exactly which transactions Larry identified as potential duplicates and why.

### 5. What about partial payments and split settlements?
Larry groups split settlements, partial receipts, payouts, fees, and refunds automatically. A single bank line can match to multiple ledger entries (or vice versa), with clear documentation of how the match was constructed.

### 6. How do you handle tax deductions like withholding taxes?
Larry automatically detects tax deductions and matches the net amount (e.g., "Matched with tax deduction on invoice value"). The system auto-populates the tax entries in vouchers with proper GL coding.

### 7. How fast can we close our bank accounts with Komplai?
Most teams close bank accounts 2-5 days faster because exceptions are handled continuously throughout the month, not discovered at month-end. Typical impact: 60-90% less reconciliation effort.

---

## Payroll Accounting FAQs

**Target audience:** Controllers managing payroll journal entries

### 1. Which payroll providers do you support?
We support all major platforms including Gusto, ADP, Rippling, Paychex, DarwinBox, Keka and others via CSV ingestion or direct API connections. If your provider exports data, Larry can ingest it.

### 2. How does Larry handle new employees or new cost centres?
Larry flags any unmapped employee, department, or cost centre during validation. You map it once, and Larry remembers that mapping for all future pay runs—no repetitive data entry.

### 3. Can we split payroll costs across multiple departments or locations?
Yes. Komplai supports complex allocation rules based on your specific requirements. Define your allocation logic once, and Larry applies it consistently across pay periods.

### 4. Does this handle employer-side taxes and benefits accurately?
Absolutely. Larry parses specific line items from your payroll export (salaries, employer taxes, benefits, deductions) and maps them to the correct GL accounts based on your chart of accounts structure.

### 5. How do you ensure payroll journals match our payroll register exactly?
Komplai performs payroll-to-ledger reconciliation automatically. Differences between your ADP/Gusto output and ledger postings are identified early with clear reasons and suggested corrections.

### 6. What if our cost centre structure changes mid-year?
Larry adapts to mapping changes. When you update a cost centre or department mapping, Larry applies it going forward while preserving historical accuracy. No re-processing required.

### 7. How much time can we save on payroll accounting?
Typical teams see 60-85% less payroll journal prep time. Payroll accounting becomes a standard workflow instead of a custom spreadsheet exercise each month.

---

## Accruals Page FAQs

**Target audience:** Controllers and Senior Accountants managing accruals and deferrals

### 1. How does Larry identify missing invoices that require accrual?
Larry monitors historical monthly patterns and contract start/end dates. When an expected recurring cost hasn't arrived (e.g., your monthly AWS bill), Larry flags it and suggests an accrual entry based on historical amounts.

### 2. Can we customize the amortisation logic for different expense categories?
Absolutely. You set the rules—linear, threshold-based, or event-driven—and Larry executes the schedule. Different expense categories can have different amortisation policies, all managed in one place.

### 3. Does this support ASC 606 / IFRS 15 revenue recognition?
Yes. Komplai is designed to support the 5-step model for revenue recognition, ensuring GAAP/IFRS compliance. Apply your Rev Rec policy over time using milestones, usage, or time-based schedules.

### 4. What happens when the actual invoice amount differs from the accrual?
Larry automatically suggests a "True-up" entry to adjust the variance and handles the reversal of the original estimate. You'll see the before/after comparison and can approve or modify the adjustment.

### 5. How do you handle schedule changes or early terminations?
When a prepaid contract is modified or terminated early, Larry recalculates the remaining amortisation or deferral schedule. You review and approve the adjustment entries with full audit trail.

### 6. Can Larry read service periods from invoice documents?
Yes. Larry extracts service periods directly from bills / invoices and uses that information to create accurate amortisation and deferral schedules automatically. No manual date entry required.

### 7. How does this reduce audit prep time?
Every accrual, deferral, reversal, and true-up carries complete source data, schedule logic, approvals, and period postings. When auditors ask questions, you retrieve evidence in clicks—not hours. Teams typically reduce audit back-and-forth by 30-60%.

---

## Close Analytics / Variance Insights FAQs

**Target audience:** CFOs and Controllers reviewing month-end variances

### 1. Can Larry explain variances at the department or cost-centre level?
Yes. Larry drills down into any dimension in your ERP—departments, locations, custom classes, or any segment you track. Ask "Why did Marketing spend increase 30%?" and Larry shows the specific vouchers and entries.

### 2. How does the materiality threshold work?
You set custom $ or % thresholds, and the system only surfaces movements that exceed those limits. This filters out noise so your team focuses on variances that actually impact decisions.

### 3. Can we compare actuals against our Budget or Annual Operating Plan?
Absolutely. Upload your budget or AOP, and Komplai tracks month-over-month variances against your strategic targets. Larry can answer questions like "How are we tracking vs. Q1 forecast?"

### 4. Does this replace our month-end close package?
It automates the drafting of it. Larry provides the commentary and evidence trails for significant variances, so your team only needs to add the final narrative—not hunt for explanations.

### 5. How do you identify if a variance is caused by misclassification vs. actual spend change?
Larry surfaces when "Unknown" or misclassified ledger entries are driving top movements. You'll see whether a variance is caused by genuine business activity or classification errors—helping you fix the root cause.

### 6. How quickly can we get variance explanations?
Most variance reviews that previously took hours can be completed in minutes. Teams typically cut variance review cycles by 50-70%, with answers ready during close—not after books are locked.

### 7. Can Larry generate board-ready variance commentary?
Yes. Larry drafts executive-ready explanations for material variances, including the underlying vouchers and drivers. Your CFO gets answers like "Marketing increased 25% due to new agency contract signed in October" instead of just numbers.

---

---

## Why Komplai Page FAQs

**Target audience:** Prospects evaluating the core platform value and AI-driven automation model.

### 1. How does Larry differ from basic ERP automation?
Standard automation follows static "if-this-then-that" rules. Larry is agentic—he learns from your historic bookkeeping patterns, explains his reasoning for every match, and proactively identifies exceptions. If Larry isn't sure, he flags it for review rather than making a blind entry.

### 2. What does the "Maker-Checker" workflow look like in practice?
In most finance teams, a staff accountant "makes" the entry and a Controller "checks" it. Komplai acts as the Maker—Larry handles the tedious data entry, reconciliation, and voucher preparation. Your team acts as the Checker, reviewing Larry’s work and providing final approval before anything hits the books.

### 3. Can we trust the AI’s decisions? How is "hallucination" prevented?
Finance demands 100% accuracy. Larry eliminates hallucinations by showing his work: every automated entry is backed by a "Source" tab linking directly to the transaction, invoice, or ledger entry. Larry also identifies when data is "stale" or inaccurate, ensuring you never make decisions on bad numbers.

### 4. How long does implementation take?
Most teams are live with their first automated close cycle in under 30 minutes. We connect to your existing ERP (QuickBooks, Xero, Zoho Books, or ERPNext) via secure OAuth, sync historical data, and Larry starts matching transactions immediately. There is no multi-month implementation project.

### 5. Is Komplai secure enough for sensitive financial data?
Yes. Komplai is enterprise-ready and holds SOC1, SOC2, ISO 27001, and GDPR certifications. We use bank-level encryption for data at rest and data in transit. You always maintain full control over account access and API permissions.

### 6. How does Komplai help us scale without adding headcount?
As transaction volume grows, manual teams usually need more people. Komplai breaks this linear growth. Because Larry handles 65%+ of the manual effort on day one, your existing team can manage 3x the volume without feeling the burn, effectively turning your finance function into a scalable profit center.

### 7. Does my historical data need to be perfect for Larry to learn from it?
No. Larry is designed to handle "messy" data. He identifies patterns even in noisy historical records and will proactively flag inconsistencies for your review. As your team confirms the correct classifications, Larry builds a high-fidelity "memory" of your specific business rules, effectively helping you clean up your books as you work.

---

## CEO / Founder Perspective FAQs

**Target audience:** CEOs and Business Owners focused on growth, scaling, and strategic visibility.

### 1. How does Komplai impact our bottom line?
Komplai reduces the need for additional finance headcount as you scale. By automating 65% of the preparation work on day one, your existing team can handle 3x the transaction volume. Most customers see a full ROI within 3 months through reduced consultant fees and improved cash flow visibility.

### 2. Can I get a consolidated view if I have multiple entities and currencies?
Yes. Komplai specializes in multi-entity consolidation. Whether you operate in the UK, UAE, India, or SE Asia, Komplai syncs data across all your entities, handles currency conversion automatically, and provides a unified P&L and Balance Sheet in minutes, not days.

### 3. How quickly can I see real-time financials?
Instead of waiting 10-15 days after month-end for reports, Komplai enables a "Continuous Close." You get visibility into your burn, churn, and cash position every day. Larry can answer questions about your current financial health instantly, so you make decisions based on today's data, not last month's.

### 4. Will this reduce my dependency on external consultants/CAs?
Absolutely. Many teams use Komplai to bring core accounting functions in-house. Because Larry learns your specific accounting patterns and handles the tedious data entry, your small internal team can manage what previously required a small army of consultants.

### 5. Do we need stop using our current ERP to use Komplai? 
Not at all. We don't require you to rip and replace your ERP. Komplai hooks into your existing systems (QuickBooks, Xero, etc.) and layers automation on top. Implementation takes about 30 minutes, and you and your team are good to go. 

---

## CFO Perspective FAQs

**Target audience:** CFOs focused on accuracy, compliance, risk management, and strategic finance.

### 1. How does Larry handle complex, high-volume transactions?
Larry is built for scale. Whether you’re a high-volume remittance business or a marketplace with thousands of monthly orders, Larry’s agentic architecture processes thousands of lines in parallel. Each transaction is validated against historical patterns with clear confidence scores.

### 2. Can Larry identify financial risks or anomalies before they hit the books?
Yes. Larry’s "Identify" mode is specifically designed to surface risks like unusual vendor spend, duplicate invoices, or Budget vs. Actual variances that exceed your custom thresholds. You get alerted to anomalies while there's still time to act, rather than discovering them during an audit.

### 3. How does the AI ensure we stay compliant with local tax laws (like TDS in India)?
Komplai has built-in logic for multi-jurisdiction compliance. For example, in India, Larry automatically detects TDS-applicable transactions, matches net amounts in bank recon, and pre-populates the correct tax entries in your vouchers. It also tracks upcoming filing deadlines so you never miss a compliance window.

### 4. What happens to our institutional knowledge when team members leave?
This is one of Komplai’s biggest strengths. Every time your team approves a classification or a match, Larry "remembers" it. This institutional knowledge is stored in the system, not in people's heads. When a new team member joins, Larry "onboards" them by suggesting the same patterns the previous team used.

### 5. Does Komplai support Budget vs. Actual tracking and variance analysis?
Yes. You can upload your Budget or Annual Operating Plan (AOP), and Komplai tracks performance against it in real-time. Larry doesn't just show the variance; he can drill down to the voucher level to "Explain" why a specific department exceeded its budget, saving days of manual investigation.

---

## Controller Perspective FAQs

**Target audience:** Controllers and Finance Managers focused on operational efficiency, accuracy, and team management.

### 1. How much control do I really have over Larry’s automated entries?
You maintain 100% control. We use a "Maker-Checker" workflow where Larry acts as the maker (preparing entries, matching transactions, classifying invoices) and your team acts as the checker. Nothing is posted to your ERP without a human sign-off. You get the speed of AI with the oversight of a pro.

### 2. How does Larry learn my specific Chart of Accounts and categorization?
Larry uses "Memory Lookup" to analyze your historical data. He looks at how you’ve classified similar vendors and amounts in the past and suggests a mapping with a consensus percentage (e.g., "100% of similar invoices classified as 'Travel'"). You can also give Larry "Directives" to teach him new rules.

### 3. Can Larry handle retrospective bulk changes if we re-org our GL?
Yes. Unlike manual entry, Larry can process bulk changes across the entire financial year based on new rules you provide. If you decide to split a cost center or re-map a vendor, Larry can draft the necessary adjusting entries to ensure your historical data remains consistent.

### 4. How does the bank reconciliation handle "messy" data from payment gateways?
Larry excels at "messy" data. He can group split settlements, payouts, fees, and refunds from providers like Stripe or Razorpay automatically. He matches the net bank deposit to multiple ledger entries, providing clear documentation for every penny, so you don't have to hunt through gateway portals.

### 5. Does this help with audit preparation and supporting documentation?
Significantly. Every entry Larry creates is linked to its source document (invoice, payroll export, bank line) and includes a full activity log of who approved what and when. During an audit, you can pull complete evidence trails in clicks, reducing audit back-and-forth by upwards of 40%.

---

## General Guidelines for FAQ Implementation

1. **Keep answers concise** — Aim for 2-4 sentences per answer
2. **Lead with "Yes" or "Absolutely"** — For feature capability questions, confirm first, then explain
3. **Include specific examples** — Concrete numbers and scenarios build trust
4. **Avoid jargon** — Use language your prospects use, not internal terminology
5. **Link to deeper content** — FAQs can link to help docs or demo videos if available
6. **Update quarterly** — Review FAQs based on common sales objections and support tickets
