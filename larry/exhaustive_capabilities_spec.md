# Exhaustive Larry Capabilities & Schema Mapping

This document provides a comprehensive list of capabilities, questions, and insights Larry can generate, mapped directly to the Komplai schema and their specific impact on Finance personas.

**Data Sources Key:**
*   **Direct (Invoices/Bank):** Data derived directly from `Invoice` or `Transaction` tables. High velocity, available immediately.
*   **Vouchers (GL/Accounting):** Data derived from `Voucher`, `VoucherEntry`, or `GL Account Balance`. Requires accounting logic or reconciliation.

**Decision Context Key:**
*   **Strategic / Ongoing:** Real-time decisions about cash, risk, or operations. Daily usage.
*   **Close Tracking:** Tasks related to period-end reporting, accuracy, and audit. Monthly/Quarterly usage.

---

## 1. Income & Receivables (Cash In)

**Primary Persona:** CFO (Liquidity), Controller (Collection Efficiency)

| Query / Recommendation | Calculation Logic (Schema Based) | Impact / Actionable | Data Source Level | Decision Context |
| :--- | :--- | :--- | :--- | :--- |
| **"What is our projected cash collection for the next 30 days?"** | `SUM(Invoice.grossAmountNormalised)` WHERE `type='RECEIVABLE'`, `status='UNPAID'`, `dueDate` between `TODAY` and `TODAY+30`. | **CFO:** Critical for liquidity planning. **Action:** If low, trigger credit line draw. | **Direct (Invoices)** | **Strategic / Ongoing** |
| **"Who are our riskiest customers?" (Concentration + Delinquency)** | (1) Top 5 customers by `SUM(grossAmountNormalised)` (Concentration). (2) Filter customers where `AVG(TODAY - dueDate)` > 45 days (Delinquency). | **CFO:** Revenue risk assessment. **Action:** Renegotiate terms or diversify client base. | **Direct (Invoices)** | **Strategic / Ongoing** |
| **"Which invoices are seriously overdue (>90 days)?"** | `SELECT *` FROM `Invoice` WHERE `type='RECEIVABLE'`, `status='UNPAID'`, `(TODAY - dueDate) > 90`. | **Controller:** Bad debt provision needed. **Action:** Initiate legal collections or write-off. | **Direct (Invoices)** | **Close Tracking** (Provisioning) |
| **"What is our Collection Effectiveness Index (CEI) this month?"** | `(Beginning Receivables + Monthly Credit Sales - Ending Total Receivables) / (Beginning Receivables + Monthly Credit Sales - Ending Current Receivables)`. *Requires historical snapshots.* | **CFO:** Efficiency metric. **Action:** Review collections team performance. | **Vouchers (GL)** (Requires opening balances) | **Strategic / Ongoing** |
| **"Show me revenue by currency to check FX exposure."** | `SUM(grossAmount)` GROUP BY `invoiceCurrency` WHERE `type='RECEIVABLE'`, `status='UNPAID'`. | **CFO:** Hedging decisions. **Action:** Book forward contracts if exposure > threshold. | **Direct (Invoices)** | **Strategic / Ongoing** |
| **"Which customers usually pay late?"** | For each `Vendor` (Client), Calculate `AVG(TransactionInvoice.createdAt - Invoice.dueDate)` where `status='PAID'`. | **Controller:** Cash flow forecasting accuracy. **Action:** Adjust expected payment dates in forecast models. | **Direct (Invoices + Bank)** | **Strategic / Ongoing** |
| **"Show unbilled revenue or work-in-progress."** | *(Requires `ServicePeriod` schema enhancement)* Identify contracts active vs. invoices generated. Currently: List `RecurringInvoiceSeries` where `Invoice` for current period is missing. | **CFO:** Revenue leakage. **Action:** Trigger immediate billing. | **Direct (Invoices)** (Using Recurring Series) | **Close Tracking** (Revenue Rec) |

---

## 2. Expenses & Payables (Cash Out)

**Primary Persona:** CFO (Burn Rate), Controller (Spend Control)

| Query / Recommendation | Calculation Logic (Schema Based) | Impact / Actionable | Data Source Level | Decision Context |
| :--- | :--- | :--- | :--- | :--- |
| **"What is our current burn rate?"** | `AVG(SUM(grossAmountNormalised))` per month over last 3 months WHERE `type='PAYABLE'`. | **CFO:** Runway calculation. **Action:** Freeze hiring if burn > budget. | **Direct (Invoices)** | **Strategic / Ongoing** |
| **"Which vendors are we spending the most with?"** | `SUM(grossAmountNormalised)` GROUP BY `vendorId` WHERE `type='PAYABLE'`, `invoiceDate` in Current FY. | **CFO:** Cost reduction targets. **Action:** Negotiate volume discounts with top 3 vendors. | **Direct (Invoices)** | **Strategic / Ongoing** |
| **"Do we have any 'Zombie' subscriptions?"** | List `RecurringInvoiceSeries` where `invoiceDate` exists but usage (if integrated) is zero. *Alternatively:* Show recurring vendors with < 5% variance in amount for >12 months. | **CFO:** Cost cutting. **Action:** Cancel unused SaaS licenses. | **Direct (Invoices)** | **Strategic / Ongoing** |
| **"What are our upcoming unauthorized liabilities?"** | `SUM(grossAmountNormalised)` WHERE `type='PAYABLE'`, `status='UNPAID'`, `state != 'APPROVED'` (or `classificationScore` < threshold). | **Controller:** Control risk. **Action:** Force approval workflow before payment run. | **Direct (Invoices)** | **Strategic / Ongoing** (Control) |
| **"Show me expenses classified as 'Miscellaneous' or 'General'."** | `SELECT *` WHERE `ChartOfAccount.name` IN ['General Expenses', 'Miscellaneous'] AND `amount > threshold`. | **Controller:** Audit risk/Lazy bookkeeping. **Action:** Reclassify to correct heads. | **Vouchers (GL)** (To catch manual journals) or **Direct** (if only invoices) | **Close Tracking** (Hygiene) |
| **"What invoices are due this week?"** | `SUM(grossAmountNormalised)` WHERE `type='PAYABLE'`, `status='UNPAID'`, `dueDate` between `TODAY` and `TODAY+7`. | **CFO:** Cash requirements. **Action:** Approve weekly payment run. | **Direct (Invoices)** | **Strategic / Ongoing** |
| **"Are we paying anyone too early?"** | Compare `TransactionInvoice.createdAt` (Payment Date) vs `Invoice.dueDate`. Highlight if Payment Date < Due Date - 5 days. | **CFO:** Working capital inefficiency. **Action:** Delay payments to due date to preserve cash. | **Direct (Invoices + Bank)** | **Strategic / Ongoing** |

---

## 3. Operations & Closing (Efficiency)

**Primary Persona:** Controller (Process Health), CFO (Speed)

| Query / Recommendation | Calculation Logic (Schema Based) | Impact / Actionable | Data Source Level | Decision Context |
| :--- | :--- | :--- | :--- | :--- |
| **"What is the status of the Month-End Close?"** | `COUNT(Tasks)` where `status='COMPLETED'` / `Total Tasks` for current `Task.closePeriod`. | **CFO:** Financial reporting timeline. **Action:** Report to Board / Investors. | **Direct (Tasks)** | **Close Tracking** |
| **"Where is the bottleneck in the close process?"** | Identify `Task` where `status='PENDING'` AND `dueDate` < `TODAY`. Group by `assignedToId`. | **Controller:** Resource allocation. **Action:** Reassign tasks or support blocked team member. | **Direct (Tasks)** | **Close Tracking** |
| **"How accurately is the AI coding invoices?"** | `AVG(classificationScore)` for `Invoices` in current month. | **Controller:** Trust & Automation level. **Action:** Review low-score clusters to improve training. | **Direct (Invoices)** | **Strategic / Ongoing** |
| **"Show unreconciled bank transactions > 10 days old."** | `SELECT *` FROM `Transaction` WHERE `type` is not matched AND `date < TODAY-10`. | **Controller:** Data integrity risk. **Action:** Immediate investigation required. | **Direct (Bank)** | **Close Tracking** (Readiness) |
| **"Do we have all invoices for our recurring expenses?"** | Compare `RecurringInvoiceSeries` vs actual `Invoice` created for current month. List missing. | **Controller:** Accrual accuracy. **Action:** Post accrual entries for missing invoices. | **Direct (Invoices)** | **Close Tracking** (Accruals) |
| **"What is the variance between our Bank and Book balance?"** | `TransactionAccount.balance` (Bank Feed) - `GL Account Balance` (Books). | **Controller:** Reconciliation completeness. **Action:** Investigate unidentified variances. | **Vouchers (GL) + Bank** | **Close Tracking** |

---

## 4. Risk, Fraud & Compliance (Governance)

**Primary Persona:** CFO (Fiduciary Duty), Controller (Internal Controls)

| Query / Recommendation | Calculation Logic (Schema Based) | Impact / Actionable | Data Source Level | Decision Context |
| :--- | :--- | :--- | :--- | :--- |
| **"Are there duplicate invoices?"** | Find `Invoice` pairs with same `vendorId`, `grossAmountNormalised`, and similar `invoiceDate` (within 2 days). | **Controller:** Fraud/Error prevention. **Action:** Block payment and flag for review. | **Direct (Invoices)** | **Strategic / Ongoing** |
| **"Show payments made to new vendors this month."** | List `Transaction` -> `Vendor` where `Vendor.createdAt` is in current month. | **CFO:** Fraud risk (shell companies). **Action:** Verify vendor legitimacy. | **Direct (Bank)** | **Strategic / Ongoing** |
| **"Identify spikes in T&E (Travel & Expense) spend."** | Compare `SUM(grossAmount)` for "Travel" CoA vs 3-month average. Highlight if > 20% variance. | **CFO:** Policy compliance. **Action:** Send policy reminder or audit specific claims. | **Direct (Invoices)** | **Strategic / Ongoing** |
| **"Do we have missing tax IDs for any vendors?"** | List `Vendor` where `VendorIdentifier` (Tax ID) is NULL or invalid format. | **Controller:** TDS/GST Compliance risk. **Action:** Withhold payment until Tax ID provided. | **Direct (Invoices/Vendor)** | **Close Tracking** (Filing Prep) |
| **"Are there any large round-dollar transactions?"** | `SELECT *` FROM `Transaction` WHERE `amount` % 1000 = 0 AND `amount` > 10000. (Often a red flag for fraud or estimates). | **Controller:** Audit flag. **Action:** Request supporting documentation. | **Direct (Bank)** | **Strategic / Ongoing** |
| **"Which tasks are constantly overdue?"** | Group `Task` history by `title` where `completedAt > dueDate`. | **Controller:** Process failure. **Action:** Redesign process or adjust SLAs. | **Direct (Tasks)** | **Strategic / Ongoing** |

---

## 5. Strategic Insights (The "So What?")

Beyond simple queries, Larry should synthesize data to answer "So What?":

1.  **Runway Alert:** "Based on this month's higher burn (₹50L vs ₹40L avg) and current cash (₹4Cr), your runway has decreased from 10 months to 8 months. **Action:** Review 'Marketing' spend which is up 40%." (Source: **Direct**, Context: **Strategic**)
2.  **Cost of Delay:** "You have ₹20L in payables due this week, but only ₹5L in expected collections. **Action:** You may need to delay 'Vendor X' payment or dip into reserves." (Source: **Direct**, Context: **Strategic**)
3.  **Vendor Negotiation:** "You spent ₹1Cr with 'Tech Corp' this year, making them your #2 vendor. **Action:** You are in the top tier for their volume discounts—ask for an extra 5% off." (Source: **Direct**, Context: **Strategic**)

---

## 6. Advanced GL & Voucher Insights (Technical Accounting)

**Primary Persona:** Controller (Audit & Compliance), CFO (Tax & Allocations)

| Query / Recommendation | Calculation Logic (Schema Based) | Impact / Actionable | Data Source Level | Decision Context |
| :--- | :--- | :--- | :--- | :--- |
| **"What is our net GST/VAT liability for this month?"** | `SUM(VoucherEntry.credit - VoucherEntry.debit)` where `ChartOfAccount.type = 'DUTIES_AND_TAXES'`. | **CFO:** Tax cash outflow planning. **Action:** Ensure sufficient balance for tax payment date. | **Vouchers (GL)** | **Close Tracking** (Filing) |
| **"Show me all manual journal entries posted to Revenue accounts."** | `SELECT *` from `Voucher` where `type='JOURNAL'` AND `VoucherEntry.ChartOfAccount.type = 'REVENUE'`. (Revenue should usually come via Invoices, not Manual Journals). | **Controller:** Revenue recognition risk / Audit flag. **Action:** Audit these entries for validity. | **Vouchers (GL)** | **Close Tracking** (Audit) |
| **"Are there any uncleaned 'Suspense' or 'Clearing' accounts?"** | `SUM(balance)` for `ChartOfAccount.name` LIKE '%Suspense%' OR '%Clearing%'. Should be `0` at month-end. | **Controller:** Closing hygiene. **Action:** Reclassify remaining balances before closing. | **Vouchers (GL)** | **Close Tracking** |
| **"What is our Payroll cost breakdown by Department?"** | `SUM(VoucherEntry.amount)` grouped by `Tag` (Department) where `Voucher.type = 'PAYROLL'`. | **CFO:** Budgeting accuracy. **Action:** Compare actuals vs budget per department. | **Vouchers (GL)** (Allocations) | **Strategic / Ongoing** |
| **"Have monthly depreciation entries been passed?"** | Check if `Voucher` exists where `type='DEPRECIATION'` for current month. Compare total vs expected schedule. | **Controller:** Asset register completeness. **Action:** Run depreciation schedule if missing. | **Vouchers (GL)** | **Close Tracking** |
| **"Show me inter-company transactions that need elimination."** | `SELECT *` FROM `Voucher` where `Tag` (or `ChartOfAccount`) indicates 'Related Party' or 'Inter-company'. | **Controller:** Consolidation accuracy. **Action:** Verify corresponding entry exists in the other entity. | **Vouchers (GL)** | **Close Tracking** |
| **"Identify 'Provisions' that haven't been reversed after 60 days."** | Find `Voucher` where `type='PROVISION'` ($X) created > 60 days ago without a matching Reversal or Invoice link. | **Controller:** Balance Sheet accuracy. **Action:** Reverse if expense never materialized or invoice is lost. | **Vouchers (GL)** | **Close Tracking** |
