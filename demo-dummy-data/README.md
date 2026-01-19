# Komplai Demo Data Pipeline
**Automated weekly generation of realistic financial transaction data**

## 📊 Project Overview

This pipeline automatically generates invoices, bills, and bank transactions every Monday at 10 AM, converts them to PDFs, and emails them to Komplai's inbox for continuous demo capabilities.

### Key Features
- ✅ **2 invoices/week** with deferred revenue handling (70% multi-month contracts)
- ✅ **4 bills/week** with TDS auto-calculation and prepaid expense detection
- ✅ **Weekly bank statements** with 95% reconciliation + 5% anomalies
- ✅ **Dual persistence**: Google Sheets + Local Excel
- ✅ **Deterministic randomness** for reproducible data
- ✅ **Comprehensive validation** (14 business rules)

---

## 🏗️ Architecture

```
komplai_demo_pipeline/
├── config/
│   └── config.yaml              # All pipeline settings
├── generators/
│   ├── invoice_generator.py     # ✅ COMPLETE
│   ├── bill_generator.py        # ✅ COMPLETE
│   └── bank_generator.py        # ✅ COMPLETE
├── validators/
│   └── validator.py             # ⏳ TO IMPLEMENT
├── utils/
│   ├── utils.py                 # ✅ COMPLETE (all helpers)
│   ├── excel_manager.py         # ⏳ TO IMPLEMENT
│   └── sheets_manager.py        # ⏳ TO IMPLEMENT
├── pdf/
│   └── pdf_generator.py         # ⏳ TO IMPLEMENT
├── email/
│   └── email_service.py         # ⏳ TO IMPLEMENT
├── templates/
│   ├── invoice_template.html    # ✅ PROVIDED
│   ├── bill_template.html       # ✅ PROVIDED
│   └── statement_template.html  # ✅ PROVIDED
├── output/
│   ├── invoices/
│   ├── bills/
│   └── statements/
├── main_pipeline.py             # ⏳ TO IMPLEMENT
├── scheduler.py                 # ⏳ TO IMPLEMENT
└── requirements.txt             # ✅ COMPLETE
```

---

## ✅ COMPLETED COMPONENTS (Day 1)

### 1. Core Utilities (`utils/utils.py`)
**All helper functions implemented:**
- Date handling (next Monday, business days, formatting)
- ID generation (invoices, bills, transactions)
- Currency conversion (USD ↔ INR @ 85.0)
- Tax calculations (IGST, TDS, withholding, sales tax)
- TDS mapping by expense category
- 14 validation functions
- Service period detection
- Prepaid/deferred detection

**Key Functions:**
```python
generate_invoice_id(date, seq)           # INV-202601-0001
generate_bill_id(date, seq)              # BILL-202601-0001
calculate_tds(subtotal, rate)            # TDS = Subtotal × Rate
get_tds_section_for_expense(account)     # Auto-map TDS section
is_deferred_revenue(service_period, date) # Detect 3+ month periods
validate_tds_calculation(subtotal, rate, amount)  # Critical validation
```

### 2. Invoice Generator (`generators/invoice_generator.py`)
**Features:**
- Weighted customer selection by transaction value
- 1-3 line items per invoice
- 70% probability of deferred revenue (3-12 month contracts)
- Service period injection: `"Term: 01 Jan 2026 – 31 Dec 2026"`
- Tax calculation (IGST 18% for INR, Sales Tax 4-8% for USD)
- Deferral schedule calculation

**Usage:**
```python
from generators.invoice_generator import InvoiceGenerator

gen = InvoiceGenerator(entities_df, config)
invoices = gen.generate_weekly_invoices(run_date, last_invoices, count=2)
```

### 3. Bill Generator (`generators/bill_generator.py`)
**Features:**
- 10 recurring vendors rotated across weeks (no monthly clustering)
- Weighted one-time bill generation by expense category
- Auto-TDS application based on expense account:
  - 194I (Rent): 10%
  - 194C (Contractor): 2%
  - 194J (Professional): 10%
- Prepaid expense detection (annual subscriptions)
- Service period for recurring expenses

**TDS Logic:**
```python
# Automatically applies correct TDS based on expense account
"Rent Expense" → 194I @ 10%
"Consultant Expense" → 194J @ 10%
"Repairs and Maintenance" → 194C @ 2%
"Software Subscriptions" → No TDS
```

**Usage:**
```python
from generators.bill_generator import BillGenerator

gen = BillGenerator(entities_df, recurring_df, config)
bills = gen.generate_weekly_bills(run_date, last_bills, count=4)
```

### 4. Bank Transaction Generator (`generators/bank_generator.py`)
**Features:**
- Receipt generation (invoice payments with Net 15 ± 3 days)
- Payment generation (all bills paid on 25th of month)
- Running balance maintenance
- 95% reconciliation rate
- 5% anomalies:
  - 2.5% orphaned payments (no matching bill)
  - 2.5% missing receipts (invoice unpaid)
- Withholding tax reflection (US customers: 70% received)
- TDS reflection (vendors: Net_Payable paid)

**Usage:**
```python
from generators.bank_generator import BankTransactionGenerator

gen = BankTransactionGenerator(config)
txns, balance = gen.generate_weekly_bank_statement(
    run_date, invoices_df, bills_df, bank_df
)
```

---

## ⏳ REMAINING IMPLEMENTATION (Day 2)

### Priority 1: Data Persistence (4 hours)

#### Excel Manager (`utils/excel_manager.py`)
```python
import pandas as pd
from openpyxl import load_workbook

class ExcelManager:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def read_sheet(self, sheet_name):
        return pd.read_excel(self.file_path, sheet_name=sheet_name)
    
    def append_data(self, sheet_name, new_data_df):
        """Append rows to existing sheet"""
        # Use openpyxl in append mode
        with pd.ExcelWriter(self.file_path, engine='openpyxl', 
                           mode='a', if_sheet_exists='overlay') as writer:
            existing = self.read_sheet(sheet_name)
            start_row = len(existing) + 1
            new_data_df.to_excel(writer, sheet_name=sheet_name,
                                startrow=start_row, header=False, index=False)
```

#### Google Sheets Manager (`utils/sheets_manager.py`)
```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SheetsManager:
    def __init__(self, creds_path, sheet_id):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(sheet_id)
    
    def append_rows(self, sheet_name, data_list):
        """Append rows to sheet"""
        worksheet = self.sheet.worksheet(sheet_name)
        worksheet.append_rows(data_list)
```

**Setup Instructions:**
1. Go to Google Cloud Console
2. Enable Google Sheets API
3. Create Service Account
4. Download JSON key
5. Share spreadsheet with service account email
6. Save JSON as `config/google_service_account.json`

### Priority 2: Validation Framework (2 hours)

#### Validator (`validators/validator.py`)
```python
from utils.utils import ValidationError, validate_*

class DataValidator:
    def __init__(self, entities_df):
        self.entities = entities_df
        self.errors = []
    
    def validate_invoice(self, invoice):
        """Run all 14 validation checks"""
        try:
            validate_entity_exists(invoice['Customer_ID'], self.entities)
            validate_currency(invoice['Currency'])
            validate_amount_positive(invoice['Subtotal'], 'Subtotal')
            # ... all validations
            return True
        except ValidationError as e:
            self.log_error('Invoice', invoice['Invoice_ID'], str(e))
            return False
    
    def validate_bill(self, bill):
        # Same pattern, includes TDS validation
        validate_tds_calculation(bill['Subtotal'], bill['TDS_Rate'], bill['TDS_Amount'])
        # ...
```

### Priority 3: PDF Generation (3 hours)

#### PDF Generator (`pdf/pdf_generator.py`)
```python
from weasyprint import HTML
from jinja2 import Template
from datetime import datetime

class PDFGenerator:
    def __init__(self, template_dir):
        self.template_dir = template_dir
    
    def generate_invoice_pdf(self, invoice_data, output_path):
        # Load HTML template
        with open(f"{self.template_dir}/invoice_template.html") as f:
            template = Template(f.read())
        
        # Render with data
        html = template.render(
            invoice_id=invoice_data['Invoice_ID'],
            invoice_date=invoice_data['Invoice_Date'].strftime('%d %b %Y'),
            customer_name=invoice_data['Customer_Name'],
            # ... all invoice fields
        )
        
        # Convert to PDF
        HTML(string=html).write_pdf(output_path)
        return output_path
```

**Template Variables Mapping:**
```
Invoice Template:
- {{ invoice_id }}           → Invoice_ID
- {{ invoice_date }}         → Invoice_Date (formatted)
- {{ customer_name }}        → Customer_Name
- {{ customer_address }}     → Customer_Address
- {{ customer_tax_id }}      → Customer_Tax_ID
- {{ line_items }}           → List of {description, qty, rate, amount}
- {{ subtotal }}             → Subtotal (formatted ₹)
- {{ tax_type }}             → Tax_Type (IGST/Sales Tax)
- {{ tax_rate }}             → Tax_Rate (18% / 6%)
- {{ tax_amount }}           → Tax_Amount (formatted)
- {{ total_amount }}         → Total_Amount (formatted)
- {{ bank_details }}         → From config

Bill Template: Same pattern
Statement Template:
- {{ statement_period }}     → "Jan 1 - Jan 7, 2026"
- {{ opening_balance }}      → First transaction balance
- {{ closing_balance }}      → Last transaction balance
- {{ transactions }}         → List of {date, description, type, amount, balance}
- {{ total_credits }}        → Sum of credits
- {{ total_debits }}         → Sum of debits
```

### Priority 4: Email Service (2 hours)

#### Email Service (`email/email_service.py`)
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time

class EmailService:
    def __init__(self, smtp_config):
        self.smtp_server = smtp_config['smtp_server']
        self.smtp_port = smtp_config['smtp_port']
        self.sender_email = smtp_config['sender_email']
        self.sender_password = smtp_config['sender_password']
        self.recipient_email = smtp_config['recipient_email']
    
    def send_document(self, pdf_path, document_type):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = f"{document_type} - {os.path.basename(pdf_path)}"
        
        # Attach PDF
        with open(pdf_path, 'rb') as f:
            part = MIMEBase('application', 'pdf')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 
                          f'attachment; filename={os.path.basename(pdf_path)}')
            msg.attach(part)
        
        # Send via Gmail SMTP
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
    
    def send_batch(self, pdf_files, delay=60):
        for pdf in pdf_files:
            self.send_document(pdf['path'], pdf['type'])
            time.sleep(delay)  # 60 second delay
```

**Gmail Setup:**
1. Enable 2FA on Gmail
2. Generate App Password: Settings → Security → App Passwords
3. Update `config.yaml`:
```yaml
email:
  sender_email: "your-email@gmail.com"
  sender_password: "your-app-password-here"
  recipient_email: "demo@letskomplai.com"
```

### Priority 5: Main Pipeline (2 hours)

#### Main Pipeline (`main_pipeline.py`)
```python
from datetime import datetime
import pandas as pd
import yaml

from generators.invoice_generator import InvoiceGenerator
from generators.bill_generator import BillGenerator
from generators.bank_generator import BankTransactionGenerator
from validators.validator import DataValidator
from utils.excel_manager import ExcelManager
from utils.sheets_manager import SheetsManager
from pdf.pdf_generator import PDFGenerator
from email.email_service import EmailService

class KomplaiDataPipeline:
    def __init__(self, config_path):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        # Initialize managers
        self.excel = ExcelManager(self.config['data_sources']['excel_path'])
        self.sheets = SheetsManager(
            self.config['data_sources']['google_credentials'],
            self.config['data_sources']['google_sheet_id']
        )
        self.pdf_gen = PDFGenerator(self.config['templates']['template_dir'])
        self.email = EmailService(self.config['email'])
    
    def run(self, run_date=None):
        if run_date is None:
            run_date = datetime.now()
        
        print(f"[{run_date}] Starting pipeline...")
        
        try:
            # Step 1: Load existing data
            entities = self.excel.read_sheet('Entities')
            invoices = self.excel.read_sheet('Invoices_Master')
            bills = self.excel.read_sheet('Bills_Master')
            bank = self.excel.read_sheet('Bank_Transactions')
            recurring = self.excel.read_sheet('Recurring_Schedule')
            
            # Step 2: Initialize generators
            inv_gen = InvoiceGenerator(entities, self.config)
            bill_gen = BillGenerator(entities, recurring, self.config)
            bank_gen = BankTransactionGenerator(self.config)
            validator = DataValidator(entities)
            
            # Step 3: Generate new data
            new_invoices = inv_gen.generate_weekly_invoices(run_date, invoices, 2)
            new_bills = bill_gen.generate_weekly_bills(run_date, bills, 4)
            new_bank_txns, balance = bank_gen.generate_weekly_bank_statement(
                run_date, invoices, bills, bank
            )
            
            # Step 4: Validate
            validated_invoices = [inv for inv in new_invoices 
                                 if validator.validate_invoice(inv)]
            validated_bills = [bill for bill in new_bills 
                             if validator.validate_bill(bill)]
            validated_bank = [txn for txn in new_bank_txns 
                            if validator.validate_bank_transaction(txn)]
            
            # Step 5: Persist to Excel + Sheets
            inv_df = pd.DataFrame(validated_invoices)
            bill_df = pd.DataFrame(validated_bills)
            bank_df = pd.DataFrame(validated_bank)
            
            self.excel.append_data('Invoices_Master', inv_df)
            self.excel.append_data('Bills_Master', bill_df)
            self.excel.append_data('Bank_Transactions', bank_df)
            
            self.sheets.append_rows('Invoices_Master', inv_df.values.tolist())
            self.sheets.append_rows('Bills_Master', bill_df.values.tolist())
            self.sheets.append_rows('Bank_Transactions', bank_df.values.tolist())
            
            # Step 6: Generate PDFs
            pdf_files = []
            
            for inv in validated_invoices:
                pdf_path = f"output/invoices/{inv['Invoice_ID']}.pdf"
                self.pdf_gen.generate_invoice_pdf(inv, pdf_path)
                pdf_files.append({'path': pdf_path, 'type': 'Invoice'})
            
            for bill in validated_bills:
                pdf_path = f"output/bills/{bill['Bill_ID']}.pdf"
                self.pdf_gen.generate_bill_pdf(bill, pdf_path)
                pdf_files.append({'path': pdf_path, 'type': 'Bill'})
            
            stmt_path = f"output/statements/STMT-{run_date.strftime('%Y%m%d')}.pdf"
            self.pdf_gen.generate_statement_pdf(validated_bank, stmt_path)
            pdf_files.append({'path': stmt_path, 'type': 'Bank Statement'})
            
            # Step 7: Send emails
            self.email.send_batch(pdf_files, delay=60)
            
            print(f"✅ Pipeline completed: {len(validated_invoices)} invoices, "
                  f"{len(validated_bills)} bills, {len(validated_bank)} transactions")
            
        except Exception as e:
            print(f"❌ Pipeline failed: {e}")
            raise

if __name__ == "__main__":
    pipeline = KomplaiDataPipeline('config/config.yaml')
    pipeline.run()
```

### Priority 6: Scheduler (`scheduler.py`)
```python
import schedule
import time
from datetime import datetime
from main_pipeline import KomplaiDataPipeline

def run_pipeline():
    pipeline = KomplaiDataPipeline('config/config.yaml')
    pipeline.run()

# Schedule for every Monday at 10:00 AM IST
schedule.every().monday.at("10:00").do(run_pipeline)

print("🚀 Komplai Pipeline Scheduler Started")
print("⏰ Scheduled: Every Monday at 10:00 AM IST")
print("📅 Next run:", schedule.next_run())

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

---

## 🚀 DEPLOYMENT STEPS

### 1. Install Dependencies
```bash
cd /home/claude/komplai_demo_pipeline
pip install -r requirements.txt
```

### 2. Configure Google Sheets API
```bash
# Place your service account JSON in:
config/google_service_account.json
```

### 3. Configure Gmail SMTP
```bash
# Update config/config.yaml with:
email:
  sender_email: "your-gmail@gmail.com"
  sender_password: "your-app-password"  # From Gmail Settings
```

### 4. Test Single Run
```bash
python main_pipeline.py
```

### 5. Start Scheduler (Production)
```bash
# Run in background
nohup python scheduler.py > logs/scheduler.log 2>&1 &

# Or use cron
crontab -e
# Add: 0 10 * * 1 /usr/bin/python3 /path/to/main_pipeline.py
```

---

## 📝 DATA FLOW

```
Monday 10 AM Trigger
    ↓
Load Entities, Invoices, Bills, Bank
    ↓
Generate 2 Invoices (70% with 3-12 month service periods)
Generate 4 Bills (2 recurring + 2 one-time, auto-TDS)
Generate ~15 Bank Transactions (95% matched, 5% anomalies)
    ↓
Validate All (14 business rules)
    ↓
Append to Excel (local backup)
Append to Google Sheets (live monitoring)
    ↓
Generate 7 PDFs (2 invoices + 4 bills + 1 statement)
    ↓
Email 7 PDFs to demo@letskomplai.com (60s delays)
    ↓
Log to Monitoring Sheets
```

---

## 📊 MONITORING

### Dashboard Sheets (Auto-Updated)

**Pipeline_Logs:**
| Run_ID | Timestamp | Invoices | Bills | Bank_Txns | Errors | Status |
|--------|-----------|----------|-------|-----------|--------|--------|
| RUN-202601061000 | 2026-01-06 10:00 | 2 | 4 | 15 | 0 | SUCCESS |

**Data_Health:**
| Week_Ending | Invoices | Bills | Bank_Balance | Recon_Rate | Anomalies |
|-------------|----------|-------|--------------|------------|-----------|
| 2026-01-06 | 45 | 51 | ₹104.2M | 95.2% | 1 |

**Validation_Errors:**
| Error_ID | Timestamp | Doc_Type | Doc_ID | Error | Data |
|----------|-----------|----------|--------|-------|------|
| ERR001 | ... | Bill | BILL-... | TDS calc error | {...} |

---

## 🧪 TESTING

### Unit Tests
```python
# Test invoice generator
python generators/invoice_generator.py

# Test bill generator
python generators/bill_generator.py

# Test bank generator
python generators/bank_generator.py
```

### Integration Test
```python
# Full pipeline test
python main_pipeline.py
```

---

## 🔑 CRITICAL VALIDATIONS

1. **TDS Calculation:** `TDS_Amount = Subtotal × TDS_Rate`
2. **Total Amount:** `Total = Subtotal + Tax - TDS`
3. **Bank Balance:** Never negative
4. **Entity Exists:** All IDs valid
5. **Currency:** Only USD/INR
6. **Account Categories:** Invoices → Sales only, Bills → Expense only

---

## 📞 NEXT STEPS FOR YOU

1. **Install missing packages** (when network available):
   ```bash
   pip install gspread oauth2client weasyprint
   ```

2. **Set up Google Sheets API**:
   - Create service account
   - Download JSON credentials
   - Share spreadsheet with service account email

3. **Set up Gmail App Password**:
   - Enable 2FA
   - Generate app password
   - Update config.yaml

4. **Implement remaining 6 files**:
   - validators/validator.py (use patterns from utils.py)
   - utils/excel_manager.py (see code above)
   - utils/sheets_manager.py (see code above)
   - pdf/pdf_generator.py (see code above)
   - email/email_service.py (see code above)
   - main_pipeline.py (see code above)

5. **Test & Deploy**:
   - Single test run
   - Verify Google Sheets updates
   - Verify PDFs generated
   - Verify emails sent
   - Start scheduler

---

## ✅ SUCCESS CRITERIA

- ✅ Generates 2 + 4 + 1 documents every Monday
- ✅ 100% validation pass rate
- ✅ Excel ↔ Google Sheets synchronized
- ✅ PDFs match template format
- ✅ All 7 emails delivered
- ✅ Bank balance never negative
- ✅ 95% reconciliation rate maintained

---

**Status: 60% Complete - Core generators + utilities done!**
**Next: Implement 6 remaining components (Day 2 - 10 hours)**
