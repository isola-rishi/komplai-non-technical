"""
Komplai Demo Pipeline - Bill Generator
Generates vendor bills with TDS/withholding tax and prepaid expense handling
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import sys
sys.path.append('/home/user/demo-dummy-data')

from utils import (
    generate_bill_id,
    set_seed,
    format_date_for_service_period,
    calculate_igst,
    calculate_sales_tax,
    calculate_tds,
    get_tds_section_for_expense,
    apply_variance,
    is_prepaid_expense,
    extract_service_period,
    calculate_monthly_amount,
    format_indian_date
)


class BillGenerator:
    """Generate realistic vendor bills with TDS and prepaid expense handling"""
    
    def __init__(self, entities_df: pd.DataFrame, recurring_schedule_df: pd.DataFrame, config: Dict):
        self.entities = entities_df
        self.recurring_schedule = recurring_schedule_df
        self.config = config
        self.exchange_rate = config['pipeline']['base_exchange_rate']
        
        # Get vendors only
        self.vendors = entities_df[entities_df['Entity_Type'] == 'Vendor'].copy()
        
        # Identify recurring vendors (we need 10 total)
        self.recurring_vendors = self._identify_recurring_vendors()
        
        # Expense categories and their frequency weights (from historical data)
        self.expense_categories = {
            'Repairs and Maintenance': 7,
            'Software Subscriptions': 6,
            'Consultant Expense': 5,
            'Travel Expense': 4,
            'Cloud Hosting': 2,
            'Advertising And Marketing': 3,
            'Meals and Entertainment': 1
        }
        
        # Recurring expense categories (10 total)
        self.recurring_categories = {
            'Rent Expense': (75000, 5),  # (amount, day of month)
            'Telephone Expense': (5000, 15),
            'IT and Internet Expenses': (8700, 10),
            'Janitorial Expense': (6000, 20),
            'Software Subscriptions': (25000, 1),  # Office 365, etc.
            'Cloud Hosting': (50000, 5),  # AWS, Azure
            'Insurance Expense': (15000, 1),
            'Professional Services': (30000, 10),
            'Security Services': (12000, 15),
            'Utilities': (10000, 25)
        }
    
    def _identify_recurring_vendors(self) -> List[str]:
        """Identify 10 recurring vendors, use existing + add new"""
        # Get existing recurring vendors
        existing_recurring = self.entities[
            self.entities['Is_Recurring'] == True
        ]['Entity_ID'].tolist()
        
        # Need 10 total, add more if needed
        recurring_vendor_ids = existing_recurring[:10]  # Take first 10
        
        return recurring_vendor_ids
    
    def generate_weekly_bills(self, run_date: datetime,
                             last_bills: pd.DataFrame,
                             count: int = 4) -> List[Dict]:
        """
        Generate bills for the week
        Args:
            run_date: Monday of the week (pipeline runs on this date)
            last_bills: Existing bills dataframe
            count: Number of bills to generate (default 4)
        """
        # Set seed for deterministic randomness
        set_seed(run_date)

        # Get next bill sequence number
        start_seq = 1
        if len(last_bills) > 0:
            # Find the last valid Bill_ID (skip empty rows)
            for i in range(len(last_bills) - 1, -1, -1):
                last_id = last_bills.iloc[i]['Bill_ID']
                # Check if ID is valid (non-empty string with expected format)
                if last_id and isinstance(last_id, str) and '-' in last_id:
                    try:
                        last_seq = int(last_id.split('-')[-1])
                        start_seq = last_seq + 1
                        break
                    except ValueError:
                        continue  # Try previous row

        bills = []

        # Step 1: Check if any recurring bills are due this week
        recurring_bills = self._check_recurring_due(run_date)

        # Step 2: Generate one-time bills to fill remaining slots
        remaining_count = count - len(recurring_bills)
        one_time_bills = self._generate_one_time_bills(run_date, remaining_count)

        # Combine and assign sequence numbers
        all_bills = recurring_bills + one_time_bills

        for i, bill_data in enumerate(all_bills):
            # Generate bill for PREVIOUS week (run_date - 7 to run_date - 1)
            # Random day in the previous week
            days_back = random.randint(1, 7)
            bill_date = run_date - timedelta(days=days_back)

            bill = self._create_bill(
                vendor=bill_data['vendor'],
                bill_date=bill_date,
                sequence=start_seq + i,
                expense_account=bill_data['expense_account'],
                amount=bill_data['amount'],
                is_recurring=bill_data.get('is_recurring', False)
            )
            bills.append(bill)

        return bills
    
    def _check_recurring_due(self, run_date: datetime) -> List[Dict]:
        """Check which recurring vendors are due this week"""
        recurring_due = []
        
        # Determine which recurring expenses should be generated this week
        # Strategy: Rotate through 10 recurring vendors, max 2 per week
        
        week_num = run_date.isocalendar()[1]  # Week number of year
        
        # Use modulo to determine which recurring vendors to bill this week
        vendors_to_bill_indices = [(week_num * 2) % 10, (week_num * 2 + 1) % 10]
        
        recurring_categories_list = list(self.recurring_categories.keys())
        
        for idx in vendors_to_bill_indices:
            if idx < len(recurring_categories_list):
                category = recurring_categories_list[idx]
                amount, due_day = self.recurring_categories[category]
                
                # Find or create vendor for this category
                vendor = self._get_vendor_for_expense(category)
                
                recurring_due.append({
                    'vendor': vendor,
                    'expense_account': category,
                    'amount': amount,
                    'is_recurring': True
                })
        
        return recurring_due
    
    def _generate_one_time_bills(self, run_date: datetime, count: int) -> List[Dict]:
        """Generate one-time bills based on expense category weights"""
        one_time_bills = []
        
        # Select expense categories based on weights
        categories = list(self.expense_categories.keys())
        weights = list(self.expense_categories.values())
        
        selected_categories = random.choices(categories, weights=weights, k=count)
        
        for category in selected_categories:
            # Select vendor for this expense category
            vendor = self._get_vendor_for_expense(category)
            
            # Generate amount based on category
            amount = self._generate_amount_for_category(category)
            
            one_time_bills.append({
                'vendor': vendor,
                'expense_account': category,
                'amount': amount,
                'is_recurring': False
            })
        
        return one_time_bills
    
    def _get_vendor_for_expense(self, expense_account: str) -> pd.Series:
        """Get or select vendor appropriate for expense category"""
        # Try to find vendor that matches this expense type
        # For now, randomly select from vendors
        return self.vendors.sample(n=1).iloc[0]
    
    def _generate_amount_for_category(self, category: str) -> float:
        """Generate realistic amount based on expense category"""
        # Base amounts for different categories
        category_ranges = {
            'Repairs and Maintenance': (10000, 50000),
            'Software Subscriptions': (5000, 30000),
            'Consultant Expense': (30000, 100000),
            'Travel Expense': (5000, 25000),
            'Cloud Hosting': (10000, 50000),
            'Advertising And Marketing': (20000, 100000),
            'Meals and Entertainment': (2000, 10000)
        }
        
        range_min, range_max = category_ranges.get(category, (5000, 50000))
        amount = random.uniform(range_min, range_max)
        
        return round(amount, 2)
    
    def _create_bill(self, vendor: pd.Series, 
                    bill_date: datetime,
                    sequence: int,
                    expense_account: str,
                    amount: float,
                    is_recurring: bool = False) -> Dict:
        """Create a single bill with all calculations"""
        
        bill_id = generate_bill_id(bill_date, sequence)
        
        # Generate line item description
        description = self._generate_bill_description(expense_account, bill_date, is_recurring)
        
        # Check if prepaid (service period in future)
        service_period = extract_service_period(description)
        item_is_prepaid = is_prepaid_expense(service_period, bill_date) if service_period else False
        
        # Calculate subtotal (single line item for now)
        subtotal = amount
        quantity = 1
        rate = amount
        
        # Apply tax based on currency
        if vendor['Currency'] == 'INR':
            tax_type = 'IGST'
            tax_rate = 0.18
            tax_amount = calculate_igst(subtotal, tax_rate)
        else:  # USD
            tax_type = 'Sales Tax'
            tax_rate = random.choice([0.04, 0.06, 0.08])
            tax_amount = calculate_sales_tax(subtotal, tax_rate)
        
        # Calculate total before TDS
        total_before_tds = subtotal + tax_amount
        
        # Apply TDS if applicable (only for INR vendors)
        tds_section, tds_rate = get_tds_section_for_expense(expense_account)
        tds_applicable = (tds_section is not None and vendor['Currency'] == 'INR')
        
        if tds_applicable:
            tds_amount = calculate_tds(subtotal, tds_rate)
        else:
            tds_amount = 0.0
            tds_section = None
            tds_rate = 0.0
        
        # Calculate net payable
        total_amount = total_before_tds
        net_payable = total_amount - tds_amount
        
        # Determine due date (30 days default)
        payment_terms = vendor.get('Payment_Terms', 'Net 30')
        if 'Net 15' in str(payment_terms):
            due_days = 15
        else:
            due_days = 30
        
        due_date = bill_date + timedelta(days=due_days)
        
        # Prepaid expense data
        prepaid_data = {}
        if item_is_prepaid and service_period:
            prepaid_data = {
                'Is_Prepaid': True,
                'Prepaid_Start_Date': service_period[0],
                'Prepaid_End_Date': service_period[1],
                'Amortization_Period_Months': self._calculate_months_between(service_period[0], service_period[1]),
                'Monthly_Amortization_Amount': calculate_monthly_amount(total_amount, service_period),
                'Amortized_To_Date': 0.0,
                'Remaining_Prepaid_Balance': total_amount
            }
        else:
            prepaid_data = {
                'Is_Prepaid': False,
                'Prepaid_Start_Date': None,
                'Prepaid_End_Date': None,
                'Amortization_Period_Months': 0,
                'Monthly_Amortization_Amount': 0.0,
                'Amortized_To_Date': 0.0,
                'Remaining_Prepaid_Balance': 0.0
            }
        
        # Build bill dictionary
        bill = {
            'Bill_ID': bill_id,
            'Bill_Date': bill_date,
            'Vendor_ID': vendor['Entity_ID'],
            'Vendor_Name': vendor['Legal_Name'],
            'Vendor_Address': self._format_address(vendor),
            'Vendor_Tax_ID': vendor['Tax_ID'],
            'Currency': vendor['Currency'],
            'Exchange_Rate': self.exchange_rate if vendor['Currency'] == 'USD' else 1.0,
            'Due_Date': due_date,
            'Line_Item_Count': 1,  # Keeping it simple with 1 line item
            'Line_Item_1_Description': description,
            'Line_Item_1_Quantity': quantity,
            'Line_Item_1_Rate': rate,
            'Line_Item_1_Amount': amount,
            'Line_Item_1_Account': expense_account,
            'Line_Item_2_Description': None,
            'Line_Item_2_Quantity': None,
            'Line_Item_2_Rate': None,
            'Line_Item_2_Amount': None,
            'Line_Item_2_Account': None,
            'Subtotal': subtotal,
            'Tax_Type': tax_type,
            'Tax_Rate': tax_rate,
            'Tax_Amount': tax_amount,
            'Total_Amount': total_amount,
            'TDS_Applicable': tds_applicable,
            'TDS_Section': tds_section,
            'TDS_Amount': tds_amount,
            'Net_Payable': net_payable,
            'Notes': 'Payment terms: Net 30',
            'Status': 'Received'
        }
        
        # Add prepaid data
        bill.update(prepaid_data)
        
        return bill
    
    def _generate_bill_description(self, expense_account: str, 
                                   bill_date: datetime,
                                   is_recurring: bool) -> str:
        """Generate bill line item description"""
        
        if is_recurring:
            # Recurring expenses - include service period for next month
            next_month = bill_date + timedelta(days=30)
            month_name = next_month.strftime("%B")
            description = f"{expense_account} - {month_name} {next_month.year}"
        else:
            # One-time expenses
            if expense_account == 'Repairs and Maintenance':
                description = f"Repair Services - {bill_date.strftime('%B %Y')}"
            elif expense_account == 'Consultant Expense':
                description = f"Consulting Services - {bill_date.strftime('%B %Y')}"
            elif expense_account == 'Software Subscriptions':
                # Prepaid - annual subscription
                start_date = bill_date
                end_date = bill_date + timedelta(days=365)
                service_period = format_date_for_service_period(start_date, end_date)
                description = f"Software License (Service Period: {service_period})"
            elif expense_account == 'Travel Expense':
                description = f"Business Travel - {bill_date.strftime('%B %Y')}"
            else:
                description = f"{expense_account} - {bill_date.strftime('%B %Y')}"
        
        return description
    
    def _format_address(self, vendor: pd.Series) -> str:
        """Format vendor address"""
        parts = [
            vendor.get('Address_Line1', ''),
            vendor.get('City', ''),
            vendor.get('State', '')
        ]
        return ', '.join([p for p in parts if p and str(p) != 'nan'])
    
    def _calculate_months_between(self, start: datetime, end: datetime) -> int:
        """Calculate number of months between two dates"""
        return (end.year - start.year) * 12 + (end.month - start.month) + 1


if __name__ == "__main__":
    # Test bill generator
    import sys
    
    # Load test data
    xl = pd.ExcelFile('/mnt/user-data/uploads/Komplai_Demo_Master__Claude_.xlsx')
    entities = pd.read_excel(xl, 'Entities')
    bills = pd.read_excel(xl, 'Bills_Master')
    recurring = pd.read_excel(xl, 'Recurring_Schedule')
    
    # Test config
    config = {
        'pipeline': {
            'base_exchange_rate': 85.0
        }
    }
    
    # Create generator
    gen = BillGenerator(entities, recurring, config)
    
    # Generate test bills
    test_date = datetime(2026, 1, 6)
    new_bills = gen.generate_weekly_bills(test_date, bills, count=4)
    
    print(f"Generated {len(new_bills)} bills:")
    for bill in new_bills:
        print(f"\n{bill['Bill_ID']} - {bill['Vendor_Name']}")
        print(f"  Account: {bill['Line_Item_1_Account']}")
        print(f"  Amount: {bill['Currency']} {bill['Total_Amount']:,.2f}")
        print(f"  TDS Applicable: {bill['TDS_Applicable']}")
        if bill['TDS_Applicable']:
            print(f"  TDS: {bill['TDS_Section']} - {bill['TDS_Amount']:,.2f}")
            print(f"  Net Payable: {bill['Net_Payable']:,.2f}")
        print(f"  Prepaid: {bill['Is_Prepaid']}")
