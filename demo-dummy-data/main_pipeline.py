"""
Komplai Demo Pipeline - Main Orchestrator
Coordinates all components to generate weekly demo data
"""

import yaml
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict
import sys
import os

# Import all modules
from excel_manager import ExcelManager
from sheets_manager import SheetsManager
from invoice_generator import InvoiceGenerator
from bill_generator import BillGenerator
from bank_generator import BankTransactionGenerator
from pdf_generator import PDFGenerator
from email_sender import GmailEmailSender


class DemoPipeline:
    """Main pipeline orchestrator"""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize pipeline with configuration"""
        print("\n" + "="*70)
        print("  KOMPLAI DEMO DATA PIPELINE")
        print("="*70)

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Check if running in cloud mode (use Google Sheets as primary data source)
        self.cloud_mode = os.environ.get('CLOUD_MODE', 'false').lower() == 'true'
        if self.cloud_mode:
            print(f"\n✓ Running in CLOUD MODE (Google Sheets as data source)")

        print(f"✓ Loaded configuration from {config_path}")
        self._initialize_components()

    def _initialize_components(self):
        """Initialize all pipeline components"""
        print("\n[Initializing Components]")

        # Initialize Excel Manager (skip in cloud mode)
        if not self.cloud_mode:
            excel_path = self.config['data_sources']['excel_path']
            if not os.path.exists(excel_path):
                excel_path = "Komplai_Demo_Master (Claude).xlsx"

            self.excel = ExcelManager(excel_path)
            print(f"✓ Excel Manager: {excel_path}")
        else:
            self.excel = None
            print(f"⏭ Excel Manager: Skipped (cloud mode)")

        # Initialize Google Sheets Manager
        try:
            credentials_path = self.config['data_sources'].get('google_credentials')
            if credentials_path and not os.path.exists(credentials_path):
                credentials_path = "dummy-data-483609-2b5f128b43ad.json"

            sheet_id = self.config['data_sources']['google_sheet_id']
            self.sheets = SheetsManager(credentials_path, sheet_id)
            self.sheets_enabled = True
            print(f"✓ Google Sheets Manager")
        except Exception as e:
            print(f"⚠ Google Sheets Manager disabled: {e}")
            self.sheets = None
            self.sheets_enabled = False
            if self.cloud_mode:
                raise Exception("Cloud mode requires Google Sheets to be enabled")

        # PDF Generator (optional - may fail on Mac without GTK libraries)
        try:
            output_dir = self.config.get('output', {}).get('base_dir', './output')
            self.pdf_gen = PDFGenerator(output_dir=f"{output_dir}/pdfs")
            self.pdf_enabled = True
            print(f"✓ PDF Generator: {output_dir}/pdfs")
        except Exception as e:
            print(f"⚠ PDF Generator disabled: {e}")
            print(f"  (Pipeline will still generate data and save to Excel)")
            self.pdf_gen = None
            self.pdf_enabled = False

        # Email Sender (optional - requires SMTP_EMAIL and SMTP_PASSWORD env vars)
        try:
            self.email_sender = GmailEmailSender()
            self.email_enabled = True
            self.recipient_email = os.environ.get('RECIPIENT_EMAIL', 'demo.komplai@gmail.com')
            self.notification_email = os.environ.get('NOTIFICATION_EMAIL')
            print(f"✓ Email Sender: {self.recipient_email}")
            if self.notification_email:
                print(f"✓ Notifications: {self.notification_email}")
        except Exception as e:
            print(f"⚠ Email Sender disabled: {e}")
            self.email_sender = None
            self.email_enabled = False
            self.notification_email = None

    def run_weekly_generation(self, run_date: datetime = None) -> Dict:
        """Run complete weekly data generation"""
        if run_date is None:
            run_date = datetime.now()

        if run_date.weekday() != 0:
            print(f"⚠ Warning: {run_date.date()} is not a Monday")

        print(f"\n{'='*70}")
        print(f"  GENERATING DATA FOR WEEK OF {run_date.date()}")
        print(f"{'='*70}")

        results = {
            'run_date': run_date,
            'invoices_generated': 0,
            'bills_generated': 0,
            'transactions_generated': 0,
            'pdfs_generated': 0,
            'emails_sent': 0,
            'errors': []
        }

        try:
            # Step 1: Load existing data
            print("\n[Step 1/7] Loading existing data...")
            if self.cloud_mode:
                # Read from Google Sheets in cloud mode
                entities = self.sheets.read_sheet('Entities')
                invoices = self.sheets.read_sheet('Invoices_Master')
                bills = self.sheets.read_sheet('Bills_Master')
                bank = self.sheets.read_sheet('Bank_Transactions')
                recurring = self.sheets.read_sheet('Recurring_Schedule')
            else:
                # Read from Excel in local mode
                entities = self.excel.read_sheet('Entities')
                invoices = self.excel.read_sheet('Invoices_Master')
                bills = self.excel.read_sheet('Bills_Master')
                bank = self.excel.read_sheet('Bank_Transactions')
                recurring = self.excel.read_sheet('Recurring_Schedule')

            # Step 2: Generate invoices
            print(f"\n[Step 2/7] Generating invoices...")
            inv_gen = InvoiceGenerator(entities, self.config)
            invoices_per_week = self.config['pipeline']['invoices_per_week']
            new_invoices = inv_gen.generate_weekly_invoices(run_date, invoices, count=invoices_per_week)
            results['invoices_generated'] = len(new_invoices)
            print(f"✓ Generated {len(new_invoices)} invoices")

            # Step 3: Generate bills
            print(f"\n[Step 3/7] Generating bills...")
            bill_gen = BillGenerator(entities, recurring, self.config)
            bills_per_week = self.config['pipeline']['bills_per_week']
            new_bills = bill_gen.generate_weekly_bills(run_date, bills, count=bills_per_week)
            results['bills_generated'] = len(new_bills)
            print(f"✓ Generated {len(new_bills)} bills")

            # Step 4: Generate bank transactions
            print(f"\n[Step 4/7] Generating bank transactions...")
            bank_gen = BankTransactionGenerator(self.config)
            all_invoices = pd.concat([invoices, pd.DataFrame(new_invoices)], ignore_index=True)
            all_bills = pd.concat([bills, pd.DataFrame(new_bills)], ignore_index=True)

            new_transactions, ending_balance = bank_gen.generate_weekly_bank_statement(
                run_date, all_invoices, all_bills, bank
            )
            results['transactions_generated'] = len(new_transactions)
            print(f"✓ Generated {len(new_transactions)} transactions")
            print(f"  Ending Balance: ₹{ending_balance:,.2f}")

            # Step 5: Save data
            print(f"\n[Step 5/7] Saving data...")

            if not self.cloud_mode and self.excel:
                # Save to Excel in local mode
                self.excel.append_to_sheet('Invoices_Master', new_invoices)
                self.excel.append_to_sheet('Bills_Master', new_bills)
                self.excel.append_to_sheet('Bank_Transactions', new_transactions)
                print(f"✓ Saved to Excel")

            if self.sheets_enabled:
                try:
                    print(f"  Syncing to Google Sheets...")
                    self.sheets.append_to_sheet('Invoices_Master', new_invoices)
                    self.sheets.append_to_sheet('Bills_Master', new_bills)
                    self.sheets.append_to_sheet('Bank_Transactions', new_transactions)
                    print(f"  ✓ Synced to Google Sheets")
                except Exception as e:
                    print(f"  ⚠ Google Sheets sync failed: {e}")
                    results['errors'].append(f"Sheets sync: {e}")

            # Step 6: Generate PDFs (if enabled)
            generated_invoice_pdfs = []
            generated_bill_pdfs = []

            if self.pdf_enabled:
                print(f"\n[Step 6/7] Generating PDFs...")
                pdf_count = 0
                output_dir = self.config.get('output', {}).get('base_dir', './output')

                for invoice in new_invoices:
                    try:
                        pdf_data = self._prepare_invoice_pdf_data(invoice)
                        filename = f"{invoice['Invoice_ID']}.pdf"
                        self.pdf_gen.generate_invoice_pdf(pdf_data, filename)
                        pdf_path = os.path.join(output_dir, 'pdfs', filename)
                        generated_invoice_pdfs.append((invoice, pdf_path))
                        pdf_count += 1
                    except Exception as e:
                        print(f"  ⚠ Failed PDF for {invoice['Invoice_ID']}: {e}")
                        results['errors'].append(f"Invoice PDF {invoice['Invoice_ID']}: {e}")

                for bill in new_bills:
                    try:
                        pdf_data = self._prepare_bill_pdf_data(bill)
                        filename = f"{bill['Bill_ID']}.pdf"
                        self.pdf_gen.generate_bill_pdf(pdf_data, filename)
                        pdf_path = os.path.join(output_dir, 'pdfs', filename)
                        generated_bill_pdfs.append((bill, pdf_path))
                        pdf_count += 1
                    except Exception as e:
                        print(f"  ⚠ Failed PDF for {bill['Bill_ID']}: {e}")
                        results['errors'].append(f"Bill PDF {bill['Bill_ID']}: {e}")

                results['pdfs_generated'] = pdf_count
                print(f"✓ Generated {pdf_count} PDFs")
            else:
                print(f"\n[Step 6/7] Skipping PDF generation (not available)")
                results['pdfs_generated'] = 0

            # Step 7: Send emails with PDFs (if enabled)
            if self.email_enabled and (generated_invoice_pdfs or generated_bill_pdfs):
                print(f"\n[Step 7/7] Sending emails...")
                email_count = 0

                for invoice, pdf_path in generated_invoice_pdfs:
                    try:
                        success = self.email_sender.send_invoice_email(
                            recipient=self.recipient_email,
                            invoice_id=invoice['Invoice_ID'],
                            customer_name=invoice['Customer_Name'],
                            amount=invoice['Total_Amount'],
                            currency=invoice['Currency'],
                            pdf_path=pdf_path
                        )
                        if success:
                            email_count += 1
                    except Exception as e:
                        print(f"  ⚠ Failed email for {invoice['Invoice_ID']}: {e}")
                        results['errors'].append(f"Invoice email {invoice['Invoice_ID']}: {e}")

                for bill, pdf_path in generated_bill_pdfs:
                    try:
                        success = self.email_sender.send_bill_email(
                            recipient=self.recipient_email,
                            bill_id=bill['Bill_ID'],
                            vendor_name=bill['Vendor_Name'],
                            amount=bill['Total_Amount'],
                            currency=bill['Currency'],
                            pdf_path=pdf_path
                        )
                        if success:
                            email_count += 1
                    except Exception as e:
                        print(f"  ⚠ Failed email for {bill['Bill_ID']}: {e}")
                        results['errors'].append(f"Bill email {bill['Bill_ID']}: {e}")

                results['emails_sent'] = email_count
                print(f"✓ Sent {email_count} emails to {self.recipient_email}")
            else:
                print(f"\n[Step 7/7] Skipping email sending (not available or no PDFs)")
                results['emails_sent'] = 0

            # Biweekly bank statement (every 2nd week based on ISO week number)
            week_num = run_date.isocalendar()[1]
            is_biweekly = (week_num % 2 == 0)

            if is_biweekly and self.pdf_enabled and self.email_enabled:
                print(f"\n[Biweekly] Generating bank statement (Week {week_num})...")
                try:
                    statement_pdf_path = self._generate_bank_statement_pdf(run_date, bank)
                    if statement_pdf_path:
                        # Calculate statement period (last 2 weeks)
                        end_date = run_date
                        start_date = run_date - timedelta(days=14)
                        statement_period = f"{start_date.strftime('%d %b')} - {end_date.strftime('%d %b %Y')}"

                        success = self.email_sender.send_bank_statement_email(
                            recipient=self.recipient_email,
                            statement_period=statement_period,
                            pdf_path=statement_pdf_path
                        )
                        if success:
                            results['bank_statement_sent'] = True
                            print(f"✓ Bank statement sent to {self.recipient_email}")
                except Exception as e:
                    print(f"⚠ Failed to generate/send bank statement: {e}")
                    results['errors'].append(f"Bank statement: {e}")
            elif is_biweekly:
                print(f"\n[Biweekly] Week {week_num} - Skipping bank statement (PDF/email not available)")

        except Exception as e:
            print(f"\n✗ Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            results['errors'].append(f"Pipeline error: {e}")

        self._print_summary(results)

        # Send notification email if configured
        if self.email_enabled and self.notification_email:
            try:
                print(f"\n[Sending notification to {self.notification_email}]")
                self.email_sender.send_pipeline_summary(self.notification_email, results)
            except Exception as e:
                print(f"⚠ Failed to send notification: {e}")

        return results

    def _prepare_invoice_pdf_data(self, invoice: Dict) -> Dict:
        """Prepare invoice data for PDF"""
        line_items = []
        for i in range(1, 4):
            if invoice.get(f'Line_Item_{i}_Description'):
                line_items.append({
                    'description': invoice[f'Line_Item_{i}_Description'],
                    'quantity': invoice[f'Line_Item_{i}_Quantity'],
                    'rate': invoice[f'Line_Item_{i}_Rate'],
                    'amount': invoice[f'Line_Item_{i}_Amount']
                })

        return {
            'invoice_id': invoice['Invoice_ID'],
            'invoice_date': invoice['Invoice_Date'].strftime('%Y-%m-%d') if hasattr(invoice['Invoice_Date'], 'strftime') else str(invoice['Invoice_Date']),
            'due_date': invoice['Due_Date'].strftime('%Y-%m-%d') if hasattr(invoice['Due_Date'], 'strftime') else str(invoice['Due_Date']),
            'customer_name': invoice['Customer_Name'],
            'customer_address': invoice['Customer_Address'],
            'customer_tax_id': invoice['Customer_Tax_ID'],
            'currency': invoice['Currency'],
            'line_items': line_items,
            'subtotal': invoice['Subtotal'],
            'tax_type': invoice['Tax_Type'],
            'tax_rate': invoice['Tax_Rate'],
            'tax_amount': invoice['Tax_Amount'],
            'total_amount': invoice['Total_Amount'],
            'notes': invoice.get('Notes', '')
        }

    def _prepare_bill_pdf_data(self, bill: Dict) -> Dict:
        """Prepare bill data for PDF"""
        line_items = []
        for i in range(1, 3):
            if bill.get(f'Line_Item_{i}_Description'):
                line_items.append({
                    'description': bill[f'Line_Item_{i}_Description'],
                    'quantity': bill[f'Line_Item_{i}_Quantity'],
                    'rate': bill[f'Line_Item_{i}_Rate'],
                    'amount': bill[f'Line_Item_{i}_Amount']
                })

        return {
            'bill_id': bill['Bill_ID'],
            'bill_date': bill['Bill_Date'].strftime('%Y-%m-%d') if hasattr(bill['Bill_Date'], 'strftime') else str(bill['Bill_Date']),
            'due_date': bill['Due_Date'].strftime('%Y-%m-%d') if hasattr(bill['Due_Date'], 'strftime') else str(bill['Due_Date']),
            'vendor_name': bill['Vendor_Name'],
            'vendor_address': bill['Vendor_Address'],
            'vendor_tax_id': bill['Vendor_Tax_ID'],
            'currency': bill['Currency'],
            'line_items': line_items,
            'subtotal': bill['Subtotal'],
            'tax_type': bill['Tax_Type'],
            'tax_rate': bill['Tax_Rate'],
            'tax_amount': bill['Tax_Amount'],
            'total_amount': bill['Total_Amount'],
            'tds_applicable': bill['TDS_Applicable'],
            'tds_section': bill.get('TDS_Section'),
            'tds_amount': bill.get('TDS_Amount', 0),
            'net_payable': bill['Net_Payable'],
            'notes': bill.get('Notes', '')
        }

    def _generate_bank_statement_pdf(self, run_date: datetime, bank_df: pd.DataFrame) -> str:
        """Generate bank statement PDF for the last 2 weeks"""
        # Filter transactions for the last 2 weeks
        end_date = run_date
        start_date = run_date - timedelta(days=14)

        # Convert Transaction_Date to datetime if needed
        if len(bank_df) > 0:
            if not pd.api.types.is_datetime64_any_dtype(bank_df['Transaction_Date']):
                bank_df['Transaction_Date'] = pd.to_datetime(bank_df['Transaction_Date'])

            # Filter transactions in the date range
            mask = (bank_df['Transaction_Date'] >= start_date) & (bank_df['Transaction_Date'] <= end_date)
            period_transactions = bank_df[mask].copy()
        else:
            period_transactions = bank_df

        if len(period_transactions) == 0:
            print("  No transactions in the last 2 weeks")
            return None

        # Sort by date
        period_transactions = period_transactions.sort_values('Transaction_Date')

        # Prepare transaction list for template
        transactions = []
        for _, txn in period_transactions.iterrows():
            txn_date = txn['Transaction_Date']
            if hasattr(txn_date, 'strftime'):
                date_str = txn_date.strftime('%Y-%m-%d')
            else:
                date_str = str(txn_date)

            transactions.append({
                'date': date_str,
                'description': txn.get('Description', txn.get('Narration', '')),
                'debit': float(txn.get('Debit', 0) or 0),
                'credit': float(txn.get('Credit', 0) or 0),
                'balance': float(txn.get('Balance', 0) or 0)
            })

        # Get opening and closing balance
        opening_balance = float(period_transactions.iloc[0].get('Balance', 0) or 0)
        closing_balance = float(period_transactions.iloc[-1].get('Balance', 0) or 0)

        # Adjust opening balance (subtract first transaction)
        first_txn = period_transactions.iloc[0]
        first_debit = float(first_txn.get('Debit', 0) or 0)
        first_credit = float(first_txn.get('Credit', 0) or 0)
        opening_balance = opening_balance + first_debit - first_credit

        # Prepare statement data
        statement_data = {
            'bank_name': 'HDFC Bank',
            'account_name': 'Acme Technologies Private Limited',
            'account_number': 'XXXX XXXX 5678',
            'ifsc_code': 'HDFC0001234',
            'start_date': start_date.strftime('%d %b %Y'),
            'end_date': end_date.strftime('%d %b %Y'),
            'transactions': transactions,
            'opening_balance': opening_balance,
            'closing_balance': closing_balance
        }

        # Generate PDF
        filename = f"Bank_Statement_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.pdf"
        output_path = self.pdf_gen.generate_statement_pdf(statement_data, filename)

        return output_path

    def _print_summary(self, results: Dict):
        """Print pipeline execution summary"""
        print(f"\n{'='*70}")
        print("  PIPELINE SUMMARY")
        print(f"{'='*70}")
        print(f"\n✓ Run Date: {results['run_date'].date()}")
        print(f"✓ Invoices Generated: {results['invoices_generated']}")
        print(f"✓ Bills Generated: {results['bills_generated']}")
        print(f"✓ Transactions Generated: {results['transactions_generated']}")

        if results['pdfs_generated'] > 0:
            print(f"✓ PDFs Generated: {results['pdfs_generated']}")
        else:
            print(f"⏭  PDFs: Skipped (WeasyPrint not available)")

        if results['emails_sent'] > 0:
            print(f"✓ Emails Sent: {results['emails_sent']}")
        else:
            print(f"⏭  Emails: Skipped (not configured or no PDFs)")

        if results.get('bank_statement_sent'):
            print(f"✓ Bank Statement: Sent (biweekly)")

        if results['errors']:
            print(f"\n⚠ Errors ({len(results['errors'])}):")
            for error in results['errors']:
                print(f"  - {error}")
        else:
            print(f"\n✓ No errors")

        print(f"\n{'='*70}\n")


if __name__ == "__main__":
    pipeline = DemoPipeline()
    # Use current date - generators will create dates for the previous week
    run_date = datetime.now()
    results = pipeline.run_weekly_generation(run_date)
    sys.exit(0 if not results['errors'] else 1)
