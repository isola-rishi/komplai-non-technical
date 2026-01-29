# Komplai Dashboard Visualizations Specification

**Last Updated:** January 29, 2026  
**Target ICP:** CFOs / Controllers  
**Core Objective:** Snapshot visibility before drilling into data tables

---

## Section A: Income Page Visualizations (15 Options)

### 1. AR Aging Buckets
| Attribute | Value |
|-----------|-------|
| **Type** | Horizontal Stacked Bar Chart |
| **Priority** | 🔴 HIGH |

**Description:**  
Shows outstanding receivables grouped by days overdue:
- 1-30 days (Current)
- 31-60 days (Moderately overdue)
- 61-90 days (Significantly overdue)
- 90+ days (Critical)

**Calculation:**
```
Days Overdue = TODAY - dueDate (for invoices where dueDate < TODAY)
Group invoices by aging bucket
Sum grossAmountNormalised per bucket
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `status`: `'UNPAID'` or `'PARTIALLY_PAID'`
- `dueDate`: `< TODAY` (overdue only) OR all unpaid

**Schema Fields:**
- `Invoice.type`
- `Invoice.paymentStatus`
- `Invoice.dueDate`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `dueDate` range on table based on bucket clicked

---

### 2. Cash Collection Forecast
| Attribute | Value |
|-----------|-------|
| **Type** | Line Chart with area fill |
| **Priority** | 🔴 HIGH |

**Description:**  
Projects expected cash inflows based on due dates of unpaid invoices for the next 30, 60, and 90 days.

**Calculation:**
```
Group unpaid invoices by dueDate week/month
Sum grossAmountNormalised per period
Show cumulative line for total expected collections
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `status`: `'UNPAID'`
- `dueDate`: `BETWEEN TODAY AND TODAY + 90 days`

**Schema Fields:**
- `Invoice.dueDate`
- `Invoice.grossAmountNormalised`
- `Invoice.paymentStatus`

**Click-Through:** Sets `dueDate` range for selected period

---

### 3. Top 5 Customers by Outstanding
| Attribute | Value |
|-----------|-------|
| **Type** | Horizontal Bar Chart or Donut |
| **Priority** | 🔴 HIGH |

**Description:**  
Shows the 5 vendors (customers) with the largest unpaid receivables. Highlights customer concentration risk.

**Calculation:**
```
Group invoices by vendorId
Sum grossAmountNormalised WHERE status != 'PAID'
Sort descending, take top 5
Calculate % of total outstanding per customer
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `status`: `'UNPAID'` or `'PARTIALLY_PAID'`

**Schema Fields:**
- `Invoice.vendorId`
- `Vendor.name`
- `Invoice.grossAmountNormalised`
- `Invoice.paymentStatus`

**Click-Through:** Sets `vendorIds` filter to selected customer

---

### 4. Income Trend (Month-over-Month)
| Attribute | Value |
|-----------|-------|
| **Type** | Bar Chart with trend line overlay |
| **Priority** | 🔴 HIGH (Already exists - enhance) |

**Description:**  
Monthly income totals with a trend line showing direction. Current FY by default, with toggle for prior periods.

**Calculation:**
```
Group invoices by MONTH(invoiceDate)
Sum grossAmountNormalised per month
Calculate 3-month moving average for trend line
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `invoiceDate`: Current Fiscal Year range

**Schema Fields:**
- `Invoice.invoiceDate`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `invoiceDate` range to selected month

---

### 5. Payment Collection Rate
| Attribute | Value |
|-----------|-------|
| **Type** | Gauge or KPI Card with percentage |
| **Priority** | 🟡 MEDIUM |

**Description:**  
Shows percentage of invoices collected on time vs. late. Measures collection efficiency.

**Calculation:**
```
On-Time: Invoices where payment received before dueDate
Late: Invoices where payment received after dueDate
Rate = (On-Time Count / Total Paid Count) * 100
```

> **Note:** Requires tracking payment date (may need schema addition or derive from `TransactionInvoice.createdAt`)

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `status`: `'PAID'`
- `invoiceDate`: Current FY or selected period

**Schema Fields:**
- `Invoice.paymentStatus`
- `Invoice.dueDate`
- `TransactionInvoice.createdAt` (as payment date proxy)

**Click-Through:** Sets `status` filter + `dueDate` comparison

---

### 6. Recurring Revenue Tracker
| Attribute | Value |
|-----------|-------|
| **Type** | Card grid or status list |
| **Priority** | 🔴 HIGH |

**Description:**  
Shows recurring invoice series status:
- Expected this month vs. received
- Any missing invoices flagged

**Calculation:**
```
Query RecurringInvoiceSeries with frequency
Check if Invoice exists for current period where recurringSeriesId = series.id
Flag as "Received" or "Not Received"
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `recurringSeriesId`: `NOT NULL`
- `invoiceDate`: Current month

**Schema Fields:**
- `RecurringInvoiceSeries.id`, `label`, `frequency`, `vendorId`
- `Invoice.recurringSeriesId`
- `Invoice.invoiceDate`

**Click-Through:** Sets `recurring: true` + selected series

---

### 7. Overdue by Days Outstanding (Heat Map)
| Attribute | Value |
|-----------|-------|
| **Type** | Heat map or intensity bar |
| **Priority** | 🟡 MEDIUM |

**Description:**  
Visual intensity showing how many days each overdue invoice has been pending. Helps prioritize collection efforts by severity.

**Calculation:**
```
Days Outstanding = TODAY - dueDate
Color intensity based on days (higher = more intense/red)
Group by customer or show individual invoices
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `status`: `'UNPAID'`
- `dueDate`: `< TODAY`

**Schema Fields:**
- `Invoice.dueDate`
- `Invoice.grossAmountNormalised`
- `Invoice.vendorId`

**Click-Through:** Sets `dueDate` range based on intensity zone selected

---

### 8. Invoice Volume vs. Amount
| Attribute | Value |
|-----------|-------|
| **Type** | Dual-axis bar + line chart |
| **Priority** | 🟢 LOW |

**Description:**  
Compares count of invoices vs. total amount by month. Helps spot anomalies (many small invoices vs. few large ones).

**Calculation:**
```
Group by MONTH(invoiceDate)
Left axis: COUNT of invoices
Right axis: SUM of grossAmountNormalised
Overlay both
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `invoiceDate`: Current FY

**Schema Fields:**
- `Invoice.invoiceDate`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `invoiceDate` range to selected month

---

### 9. Chart of Account Breakdown
| Attribute | Value |
|-----------|-------|
| **Type** | Treemap or Pie Chart |
| **Priority** | 🟡 MEDIUM |

**Description:**  
Shows income distribution by Chart of Account category. Reveals revenue mix and diversification.

**Calculation:**
```
Group invoices by chartOfAccountId
Sum grossAmountNormalised per CoA
Calculate % of total
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `invoiceDate`: Current FY or selected period

**Schema Fields:**
- `Invoice.chartOfAccountId`
- `ChartOfAccount.name`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `chartOfAccountIds` filter to selected category

---

### 10. Customer Payment Velocity
| Attribute | Value |
|-----------|-------|
| **Type** | Scatter plot |
| **Priority** | 🟢 LOW |

**Description:**  
Shows average days-to-payment for each customer. Identifies slow payers and negotiation opportunities.

**Calculation:**
```
For each customer, calculate average (paymentDate - invoiceDate)
X-axis: Total invoices from customer
Y-axis: Average days to payment
Size: Total $ volume
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `status`: `'PAID'`

**Schema Fields:**
- `Invoice.vendorId`
- `Invoice.invoiceDate`
- `TransactionInvoice.createdAt` (as payment date proxy)

**Click-Through:** Sets `vendorIds` to selected customer

---

### 11. Weekly Income Snapshot
| Attribute | Value |
|-----------|-------|
| **Type** | KPI Card with sparkline |
| **Priority** | 🟡 MEDIUM |

**Description:**  
This week's income vs. last week with trend sparkline. Quick pulse check on short-term performance.

**Calculation:**
```
This Week: SUM(grossAmountNormalised) WHERE invoiceDate IN current week
Last Week: SUM(grossAmountNormalised) WHERE invoiceDate IN prior week
Change %: (This Week - Last Week) / Last Week * 100
Sparkline: Last 8 weeks daily data
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `invoiceDate`: Last 8 weeks

**Schema Fields:**
- `Invoice.invoiceDate`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `invoiceDate` to current week

---

### 12. At-Risk Receivables Alert
| Attribute | Value |
|-----------|-------|
| **Type** | Alert cards / notification list |
| **Priority** | 🔴 HIGH |

**Description:**  
Highlights invoices 60+ days overdue with dollar amounts. Immediate action items for collections team.

**Calculation:**
```
Filter: (TODAY - dueDate) >= 60 AND status = 'UNPAID'
Sort by amount descending
Show top 5-10 with customer name and amount
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `status`: `'UNPAID'`
- `dueDate`: `< (TODAY - 60 days)`

**Schema Fields:**
- `Invoice.dueDate`
- `Invoice.grossAmountNormalised`
- `Invoice.vendorId`
- `Vendor.name`

**Click-Through:** Shows all invoices 60+ days overdue

---

### 13. Revenue by Currency
| Attribute | Value |
|-----------|-------|
| **Type** | Stacked bar or small multiples |
| **Priority** | 🟢 LOW (Only for multi-currency businesses) |

**Description:**  
Shows revenue breakdown by invoice currency. Highlights FX exposure.

**Calculation:**
```
Group invoices by invoiceCurrency
Sum grossAmountNormalised per currency
Show both original currency and normalized amounts
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `invoiceDate`: Current FY

**Schema Fields:**
- `Invoice.invoiceCurrency`
- `Invoice.grossAmount` (original)
- `Invoice.grossAmountNormalised`
- `Invoice.currencyRate`

**Click-Through:** Sets `invoiceCurrency` filter

---

### 14. Invoice Processing Queue (Funnel)
| Attribute | Value |
|-----------|-------|
| **Type** | Funnel chart |
| **Priority** | 🟡 MEDIUM |

**Description:**  
Shows invoice status flow: Draft → Published → Paid. Identifies operational bottlenecks.

**Calculation:**
```
Count invoices by state and paymentStatus
Funnel stages:
  1. Total Created
  2. Published/Sent
  3. Partially Paid
  4. Fully Paid
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `invoiceDate`: Current period

**Schema Fields:**
- `Invoice.state`
- `Invoice.paymentStatus`

**Click-Through:** Sets `state` or `status` filter based on funnel stage

---

### 15. Year-over-Year Comparison
| Attribute | Value |
|-----------|-------|
| **Type** | Grouped bar chart (dual bars per month) |
| **Priority** | 🟡 MEDIUM |

**Description:**  
Compares current FY income vs. prior FY by month. Provides growth/decline context.

**Calculation:**
```
Current FY: Group by month, sum grossAmountNormalised
Prior FY: Same calculation for previous fiscal year
YoY Change %: (Current - Prior) / Prior * 100
```

**Filters Applied:**
- `type`: `'RECEIVABLE'`
- `invoiceDate`: Current FY and Prior FY ranges

**Schema Fields:**
- `Invoice.invoiceDate`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `invoiceDate` range with FY toggle

---

## Section B: Expense Page Visualizations (15 Options)

### 1. AP Aging Buckets
| Attribute | Value |
|-----------|-------|
| **Type** | Horizontal Stacked Bar Chart |
| **Priority** | 🔴 HIGH |

**Description:**  
Shows outstanding payables grouped by days overdue:
- 1-30 days (Current)
- 31-60 days
- 61-90 days
- 90+ days

**Calculation:**
```
Days Overdue = TODAY - dueDate
Group invoices by aging bucket
Sum grossAmountNormalised per bucket
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `status`: `'UNPAID'` or `'PARTIALLY_PAID'`
- `dueDate`: `< TODAY` (overdue) OR all unpaid

**Schema Fields:**
- `Invoice.type`
- `Invoice.paymentStatus`
- `Invoice.dueDate`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `dueDate` range based on bucket clicked

---

### 2. Cash Outflow Forecast
| Attribute | Value |
|-----------|-------|
| **Type** | Line Chart with area fill |
| **Priority** | 🔴 HIGH |

**Description:**  
Projects expected cash outflows based on due dates of unpaid bills for the next 30, 60, and 90 days.

**Calculation:**
```
Group unpaid invoices by dueDate week/month
Sum grossAmountNormalised per period
Show cumulative line for total expected payments
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `status`: `'UNPAID'`
- `dueDate`: `BETWEEN TODAY AND TODAY + 90 days`

**Schema Fields:**
- `Invoice.dueDate`
- `Invoice.grossAmountNormalised`
- `Invoice.paymentStatus`

**Click-Through:** Sets `dueDate` range for selected period

---

### 3. Top 5 Vendors by Spend
| Attribute | Value |
|-----------|-------|
| **Type** | Horizontal Bar Chart or Donut |
| **Priority** | 🔴 HIGH |

**Description:**  
Shows the 5 vendors with the largest spend (current FY). Identifies vendor concentration and negotiation opportunities.

**Calculation:**
```
Group invoices by vendorId
Sum grossAmountNormalised for current FY
Sort descending, take top 5
Calculate % of total spend per vendor
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `invoiceDate`: Current FY

**Schema Fields:**
- `Invoice.vendorId`
- `Vendor.name`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `vendorIds` filter to selected vendor

---

### 4. Expense Trend (Month-over-Month)
| Attribute | Value |
|-----------|-------|
| **Type** | Bar Chart with trend line overlay |
| **Priority** | 🔴 HIGH (Already exists - enhance) |

**Description:**  
Monthly expense totals with a trend line showing direction. Burn rate visibility.

**Calculation:**
```
Group invoices by MONTH(invoiceDate)
Sum grossAmountNormalised per month
Calculate 3-month moving average for trend line
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `invoiceDate`: Current Fiscal Year range

**Schema Fields:**
- `Invoice.invoiceDate`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `invoiceDate` range to selected month

---

### 5. Recurring Expense Tracker
| Attribute | Value |
|-----------|-------|
| **Type** | Card grid or status list with alerts |
| **Priority** | 🔴 HIGH (Key differentiator) |

**Description:**  
Shows recurring subscription status:
- Expected this month vs. received
- Missing invoices flagged in red
- Accrual status for each

**Calculation:**
```
Query RecurringInvoiceSeries with frequency
Check if Invoice exists for current period
Join with InvoiceAccrual for accrual status
Flag as "Received" / "Not Received" / "Accrued"
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `recurringSeriesId`: `NOT NULL`
- `invoiceDate`: Current month

**Schema Fields:**
- `RecurringInvoiceSeries.id`, `label`, `frequency`, `vendorId`
- `Invoice.recurringSeriesId`
- `Invoice.invoiceDate`
- `InvoiceAccrual.status`

**Click-Through:** Sets `recurring: true` + selected series

---

### 6. Expense by Category (Chart of Account)
| Attribute | Value |
|-----------|-------|
| **Type** | Treemap or Pie Chart |
| **Priority** | 🟡 MEDIUM |

**Description:**  
Shows spend distribution by Chart of Account category. Reveals cost structure.

**Calculation:**
```
Group invoices by chartOfAccountId
Sum grossAmountNormalised per CoA
Calculate % of total
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `invoiceDate`: Current FY or selected period

**Schema Fields:**
- `Invoice.chartOfAccountId`
- `ChartOfAccount.name`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `chartOfAccountIds` filter to selected category

---

### 7. Due This Week Alert
| Attribute | Value |
|-----------|-------|
| **Type** | KPI Card with drilldown |
| **Priority** | 🔴 HIGH |

**Description:**  
Shows $ amount and count of bills due in the next 7 days. Immediate liability visibility.

**Calculation:**
```
Filter: dueDate BETWEEN TODAY AND TODAY + 7 days
Sum grossAmountNormalised
Count invoices
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `status`: `'UNPAID'`
- `dueDate`: `BETWEEN TODAY AND TODAY + 7 days`

**Schema Fields:**
- `Invoice.dueDate`
- `Invoice.grossAmountNormalised`
- `Invoice.paymentStatus`

**Click-Through:** Sets `dueDate` range to next 7 days

---

### 8. Vendor Payment Terms Analysis
| Attribute | Value |
|-----------|-------|
| **Type** | Horizontal bar chart |
| **Priority** | 🟢 LOW |

**Description:**  
Shows average days-to-payment for top vendors. Identifies if you're paying too early (losing cash float) or too late (risking relationships).

**Calculation:**
```
For each vendor, calculate average (paymentDate - invoiceDate)
Compare against dueDate to show early/late payment pattern
Sort by total spend
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `status`: `'PAID'`

**Schema Fields:**
- `Invoice.vendorId`
- `Invoice.invoiceDate`
- `Invoice.dueDate`
- `TransactionInvoice.createdAt`

**Click-Through:** Sets `vendorIds` to selected vendor

---

### 9. Accrual Status Dashboard
| Attribute | Value |
|-----------|-------|
| **Type** | Stacked bar or status cards |
| **Priority** | 🔴 HIGH (Unique to Komplai) |

**Description:**  
Shows provisions pending vs. actuals received:
- Accrued (invoice not yet received, provision passed)
- Received (invoice arrived, matched to accrual)
- Variance (actual vs. accrued amount)

**Calculation:**
```
Join RecurringInvoiceSeries with InvoiceAccrual
For each series, check:
  - Has accrual entry been created?
  - Has actual invoice been received?
Calculate variance if actual differs from expected
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `provisions`: `true`

**Schema Fields:**
- `RecurringInvoiceSeries.*`
- `InvoiceAccrual.status`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `provisions: true` filter

---

### 10. Expense Approval Queue (Funnel)
| Attribute | Value |
|-----------|-------|
| **Type** | Funnel chart |
| **Priority** | 🟡 MEDIUM |

**Description:**  
Shows invoice classification status:
- Needs Review
- Fast Track (high confidence)
- Completed

**Calculation:**
```
Group invoices by extraction/classification state
Count per stage:
  1. Unclassified
  2. Needs Review (low confidence)
  3. Fast Track (high confidence)
  4. Validated
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `invoiceDate`: Current period

**Schema Fields:**
- `Invoice.extractionState`
- `Invoice.classificationScore`
- `InvoiceClassification.method`, `score`

**Click-Through:** Sets extraction state filter

---

### 11. Unpaid vs. Paid Ratio
| Attribute | Value |
|-----------|-------|
| **Type** | Donut chart |
| **Priority** | 🟢 LOW |

**Description:**  
Shows current period's paid vs. outstanding expenses. Liability coverage snapshot.

**Calculation:**
```
Paid: SUM(grossAmountNormalised) WHERE status = 'PAID'
Unpaid: SUM(grossAmountNormalised) WHERE status = 'UNPAID'
Calculate %
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `invoiceDate`: Current month/quarter

**Schema Fields:**
- `Invoice.paymentStatus`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `status` filter

---

### 12. Expense Variance (Month-over-Month)
| Attribute | Value |
|-----------|-------|
| **Type** | Waterfall chart |
| **Priority** | 🟡 MEDIUM |

**Description:**  
Shows expense change from last month with breakdown by category. Identifies what's driving cost increases/decreases.

**Calculation:**
```
Current Month total by CoA
Prior Month total by CoA
Variance = Current - Prior per CoA
Show as waterfall: Start (prior) → +/- by category → End (current)
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `invoiceDate`: Current month vs. prior month

**Schema Fields:**
- `Invoice.invoiceDate`
- `Invoice.chartOfAccountId`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `chartOfAccountIds` + `invoiceDate` range

---

### 13. Prepaid Amortization Waterfall
| Attribute | Value |
|-----------|-------|
| **Type** | Waterfall or Gantt timeline |
| **Priority** | 🔴 HIGH (Unique to Komplai) |

**Description:**  
Shows upcoming amortization entries from InvoiceAccrual. Visualizes how prepaid balances decrease over service periods.

**Calculation:**
```
Query InvoiceAccrual with status = 'PENDING' or 'IN_PROGRESS'
For each:
  - Total amount from Invoice
  - Months remaining = endMonth - max(TODAY, startMonth)
  - Monthly amortization = Total / Total Months
Show month-by-month waterfall of remaining balance
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- Join `InvoiceAccrual` where `status != 'COMPLETED'`

**Schema Fields:**
- `InvoiceAccrual.startMonth`
- `InvoiceAccrual.endMonth`
- `InvoiceAccrual.status`
- `Invoice.grossAmountNormalised`
- `BusinessAccrualConfig.chartOfAccountId`

**Click-Through:** Shows invoices with active accrual schedules

---

### 14. Top Cost Centers Growth
| Attribute | Value |
|-----------|-------|
| **Type** | Small multiples (sparklines per category) |
| **Priority** | 🟢 LOW |

**Description:**  
Shows fastest-growing expense categories over last 6 months. Trend alerting for cost control.

**Calculation:**
```
For each CoA, calculate monthly spend for last 6 months
Calculate MoM growth rate
Rank by growth rate
Show top 5 with sparklines
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `invoiceDate`: Last 6 months

**Schema Fields:**
- `Invoice.chartOfAccountId`
- `Invoice.invoiceDate`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `chartOfAccountIds` to selected category

---

### 15. Payment Due Calendar (Heat Map)
| Attribute | Value |
|-----------|-------|
| **Type** | Calendar heat map |
| **Priority** | 🟡 MEDIUM |

**Description:**  
Shows intensity of $ due per day for the current/next month. Visual scheduling of cash outflows.

**Calculation:**
```
Group unpaid invoices by dueDate (day)
Sum grossAmountNormalised per day
Color intensity based on $ amount (higher = darker/red)
```

**Filters Applied:**
- `type`: `'PAYABLE'`
- `status`: `'UNPAID'`
- `dueDate`: Current month or next 30 days

**Schema Fields:**
- `Invoice.dueDate`
- `Invoice.grossAmountNormalised`

**Click-Through:** Sets `dueDate` to selected day

---

## Section C: Overlapping Visualizations (Shared Components)

These visualizations use the same component, only differentiated by `type`:
- `'RECEIVABLE'` → Income page
- `'PAYABLE'` → Expense page

| # | Visualization |
|---|---------------|
| 1 | Aging Buckets (AR vs. AP) |
| 2 | Top 5 Customers/Vendors by Outstanding |
| 3 | Category Breakdown by Chart of Account |
| 4 | Recurring Tracker (subscriptions for income and expense) |
| 5 | Monthly Trend with Line |
| 6 | Due This Week Alerts |
| 7 | Year-over-Year Comparison |

---

## Section D: Recommended MVP Implementation

Start with **4 high-impact visualizations per page** to avoid overwhelming users:

### Income Page
1. **AR Aging Buckets** — Risk visibility
2. **Cash Collection Forecast** — Cash planning
3. **Top 5 Customers by Outstanding** — Concentration risk
4. **Recurring Revenue Tracker** — Subscription health

### Expense Page
1. **AP Aging Buckets** — Liability visibility
2. **Cash Outflow Forecast** — Cash planning
3. **Top 5 Vendors by Spend** — Vendor concentration
4. **Recurring Expense Tracker** — Subscription tracking + accrual alerts

---

## Section E: Larry Integration Opportunities

Each visualization can surface **"Larry's Insights"** badges:

| Visualization | Example Insight |
|---------------|-----------------|
| AR Aging | "3 invoices totaling ₹4.2L are 90+ days overdue. Ask Larry for collection recommendations." |
| Cash Forecast | "Projected collections fall short of upcoming expenses by ₹2.1L. Ask Larry for cashflow analysis." |
| Recurring | "AWS invoice is 5 days late. Accrual has been auto-passed. Ask Larry for accrual status." |
| Vendor Spend | "Spend with Vendor X increased 45% MoM. Ask Larry what's driving the change." |
| Amortization | "₹3.2L in prepaids amortize next month. Ask Larry for P&L impact." |
