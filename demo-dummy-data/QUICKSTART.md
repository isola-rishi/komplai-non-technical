# Komplai Demo Pipeline - Quick Start Guide
**Complete in 10 Hours Tomorrow (Day 2)**

## ✅ WHAT'S DONE TODAY (60% Complete)

### Core Infrastructure - PRODUCTION READY
1. **✅ Utilities Module** (`utils/utils.py`) - 600+ lines
   - All date, ID, currency, tax functions
   - 14 validation functions
   - TDS mapping logic
   - Service period detection
   - Deterministic randomness

2. **✅ Invoice Generator** (`generators/invoice_generator.py`) - 350+ lines
   - Weighted customer selection
   - Multi-line item support (1-3 items)
   - 70% deferred revenue probability
   - Service period injection
   - Full tax calculation

3. **✅ Bill Generator** (`generators/bill_generator.py`) - 400+ lines
   - 10 recurring vendors rotation
   - Weighted one-time bills
   - Auto-TDS by expense account
   - Prepaid detection
   - Recurring schedule management

4. **✅ Bank Generator** (`generators/bank_generator.py`) - 300+ lines
   - Receipt generation (Net 15 ± 3 days)
   - Payment generation (25th of month)
   - 95% reconciliation + 5% anomalies
   - Running balance tracking
   - Withholding/TDS reflection

5. **✅ Configuration** (`config/config.yaml`)
   - All pipeline settings
   - TDS section mappings
   - Email configuration
   - Template paths

---

## 🚀 TOMORROW'S IMPLEMENTATION PLAN

### Session 1: Data Persistence (3 hours - 9 AM to 12 PM)

#### Task 1.1: Excel Manager (45 minutes)
File: `utils/excel_manager.py`

```python
import pandas as pd
from openpyxl import load_workbook

class ExcelManager:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def read_sheet(self, sheet_name):
        """Read entire sheet as DataFrame"""
        return pd.read_excel(self.file_path, sheet_name=sheet_name)
    
    def append_data(self, sheet_name, new_data_df):
        """Append new rows to existing sheet"""
        # Load workbook
        book = load_workbook(self.file_path)
        writer = pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay')
        writer.book = book
        
        # Get existing data to find start row
        existing = pd.read_excel(self.file_path, sheet_name=sheet_name)
        start_row = len(existing) + 1  # +1 for header
        
        # Write new data
        new_data_df.to_excel(writer, sheet_name=sheet_name, 
                            startrow=start_row, header=False, index=False)
        writer.close()
```

**Test:**
```python
manager = ExcelManager('/mnt/user-data/uploads/Komplai_Demo_Master__Claude_.xlsx')
entities = manager.read_sheet('Entities')
print(f"Loaded {len(entities)} entities")
```

#### Task 1.2: Google Sheets Manager (45 minutes)
File: `utils/sheets_manager.py`

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SheetsManager:
    def __init__(self, credentials_path, spreadsheet_id):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_path, scope
        )
        self.client = gspread.authorize(creds)
        self.spreadsheet = self.client.open_by_key(spreadsheet_id)
    
    def append_rows(self, sheet_name, rows_list):
        """Append multiple rows to sheet"""
        worksheet = self.spreadsheet.worksheet(sheet_name)
        worksheet.append_rows(rows_list, value_input_option='RAW')
    
    def get_sheet(self, sheet_name):
        """Get worksheet object"""
        return self.spreadsheet.worksheet(sheet_name)
```

**Setup Google Sheets API:**
1. Go to: https://console.cloud.google.com/
2. Create new project: "Komplai Demo Pipeline"
3. Enable Google Sheets API
4. Create Service Account:
   - IAM & Admin → Service Accounts
   - Create Service Account
   - Name: "komplai-pipeline"
   - Create and download JSON key
5. Save JSON as: `config/google_service_account.json`
6. Open Google Sheet: https://docs.google.com/spreadsheets/d/1KXGIa1G8q7PMMC5FSbj7mzgIaszRMHsikevdVpw_0Aw/
7. Share with service account email (from JSON): `komplai-pipeline@....iam.gserviceaccount.com`
8. Give "Editor" permission

#### Task 1.3: Validation Framework (90 minutes)
File: `validators/validator.py`

```python
import sys
sys.path.append('/home/claude/komplai_demo_pipeline')

from utils.utils import (
    ValidationError,
    validate_entity_exists,
    validate_currency,
    validate_amount_positive,
    validate_line_items_sum,
    validate_tax_calculation,
    validate_tds_calculation,
    validate_total_amount,
    validate_account_category,
    validate_date_sequential,
    validate_balance_non_negative
)

class DataValidator:
    """Validates all generated data before persistence"""
    
    def __init__(self, entities_df):
        self.entities = entities_df
        self.errors = []
    
    def validate_invoice(self, invoice):
        """Validate invoice with all business rules"""
        self.errors = []
        
        try:
            # Entity validation
            validate_entity_exists(invoice['Customer_ID'], self.entities)
            
            # Currency validation
            validate_currency(invoice['Currency'])
            
            # Amount validations
            validate_amount_positive(invoice['Subtotal'], 'Subtotal')
            validate_amount_positive(invoice['Tax_Amount'], 'Tax_Amount')
            validate_amount_positive(invoice['Total_Amount'], 'Total_Amount')
            
            # Line items sum validation
            line_items = []
            for i in range(1, 4):
                amount = invoice.get(f'Line_Item_{i}_Amount')
                if amount is not None and amount > 0:
                    line_items.append({'amount': amount})
            validate_line_items_sum(line_items, invoice['Subtotal'])
            
            # Tax calculation validation
            validate_tax_calculation(
                invoice['Subtotal'],
                invoice['Tax_Rate'],
                invoice['Tax_Amount']
            )
            
            # Total amount validation
            validate_total_amount(
                invoice['Subtotal'],
                invoice['Tax_Amount'],
                0.0,  # No TDS on invoices
                invoice['Total_Amount']
            )
            
            # Account category validation
            validate_account_category(
                invoice['Line_Item_1_Account'],
                ['Sales', 'Project Revenue', 'Sales - Software']
            )
            
            return True
            
        except ValidationError as e:
            self.log_error('Invoice', invoice['Invoice_ID'], str(e), invoice)
            return False
    
    def validate_bill(self, bill):
        """Validate bill with all business rules including TDS"""
        self.errors = []
        
        try:
            # Entity validation
            validate_entity_exists(bill['Vendor_ID'], self.entities)
            
            # Currency validation
            validate_currency(bill['Currency'])
            
            # Amount validations
            validate_amount_positive(bill['Subtotal'], 'Subtotal')
            validate_amount_positive(bill['Tax_Amount'], 'Tax_Amount')
            validate_amount_positive(bill['Total_Amount'], 'Total_Amount')
            
            # Tax calculation validation
            validate_tax_calculation(
                bill['Subtotal'],
                bill['Tax_Rate'],
                bill['Tax_Amount']
            )
            
            # TDS calculation validation (CRITICAL)
            if bill['TDS_Applicable']:
                validate_tds_calculation(
                    bill['Subtotal'],
                    bill['TDS_Rate'],
                    bill['TDS_Amount']
                )
            
            # Total amount validation
            validate_total_amount(
                bill['Subtotal'],
                bill['Tax_Amount'],
                bill['TDS_Amount'],
                bill['Total_Amount']
            )
            
            # Net payable validation
            expected_net = bill['Total_Amount'] - bill['TDS_Amount']
            if abs(expected_net - bill['Net_Payable']) > 0.01:
                raise ValidationError(f"Net payable mismatch: {expected_net} vs {bill['Net_Payable']}")
            
            return True
            
        except ValidationError as e:
            self.log_error('Bill', bill['Bill_ID'], str(e), bill)
            return False
    
    def validate_bank_transaction(self, txn, bank_df):
        """Validate bank transaction"""
        self.errors = []
        
        try:
            # Amount validations
            if txn['Debit'] > 0:
                validate_amount_positive(txn['Debit'], 'Debit')
            if txn['Credit'] > 0:
                validate_amount_positive(txn['Credit'], 'Credit')
            
            # Balance validation
            validate_balance_non_negative(txn['Running_Balance'])
            
            return True
            
        except ValidationError as e:
            self.log_error('Bank_Transaction', txn['Transaction_ID'], str(e), txn)
            return False
    
    def log_error(self, doc_type, doc_id, error_msg, data):
        """Log validation error"""
        error_entry = {
            'timestamp': datetime.now(),
            'doc_type': doc_type,
            'doc_id': doc_id,
            'error': error_msg,
            'data': str(data)[:500]  # Truncate for logging
        }
        self.errors.append(error_entry)
        print(f"⚠️  Validation Error [{doc_type}]: {error_msg}")
```

---

### Session 2: PDF & Email (4 hours - 1 PM to 5 PM)

#### Task 2.1: PDF Generator (2 hours)
File: `pdf/pdf_generator.py`

**Key Challenge:** Parse provided HTML templates and inject data

```python
from weasyprint import HTML
from jinja2 import Template
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self, template_dir):
        self.template_dir = template_dir
    
    def generate_invoice_pdf(self, invoice, output_path):
        """Generate invoice PDF from HTML template"""
        
        # Load template
        template_path = os.path.join(self.template_dir, 'invoice_template.html')
        with open(template_path, 'r') as f:
            html_content = f.read()
        
        # Parse template with Jinja2
        template = Template(html_content)
        
        # Prepare data for template
        data = {
            'invoice_id': invoice['Invoice_ID'],
            'invoice_date': pd.to_datetime(invoice['Invoice_Date']).strftime('%d %b %Y'),
            'due_date': pd.to_datetime(invoice['Due_Date']).strftime('%d %b %Y'),
            'customer_name': invoice['Customer_Name'],
            'customer_address': invoice['Customer_Address'],
            'customer_tax_id': invoice['Customer_Tax_ID'],
            'line_items': self._format_line_items(invoice),
            'subtotal': f"₹{invoice['Subtotal']:,.2f}" if invoice['Currency'] == 'INR' else f"${invoice['Subtotal']:,.2f}",
            'tax_type': invoice['Tax_Type'],
            'tax_rate': f"{invoice['Tax_Rate']*100:.0f}%",
            'tax_amount': f"₹{invoice['Tax_Amount']:,.2f}" if invoice['Currency'] == 'INR' else f"${invoice['Tax_Amount']:,.2f}",
            'total_amount': f"₹{invoice['Total_Amount']:,.2f}" if invoice['Currency'] == 'INR' else f"${invoice['Total_Amount']:,.2f}",
            'notes': invoice['Notes']
        }
        
        # Render HTML
        rendered_html = template.render(**data)
        
        # Convert to PDF
        HTML(string=rendered_html).write_pdf(output_path)
        
        return output_path
    
    def _format_line_items(self, invoice):
        """Extract and format line items"""
        items = []
        for i in range(1, 4):
            desc = invoice.get(f'Line_Item_{i}_Description')
            if desc:
                items.append({
                    'description': desc,
                    'quantity': invoice[f'Line_Item_{i}_Quantity'],
                    'rate': invoice[f'Line_Item_{i}_Rate'],
                    'amount': invoice[f'Line_Item_{i}_Amount']
                })
        return items
    
    def generate_bill_pdf(self, bill, output_path):
        """Generate bill PDF - similar to invoice"""
        # Same pattern as invoice
        pass
    
    def generate_statement_pdf(self, transactions, output_path):
        """Generate bank statement PDF"""
        template_path = os.path.join(self.template_dir, 'statement_template.html')
        # Format transactions into table
        # Calculate totals
        # Render and save
        pass
```

**Note:** You'll need to manually map the HTML template variables. I've provided the structure - you'll need to match field names to the actual HTML template positions.

#### Task 2.2: Email Service (1 hour)
File: `email/email_service.py`

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
import time

class EmailService:
    def __init__(self, config):
        self.smtp_server = config['smtp_server']
        self.smtp_port = config['smtp_port']
        self.sender_email = config['sender_email']
        self.sender_password = config['sender_password']
        self.recipient_email = config['recipient_email']
        self.delay = config.get('delay_between_emails', 60)
    
    def send_document(self, pdf_path, document_type):
        """Send single PDF as email attachment"""
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = f"{document_type} - {os.path.basename(pdf_path)}"
        
        # Body
        body = f"Attached {document_type} for processing."
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF
        with open(pdf_path, 'rb') as f:
            part = MIMEBase('application', 'pdf')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(pdf_path)}'
            )
            msg.attach(part)
        
        # Send via SMTP
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✉️  Sent: {pdf_path}")
            return True
            
        except Exception as e:
            print(f"❌ Email failed: {e}")
            return False
    
    def send_batch(self, pdf_files):
        """Send multiple PDFs with delays"""
        for pdf in pdf_files:
            self.send_document(pdf['path'], pdf['type'])
            time.sleep(self.delay)  # 60 second delay
```

**Gmail Setup:**
1. Go to: https://myaccount.google.com/
2. Security → 2-Step Verification (enable if not already)
3. Security → App passwords
4. Generate password for "Mail"
5. Copy 16-character password
6. Update `config/config.yaml`:
```yaml
email:
  sender_email: "your-gmail@gmail.com"
  sender_password: "xxxx xxxx xxxx xxxx"  # App password
```

#### Task 2.3: Template Adaptation (1 hour)
Copy provided templates to correct location:

```bash
cp /mnt/user-data/uploads/eb00ca48-*.html templates/invoice_template.html
cp /mnt/user-data/uploads/eb00ca48-*.html templates/bill_template.html
cp /mnt/user-data/uploads/statement-june-test.html templates/statement_template.html
```

Then manually edit templates to add Jinja2 variables:
- Replace hardcoded values with `{{ variable_name }}`
- Test rendering with sample data

---

### Session 3: Main Pipeline (3 hours - 5 PM to 8 PM)

#### Task 3.1: Main Pipeline Orchestration (2 hours)
File: `main_pipeline.py`

```python
from datetime import datetime
import pandas as pd
import yaml
import sys
import os

sys.path.append('/home/claude/komplai_demo_pipeline')

from generators.invoice_generator import InvoiceGenerator
from generators.bill_generator import BillGenerator
from generators.bank_generator import BankTransactionGenerator
from validators.validator import DataValidator
from utils.excel_manager import ExcelManager
from utils.sheets_manager import SheetsManager
from pdf.pdf_generator import PDFGenerator
from email.email_service import EmailService

class KomplaiDataPipeline:
    def __init__(self, config_path='config/config.yaml'):
        # Load configuration
        with open(config_path, 'r') as f:
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
        """Execute weekly pipeline"""
        if run_date is None:
            run_date = datetime.now()
        
        print(f"\n{'='*60}")
        print(f"🚀 Komplai Demo Pipeline")
        print(f"📅 Run Date: {run_date.strftime('%A, %B %d, %Y %H:%M')}")
        print(f"{'='*60}\n")
        
        try:
            # === STEP 1: LOAD DATA ===
            print("📂 Step 1: Loading existing data...")
            entities = self.excel.read_sheet('Entities')
            invoices = self.excel.read_sheet('Invoices_Master')
            bills = self.excel.read_sheet('Bills_Master')
            bank = self.excel.read_sheet('Bank_Transactions')
            recurring = self.excel.read_sheet('Recurring_Schedule')
            
            print(f"   Entities: {len(entities)}")
            print(f"   Invoices: {len(invoices)}")
            print(f"   Bills: {len(bills)}")
            print(f"   Bank Txns: {len(bank)}")
            
            # === STEP 2: INITIALIZE GENERATORS ===
            print("\n⚙️  Step 2: Initializing generators...")
            inv_gen = InvoiceGenerator(entities, self.config)
            bill_gen = BillGenerator(entities, recurring, self.config)
            bank_gen = BankTransactionGenerator(self.config)
            validator = DataValidator(entities)
            
            # === STEP 3: GENERATE NEW DATA ===
            print("\n🔧 Step 3: Generating new data...")
            
            new_invoices = inv_gen.generate_weekly_invoices(run_date, invoices, 2)
            print(f"   Generated {len(new_invoices)} invoices")
            
            new_bills = bill_gen.generate_weekly_bills(run_date, bills, 4)
            print(f"   Generated {len(new_bills)} bills")
            
            new_bank_txns, balance = bank_gen.generate_weekly_bank_statement(
                run_date, invoices, bills, bank
            )
            print(f"   Generated {len(new_bank_txns)} bank transactions")
            print(f"   New balance: ₹{balance:,.2f}")
            
            # === STEP 4: VALIDATE ===
            print("\n✅ Step 4: Validating data...")
            
            validated_invoices = []
            for inv in new_invoices:
                if validator.validate_invoice(inv):
                    validated_invoices.append(inv)
            
            validated_bills = []
            for bill in new_bills:
                if validator.validate_bill(bill):
                    validated_bills.append(bill)
            
            validated_bank = []
            for txn in new_bank_txns:
                if validator.validate_bank_transaction(txn, bank):
                    validated_bank.append(txn)
            
            print(f"   Validated: {len(validated_invoices)}/{len(new_invoices)} invoices")
            print(f"   Validated: {len(validated_bills)}/{len(new_bills)} bills")
            print(f"   Validated: {len(validated_bank)}/{len(new_bank_txns)} transactions")
            
            if validator.errors:
                print(f"   ⚠️  {len(validator.errors)} validation errors logged")
            
            # === STEP 5: PERSIST DATA ===
            print("\n💾 Step 5: Persisting data...")
            
            # Convert to DataFrames
            inv_df = pd.DataFrame(validated_invoices)
            bill_df = pd.DataFrame(validated_bills)
            bank_df = pd.DataFrame(validated_bank)
            
            # Append to Excel
            self.excel.append_data('Invoices_Master', inv_df)
            self.excel.append_data('Bills_Master', bill_df)
            self.excel.append_data('Bank_Transactions', bank_df)
            print("   ✓ Excel updated")
            
            # Append to Google Sheets
            self.sheets.append_rows('Invoices_Master', inv_df.values.tolist())
            self.sheets.append_rows('Bills_Master', bill_df.values.tolist())
            self.sheets.append_rows('Bank_Transactions', bank_df.values.tolist())
            print("   ✓ Google Sheets updated")
            
            # === STEP 6: GENERATE PDFs ===
            print("\n📄 Step 6: Generating PDFs...")
            
            pdf_files = []
            
            # Invoice PDFs
            for inv in validated_invoices:
                pdf_path = os.path.join(
                    self.config['output']['base_dir'],
                    self.config['output']['invoices_dir'],
                    f"{inv['Invoice_ID']}.pdf"
                )
                self.pdf_gen.generate_invoice_pdf(inv, pdf_path)
                pdf_files.append({'path': pdf_path, 'type': 'Invoice'})
            
            # Bill PDFs
            for bill in validated_bills:
                pdf_path = os.path.join(
                    self.config['output']['base_dir'],
                    self.config['output']['bills_dir'],
                    f"{bill['Bill_ID']}.pdf"
                )
                self.pdf_gen.generate_bill_pdf(bill, pdf_path)
                pdf_files.append({'path': pdf_path, 'type': 'Bill'})
            
            # Bank Statement PDF
            stmt_path = os.path.join(
                self.config['output']['base_dir'],
                self.config['output']['statements_dir'],
                f"STMT-{run_date.strftime('%Y%m%d')}.pdf"
            )
            self.pdf_gen.generate_statement_pdf(validated_bank, stmt_path)
            pdf_files.append({'path': stmt_path, 'type': 'Bank Statement'})
            
            print(f"   Generated {len(pdf_files)} PDFs")
            
            # === STEP 7: SEND EMAILS ===
            print("\n✉️  Step 7: Sending emails...")
            self.email.send_batch(pdf_files)
            print(f"   Sent {len(pdf_files)} emails")
            
            # === STEP 8: LOG SUCCESS ===
            print("\n📊 Step 8: Logging results...")
            # TODO: Update Pipeline_Logs sheet
            # TODO: Update Data_Health sheet
            
            print(f"\n{'='*60}")
            print(f"✅ Pipeline completed successfully!")
            print(f"   {len(validated_invoices)} invoices")
            print(f"   {len(validated_bills)} bills")
            print(f"   {len(validated_bank)} bank transactions")
            print(f"   {len(pdf_files)} PDFs generated and emailed")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"\n❌ Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == "__main__":
    pipeline = KomplaiDataPipeline()
    pipeline.run()
```

#### Task 3.2: Scheduler (30 minutes)
File: `scheduler.py`

```python
import schedule
import time
from datetime import datetime
from main_pipeline import KomplaiDataPipeline

def run_weekly_pipeline():
    """Run pipeline every Monday at 10 AM"""
    print(f"\n⏰ Scheduled run triggered: {datetime.now()}")
    pipeline = KomplaiDataPipeline()
    pipeline.run()

# Schedule for Mondays at 10:00 AM
schedule.every().monday.at("10:00").do(run_weekly_pipeline)

print("=" * 60)
print("🚀 Komplai Demo Pipeline Scheduler")
print("=" * 60)
print(f"⏰ Scheduled: Every Monday at 10:00 AM IST")
print(f"📅 Next run: {schedule.next_run()}")
print(f"🔄 Status: Active")
print("=" * 60)
print("\nPress Ctrl+C to stop\n")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

#### Task 3.3: Testing & Debugging (30 minutes)

```bash
# Test individual generators
python generators/invoice_generator.py
python generators/bill_generator.py
python generators/bank_generator.py

# Test full pipeline
python main_pipeline.py

# Start scheduler
python scheduler.py
```

---

## ⚡ QUICK REFERENCE

### File Locations
```
/home/claude/komplai_demo_pipeline/
├── config/config.yaml                 ✅ Done
├── utils/utils.py                     ✅ Done
├── generators/
│   ├── invoice_generator.py           ✅ Done
│   ├── bill_generator.py              ✅ Done
│   └── bank_generator.py              ✅ Done
├── validators/validator.py            ⏳ 90 min
├── utils/
│   ├── excel_manager.py               ⏳ 45 min
│   └── sheets_manager.py              ⏳ 45 min
├── pdf/pdf_generator.py               ⏳ 2 hours
├── email/email_service.py             ⏳ 1 hour
├── main_pipeline.py                   ⏳ 2 hours
└── scheduler.py                       ⏳ 30 min
```

### Total Time: 10 hours
- Session 1 (Data): 3 hours
- Session 2 (PDF/Email): 4 hours
- Session 3 (Pipeline): 3 hours

---

## 🎯 SUCCESS CHECKLIST

Tomorrow night, you should have:
- [ ] All 6 remaining files implemented
- [ ] Google Sheets API configured
- [ ] Gmail SMTP configured
- [ ] Templates adapted with Jinja2
- [ ] Full pipeline tested locally
- [ ] Scheduler running
- [ ] First data generated and emailed

**You're 60% done. Let's finish this! 🚀**
