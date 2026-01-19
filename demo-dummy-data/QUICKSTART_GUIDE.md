# Komplai Demo Pipeline - Quick Start Guide

## ⚡ Quick Run

```bash
./run.sh
```

That's it! The pipeline will generate invoices, bills, bank transactions, and PDFs automatically.

---

## 📋 What It Does

1. Loads existing data from Excel
2. Generates 2 new invoices
3. Generates 4 new bills
4. Generates bank transactions with reconciliation
5. Saves everything to Excel (appends, doesn't overwrite)
6. Creates PDF documents in `./output/pdfs/`
7. (Optional) Syncs to Google Sheets when shared

---

## 🔧 First-Time Setup

### 1. Install Dependencies (if not already installed)

```bash
pip install pandas pyyaml openpyxl gspread oauth2client weasyprint jinja2
```

### 2. Share Google Sheet (Optional but Recommended)

To enable Google Sheets sync:

1. Open: https://docs.google.com/spreadsheets/d/1KXGIa1G8q7PMMC5FSbj7mzgIaszRMHsikevdVpw_0Aw/
2. Click "Share" → Add as **Editor**:
   ```
   komplai-dummy-data@dummy-data-483609.iam.gserviceaccount.com
   ```
3. Click "Send"

The pipeline will automatically sync to Google Sheets on next run.

---

## 🎯 Running for Specific Week

```python
from main_pipeline import DemoPipeline
from datetime import datetime

pipeline = DemoPipeline()

# Run for a specific Monday
results = pipeline.run_weekly_generation(datetime(2026, 1, 20))

print(f"Generated {results['invoices_generated']} invoices")
print(f"Generated {results['bills_generated']} bills")
print(f"Generated {results['transactions_generated']} transactions")
```

---

## 📁 Output Files

After running, check:

- **Excel**: `Komplai_Demo_Master (Claude).xlsx` (updated with new rows)
- **PDFs**: `./output/pdfs/` directory
  - `INV-202601-XXXX.pdf` (invoices)
  - `BILL-202601-XXXX.pdf` (bills)
- **Google Sheets**: Automatically synced (if shared)

---

## ⏰ Schedule to Run Automatically

### Option A: Cron Job (Linux/Mac)

```bash
crontab -e

# Add this line (runs every Monday at 10:00 AM):
0 10 * * 1 cd /home/user/demo-dummy-data && ./run.sh
```

### Option B: Python Scheduler

Create `scheduler.py`:

```python
import schedule
import time
from main_pipeline import DemoPipeline
from datetime import datetime

def run_pipeline():
    """Run the pipeline"""
    print(f"\n[{datetime.now()}] Starting scheduled pipeline run...")
    pipeline = DemoPipeline()
    pipeline.run_weekly_generation()

# Schedule for every Monday at 10:00 AM
schedule.every().monday.at("10:00").do(run_pipeline)

print("Scheduler started. Waiting for Monday 10:00 AM...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

Then run:
```bash
python scheduler.py
```

---

## 🧪 Testing

Run the test suite:

```bash
python test_components.py
```

This verifies all components are working correctly.

---

## 📊 What Gets Generated

**Per Week:**
- 2 invoices (70% with deferred revenue)
- 4 bills (with automatic TDS calculation)
- ~8 bank transactions (95% matched, 5% anomalies)
- 6 PDFs

**Business Rules:**
- ✅ Multi-currency (USD/INR) with proper conversions
- ✅ Tax calculations (IGST 18%, Sales Tax 4-8%)
- ✅ TDS by expense type (194I 10%, 194C 2%, 194J 10%)
- ✅ Bank balance tracking (never negative)
- ✅ Deterministic data (same date = same output)

---

## 🆘 Troubleshooting

### Google Sheets Not Syncing?

Check:
1. Is the service account email shared on the sheet?
2. Check the credentials file: `dummy-data-483609-2b5f128b43ad.json`
3. Pipeline will work without Google Sheets (Excel only)

### PDFs Not Generating?

Check:
1. WeasyPrint installed: `pip install weasyprint`
2. Output directory exists: `./output/pdfs/`
3. Check PDF generator output for errors

### Excel File Locked?

Close Excel if it's open before running the pipeline.

---

## 📝 Configuration

Edit `config.yaml` to change:
- Number of invoices/bills per week
- Exchange rates
- Tax rates
- Output directories
- TDS sections

---

## 🎉 That's It!

The pipeline is ready to use. Run `./run.sh` anytime to generate new data.

For detailed documentation, see:
- `COMPLETION_SUMMARY.md` - Full implementation details
- `TEST_RESULTS.md` - Test results and verification
- `README.md` - Complete architecture documentation
