"""
Gmail SMTP Email Sender for Komplai Demo Pipeline
Sends invoices and bills as PDF attachments
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Optional


class GmailEmailSender:
    """Send emails with PDF attachments via Gmail SMTP"""

    def __init__(self):
        """
        Initialize Gmail SMTP client

        Credentials from environment variables:
        - SMTP_EMAIL: Gmail address to send from
        - SMTP_PASSWORD: Gmail App Password (16 characters)
        """
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender = os.environ.get('SMTP_EMAIL')
        self.password = os.environ.get('SMTP_PASSWORD')

        if not self.sender or not self.password:
            raise ValueError(
                "SMTP_EMAIL and SMTP_PASSWORD environment variables are required. "
                "Use a Gmail App Password (not your regular password)."
            )

    def send_invoice_email(
        self,
        recipient: str,
        invoice_id: str,
        customer_name: str,
        amount: float,
        currency: str,
        pdf_path: str
    ) -> bool:
        """Send invoice email with PDF attachment"""

        subject = f"Invoice {invoice_id} from Acme Technologies"

        body_text = f"""
Dear {customer_name},

Please find attached Invoice {invoice_id} for {currency} {amount:,.2f}.

Payment Terms: Net 30
Due Date: Please see invoice for details.

Thank you for your business.

Best regards,
Acme Technologies Private Limited
        """.strip()

        body_html = f"""
<html>
<body>
<p>Dear {customer_name},</p>
<p>Please find attached <strong>Invoice {invoice_id}</strong> for <strong>{currency} {amount:,.2f}</strong>.</p>
<p><strong>Payment Terms:</strong> Net 30<br>
<strong>Due Date:</strong> Please see invoice for details.</p>
<p>Thank you for your business.</p>
<p>Best regards,<br>
<strong>Acme Technologies Private Limited</strong></p>
</body>
</html>
        """.strip()

        return self._send_email_with_attachment(
            recipient=recipient,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            attachment_path=pdf_path
        )

    def send_bill_email(
        self,
        recipient: str,
        bill_id: str,
        vendor_name: str,
        amount: float,
        currency: str,
        pdf_path: str
    ) -> bool:
        """Send bill notification email with PDF attachment"""

        subject = f"Bill {bill_id} - {vendor_name}"

        body_text = f"""
Bill Notification

Bill ID: {bill_id}
Vendor: {vendor_name}
Amount: {currency} {amount:,.2f}

Please find attached bill for your records.

Acme Technologies Private Limited
        """.strip()

        body_html = f"""
<html>
<body>
<h3>Bill Notification</h3>
<p><strong>Bill ID:</strong> {bill_id}<br>
<strong>Vendor:</strong> {vendor_name}<br>
<strong>Amount:</strong> {currency} {amount:,.2f}</p>
<p>Please find attached bill for your records.</p>
<p><strong>Acme Technologies Private Limited</strong></p>
</body>
</html>
        """.strip()

        return self._send_email_with_attachment(
            recipient=recipient,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            attachment_path=pdf_path
        )

    def _send_email_with_attachment(
        self,
        recipient: str,
        subject: str,
        body_text: str,
        body_html: str,
        attachment_path: Optional[str] = None
    ) -> bool:
        """
        Send email with optional PDF attachment using Gmail SMTP

        Returns True on success, False on failure
        """
        # Create multipart message
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipient

        # Create body container
        msg_body = MIMEMultipart('alternative')

        # Add text and HTML bodies
        text_part = MIMEText(body_text, 'plain', 'utf-8')
        html_part = MIMEText(body_html, 'html', 'utf-8')
        msg_body.attach(text_part)
        msg_body.attach(html_part)
        msg.attach(msg_body)

        # Attach PDF if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype='pdf')
                attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(attachment_path)
                )
                msg.attach(attachment)

        # Send via Gmail SMTP
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)
            print(f"  Email sent to {recipient}: {subject}")
            return True
        except Exception as e:
            print(f"  Failed to send email to {recipient}: {e}")
            return False

    def send_bank_statement_email(
        self,
        recipient: str,
        statement_period: str,
        pdf_path: str
    ) -> bool:
        """Send bank statement email with PDF attachment"""

        subject = f"Bank Statement - {statement_period}"

        body_text = f"""
Bank Statement

Please find attached the bank statement for the period: {statement_period}

This statement includes all transactions processed during the above period.

Acme Technologies Private Limited
        """.strip()

        body_html = f"""
<html>
<body>
<h3>Bank Statement</h3>
<p>Please find attached the bank statement for the period: <strong>{statement_period}</strong></p>
<p>This statement includes all transactions processed during the above period.</p>
<p><strong>Acme Technologies Private Limited</strong></p>
</body>
</html>
        """.strip()

        return self._send_email_with_attachment(
            recipient=recipient,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            attachment_path=pdf_path
        )

    def send_pipeline_summary(
        self,
        recipient: str,
        results: dict
    ) -> bool:
        """Send pipeline execution summary email"""
        from datetime import datetime

        run_date = results.get('run_date', datetime.now())
        invoices = results.get('invoices_generated', 0)
        bills = results.get('bills_generated', 0)
        transactions = results.get('transactions_generated', 0)
        pdfs = results.get('pdfs_generated', 0)
        emails = results.get('emails_sent', 0)
        bank_statement_sent = results.get('bank_statement_sent', False)
        errors = results.get('errors', [])

        status = "SUCCESS" if not errors else "COMPLETED WITH ERRORS"
        status_emoji = "✅" if not errors else "⚠️"

        subject = f"{status_emoji} Komplai Pipeline Summary - {run_date.strftime('%Y-%m-%d')}"

        # Build error section
        error_text = ""
        error_html = ""
        if errors:
            error_text = "\n\nERRORS:\n" + "\n".join(f"  - {e}" for e in errors)
            error_html = "<h3 style='color: #dc3545;'>Errors</h3><ul>" + "".join(f"<li>{e}</li>" for e in errors) + "</ul>"

        bank_stmt_text = "\n  Bank Statement: Sent (biweekly)" if bank_statement_sent else ""

        body_text = f"""
Komplai Demo Pipeline - Weekly Run Summary

Status: {status}
Run Date: {run_date.strftime('%Y-%m-%d %H:%M:%S')}

RESULTS:
  Invoices Generated: {invoices}
  Bills Generated: {bills}
  Bank Transactions: {transactions}
  PDFs Generated: {pdfs}
  Emails Sent: {emails}{bank_stmt_text}
{error_text}

---
This is an automated message from the Komplai Demo Pipeline.
        """.strip()

        body_html = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<div style="background: {'#28a745' if not errors else '#ffc107'}; color: white; padding: 20px; text-align: center;">
    <h1 style="margin: 0;">{status_emoji} Pipeline {status}</h1>
    <p style="margin: 5px 0 0 0;">{run_date.strftime('%A, %B %d, %Y at %H:%M:%S')}</p>
</div>

<div style="padding: 20px;">
    <h3>Results Summary</h3>
    <table style="width: 100%; border-collapse: collapse;">
        <tr style="background: #f8f9fa;">
            <td style="padding: 10px; border: 1px solid #dee2e6;">Invoices Generated</td>
            <td style="padding: 10px; border: 1px solid #dee2e6; text-align: right;"><strong>{invoices}</strong></td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #dee2e6;">Bills Generated</td>
            <td style="padding: 10px; border: 1px solid #dee2e6; text-align: right;"><strong>{bills}</strong></td>
        </tr>
        <tr style="background: #f8f9fa;">
            <td style="padding: 10px; border: 1px solid #dee2e6;">Bank Transactions</td>
            <td style="padding: 10px; border: 1px solid #dee2e6; text-align: right;"><strong>{transactions}</strong></td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #dee2e6;">PDFs Generated</td>
            <td style="padding: 10px; border: 1px solid #dee2e6; text-align: right;"><strong>{pdfs}</strong></td>
        </tr>
        <tr style="background: #f8f9fa;">
            <td style="padding: 10px; border: 1px solid #dee2e6;">Emails Sent</td>
            <td style="padding: 10px; border: 1px solid #dee2e6; text-align: right;"><strong>{emails}</strong></td>
        </tr>
        {'<tr><td style="padding: 10px; border: 1px solid #dee2e6;">Bank Statement</td><td style="padding: 10px; border: 1px solid #dee2e6; text-align: right;"><strong>Sent (biweekly)</strong></td></tr>' if bank_statement_sent else ''}
    </table>

    {error_html}
</div>

<div style="background: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #6c757d;">
    This is an automated message from the Komplai Demo Pipeline.
</div>
</body>
</html>
        """.strip()

        return self._send_email_with_attachment(
            recipient=recipient,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            attachment_path=None
        )
