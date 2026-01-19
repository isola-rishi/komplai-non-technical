"""
Komplai Demo Pipeline - PDF Generator
Converts HTML templates to PDFs using WeasyPrint
"""

from jinja2 import Environment, FileSystemLoader, Template
from datetime import datetime
import os
from typing import Dict

# Import WeasyPrint only when needed (may fail on Mac without GTK)
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except Exception as e:
    WEASYPRINT_AVAILABLE = False
    HTML = None
    CSS = None


class PDFGenerator:
    """Generate PDFs from HTML templates"""

    def __init__(self, template_dir: str = None, output_dir: str = None):
        """
        Initialize PDF Generator

        Args:
            template_dir: Directory containing HTML templates (optional)
            output_dir: Directory for PDF output (optional, defaults to ./output/pdfs)

        Raises:
            ImportError: If WeasyPrint is not available
        """
        if not WEASYPRINT_AVAILABLE:
            raise ImportError("WeasyPrint is not available. Install GTK libraries or skip PDF generation.")

        self.template_dir = template_dir or "."
        self.output_dir = output_dir or "./output/pdfs"

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

        # Initialize Jinja2 environment if template_dir exists
        if os.path.exists(self.template_dir):
            self.env = Environment(loader=FileSystemLoader(self.template_dir))
        else:
            self.env = None

    def generate_invoice_pdf(self, invoice_data: Dict, output_filename: str = None) -> str:
        """
        Generate PDF for an invoice

        Args:
            invoice_data: Dictionary with invoice data
            output_filename: Optional custom filename

        Returns:
            Path to generated PDF
        """
        if output_filename is None:
            output_filename = f"{invoice_data.get('Invoice_ID', 'invoice')}.pdf"

        output_path = os.path.join(self.output_dir, output_filename)

        # Generate HTML from template
        html_content = self._render_invoice_template(invoice_data)

        # Convert to PDF
        HTML(string=html_content).write_pdf(output_path)

        print(f"✓ Generated invoice PDF: {output_path}")
        return output_path

    def generate_bill_pdf(self, bill_data: Dict, output_filename: str = None) -> str:
        """
        Generate PDF for a bill

        Args:
            bill_data: Dictionary with bill data
            output_filename: Optional custom filename

        Returns:
            Path to generated PDF
        """
        if output_filename is None:
            output_filename = f"{bill_data.get('Bill_ID', 'bill')}.pdf"

        output_path = os.path.join(self.output_dir, output_filename)

        # Generate HTML from template
        html_content = self._render_bill_template(bill_data)

        # Convert to PDF
        HTML(string=html_content).write_pdf(output_path)

        print(f"✓ Generated bill PDF: {output_path}")
        return output_path

    def generate_statement_pdf(self, statement_data: Dict, output_filename: str = None) -> str:
        """
        Generate PDF for a bank statement

        Args:
            statement_data: Dictionary with statement data
            output_filename: Optional custom filename

        Returns:
            Path to generated PDF
        """
        if output_filename is None:
            date_str = datetime.now().strftime("%Y%m%d")
            output_filename = f"statement_{date_str}.pdf"

        output_path = os.path.join(self.output_dir, output_filename)

        # Generate HTML from template
        html_content = self._render_statement_template(statement_data)

        # Convert to PDF
        HTML(string=html_content).write_pdf(output_path)

        print(f"✓ Generated statement PDF: {output_path}")
        return output_path

    def _render_invoice_template(self, data: Dict) -> str:
        """Render invoice HTML template"""
        template_str = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; font-size: 12px; margin: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { margin: 0; font-size: 24px; }
        .info-section { margin: 20px 0; }
        .info-section h3 { margin: 5px 0; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .totals { text-align: right; }
        .notes { margin-top: 30px; font-size: 10px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>INVOICE</h1>
        <p><strong>Invoice #{{ invoice_id }}</strong></p>
        <p>Date: {{ invoice_date }}</p>
    </div>

    <div class="info-section">
        <h3>From:</h3>
        <p><strong>Acme Technologies Private Limited</strong></p>
        <p>123 Tech Park, Whitefield, Bangalore, KA 560066</p>
        <p>GSTIN: 29AABCA1234F1ZV</p>
    </div>

    <div class="info-section">
        <h3>Bill To:</h3>
        <p><strong>{{ customer_name }}</strong></p>
        <p>{{ customer_address }}</p>
        <p>Tax ID: {{ customer_tax_id }}</p>
    </div>

    <table>
        <thead>
            <tr>
                <th>Description</th>
                <th style="width: 10%;">Quantity</th>
                <th style="width: 15%;">Rate</th>
                <th style="width: 15%;">Amount</th>
            </tr>
        </thead>
        <tbody>
            {% for item in line_items %}
            <tr>
                <td>{{ item.description }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ currency }} {{ "%0.2f"|format(item.rate) }}</td>
                <td>{{ currency }} {{ "%0.2f"|format(item.amount) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <table class="totals">
        <tr>
            <td colspan="3"><strong>Subtotal:</strong></td>
            <td>{{ currency }} {{ "%0.2f"|format(subtotal) }}</td>
        </tr>
        <tr>
            <td colspan="3"><strong>{{ tax_type }} ({{ "%0.0f"|format(tax_rate * 100) }}%):</strong></td>
            <td>{{ currency }} {{ "%0.2f"|format(tax_amount) }}</td>
        </tr>
        <tr style="background-color: #f2f2f2;">
            <td colspan="3"><strong>TOTAL:</strong></td>
            <td><strong>{{ currency }} {{ "%0.2f"|format(total_amount) }}</strong></td>
        </tr>
    </table>

    <div class="notes">
        <p><strong>Due Date:</strong> {{ due_date }}</p>
        {% if notes %}
        <p><strong>Notes:</strong> {{ notes }}</p>
        {% endif %}
    </div>
</body>
</html>
"""
        template = Template(template_str)
        return template.render(**data)

    def _render_bill_template(self, data: Dict) -> str:
        """Render bill HTML template"""
        template_str = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; font-size: 12px; margin: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { margin: 0; font-size: 24px; }
        .info-section { margin: 20px 0; }
        .info-section h3 { margin: 5px 0; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .totals { text-align: right; }
        .notes { margin-top: 30px; font-size: 10px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>BILL</h1>
        <p><strong>Bill #{{ bill_id }}</strong></p>
        <p>Date: {{ bill_date }}</p>
    </div>

    <div class="info-section">
        <h3>From:</h3>
        <p><strong>{{ vendor_name }}</strong></p>
        <p>{{ vendor_address }}</p>
        <p>Tax ID: {{ vendor_tax_id }}</p>
    </div>

    <div class="info-section">
        <h3>Bill To:</h3>
        <p><strong>Acme Technologies Private Limited</strong></p>
        <p>123 Tech Park, Whitefield, Bangalore, KA 560066</p>
        <p>GSTIN: 29AABCA1234F1ZV</p>
    </div>

    <table>
        <thead>
            <tr>
                <th>Description</th>
                <th style="width: 10%;">Quantity</th>
                <th style="width: 15%;">Rate</th>
                <th style="width: 15%;">Amount</th>
            </tr>
        </thead>
        <tbody>
            {% for item in line_items %}
            <tr>
                <td>{{ item.description }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ currency }} {{ "%0.2f"|format(item.rate) }}</td>
                <td>{{ currency }} {{ "%0.2f"|format(item.amount) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <table class="totals">
        <tr>
            <td colspan="3"><strong>Subtotal:</strong></td>
            <td>{{ currency }} {{ "%0.2f"|format(subtotal) }}</td>
        </tr>
        <tr>
            <td colspan="3"><strong>{{ tax_type }} ({{ "%0.0f"|format(tax_rate * 100) }}%):</strong></td>
            <td>{{ currency }} {{ "%0.2f"|format(tax_amount) }}</td>
        </tr>
        <tr>
            <td colspan="3"><strong>Total:</strong></td>
            <td>{{ currency }} {{ "%0.2f"|format(total_amount) }}</td>
        </tr>
        {% if tds_applicable %}
        <tr>
            <td colspan="3"><strong>TDS Deduction ({{ tds_section }}):</strong></td>
            <td>- {{ currency }} {{ "%0.2f"|format(tds_amount) }}</td>
        </tr>
        <tr style="background-color: #f2f2f2;">
            <td colspan="3"><strong>NET PAYABLE:</strong></td>
            <td><strong>{{ currency }} {{ "%0.2f"|format(net_payable) }}</strong></td>
        </tr>
        {% else %}
        <tr style="background-color: #f2f2f2;">
            <td colspan="3"><strong>TOTAL PAYABLE:</strong></td>
            <td><strong>{{ currency }} {{ "%0.2f"|format(total_amount) }}</strong></td>
        </tr>
        {% endif %}
    </table>

    <div class="notes">
        <p><strong>Due Date:</strong> {{ due_date }}</p>
        {% if notes %}
        <p><strong>Notes:</strong> {{ notes }}</p>
        {% endif %}
    </div>
</body>
</html>
"""
        template = Template(template_str)
        return template.render(**data)

    def _render_statement_template(self, data: Dict) -> str:
        """Render bank statement HTML template"""
        template_str = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; font-size: 11px; margin: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { margin: 0; font-size: 24px; }
        .account-info { margin: 20px 0; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 10px; }
        th, td { border: 1px solid #ddd; padding: 6px; text-align: left; }
        th { background-color: #f2f2f2; }
        .amount-debit { color: #d9534f; }
        .amount-credit { color: #5cb85c; }
        .summary { margin-top: 30px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>BANK STATEMENT</h1>
        <p>{{ bank_name }}</p>
        <p>Statement Period: {{ start_date }} to {{ end_date }}</p>
    </div>

    <div class="account-info">
        <p><strong>Account Holder:</strong> {{ account_name }}</p>
        <p><strong>Account Number:</strong> {{ account_number }}</p>
        <p><strong>IFSC Code:</strong> {{ ifsc_code }}</p>
    </div>

    <table>
        <thead>
            <tr>
                <th style="width: 12%;">Date</th>
                <th>Description</th>
                <th style="width: 15%;">Debit</th>
                <th style="width: 15%;">Credit</th>
                <th style="width: 15%;">Balance</th>
            </tr>
        </thead>
        <tbody>
            {% for txn in transactions %}
            <tr>
                <td>{{ txn.date }}</td>
                <td>{{ txn.description }}</td>
                <td class="amount-debit">{% if txn.debit > 0 %}₹ {{ "%0.2f"|format(txn.debit) }}{% endif %}</td>
                <td class="amount-credit">{% if txn.credit > 0 %}₹ {{ "%0.2f"|format(txn.credit) }}{% endif %}</td>
                <td>₹ {{ "%0.2f"|format(txn.balance) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="summary">
        <p><strong>Opening Balance:</strong> ₹ {{ "%0.2f"|format(opening_balance) }}</p>
        <p><strong>Closing Balance:</strong> ₹ {{ "%0.2f"|format(closing_balance) }}</p>
    </div>
</body>
</html>
"""
        template = Template(template_str)
        return template.render(**data)


if __name__ == "__main__":
    # Test PDF Generator
    print("\n" + "="*60)
    print("TESTING PDF GENERATOR")
    print("="*60)

    generator = PDFGenerator()

    # Test invoice generation
    print("\n[Generating Test Invoice PDF]")
    invoice_data = {
        'invoice_id': 'INV-202601-0001',
        'invoice_date': '2026-01-06',
        'due_date': '2026-02-05',
        'customer_name': 'Test Customer Ltd',
        'customer_address': '123 Test Street, Mumbai, MH 400001',
        'customer_tax_id': 'GSTIN123456789',
        'currency': 'INR',
        'line_items': [
            {'description': 'Software Development Services', 'quantity': 1, 'rate': 100000.00, 'amount': 100000.00},
            {'description': 'Consulting Hours', 'quantity': 10, 'rate': 5000.00, 'amount': 50000.00}
        ],
        'subtotal': 150000.00,
        'tax_type': 'IGST',
        'tax_rate': 0.18,
        'tax_amount': 27000.00,
        'total_amount': 177000.00,
        'notes': 'Payment due within 30 days'
    }

    invoice_pdf = generator.generate_invoice_pdf(invoice_data, 'test_invoice.pdf')

    # Test bill generation
    print("\n[Generating Test Bill PDF]")
    bill_data = {
        'bill_id': 'BILL-202601-0001',
        'bill_date': '2026-01-06',
        'due_date': '2026-02-05',
        'vendor_name': 'Test Vendor Pvt Ltd',
        'vendor_address': '456 Vendor Lane, Delhi, DL 110001',
        'vendor_tax_id': 'GSTIN987654321',
        'currency': 'INR',
        'line_items': [
            {'description': 'Cloud Hosting - January 2026', 'quantity': 1, 'rate': 50000.00, 'amount': 50000.00}
        ],
        'subtotal': 50000.00,
        'tax_type': 'IGST',
        'tax_rate': 0.18,
        'tax_amount': 9000.00,
        'total_amount': 59000.00,
        'tds_applicable': False,
        'tds_section': None,
        'tds_amount': 0.00,
        'net_payable': 59000.00,
        'notes': 'Payment due within 30 days'
    }

    bill_pdf = generator.generate_bill_pdf(bill_data, 'test_bill.pdf')

    print("\n" + "="*60)
    print("✓ PDF GENERATOR TEST COMPLETE")
    print("="*60)
    print(f"\nGenerated PDFs in: {generator.output_dir}")
