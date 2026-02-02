# Larry Capabilities Evaluation: CFO & Controller

**Objective:** Define and evaluate the functionality of Larry (AI Assistant) specifically for Finance Leaders (CFOs) and Operational Leaders (Controllers), incorporating risk highlighting and actionable insights.

---

## 1. Core Value Proposition

Larry serves as an "always-on" Chief of Staff for the finance team.
- **For CFOs:** Acts as a real-time analyst for strategic visibility (Cash, Burn, Risk).
- **For Controllers:** Acts as an intelligent auditor for operational accuracy (Reconciliation, Closing, Compliance).

**Key Differentiator:** Larry doesn't just "show data"; it *interprets* data to highlight risks and suggest actions.

---

## 2. Capability Matrix

| Feature | CFO Capability (Strategic) | Controller Capability (Operational) |
| :--- | :--- | :--- |
| **Analyze** | Cash flow trends, burn rate, vendor spend concentration. | Operational metrics (invoice processing velocity), closing progress % by day. |
| **Explain** | "Why is burn up 15%?" (Drivers: specific large vendor payments). | "Why is there a variance in the GL?" (Drill down to specific vouchers). |
| **Search** | "High-value contracts expiring soon" (Risk exposure). | "Unpaid bills for vendor X," "Missing invoices for recurring ops." |
| **Identify** | **Risk:** Cash runway < 6 months, reliance on single customer. | **Risk:** Anomalous unapproved invoices, stalled reconciliation tasks. |

---

## 3. CFO Deep Dive: The Strategic Analyst

The CFO uses Larry to maintain a pulse on the company's financial health without waiting for month-end reports.

### Top Use Cases
1.  **Liquidity & Cash Flow**
    *   *Query:* "What is our current cash runway based on last 3 months burn?"
    *   *Larry Output:* "Runway is approx. 8.5 months."
    *   *Risk Highlight:* "⚠️ **Alert:** Burn increased by 12% in Aug vs July due to one-time legal fees."
    *   *Actionable:* [View Cash Flow Chart] [Analyze Legal Spend]

2.  **Receivables & Working Capital**
    *   *Query:* "Who handles our biggest outstanding receivables?"
    *   *Larry Output:* "Acme Corp owes ₹50L (45% of total AR)."
    *   *Risk Highlight:* "⚠️ **Concentration Risk:** 45% of AR is tied to one customer."
    *   *Actionable:* [View Customer Aging] [Draft Follow-up Email]

3.  **Vendor Management**
    *   *Query:* "Top vendors by spend this quarter."
    *   *Larry Output:* List of top 5 vendors.
    *   *Risk Highlight:* "ℹ️ **Renewal Risk:** AWS spend is trending up 5% MoM; check for unused instances."
    *   *Actionable:* [Breakdown AWS Spend]

---

## 4. Controller Deep Dive: The Intelligent Auditor

The Controller uses Larry to ensure accuracy, compliance, and speed of the close process.

### Top Use Cases
1.  **Month-End Close Orchestration**
    *   *Query:* "Status of the August close?"
    *   *Larry Output:* "65% complete. Day 4 of 10."
    *   *Risk Highlight:* "⚠️ **Bottleneck:** Bank Reconciliation is 2 days behind schedule compared to last month."
    *   *Actionable:* [View Unreconciled Transactions] [Nudge Assignee]

2.  **Anomaly Detection (Audit Prep)**
    *   *Query:* "Any unusual expenses this week?"
    *   *Larry Output:* "Found 3 transactions > ₹50k without POs."
    *   *Risk Highlight:* "⚠️ **Compliance Gap:** 3 large invoices processed without Purchase Orders."
    *   *Actionable:* [Review Invoices] [Flag for Audit]

3.  **Reconciliation Assistant**
    *   *Query:* "Why is the GL balance different from the bank statement?"
    *   *Larry Output:* "Difference of ₹12,500 identified."
    *   *Risk Highlight:* "ℹ️ **Variance Source:** Likely due to 2 unposted checks from Vendors A & B."
    *   *Actionable:* [Auto-Process Adjustments] [View Variance Report]

---

## 5. Risk & Actionables Framework

Feedback indicates Larry must be proactive, not just reactive. Every "Answer" should be paired with a "Risk Assessment" and an "Actionable".

**The "ARA" Output Model for Larry:**

1.  **Answer:** Direct, data-backed response to the query.
2.  **Risk:** (Optional) If thresholds are breached or anomalies found, highlight clearly with warnings (⚠️) or info icons (ℹ️).
3.  **Actionable:** Immediate buttons or links to resolve the issue or drill deeper.

**Example: Aging Query**
*   **A:** "Total AR is ₹1.2Cr. ₹40L is >90 days overdue."
*   **R:** "⚠️ **Critical:** The 90+ day bucket has grown 20% since last week."
*   **A:** [Send Dunning Emails] [View 90+ Day Invoices]
