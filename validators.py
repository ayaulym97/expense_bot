"""
Validation models for expense tracking bot.
Uses Pydantic for data validation and parsing.
"""

from datetime import datetime
import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ExpenseInput(BaseModel):
    """
    Model for validating expense input data.
    
    Attributes:
        category: Expense category (e.g., food, transport)
        amount: Expense amount (must be positive)
        comment: Optional comment about the expense
        user_id: Telegram user ID
        date: Timestamp of the expense
    """
    
    category: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)
    comment: Optional[str] = Field(default="", max_length=200)
    user_id: int
    date: datetime = Field(default_factory=datetime.now)
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v: str) -> str:
        """
        Validate and normalize category name.
        
        Args:
            v: Category string to validate
            
        Returns:
            Normalized category string (lowercase, stripped)
        """
        return v.strip().lower()
    
    @field_validator('comment')
    @classmethod
    def validate_comment(cls, v: Optional[str]) -> str:
        """
        Validate and normalize comment.
        
        Args:
            v: Comment string to validate
            
        Returns:
            Normalized comment string (stripped)
        """
        if v is None:
            return ""
        return v.strip()
    
    def to_sheet_row(self) -> list:
        """
        Convert expense to a row format for Google Sheets.
        
        Returns:
            List containing [date, category, amount, comment, user_id]
        """
        return [
            self.date.strftime("%Y-%m-%d %H:%M"),
            self.category,
            self.amount,
            self.comment,
            self.user_id
        ]


class ParsedMessage(BaseModel):
    """
    Model for parsed user message.
    
    Attributes:
        category: Expense category (optional if only amount provided)
        amount: Expense amount
        comment: Optional comment
        date: Optional date for the expense
    """
    
    category: Optional[str] = None
    amount: Optional[float] = None
    comment: Optional[str] = ""
    date: Optional[datetime] = None
    
    @staticmethod
    def _parse_date(text: str) -> Optional[datetime]:
        """
        Try to parse date from text.
        
        Supports formats:
        - DD.MM (e.g., 24.12) - current year assumed
        - DD.MM.YYYY (e.g., 24.12.2024)
        - DD.MM.YY (e.g., 24.12.24)
        - DD/MM, DD/MM/YYYY, DD/MM/YY
        
        Returns:
            datetime object or None if not a valid date
        """
        date_patterns = [
            (r'^(\d{1,2})[./](\d{1,2})[./](\d{4})$', '%d.%m.%Y'),  # DD.MM.YYYY
            (r'^(\d{1,2})[./](\d{1,2})[./](\d{2})$', '%d.%m.%y'),  # DD.MM.YY
            (r'^(\d{1,2})[./](\d{1,2})$', '%d.%m'),                 # DD.MM
        ]
        
        text = text.strip()
        
        for pattern, fmt in date_patterns:
            if re.match(pattern, text):
                try:
                    # Normalize separators to dots
                    normalized = text.replace('/', '.')
                    parsed = datetime.strptime(normalized, fmt)
                    
                    # If year not specified, use current year
                    if fmt == '%d.%m':
                        parsed = parsed.replace(year=datetime.now().year)
                    
                    return parsed
                except ValueError:
                    continue
        
        return None
    
    @classmethod
    def parse_from_text(cls, text: str) -> 'ParsedMessage':
        """
        Parse expense data from user text input.
        
        Supports formats:
        - "category amount comment"
        - "category amount"
        - "amount" (only number)
        - "DD.MM category amount comment" (with date)
        - "category amount DD.MM" (date at end)
        
        Args:
            text: User input text
            
        Returns:
            ParsedMessage object with parsed data
            
        Raises:
            ValueError: If text cannot be parsed
        """
        parts = text.strip().split()
        
        if not parts:
            raise ValueError("Empty message")
        
        parsed_date = None
        
        # Check if first part is a date
        first_date = cls._parse_date(parts[0])
        if first_date:
            parsed_date = first_date
            parts = parts[1:]  # Remove date from parts
        # Check if last part is a date
        elif len(parts) > 1:
            last_date = cls._parse_date(parts[-1])
            if last_date:
                parsed_date = last_date
                parts = parts[:-1]  # Remove date from parts
        
        if not parts:
            raise ValueError("Empty message after date")
        
        # Case 1: Only a number (amount)
        if len(parts) == 1:
            try:
                amount = float(parts[0])
                return cls(amount=amount, date=parsed_date)
            except ValueError:
                raise ValueError("Invalid format. Expected: category amount [comment]")
        
        # Case 2: category amount [comment]
        category = parts[0]
        try:
            amount = float(parts[1])
        except ValueError:
            raise ValueError(f"Invalid amount: {parts[1]}")
        
        comment = " ".join(parts[2:]) if len(parts) > 2 else ""
        
        return cls(category=category, amount=amount, comment=comment, date=parsed_date)
