"""
Komplai Demo Pipeline - Google Sheets Manager
Handles syncing data to Google Sheets
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import os
import json
import base64
from typing import List, Dict, Optional
from datetime import datetime


class SheetsManager:
    """Manage Google Sheets operations for the demo pipeline"""

    def __init__(self, credentials_path: Optional[str] = None, sheet_id: Optional[str] = None):
        """
        Initialize Google Sheets Manager

        Credentials can be provided via:
        1. GOOGLE_CREDENTIALS_JSON env var (base64-encoded JSON) - for production
        2. credentials_path parameter - for local development

        Sheet ID can be provided via:
        1. GOOGLE_SHEET_ID env var - for production
        2. sheet_id parameter - for local development

        Args:
            credentials_path: Path to service account JSON credentials (optional)
            sheet_id: Google Sheets ID (optional)
        """
        self.credentials_path = credentials_path
        self.sheet_id = sheet_id or os.environ.get('GOOGLE_SHEET_ID')
        self.client = None
        self.spreadsheet = None

        if not self.sheet_id:
            raise ValueError("Sheet ID required via sheet_id parameter or GOOGLE_SHEET_ID env var")

        # Initialize connection
        self._connect()

    def _get_credentials(self):
        """
        Get credentials from environment variable or file

        Returns:
            ServiceAccountCredentials object
        """
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        # Check for base64-encoded JSON in environment variable (production)
        creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        if creds_json:
            try:
                # Decode base64 and parse JSON
                creds_data = json.loads(base64.b64decode(creds_json))
                return ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
            except Exception as e:
                print(f"⚠ Failed to load credentials from env var: {e}")

        # Fall back to file-based credentials (local development)
        if self.credentials_path and os.path.exists(self.credentials_path):
            return ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_path, scope
            )

        raise ValueError(
            "No Google credentials found. Provide either:\n"
            "  - GOOGLE_CREDENTIALS_JSON env var (base64-encoded JSON)\n"
            "  - credentials_path parameter pointing to service account JSON file"
        )

    def _connect(self):
        """Establish connection to Google Sheets"""
        try:
            # Get credentials (from env var or file)
            creds = self._get_credentials()
            self.client = gspread.authorize(creds)

            # Open spreadsheet
            self.spreadsheet = self.client.open_by_key(self.sheet_id)

            print(f"✓ Connected to Google Sheet: {self.spreadsheet.title}")

        except Exception as e:
            print(f"✗ Error connecting to Google Sheets: {e}")
            raise

    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        """
        Read data from a Google Sheet

        Args:
            sheet_name: Name of the worksheet

        Returns:
            DataFrame with the sheet data
        """
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            data = worksheet.get_all_records()
            df = pd.DataFrame(data)
            print(f"✓ Read {len(df)} rows from Google Sheet: {sheet_name}")
            return df

        except Exception as e:
            print(f"✗ Error reading Google Sheet {sheet_name}: {e}")
            raise

    def append_to_sheet(self, sheet_name: str, data: List[Dict]) -> bool:
        """
        Append rows to a Google Sheet

        Args:
            sheet_name: Name of the worksheet
            data: List of dictionaries with row data

        Returns:
            True if successful, False otherwise
        """
        if not data:
            print(f"⚠ No data to append to Google Sheet: {sheet_name}")
            return True

        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)

            # Get existing headers from the sheet to ensure correct column order
            existing_headers = worksheet.row_values(1)

            # Convert data to DataFrame
            df = pd.DataFrame(data)

            # Reorder columns to match existing sheet headers
            # Only include columns that exist in the sheet (don't add new columns)
            ordered_columns = [col for col in existing_headers if col in df.columns]
            df = df[ordered_columns]

            # Convert datetime columns to strings
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
                elif df[col].dtype == 'object':
                    # Handle any Timestamp objects in object columns
                    df[col] = df[col].apply(
                        lambda x: x.strftime('%Y-%m-%d %H:%M:%S')
                        if isinstance(x, (pd.Timestamp, datetime))
                        else x
                    )

            # Convert to list of lists (without header)
            rows = df.values.tolist()

            # Replace NaN, Inf, -Inf with None (JSON compliant) in each cell
            sanitized_rows = []
            for row in rows:
                sanitized_row = []
                for value in row:
                    if isinstance(value, float):
                        if np.isnan(value) or np.isinf(value):
                            sanitized_row.append(None)
                        else:
                            sanitized_row.append(value)
                    else:
                        sanitized_row.append(value)
                sanitized_rows.append(sanitized_row)

            # Append rows
            worksheet.append_rows(sanitized_rows, value_input_option='USER_ENTERED')

            print(f"✓ Appended {len(data)} rows to Google Sheet: {sheet_name}")
            return True

        except Exception as e:
            print(f"✗ Error appending to Google Sheet {sheet_name}: {e}")
            import traceback
            traceback.print_exc()
            return False

    def get_all_worksheets(self) -> List[str]:
        """
        Get list of all worksheet names

        Returns:
            List of worksheet names
        """
        try:
            worksheets = self.spreadsheet.worksheets()
            return [ws.title for ws in worksheets]
        except Exception as e:
            print(f"✗ Error getting worksheets: {e}")
            return []

    def clear_sheet(self, sheet_name: str, keep_header: bool = True) -> bool:
        """
        Clear all data from a sheet (optionally keeping header)

        Args:
            sheet_name: Name of the worksheet
            keep_header: If True, keep the first row (header)

        Returns:
            True if successful
        """
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)

            if keep_header:
                # Get all data
                all_data = worksheet.get_all_values()
                if len(all_data) > 1:
                    # Clear from row 2 onwards
                    worksheet.delete_rows(2, len(all_data))
            else:
                # Clear entire sheet
                worksheet.clear()

            print(f"✓ Cleared Google Sheet: {sheet_name}")
            return True

        except Exception as e:
            print(f"✗ Error clearing Google Sheet {sheet_name}: {e}")
            return False

    def batch_update(self, sheet_name: str, data: List[Dict], start_row: int = None) -> bool:
        """
        Batch update rows in a sheet

        Args:
            sheet_name: Name of the worksheet
            data: List of dictionaries with row data
            start_row: Starting row number (None = append)

        Returns:
            True if successful
        """
        if not data:
            return True

        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)

            # Get existing headers from the sheet to ensure correct column order
            existing_headers = worksheet.row_values(1)

            df = pd.DataFrame(data)

            # Reorder columns to match existing sheet headers
            ordered_columns = [col for col in existing_headers if col in df.columns]
            df = df[ordered_columns]

            # Convert datetime columns
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

            if start_row is None:
                # Append
                return self.append_to_sheet(sheet_name, data)
            else:
                # Update at specific row
                rows = df.values.tolist()

                # Replace NaN, Inf, -Inf with None (JSON compliant) in each cell
                sanitized_rows = []
                for row in rows:
                    sanitized_row = []
                    for value in row:
                        if isinstance(value, float):
                            if np.isnan(value) or np.isinf(value):
                                sanitized_row.append(None)
                            else:
                                sanitized_row.append(value)
                        else:
                            sanitized_row.append(value)
                    sanitized_rows.append(sanitized_row)

                cell_range = f'A{start_row}:{chr(65 + len(df.columns) - 1)}{start_row + len(rows) - 1}'
                worksheet.update(cell_range, sanitized_rows, value_input_option='USER_ENTERED')

                print(f"✓ Updated {len(data)} rows in Google Sheet: {sheet_name}")
                return True

        except Exception as e:
            print(f"✗ Error batch updating Google Sheet {sheet_name}: {e}")
            return False


if __name__ == "__main__":
    # Test Google Sheets Manager
    print("\n" + "="*60)
    print("TESTING GOOGLE SHEETS MANAGER")
    print("="*60)

    # Initialize
    credentials_path = "dummy-data-483609-2b5f128b43ad.json"
    sheet_id = "1KXGIa1G8q7PMMC5FSbj7mzgIaszRMHsikevdVpw_0Aw"

    try:
        manager = SheetsManager(credentials_path, sheet_id)

        # Test getting worksheets
        print("\n[Worksheets]")
        worksheets = manager.get_all_worksheets()
        print(f"Available sheets: {worksheets}")

        # Test reading (if Entities sheet exists)
        if 'Entities' in worksheets:
            print("\n[Reading Data]")
            entities = manager.read_sheet('Entities')
            print(f"Entities: {len(entities)} rows, {len(entities.columns)} columns")

        print("\n" + "="*60)
        print("✓ GOOGLE SHEETS MANAGER TEST COMPLETE")
        print("="*60)

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
