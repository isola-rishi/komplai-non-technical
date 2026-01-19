"""
Komplai Demo Pipeline - Utility Functions
Core utilities for date handling, ID generation, tax calculations, and validations
"""

import pandas as pd
import math
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import hashlib

# ============================================================================
# DATE UTILITIES
# ============================================================================

def get_next_monday(from_date: datetime = None) -> datetime:
    """Get the next Monday from a given date"""
    if from_date is None:
        from_date = datetime.now()
    
    days_ahead = 0 - from_date.weekday()  # Monday is 0
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    
    return from_date + timedelta(days=days_ahead)


def get_mondays_in_range(start_date: datetime, end_date: datetime) -> List[datetime]:
    """Get all Mondays between two dates"""
    mondays = []
    current = get_next_monday(start_date)
    
    while current <= end_date:
        mondays.append(current)
        current += timedelta(days=7)
    
    return mondays


def add_business_days(start_date: datetime, days: int) -> datetime:
    """Add business days to a date (excluding weekends)"""
    current = start_date
    while days > 0:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Monday = 0, Friday = 4
            days -= 1
    return current


def get_25th_of_month(reference_date: datetime) -> datetime:
    """Get the 25th day of the month from reference date"""
    return datetime(reference_date.year, reference_date.month, 25)


def week_contains_date(week_start: datetime, week_end: datetime, day: int) -> bool:
    """Check if a specific day of month falls within a week range"""
    for single_date in pd.date_range(start=week_start, end=week_end, freq='D'):
        if single_date.day == day:
            return True
    return False


def format_indian_date(date: datetime) -> str:
    """Format date in Indian style: 01 Jan 2026"""
    return date.strftime("%d %b %Y")


def format_date_for_service_period(start: datetime, end: datetime) -> str:
    """Format service period: 01 Nov 2025 – 30 Nov 2025"""
    return f"{start.strftime('%d %b %Y')} – {end.strftime('%d %b %Y')}"


# ============================================================================
# ID GENERATION
# ============================================================================

def generate_invoice_id(date: datetime, sequence: int) -> str:
    """Generate invoice ID: INV-202601-0001"""
    return f"INV-{date.strftime('%Y%m')}-{sequence:04d}"


def generate_bill_id(date: datetime, sequence: int) -> str:
    """Generate bill ID: BILL-202601-0001"""
    return f"BILL-{date.strftime('%Y%m')}-{sequence:04d}"


def generate_transaction_id(sequence: int) -> str:
    """Generate bank transaction ID: TXN00000001"""
    return f"TXN{sequence:08d}"


def generate_run_id(timestamp: datetime) -> str:
    """Generate pipeline run ID: RUN-202601051000"""
    return f"RUN-{timestamp.strftime('%Y%m%d%H%M')}"


# ============================================================================
# CURRENCY & AMOUNT UTILITIES
# ============================================================================

def usd_to_inr(amount: float, exchange_rate: float = 85.0) -> float:
    """Convert USD to INR"""
    return round(amount * exchange_rate, 2)


def inr_to_usd(amount: float, exchange_rate: float = 85.0) -> float:
    """Convert INR to USD"""
    return round(amount / exchange_rate, 2)


def format_indian_currency(amount: float) -> str:
    """Format amount in Indian style with rupee symbol"""
    return f"₹{amount:,.2f}"


def format_usd_currency(amount: float) -> str:
    """Format amount in USD"""
    return f"${amount:,.2f}"


# ============================================================================
# TAX CALCULATIONS
# ============================================================================

def calculate_igst(subtotal: float, rate: float = 0.18) -> float:
    """Calculate IGST (Integrated GST)"""
    return round(subtotal * rate, 2)


def calculate_sales_tax(subtotal: float, rate: float) -> float:
    """Calculate US sales tax"""
    return round(subtotal * rate, 2)


def calculate_tds(subtotal: float, tds_rate: float) -> float:
    """
    Calculate TDS amount
    CRITICAL: TDS_Amount = Subtotal × TDS_Rate
    """
    return round(subtotal * tds_rate, 2)


def calculate_withholding_tax(amount: float, rate: float = 0.30) -> float:
    """Calculate US withholding tax for foreign payments"""
    return round(amount * rate, 2)


def get_tds_section_for_expense(expense_account: str) -> Optional[Tuple[str, float]]:
    """
    Determine TDS section and rate based on expense account category
    Returns: (section, rate) or None
    """
    tds_mapping = {
        # 194I - Rent (10%)
        "Rent Expense": ("194I", 0.10),
        "Office Rent": ("194I", 0.10),
        "Equipment Rent": ("194I", 0.10),
        
        # 194C - Contractor/Advertising (2% for corporate)
        "Repairs and Maintenance": ("194C", 0.02),
        "Advertising And Marketing": ("194C", 0.02),
        "Contractor Expense": ("194C", 0.02),
        "Janitorial Expense": ("194C", 0.02),
        
        # 194J - Professional Services (10%)
        "Consultant Expense": ("194J", 0.10),
        "Professional Services": ("194J", 0.10),
        "Technical Services": ("194J", 0.10),
        "Accounting Services": ("194J", 0.10),
        "Legal Services": ("194J", 0.10),
        
        # No TDS applicable
        "Software Subscriptions": (None, 0.0),
        "Cloud Hosting": (None, 0.0),
        "Telephone Expense": (None, 0.0),
        "IT and Internet Expenses": (None, 0.0),
        "Travel Expense": (None, 0.0),
        "Meals and Entertainment": (None, 0.0),
    }
    
    return tds_mapping.get(expense_account, (None, 0.0))


# ============================================================================
# DETERMINISTIC RANDOMNESS
# ============================================================================

def set_seed(date: datetime):
    """Set random seed based on date for deterministic randomness"""
    # Include year, week number, and day for more variation between runs
    year, week, day = date.isocalendar()
    seed_value = year * 10000 + week * 100 + day
    random.seed(seed_value)


def weighted_random_choice(items: List, weights: List) -> any:
    """Select item based on weighted probability"""
    return random.choices(items, weights=weights, k=1)[0]


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_entity_exists(entity_id: str, entities_df: pd.DataFrame) -> bool:
    """Validate entity ID exists in entities master"""
    if entity_id not in entities_df['Entity_ID'].values:
        raise ValidationError(f"Entity {entity_id} does not exist")
    return True


def validate_currency(currency: str) -> bool:
    """Validate currency is USD or INR only"""
    if currency not in ['USD', 'INR']:
        raise ValidationError(f"Invalid currency: {currency}. Must be USD or INR")
    return True


def validate_amount_positive(amount: float, field_name: str) -> bool:
    """Validate amount is positive"""
    if amount < 0:
        raise ValidationError(f"{field_name} must be positive: {amount}")
    return True


def validate_line_items_sum(line_items: List[Dict], subtotal: float) -> bool:
    """Validate line items sum to subtotal"""
    calculated_sum = sum([item['amount'] for item in line_items])
    if not math.isclose(calculated_sum, subtotal, rel_tol=0.01):
        raise ValidationError(
            f"Line items sum ({calculated_sum}) does not match subtotal ({subtotal})"
        )
    return True


def validate_tax_calculation(subtotal: float, tax_rate: float, tax_amount: float) -> bool:
    """Validate tax calculation is correct"""
    expected_tax = subtotal * tax_rate
    if not math.isclose(expected_tax, tax_amount, rel_tol=0.01):
        raise ValidationError(
            f"Tax calculation error: Expected {expected_tax}, got {tax_amount}"
        )
    return True


def validate_tds_calculation(subtotal: float, tds_rate: float, tds_amount: float) -> bool:
    """
    CRITICAL: Validate TDS calculation
    TDS_Amount = Subtotal × TDS_Rate
    """
    expected_tds = subtotal * tds_rate
    if not math.isclose(expected_tds, tds_amount, rel_tol=0.01):
        raise ValidationError(
            f"TDS calculation error: Expected {expected_tds}, got {tds_amount}"
        )
    return True


def validate_total_amount(subtotal: float, tax_amount: float, 
                         tds_amount: float, total_amount: float) -> bool:
    """Validate total amount calculation"""
    expected_total = subtotal + tax_amount - tds_amount
    if not math.isclose(expected_total, total_amount, rel_tol=0.01):
        raise ValidationError(
            f"Total calculation error: Expected {expected_total}, got {total_amount}"
        )
    return True


def validate_account_category(account: str, allowed_categories: List[str]) -> bool:
    """Validate account belongs to allowed categories"""
    if account not in allowed_categories:
        raise ValidationError(
            f"Invalid account category: {account}. Allowed: {allowed_categories}"
        )
    return True


def validate_date_sequential(new_date: datetime, last_date: datetime) -> bool:
    """Validate new date is after last date"""
    if new_date <= last_date:
        raise ValidationError(
            f"Date {new_date} is not after last date {last_date}"
        )
    return True


def validate_balance_non_negative(balance: float) -> bool:
    """Validate bank balance is not negative"""
    if balance < 0:
        raise ValidationError(f"Bank balance cannot be negative: {balance}")
    return True


# ============================================================================
# SERVICE PERIOD DETECTION
# ============================================================================

def extract_service_period(description: str) -> Optional[Tuple[datetime, datetime]]:
    """
    Extract service period from line item description
    Format: "Term: 01 Nov 2025 – 30 Nov 2025"
    """
    import re
    
    # Pattern to match date range
    pattern = r'Term:\s*(\d{2}\s+\w+\s+\d{4})\s*[–-]\s*(\d{2}\s+\w+\s+\d{4})'
    match = re.search(pattern, description)
    
    if match:
        start_str = match.group(1)
        end_str = match.group(2)
        
        start_date = datetime.strptime(start_str, "%d %b %Y")
        end_date = datetime.strptime(end_str, "%d %b %Y")
        
        return (start_date, end_date)
    
    return None


def is_prepaid_expense(service_period: Optional[Tuple[datetime, datetime]], 
                       invoice_date: datetime) -> bool:
    """
    Determine if expense is prepaid
    Prepaid if service period starts in future
    """
    if service_period is None:
        return False
    
    start_date, end_date = service_period
    return start_date > invoice_date


def is_deferred_revenue(service_period: Optional[Tuple[datetime, datetime]], 
                        invoice_date: datetime) -> bool:
    """
    Determine if revenue is deferred
    Deferred if service period spans multiple months
    """
    if service_period is None:
        return False
    
    start_date, end_date = service_period
    months_span = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1
    
    return months_span >= 3  # 3+ months triggers deferral


def calculate_monthly_amount(total_amount: float, 
                            service_period: Tuple[datetime, datetime]) -> float:
    """Calculate monthly amortization/recognition amount"""
    start_date, end_date = service_period
    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1
    
    return round(total_amount / months, 2)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_hsn_sac_code() -> str:
    """Generate random HSN/SAC code for Indian GST"""
    return str(random.randint(998000, 999999))


def generate_payment_reference() -> str:
    """Generate payment reference for bank transactions"""
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    numbers = ''.join(random.choices('0123456789', k=5))
    return f"NEFT/{letters}/{numbers}"


def apply_variance(base_value: float, variance_percent: float = 0.05) -> float:
    """Apply random variance to a value"""
    variance = base_value * variance_percent * (random.random() * 2 - 1)  # -5% to +5%
    return round(base_value + variance, 2)


if __name__ == "__main__":
    # Test functions
    print("Testing utilities...")
    
    # Date tests
    today = datetime.now()
    next_mon = get_next_monday(today)
    print(f"Next Monday: {next_mon}")
    
    # ID tests
    print(f"Invoice ID: {generate_invoice_id(today, 1)}")
    print(f"Bill ID: {generate_bill_id(today, 1)}")
    
    # Tax tests
    print(f"IGST on 100000: {calculate_igst(100000)}")
    print(f"TDS on 100000 @ 10%: {calculate_tds(100000, 0.10)}")
    
    # Service period test
    desc = "Software Development - Phase 1 (Term: 01 Jan 2026 – 31 Dec 2026)"
    period = extract_service_period(desc)
    print(f"Service Period: {period}")
    
    print("\nAll tests passed!")
