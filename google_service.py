"""
Google Sheets service module.
Handles all interactions with Google Sheets API for expense tracking.
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from config import Config
from validators import ExpenseInput


class GoogleSheetsService:
    """Service class for Google Sheets operations."""
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    HEADER_ROW = ["Date", "Category", "Amount", "Comment", "User ID"]
    
    def __init__(self):
        """Initialize Google Sheets service with credentials."""
        self.client = None
        self.sheet = None
        self.worksheet = None
        self._connect()
    
    def _connect(self) -> None:
        """
        Establish connection to Google Sheets.
        
        Raises:
            Exception: If connection fails
        """
        try:
            creds = Credentials.from_service_account_file(
                Config.GOOGLE_CREDENTIALS_PATH,
                scopes=self.SCOPES
            )
            self.client = gspread.authorize(creds)
            self._get_or_create_sheet()
        except Exception as e:
            print(f"Error connecting to Google Sheets: {e}")
            raise
    
    def _get_or_create_sheet(self) -> None:
        """Get existing spreadsheet or create a new one with header row."""
        try:
            # Try to open existing spreadsheet
            self.sheet = self.client.open(Config.GOOGLE_SHEET_NAME)
            self.worksheet = self.sheet.sheet1
            
            # Check if header exists
            if not self.worksheet.row_values(1):
                self.worksheet.append_row(self.HEADER_ROW)
        except gspread.SpreadsheetNotFound:
            # Create new spreadsheet
            self.sheet = self.client.create(Config.GOOGLE_SHEET_NAME)
            self.worksheet = self.sheet.sheet1
            self.worksheet.append_row(self.HEADER_ROW)
            print(f"Created new spreadsheet: {Config.GOOGLE_SHEET_NAME}")
    
    def add_expense(self, expense: ExpenseInput) -> bool:
        """
        Add a new expense record to the spreadsheet.
        
        Args:
            expense: ExpenseInput object containing expense data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            row = expense.to_sheet_row()
            self.worksheet.append_row(row)
            return True
        except Exception as e:
            print(f"Error adding expense: {e}")
            return False
    
    def get_all_records(self) -> List[Dict]:
        """
        Fetch all expense records from the sheet.
        
        Returns:
            List of dictionaries containing expense records
        """
        try:
            records = self.worksheet.get_all_records()
            return records
        except Exception as e:
            print(f"Error fetching records: {e}")
            return []
    
    def get_records_by_date_range(
        self, 
        start_date: datetime, 
        end_date: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Get expense records within a date range.
        
        Args:
            start_date: Start of date range
            end_date: End of date range (defaults to now)
            
        Returns:
            List of expense records within the date range
        """
        if end_date is None:
            end_date = datetime.now()
        
        all_records = self.get_all_records()
        filtered_records = []
        
        for record in all_records:
            try:
                record_date = datetime.strptime(record['Date'], "%Y-%m-%d %H:%M")
                if start_date <= record_date <= end_date:
                    filtered_records.append(record)
            except (ValueError, KeyError):
                continue
        
        return filtered_records
    
    def get_statistics(self, period: str, user_id: int) -> Dict:
        """
        Calculate expense statistics for a given period.
        
        Args:
            period: One of 'today', 'week', 'month'
            user_id: Telegram user ID to filter by
            
        Returns:
            Dictionary containing total and category breakdown
        """
        now = datetime.now()
        
        # Determine date range based on period
        if period == 'today':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'week':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'month':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            return {"error": "Invalid period"}
        
        # Get records for the period
        records = self.get_records_by_date_range(start_date, now)
        
        # Filter by user_id
        user_records = [r for r in records if r.get('User ID') == user_id]
        
        # Calculate statistics
        total = 0.0
        by_category = {}
        
        for record in user_records:
            try:
                amount = float(record.get('Amount', 0))
                category = record.get('Category', 'other')
                
                total += amount
                by_category[category] = by_category.get(category, 0) + amount
            except (ValueError, TypeError):
                continue
        
        return {
            "period": period,
            "total": total,
            "by_category": by_category,
            "count": len(user_records)
        }
    
    def get_categories(self) -> List[str]:
        """
        Get list of unique categories from all records.
        
        Returns:
            List of category names
        """
        records = self.get_all_records()
        categories = set()
        
        for record in records:
            category = record.get('Category')
            if category:
                categories.add(category)
        
        # Combine with default categories
        all_categories = categories.union(set(Config.DEFAULT_CATEGORIES))
        return sorted(list(all_categories))
