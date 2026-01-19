"""
Komplai Demo Pipeline - Bank Transaction Generator
Generates bank transactions with 95% reconciliation and 5% anomalies
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import sys
sys.path.append('/home/user/demo-dummy-data')

from utils import (
    generate_transaction_id,
    set_seed,
    generate_payment_reference,
    week_contains_date,
    get_25th_of_month
)


class BankTransactionGenerator:
    """Generate bank transactions with realistic reconciliation patterns"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.exchange_rate = config['pipeline']['base_exchange_rate']
        self.anomaly_rate = config['pipeline']['anomaly_rate']
    
    def generate_weekly_bank_statement(self,
                                      run_date: datetime,
                                      invoices_df: pd.DataFrame,
                                      bills_df: pd.DataFrame,
                                      bank_df: pd.DataFrame) -> Tuple[List[Dict], float]:
        """
        Generate bank transactions for the week ending on run_date

        Returns:
            (transactions, ending_balance)
        """
        # Set seed for deterministic randomness
        set_seed(run_date)

        # Define week boundaries for PREVIOUS week
        # If run_date is Monday Jan 13, previous week is Mon Jan 6 - Sun Jan 12
        week_start = run_date - timedelta(days=7)  # Previous Monday
        week_end = run_date - timedelta(days=1)    # Previous Sunday
        
        # Get last bank balance
        if len(bank_df) > 0:
            last_balance = bank_df.iloc[-1]['Running_Balance']
            last_txn_id = bank_df.iloc[-1]['Transaction_ID']
            start_seq = int(last_txn_id.replace('TXN', '')) + 1
        else:
            last_balance = 25000000.0  # Starting balance
            start_seq = 1
        
        running_balance = last_balance
        transactions = []
        
        # Step 1: Generate receipts (from invoices due in this week)
        receipts = self._generate_receipts(
            invoices_df, week_start, week_end, running_balance, start_seq
        )
        transactions.extend(receipts)
        
        # Update running balance and sequence
        if receipts:
            running_balance = receipts[-1]['Running_Balance']
            start_seq = int(receipts[-1]['Transaction_ID'].replace('TXN', '')) + 1
        
        # Step 2: Generate payments (bills paid on 25th if within week)
        payments = self._generate_payments(
            bills_df, week_start, week_end, run_date, running_balance, start_seq
        )
        transactions.extend(payments)
        
        # Update running balance and sequence
        if payments:
            running_balance = payments[-1]['Running_Balance']
            start_seq = int(payments[-1]['Transaction_ID'].replace('TXN', '')) + 1
        
        # Step 3: Inject anomalies (5% of expected transactions)
        total_expected_txns = len(receipts) + len(payments)
        anomaly_count = max(1, int(total_expected_txns * self.anomaly_rate / 2))  # 2.5% for orphaned
        
        anomalies = self._generate_anomalies(
            anomaly_count, week_start, week_end, running_balance, start_seq
        )
        
        # Insert anomalies at random positions
        for anomaly in anomalies:
            transactions.append(anomaly)
            running_balance = anomaly['Running_Balance']
        
        # Sort all transactions by date
        transactions.sort(key=lambda x: (x['Transaction_Date'], x['Transaction_ID']))
        
        # Recalculate running balances in chronological order
        current_balance = last_balance
        for txn in transactions:
            if txn['Transaction_Type'] in ['Receipt', 'Opening']:
                current_balance += txn['Credit']
            else:  # Payment
                current_balance -= txn['Debit']
            
            txn['Running_Balance'] = round(current_balance, 2)
        
        return transactions, current_balance
    
    def _generate_receipts(self, 
                          invoices_df: pd.DataFrame,
                          week_start: datetime,
                          week_end: datetime,
                          starting_balance: float,
                          start_seq: int) -> List[Dict]:
        """Generate receipt transactions from invoices"""
        receipts = []
        
        # Get invoices due in this week (invoice_date + payment_terms ± variance)
        due_invoices = self._get_invoices_due_in_week(invoices_df, week_start, week_end)
        
        current_balance = starting_balance
        seq = start_seq
        
        for invoice in due_invoices:
            # 97.5% probability of receipt (2.5% will be missing for anomalies)
            if random.random() < 0.975:
                # Calculate receipt date with variance
                due_date = pd.to_datetime(invoice['Due_Date'])
                variance_days = random.randint(-3, 3)  # ±3 days
                receipt_date = due_date + timedelta(days=variance_days)
                
                # Ensure receipt is within the week
                if not (week_start <= receipt_date <= week_end):
                    receipt_date = week_start + timedelta(days=random.randint(0, 6))
                
                # Calculate receipt amount
                invoice_amount = invoice['Total_Amount']
                currency = invoice['Currency']
                
                # Handle withholding tax for USD customers
                if currency == 'USD':
                    # 30% withholding tax applied
                    receipt_amount = invoice_amount * 0.70 * self.exchange_rate
                else:
                    receipt_amount = invoice_amount
                
                # Create receipt transaction
                txn = {
                    'Transaction_ID': generate_transaction_id(seq),
                    'Transaction_Date': receipt_date,
                    'Description': f"Payment from {invoice['Customer_Name']}",
                    'Reference_Number': invoice['Invoice_ID'],
                    'Entity_Name': invoice['Customer_Name'],
                    'Transaction_Type': 'Receipt',
                    'Currency': 'INR',  # Bank account is INR
                    'Debit': 0.0,
                    'Credit': round(receipt_amount, 2),
                    'Running_Balance': round(current_balance + receipt_amount, 2),
                    'Bank_Account': 'HDFC Bank Current Account',
                    'Reconciliation_Status': 'Matched',
                    'Notes': f'Payment received for invoice {invoice["Invoice_ID"]}'
                }
                
                current_balance = txn['Running_Balance']
                receipts.append(txn)
                seq += 1
        
        return receipts
    
    def _generate_payments(self,
                          bills_df: pd.DataFrame,
                          week_start: datetime,
                          week_end: datetime,
                          run_date: datetime,
                          starting_balance: float,
                          start_seq: int) -> List[Dict]:
        """Generate payment transactions for bills (paid on 25th)"""
        payments = []
        
        # Check if 25th falls within this week
        if not week_contains_date(week_start, week_end, 25):
            return payments
        
        # Get bills due for payment this month
        payment_date = get_25th_of_month(run_date)
        
        # Get bills from previous month(s) that should be paid
        bills_for_payment = self._get_bills_for_payment(bills_df, run_date)
        
        current_balance = starting_balance
        seq = start_seq
        
        for bill in bills_for_payment:
            # 97.5% probability of payment (2.5% will be skipped for anomalies)
            if random.random() < 0.975:
                # Payment amount is Net_Payable (after TDS deduction)
                payment_amount = bill['Net_Payable']
                
                # Convert to INR if USD
                if bill['Currency'] == 'USD':
                    payment_amount = payment_amount * self.exchange_rate
                
                # Create payment transaction
                txn = {
                    'Transaction_ID': generate_transaction_id(seq),
                    'Transaction_Date': payment_date,
                    'Description': f"Payment to {bill['Vendor_Name']}",
                    'Reference_Number': bill['Bill_ID'],
                    'Entity_Name': bill['Vendor_Name'],
                    'Transaction_Type': 'Payment',
                    'Currency': 'INR',
                    'Debit': round(payment_amount, 2),
                    'Credit': 0.0,
                    'Running_Balance': round(current_balance - payment_amount, 2),
                    'Bank_Account': 'HDFC Bank Current Account',
                    'Reconciliation_Status': 'Matched',
                    'Notes': f'Payment made for bill {bill["Bill_ID"]}'
                }
                
                current_balance = txn['Running_Balance']
                payments.append(txn)
                seq += 1
        
        return payments
    
    def _generate_anomalies(self,
                           count: int,
                           week_start: datetime,
                           week_end: datetime,
                           starting_balance: float,
                           start_seq: int) -> List[Dict]:
        """
        Generate anomaly transactions (orphaned payments)
        These are bank transactions with no matching invoice/bill
        """
        anomalies = []
        
        current_balance = starting_balance
        seq = start_seq
        
        for i in range(count):
            # Random date within week
            days_offset = random.randint(0, 6)
            txn_date = week_start + timedelta(days=days_offset)
            
            # Generate orphaned payment (no matching bill)
            amount = random.uniform(5000, 50000)
            
            txn = {
                'Transaction_ID': generate_transaction_id(seq + i),
                'Transaction_Date': txn_date,
                'Description': f"NEFT/{generate_payment_reference()}",
                'Reference_Number': None,
                'Entity_Name': 'Unknown Vendor',
                'Transaction_Type': 'Payment',
                'Currency': 'INR',
                'Debit': round(amount, 2),
                'Credit': 0.0,
                'Running_Balance': round(current_balance - amount, 2),
                'Bank_Account': 'HDFC Bank Current Account',
                'Reconciliation_Status': 'Unmatched',  # KEY: This is unmatched
                'Notes': 'Orphaned transaction - no matching bill found'
            }
            
            current_balance = txn['Running_Balance']
            anomalies.append(txn)
        
        return anomalies
    
    def _get_invoices_due_in_week(self,
                                  invoices_df: pd.DataFrame,
                                  week_start: datetime,
                                  week_end: datetime) -> List[Dict]:
        """Get invoices whose payment is due in this week"""
        due_invoices = []
        
        for _, invoice in invoices_df.iterrows():
            due_date = pd.to_datetime(invoice['Due_Date'])
            
            # Check if due date falls within week (with ±3 day variance)
            earliest_payment = due_date - timedelta(days=3)
            latest_payment = due_date + timedelta(days=3)
            
            # If there's any overlap with the week, include it
            if (earliest_payment <= week_end and latest_payment >= week_start):
                due_invoices.append(invoice.to_dict())
        
        return due_invoices
    
    def _get_bills_for_payment(self,
                               bills_df: pd.DataFrame,
                               run_date: datetime) -> List[Dict]:
        """Get bills that should be paid on the 25th of this month"""
        # Get bills from previous month(s) that are due
        current_month = run_date.month
        current_year = run_date.year
        
        # Pay bills from previous month
        if current_month == 1:
            target_month = 12
            target_year = current_year - 1
        else:
            target_month = current_month - 1
            target_year = current_year
        
        bills_to_pay = []
        
        for _, bill in bills_df.iterrows():
            bill_date = pd.to_datetime(bill['Bill_Date'])
            
            # Pay bills from the previous month
            if bill_date.month == target_month and bill_date.year == target_year:
                bills_to_pay.append(bill.to_dict())
        
        return bills_to_pay


if __name__ == "__main__":
    # Test bank transaction generator
    import sys
    
    # Load test data
    xl = pd.ExcelFile('/mnt/user-data/uploads/Komplai_Demo_Master__Claude_.xlsx')
    invoices = pd.read_excel(xl, 'Invoices_Master')
    bills = pd.read_excel(xl, 'Bills_Master')
    bank = pd.read_excel(xl, 'Bank_Transactions')
    
    # Test config
    config = {
        'pipeline': {
            'base_exchange_rate': 85.0,
            'anomaly_rate': 0.05
        }
    }
    
    # Create generator
    gen = BankTransactionGenerator(config)
    
    # Generate test transactions
    test_date = datetime(2026, 1, 6)  # Monday
    new_txns, ending_balance = gen.generate_weekly_bank_statement(
        test_date, invoices, bills, bank
    )
    
    print(f"Generated {len(new_txns)} bank transactions:")
    print(f"Ending balance: ₹{ending_balance:,.2f}")
    print("\nSample transactions:")
    
    for txn in new_txns[:5]:
        print(f"\n{txn['Transaction_ID']} - {txn['Transaction_Date'].strftime('%Y-%m-%d')}")
        print(f"  Type: {txn['Transaction_Type']}")
        print(f"  Entity: {txn['Entity_Name']}")
        print(f"  Amount: ₹{txn['Debit'] if txn['Debit'] > 0 else txn['Credit']:,.2f}")
        print(f"  Status: {txn['Reconciliation_Status']}")
        print(f"  Balance: ₹{txn['Running_Balance']:,.2f}")
