# E1: Larry Is Ready — Data & Prompt Specification

## Overview

This document maps every dynamic variable in the E1 onboarding email to its data source — either a Prisma query against the Komplai database, a derived calculation, or an LLM prompt that Larry runs against the synced data.

---

## Part 1: Database Queries for Template Variables

### 1. `{{first_name}}`

**Source:** `User.name` (split on first space)

```typescript
const user = await prisma.user.findUnique({
  where: { id: userId },
  select: { name: true },
});
const firstName = user.name.split(' ')[0];
```

---

### 2. `{{erp_name}}`

**Source:** `IntegrationOAuthCredentials.provider`

```typescript
const integration = await prisma.integrationOAuthCredentials.findFirst({
  where: { businessId, disabledAt: null },
  select: { provider: true },
});

const ERP_DISPLAY_NAMES: Record<string, string> = {
  ZOHO_BOOKS: 'Zoho Books',
  TRUTO_ERP_NEXT: 'ERPNext',
};

const erpName = ERP_DISPLAY_NAMES[integration.provider] ?? integration.provider;
```

---

### 3. `{{accounts_synced}}` and `{{accounts_total}}`

**Source:** `ChartOfAccount` table + `ErpEntityMapping` for sync status

`accounts_total` = total chart of account entries pulled from the ERP.
`accounts_synced` = those that have at least one successful sync event.

```typescript
// Total CoA entries for this business
const accountsTotal = await prisma.chartOfAccount.count({
  where: { businessId },
});

// Accounts that have a successful ERP mapping
const accountsSynced = await prisma.erpEntityMapping.count({
  where: {
    businessId,
    internalEntityType: 'CHART_OF_ACCOUNT',
    syncEvents: {
      some: {
        status: { in: ['SUCCESS', 'CREATED', 'UPDATED'] },
        direction: 'FROM_ERP',
      },
    },
  },
});
```

---

### 4. `{{transactions_analyzed}}`

**Source:** `Transaction` table — count all transactions synced for this business.

```typescript
const transactionsAnalyzed = await prisma.transaction.count({
  where: { businessId },
});
```

---

### 5. `{{date_range_start}}` and `{{date_range_end}}`

**Source:** `Transaction.date` — min and max dates across all synced transactions.

```typescript
const dateRange = await prisma.transaction.aggregate({
  where: { businessId },
  _min: { date: true },
  _max: { date: true },
});

const dateRangeStart = formatDate(dateRange._min.date); // e.g. "Apr 2024"
const dateRangeEnd = formatDate(dateRange._max.date);   // e.g. "Jan 2026"
```

---

### 6. `{{data_completeness_pct}}`

**Source:** Composite score derived from multiple entity types. This is a calculated metric, not a single field.

**Logic:** Check which entity categories have been synced and weight them by importance.

```typescript
// Define expected entity types and their weights
const COMPLETENESS_WEIGHTS = {
  CHART_OF_ACCOUNT: 0.20,  // CoA is foundational
  VENDOR: 0.15,            // Vendor master data
  INVOICE: 0.30,           // Core transactional data
  TRANSACTION: 0.25,       // Bank/payment data
  BANK_ACCOUNT: 0.10,      // Account structure
};

async function calculateCompleteness(businessId: string): Promise<number> {
  let score = 0;

  for (const [entityType, weight] of Object.entries(COMPLETENESS_WEIGHTS)) {
    const syncCount = await prisma.erpEntityMapping.count({
      where: {
        businessId,
        internalEntityType: entityType as KomplaiSyncEntityType,
        syncEvents: {
          some: {
            status: { in: ['SUCCESS', 'CREATED', 'UPDATED'] },
            direction: 'FROM_ERP',
          },
        },
      },
    });

    // Binary: if at least one entity of this type synced, grant the weight
    // For a more granular approach, compare syncCount against expected count
    if (syncCount > 0) {
      score += weight;
    }
  }

  return Math.round(score * 100);
}
```

**Alternative (more granular):** If you want partial credit per entity type, compare against what the ERP reports as total. This requires storing expected counts during the sync workflow, e.g., if Zoho says there are 200 invoices and you synced 156, that's 78% for the invoice component.

---

### 7. `{{app_link}}`

**Source:** Constructed URL. Not a database query.

```typescript
const appLink = `${APP_BASE_URL}/chat?ref=onboarding-email`;
// or deep-link to a specific conversation:
const appLink = `${APP_BASE_URL}/chat/new?context=erp-sync-complete&ref=e1-email`;
```

---

## Part 2: LLM Prompts for Insight Generation

These are the prompts Larry should execute against the synced data to produce the insight cards shown in the email. The flow is:

1. **Query** the database for raw analysis inputs
2. **Pass** the structured data into the LLM prompt
3. **Parse** the LLM's structured output into template variables

### Step 2a: Pre-prompt Data Assembly

Before calling the LLM, assemble a data snapshot:

```typescript
interface ErpSyncSnapshot {
  businessName: string;
  erpProvider: string;
  currency: string;

  // Counts
  totalInvoices: number;
  payableInvoices: number;
  receivableInvoices: number;
  totalTransactions: number;
  totalVendors: number;
  totalCoaAccounts: number;

  // Date range
  earliestTransactionDate: string;
  latestTransactionDate: string;

  // Anomaly signals (pre-computed queries to feed the LLM)
  overdueInvoices: { count: number; totalAmount: number };
  unmatchedTransactions: { count: number; totalAmount: number };
  vendorsWithoutIdentifiers: number;
  duplicateInvoiceCandidates: number;
  invoicesWithoutCoaClassification: number;
  reconWorkflowsPending: number;
  highValueTransactionsWithoutInvoice: { count: number; threshold: number };
}
```

**Queries for each signal:**

```typescript
// Overdue invoices (unpaid with due date in the past)
const overdueInvoices = await prisma.invoice.aggregate({
  where: {
    clientBusinessId: businessId,
    paymentStatus: 'UNPAID',
    dueDate: { lt: new Date() },
    deletedAt: null,
  },
  _count: true,
  _sum: { grossAmountNormalised: true },
});

// Unmatched transactions (transactions not linked to any invoice)
const unmatchedTransactions = await prisma.transaction.count({
  where: {
    businessId,
    TransactionInvoice: { none: {} },
  },
});
const unmatchedAmount = await prisma.transaction.aggregate({
  where: {
    businessId,
    TransactionInvoice: { none: {} },
  },
  _sum: { amount: true },
});

// Vendors missing tax identifiers (GST, PAN, etc.)
const vendorsWithoutIdentifiers = await prisma.vendor.count({
  where: {
    vendorForId: businessId,
    identifiers: { none: {} },
  },
});

// Invoices without Chart of Account classification
const unclassifiedInvoices = await prisma.invoice.count({
  where: {
    clientBusinessId: businessId,
    chartOfAccountId: null,
    ledgerType: null,
    deletedAt: null,
  },
});

// Potential duplicate invoices (same vendor + same amount + same date)
// This requires a raw query or groupBy
const duplicateCandidates = await prisma.$queryRaw`
  SELECT COUNT(*) as duplicate_groups
  FROM (
    SELECT "vendorId", "grossAmountNormalised", "invoiceDate"
    FROM invoices
    WHERE "clientBusinessId" = ${businessId}::uuid
      AND "deletedAt" IS NULL
    GROUP BY "vendorId", "grossAmountNormalised", "invoiceDate"
    HAVING COUNT(*) > 1
  ) dupes;
`;

// High-value transactions without invoice match
const avgTransactionAmount = await prisma.transaction.aggregate({
  where: { businessId },
  _avg: { amount: true },
});
const threshold = Number(avgTransactionAmount._avg.amount ?? 0) * 3;
const highValueUnmatched = await prisma.transaction.count({
  where: {
    businessId,
    amount: { gte: threshold },
    TransactionInvoice: { none: {} },
  },
});

// Pending reconciliation workflows
const pendingRecons = await prisma.reconciliationWorkflow.count({
  where: {
    businessId,
    stage: { not: 'COMPLETED' },
  },
});
```

---

### Step 2b: The LLM Prompt

This is the core prompt Larry uses to generate the insight cards.

```
SYSTEM PROMPT:
--------------
You are Larry, the AI close manager for Komplai. A new user just connected
their ERP ({{erp_provider}}) and you've completed the initial data sync.
Your job is to analyze the data snapshot below and surface the 3-5 most
important observations for this user's first interaction with Komplai.

RULES:
- You are writing for a Controller, Head of Finance, or senior accountant.
  They are busy. Be specific and quantitative — never vague.
- Each insight must be grounded in the data provided. Do not fabricate
  numbers or invent issues that aren't supported by the data.
- Prioritize insights by business impact: cash flow risks > compliance gaps
  > operational inefficiencies > informational observations.
- For each insight, assign a severity:
    - "high" = Needs immediate attention (cash at risk, compliance issue,
      data integrity problem)
    - "medium" = Worth investigating soon (efficiency opportunity,
      pattern worth understanding)
    - "low" = Informational (data overview, positive observation)
- Headline must be ≤10 words. One-liner must be ≤25 words.
- The tone is direct, professional, and slightly conversational — like a
  sharp colleague giving you a heads-up, not a consultant writing a report.

OUTPUT FORMAT (JSON):
{
  "insights": [
    {
      "headline": "string — ≤10 words, specific and quantitative",
      "one_liner": "string — ≤25 words, explains the 'so what'",
      "severity": "high" | "medium" | "low",
      "category": "cash_flow" | "compliance" | "data_quality" |
                  "reconciliation" | "vendor_management" | "classification"
    }
  ],
  "remaining_teaser": "string — ≤15 words, teases the other insights
                        the user hasn't seen yet"
}

USER PROMPT:
------------
Here's the data snapshot from {{business_name}}'s {{erp_provider}} sync:

**Summary:**
- Currency: {{currency}}
- Chart of Accounts: {{total_coa_accounts}} accounts
- Vendors: {{total_vendors}}
- Invoices: {{total_invoices}} ({{payable_invoices}} payable,
  {{receivable_invoices}} receivable)
- Transactions: {{total_transactions}}
- Date range: {{earliest_date}} to {{latest_date}}

**Signals detected:**
- Overdue unpaid invoices: {{overdue_count}} totaling
  {{currency}} {{overdue_amount}}
- Transactions with no matching invoice: {{unmatched_tx_count}} totaling
  {{currency}} {{unmatched_tx_amount}}
- Vendors missing tax identifiers (GST/PAN): {{vendors_no_id}} of
  {{total_vendors}}
- Invoices without expense/income classification:
  {{unclassified_invoices}} of {{total_invoices}}
- Potential duplicate invoice groups: {{duplicate_groups}}
- High-value unmatched transactions (>3x average): {{high_value_unmatched}}
- Pending reconciliation workflows: {{pending_recons}}

Generate the top 3 insights for the onboarding email. Return exactly 3 — the
2-3 most impactful ones. Save the rest for the in-app experience.
```

---

### Step 2c: Parsing LLM Output → Email Variables

```typescript
interface LarryInsightOutput {
  insights: Array<{
    headline: string;
    one_liner: string;
    severity: 'high' | 'medium' | 'low';
    category: string;
  }>;
  remaining_teaser: string;
}

function mapToEmailVariables(
  output: LarryInsightOutput,
  totalInsightCount: number // sum of all signals detected
) {
  return {
    insight_count: totalInsightCount,
    insight_1_headline: output.insights[0]?.headline,
    insight_1_one_liner: output.insights[0]?.one_liner,
    insight_1_severity_high: output.insights[0]?.severity === 'high',
    insight_2_headline: output.insights[1]?.headline ?? null,
    insight_2_one_liner: output.insights[1]?.one_liner ?? null,
    insight_2_severity_high: output.insights[1]?.severity === 'high',
    insight_3_headline: output.insights[2]?.headline ?? null,
    insight_3_one_liner: output.insights[2]?.one_liner ?? null,
    remaining_insight_teaser: output.remaining_teaser,
  };
}
```

---

## Part 3: Example Outputs

### Example: Healthy mid-size company

Given signals: 12 overdue invoices (₹4.2L), 87 unmatched transactions, 15 vendors missing PAN.

**LLM output:**

```json
{
  "insights": [
    {
      "headline": "₹4.2L in overdue invoices across 12 bills",
      "one_liner": "These are past due date and unpaid — could be a collections gap or a data lag from Zoho.",
      "severity": "high",
      "category": "cash_flow"
    },
    {
      "headline": "87 bank transactions don't match any invoice",
      "one_liner": "Likely missing bills or payments booked directly — worth reviewing before your next close.",
      "severity": "medium",
      "category": "reconciliation"
    },
    {
      "headline": "15 vendors missing PAN or GST registration",
      "one_liner": "TDS compliance risk — these vendors may need identifier updates before the next filing.",
      "severity": "high",
      "category": "compliance"
    }
  ],
  "remaining_teaser": "Larry also spotted classification gaps and potential duplicates worth reviewing"
}
```

### Example: Clean small company

Given signals: 0 overdue, 5 unmatched transactions, 2 vendors missing PAN, 180 invoices classified.

**LLM output:**

```json
{
  "insights": [
    {
      "headline": "180 invoices synced and classified — strong baseline",
      "one_liner": "Your Zoho data is well-organized. Larry can start helping with close tasks right away.",
      "severity": "low",
      "category": "data_quality"
    },
    {
      "headline": "5 bank transactions without matching invoices",
      "one_liner": "Small count, but worth checking — these may be direct payments or missing bills.",
      "severity": "medium",
      "category": "reconciliation"
    },
    {
      "headline": "2 vendors missing tax identifiers",
      "one_liner": "Minor gap — updating these before the next TDS cycle keeps your filing clean.",
      "severity": "low",
      "category": "compliance"
    }
  ],
  "remaining_teaser": "Your data looks solid — Larry's ready to tackle your next month-end close"
}
```

---

## Part 4: Insight Count (`{{insight_count}}`)

This is the total number of signals detected, NOT the number of insight cards shown in the email (which is always 2-3). The logic:

```typescript
function calculateInsightCount(signals: ErpSyncSnapshot): number {
  let count = 0;
  if (signals.overdueInvoices.count > 0) count++;
  if (signals.unmatchedTransactions.count > 0) count++;
  if (signals.vendorsWithoutIdentifiers > 0) count++;
  if (signals.duplicateInvoiceCandidates > 0) count++;
  if (signals.invoicesWithoutCoaClassification > 0) count++;
  if (signals.reconWorkflowsPending > 0) count++;
  if (signals.highValueTransactionsWithoutInvoice.count > 0) count++;
  return count;
}
```

This gives a number like "Larry flagged **5** patterns total" — implying there's more to see inside the app than the 2-3 cards shown in the email.

---

## Part 5: Edge Cases & Fallbacks

| Scenario | Handling |
|---|---|
| **Zero transactions synced** | Skip "WHAT LARRY FOUND" section entirely. Replace with: "Your accounts are connected — Larry is waiting for transaction data to start analyzing." |
| **Zero insights generated** (everything clean) | Show a single positive insight: "Your data looks well-organized" + CTA to explore Larry's other capabilities. |
| **ERP sync partially failed** | Check `ErpSyncEvent.status = 'FAILED'` count. If >20% failed, add a "Data sync incomplete" banner above insights. Don't pretend data is complete. |
| **Only one entity type synced** (e.g., only CoA, no invoices yet) | Adjust completeness bar accordingly. Insights should note: "Larry has limited data so far — connect more modules for a full picture." |
| **Very large dataset** (>50k transactions) | Pre-aggregate signals via raw SQL before passing to LLM. Don't pass raw row-level data. |

---

## Part 6: Execution Sequence

```
1. ERP sync workflow completes (Temporal: syncZohoErp / syncTrutoErp)
2. Post-sync hook triggers E1 email assembly:
   a. Query user + business metadata (first_name, erp_name)
   b. Run stat queries (accounts, transactions, date range, completeness)
   c. Run signal queries (overdue, unmatched, duplicates, etc.)
   d. Call Larry LLM with assembled snapshot → get structured insights JSON
   e. Parse into email template variables
   f. Send via Courier with all variables populated
3. Log email send event for analytics (user_id, business_id, insight_count,
   erp_provider, timestamp)
```
