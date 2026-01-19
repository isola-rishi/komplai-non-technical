"""
Komplai Demo Pipeline - Invoice Generator
Generates customer invoices with deferred revenue handling
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from typing import Dict, List
import sys
sys.path.append('/home/user/demo-dummy-data')

from utils import (
    generate_invoice_id,
    set_seed,
    format_date_for_service_period,
    calculate_igst,
    calculate_sales_tax,
    calculate_withholding_tax,
    generate_hsn_sac_code,
    apply_variance,
    extract_service_period,
    is_deferred_revenue,
    calculate_monthly_amount,
    format_indian_date
)


class InvoiceGenerator:
    """Generate realistic invoices with deferred revenue handling"""
    
    def __init__(self, entities_df: pd.DataFrame, config: Dict):
        self.entities = entities_df
        self.config = config
        self.exchange_rate = config['pipeline']['base_exchange_rate']
        
        # Get customers only
        self.customers = entities_df[entities_df['Entity_Type'] == 'Customer'].copy()
        
        # Service descriptions for different industries
        self.service_templates = {
            'Technology': [
                'Software Development - Phase {phase}',
                'SaaS Platform Subscription - {plan}',
                'Business Intelligence Platform - Annual',
                'Data Analytics & BI - Phase {phase}',
                'Implementation Support (Hours)',
                'Technical Consulting Services'
            ],
            'Financial Services': [
                'Financial Advisory Services',
                'Risk Management Consulting',
                'Compliance Audit Services',
                'Portfolio Management - Annual'
            ],
            'Healthcare': [
                'Healthcare IT Solutions',
                'Medical Records Management',
                'Telemedicine Platform Subscription'
            ],
            'Retail & E-commerce': [
                'E-commerce Platform Subscription',
                'Inventory Management System',
                'Point of Sale Software'
            ]
        }
    
    def generate_weekly_invoices(self, run_date: datetime,
                                 last_invoices: pd.DataFrame,
                                 count: int = 2) -> List[Dict]:
        """
        Generate invoices for the week
        Args:
            run_date: Monday of the week (pipeline runs on this date)
            last_invoices: Existing invoices dataframe
            count: Number of invoices to generate (default 2)
        """
        # Set seed for deterministic randomness
        set_seed(run_date)

        # Get next invoice sequence number
        start_seq = 1
        if len(last_invoices) > 0:
            # Find the last valid Invoice_ID (skip empty rows)
            for i in range(len(last_invoices) - 1, -1, -1):
                last_id = last_invoices.iloc[i]['Invoice_ID']
                # Check if ID is valid (non-empty string with expected format)
                if last_id and isinstance(last_id, str) and '-' in last_id:
                    try:
                        last_seq = int(last_id.split('-')[-1])
                        start_seq = last_seq + 1
                        break
                    except ValueError:
                        continue  # Try previous row

        invoices = []

        # Select customers weighted by transaction value
        selected_customers = self._select_customers(count)

        for i, customer in enumerate(selected_customers):
            # Generate invoice for PREVIOUS week (run_date - 7 to run_date - 1)
            # Random day in the previous week
            days_back = random.randint(1, 7)
            invoice_date = run_date - timedelta(days=days_back)

            invoice = self._create_invoice(
                customer=customer,
                invoice_date=invoice_date,
                sequence=start_seq + i
            )
            invoices.append(invoice)

        return invoices
    
    def _select_customers(self, count: int) -> List[pd.Series]:
        """Select customers based on weighted probability (without replacement)"""
        # Weight by average transaction value, but cap to prevent dominance
        raw_weights = self.customers['Average_Transaction_Value'].fillna(50000).tolist()

        # Cap weights to max 3x the median to ensure variety
        median_weight = sorted(raw_weights)[len(raw_weights) // 2]
        max_weight = median_weight * 3
        capped_weights = [min(w, max_weight) for w in raw_weights]

        # Normalize weights
        total_weight = sum(capped_weights)
        normalized_weights = [w / total_weight for w in capped_weights]

        # Select customers WITHOUT replacement (each customer only once per batch)
        customer_indices = list(range(len(self.customers)))
        selected_indices = []
        remaining_indices = customer_indices.copy()
        remaining_weights = normalized_weights.copy()

        for _ in range(min(count, len(self.customers))):
            # Select one customer
            chosen = random.choices(remaining_indices, weights=remaining_weights, k=1)[0]
            selected_indices.append(chosen)

            # Remove from pool
            idx = remaining_indices.index(chosen)
            remaining_indices.pop(idx)
            remaining_weights.pop(idx)

            # Re-normalize remaining weights
            if remaining_weights:
                total = sum(remaining_weights)
                remaining_weights = [w / total for w in remaining_weights]

        return [self.customers.iloc[idx] for idx in selected_indices]
    
    def _create_invoice(self, customer: pd.Series, 
                       invoice_date: datetime, 
                       sequence: int) -> Dict:
        """Create a single invoice with all line items and calculations"""
        
        invoice_id = generate_invoice_id(invoice_date, sequence)
        
        # Determine line item count (weighted towards 1-2 items)
        line_item_count = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
        
        # Generate line items
        line_items = self._generate_line_items(customer, invoice_date, line_item_count)
        
        # Calculate subtotal
        subtotal = sum([item['amount'] for item in line_items])
        
        # Apply tax based on currency
        if customer['Currency'] == 'INR':
            tax_type = 'IGST'
            tax_rate = 0.18
            tax_amount = calculate_igst(subtotal, tax_rate)
        else:  # USD
            tax_type = 'Sales Tax'
            # State-specific rates (simplified)
            tax_rate = random.choice([0.04, 0.06, 0.08])
            tax_amount = calculate_sales_tax(subtotal, tax_rate)
        
        # Calculate total
        total_amount = subtotal + tax_amount
        
        # Determine payment terms
        payment_terms = customer.get('Payment_Terms', 'Net 30')
        if 'Net 15' in str(payment_terms):
            due_days = 15
        else:
            due_days = 30
        
        due_date = invoice_date + timedelta(days=due_days)
        
        # Check for deferred revenue
        is_deferred = any([item.get('is_deferred', False) for item in line_items])
        
        deferral_data = {}
        if is_deferred:
            # Use first deferred line item for deferral schedule
            deferred_item = [item for item in line_items if item.get('is_deferred')][0]
            service_period = deferred_item['service_period']
            
            deferral_data = {
                'Is_Deferred': True,
                'Deferral_Start_Date': service_period[0],
                'Deferral_End_Date': service_period[1],
                'Deferral_Period_Months': self._calculate_months_between(service_period[0], service_period[1]),
                'Monthly_Recognition_Amount': calculate_monthly_amount(total_amount, service_period),
                'Recognized_To_Date': 0.0,
                'Remaining_Deferred_Balance': total_amount
            }
        else:
            deferral_data = {
                'Is_Deferred': False,
                'Deferral_Start_Date': None,
                'Deferral_End_Date': None,
                'Deferral_Period_Months': 0,
                'Monthly_Recognition_Amount': 0.0,
                'Recognized_To_Date': 0.0,
                'Remaining_Deferred_Balance': 0.0
            }
        
        # Build invoice dictionary
        invoice = {
            'Invoice_ID': invoice_id,
            'Invoice_Date': invoice_date,
            'Customer_ID': customer['Entity_ID'],
            'Customer_Name': customer['Legal_Name'],
            'Customer_Address': self._format_address(customer),
            'Customer_Tax_ID': customer['Tax_ID'],
            'Currency': customer['Currency'],
            'Exchange_Rate': self.exchange_rate if customer['Currency'] == 'USD' else 1.0,
            'Due_Date': due_date,
            'Line_Item_Count': line_item_count,
            'Subtotal': subtotal,
            'Tax_Type': tax_type,
            'Tax_Rate': tax_rate,
            'Tax_Amount': tax_amount,
            'Total_Amount': total_amount,
            'Notes': self._generate_notes(customer, is_deferred),
            'PDF_Generated': False,
            'PDF_Path': None,
            'Email_Sent': False,
            'Status': 'Sent'
        }
        
        # Add line items (up to 3)
        for i in range(1, 4):
            if i <= line_item_count:
                item = line_items[i-1]
                invoice[f'Line_Item_{i}_Description'] = item['description']
                invoice[f'Line_Item_{i}_Quantity'] = item['quantity']
                invoice[f'Line_Item_{i}_Rate'] = item['rate']
                invoice[f'Line_Item_{i}_Amount'] = item['amount']
                invoice[f'Line_Item_{i}_Account'] = item['account']
            else:
                invoice[f'Line_Item_{i}_Description'] = None
                invoice[f'Line_Item_{i}_Quantity'] = None
                invoice[f'Line_Item_{i}_Rate'] = None
                invoice[f'Line_Item_{i}_Amount'] = None
                invoice[f'Line_Item_{i}_Account'] = None
        
        # Add deferral data
        invoice.update(deferral_data)
        
        return invoice
    
    def _generate_line_items(self, customer: pd.Series, 
                            invoice_date: datetime,
                            count: int) -> List[Dict]:
        """Generate line items for invoice"""
        line_items = []
        industry = customer.get('Industry', 'Technology')
        
        # Get service templates for industry
        templates = self.service_templates.get(industry, self.service_templates['Technology'])
        
        # Base amount from average transaction value
        base_amount = customer.get('Average_Transaction_Value', 100000)
        
        # 70% chance of deferred revenue for first line item
        include_deferred = random.random() < 0.7
        
        for i in range(count):
            # Select service template
            template = random.choice(templates)
            
            # Personalize template
            if '{phase}' in template:
                template = template.format(phase=random.randint(1, 3))
            elif '{plan}' in template:
                template = template.format(plan=random.choice(['Growth Plan', 'Enterprise Plan', 'Professional Plan']))
            
            # Determine if this line item is deferred
            item_is_deferred = include_deferred and i == 0
            
            # Generate service period for deferred items
            if item_is_deferred:
                # Multi-month service period
                months = random.choice([3, 6, 12])
                start_date = invoice_date
                end_date = start_date + timedelta(days=30 * months)
                
                service_period_str = f" (Service Period: {format_date_for_service_period(start_date, end_date)})"
                description = template + service_period_str
                
                service_period = (start_date, end_date)
            else:
                # Short-term or one-time service
                if random.random() < 0.3:  # 30% have service period
                    start_date = invoice_date
                    end_date = invoice_date + timedelta(days=random.choice([15, 30]))
                    service_period_str = f" (Service Period: {format_date_for_service_period(start_date, end_date)})"
                    description = template + service_period_str
                    service_period = (start_date, end_date)
                else:
                    description = template
                    service_period = None
            
            # Calculate amount for this line item
            if count == 1:
                amount = base_amount
            else:
                # Distribute amount across line items
                if i == 0:
                    amount = base_amount * random.uniform(0.6, 0.8)
                else:
                    amount = base_amount * random.uniform(0.1, 0.3)
            
            # Apply slight variance
            amount = apply_variance(amount, 0.05)
            
            # Determine quantity and rate
            if 'Hours' in template or 'Support' in template:
                quantity = random.randint(5, 20)
                rate = round(amount / quantity, 2)
            else:
                quantity = 1
                rate = amount
            
            line_items.append({
                'description': description,
                'quantity': quantity,
                'rate': rate,
                'amount': amount,
                'account': 'Sales',  # Could be 'Project Revenue' for professional services
                'is_deferred': item_is_deferred,
                'service_period': service_period
            })
        
        return line_items
    
    def _format_address(self, customer: pd.Series) -> str:
        """Format customer address"""
        parts = [
            customer.get('Address_Line1', ''),
            customer.get('City', ''),
            customer.get('State', ''),
            str(customer.get('ZIP', ''))
        ]
        return ', '.join([p for p in parts if p and str(p) != 'nan'])
    
    def _generate_notes(self, customer: pd.Series, is_deferred: bool) -> str:
        """Generate invoice notes"""
        notes = "Payment due as per terms. Bank details: HDFC Bank, A/c: 50200012345678, IFSC: HDFC0001234"
        
        if is_deferred:
            notes += ". Revenue to be recognized over service period per accrual schedule."
        
        return notes
    
    def _calculate_months_between(self, start: datetime, end: datetime) -> int:
        """Calculate number of months between two dates"""
        return (end.year - start.year) * 12 + (end.month - start.month) + 1


if __name__ == "__main__":
    # Test invoice generator
    import sys
    sys.path.append('/mnt/user-data/uploads')
    
    # Load test data
    xl = pd.ExcelFile('/mnt/user-data/uploads/Komplai_Demo_Master__Claude_.xlsx')
    entities = pd.read_excel(xl, 'Entities')
    invoices = pd.read_excel(xl, 'Invoices_Master')
    
    # Test config
    config = {
        'pipeline': {
            'base_exchange_rate': 85.0
        }
    }
    
    # Create generator
    gen = InvoiceGenerator(entities, config)
    
    # Generate test invoices
    test_date = datetime(2026, 1, 6)
    new_invoices = gen.generate_weekly_invoices(test_date, invoices, count=2)
    
    print(f"Generated {len(new_invoices)} invoices:")
    for inv in new_invoices:
        print(f"\n{inv['Invoice_ID']} - {inv['Customer_Name']}")
        print(f"  Amount: {inv['Currency']} {inv['Total_Amount']:,.2f}")
        print(f"  Line Items: {inv['Line_Item_Count']}")
        print(f"  Deferred: {inv['Is_Deferred']}")
        if inv['Is_Deferred']:
            print(f"  Period: {inv['Deferral_Start_Date']} to {inv['Deferral_End_Date']}")
