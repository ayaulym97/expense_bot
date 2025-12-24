"""
Configuration module for the Expense Tracker Bot.
Loads environment variables and provides application settings.
"""

import os
from typing import Set
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""
    
    # Telegram Bot Token
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    
    # Google Sheets Configuration
    GOOGLE_SHEET_NAME: str = os.getenv("GOOGLE_SHEET_NAME", "Expense Tracker")
    GOOGLE_CREDENTIALS_PATH: str = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
    
    # Allowed Users (whitelist)
    ALLOWED_USERS: Set[int] = set()
    
    # Default categories
    DEFAULT_CATEGORIES = [
        "food", "transport", "entertainment", "shopping", 
        "health", "utilities", "education", "other"
    ]
    
    @classmethod
    def load_allowed_users(cls) -> None:
        """Load allowed user IDs from environment variable."""
        users_str = os.getenv("ALLOWED_USERS", "")
        if users_str:
            try:
                cls.ALLOWED_USERS = {int(user_id.strip()) for user_id in users_str.split(",") if user_id.strip()}
            except ValueError:
                print("Warning: Invalid user IDs in ALLOWED_USERS. Using empty whitelist.")
                cls.ALLOWED_USERS = set()
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required configuration is present.
        
        Returns:
            bool: True if configuration is valid, False otherwise.
        """
        if not cls.TELEGRAM_TOKEN:
            print("Error: TELEGRAM_TOKEN is not set in environment variables.")
            return False
        
        if not os.path.exists(cls.GOOGLE_CREDENTIALS_PATH):
            print(f"Error: Google credentials file not found at {cls.GOOGLE_CREDENTIALS_PATH}")
            return False
        
        if not cls.ALLOWED_USERS:
            print("Warning: No users in whitelist. Bot will not respond to anyone.")
        
        return True


# Load allowed users on module import
Config.load_allowed_users()
