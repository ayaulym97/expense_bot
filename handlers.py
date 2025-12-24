"""
Message and command handlers for the Expense Tracker Bot.
Handles user interactions and bot commands.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from typing import Optional

from config import Config
from validators import ExpenseInput, ParsedMessage
from google_service import GoogleSheetsService


# Initialize router
router = Router()

# Initialize Google Sheets service
sheets_service = GoogleSheetsService()


class ExpenseStates(StatesGroup):
    """FSM states for expense input."""
    waiting_for_category = State()


def is_user_allowed(user_id: int) -> bool:
    """
    Check if user is in the whitelist.
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        bool: True if user is allowed, False otherwise
    """
    return user_id in Config.ALLOWED_USERS


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """
    Handle /start command.
    
    Args:
        message: Incoming message object
    """
    if not is_user_allowed(message.from_user.id):
        return
    
    welcome_text = (
        "👋 <b>Welcome to Expense Tracker Bot!</b>\n\n"
        "I'll help you track your expenses and save them to Google Sheets.\n\n"
        "<b>How to add an expense:</b>\n"
        "Send a message in this format:\n"
        "<code>category amount comment</code>\n\n"
        "<b>Examples:</b>\n"
        "• <code>food 2500 coffee at Starbucks</code>\n"
        "• <code>transport 500 taxi</code>\n"
        "• <code>shopping 15000 new shoes</code>\n\n"
        "You can also send just a number, and I'll ask for the category.\n\n"
        "<b>Available commands:</b>\n"
        "/start - Show this message\n"
        "/stats - View your statistics\n"
        "/categories - List all categories\n"
        "/help - Get help\n\n"
        "Let's start tracking! 💰"
    )
    
    await message.answer(welcome_text, parse_mode="HTML")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """
    Handle /help command.
    
    Args:
        message: Incoming message object
    """
    if not is_user_allowed(message.from_user.id):
        return
    
    help_text = (
        "📖 <b>How to use Expense Tracker Bot</b>\n\n"
        "<b>Adding expenses:</b>\n"
        "Format: <code>category amount comment</code>\n\n"
        "<b>Examples:</b>\n"
        "✅ <code>food 2500 lunch</code>\n"
        "✅ <code>transport 300</code>\n"
        "✅ <code>2500</code> (I'll ask for category)\n\n"
        "<b>Common categories:</b>\n"
        "food, transport, entertainment, shopping, health, utilities, education, other\n\n"
        "<b>Commands:</b>\n"
        "/stats - View statistics (today/week/month)\n"
        "/categories - See all your categories\n"
        "/help - Show this help message\n\n"
        "All your expenses are automatically saved to Google Sheets! 📊"
    )
    
    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("categories"))
async def cmd_categories(message: Message) -> None:
    """
    Handle /categories command.
    
    Args:
        message: Incoming message object
    """
    if not is_user_allowed(message.from_user.id):
        return
    
    try:
        categories = sheets_service.get_categories()
        
        if categories:
            categories_text = "📂 <b>Available categories:</b>\n\n"
            categories_text += "\n".join([f"• {cat}" for cat in categories])
        else:
            categories_text = (
                "📂 <b>Default categories:</b>\n\n"
                + "\n".join([f"• {cat}" for cat in Config.DEFAULT_CATEGORIES])
            )
        
        await message.answer(categories_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(
            "❌ Error fetching categories. Please try again later.",
            parse_mode="HTML"
        )


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    """
    Handle /stats command.
    
    Args:
        message: Incoming message object
    """
    if not is_user_allowed(message.from_user.id):
        return
    
    user_id = message.from_user.id
    
    try:
        # Get statistics for different periods
        today_stats = sheets_service.get_statistics('today', user_id)
        week_stats = sheets_service.get_statistics('week', user_id)
        month_stats = sheets_service.get_statistics('month', user_id)
        
        stats_text = "📊 <b>Your Expense Statistics</b>\n\n"
        
        # Today
        stats_text += f"<b>📅 Today:</b>\n"
        stats_text += f"Total: <b>{today_stats['total']:.2f}</b> ({today_stats['count']} expenses)\n"
        if today_stats['by_category']:
            for cat, amount in sorted(today_stats['by_category'].items(), key=lambda x: x[1], reverse=True):
                stats_text += f"  • {cat}: {amount:.2f}\n"
        else:
            stats_text += "  No expenses yet\n"
        
        stats_text += "\n"
        
        # This week
        stats_text += f"<b>📆 This Week:</b>\n"
        stats_text += f"Total: <b>{week_stats['total']:.2f}</b> ({week_stats['count']} expenses)\n"
        if week_stats['by_category']:
            for cat, amount in sorted(week_stats['by_category'].items(), key=lambda x: x[1], reverse=True):
                stats_text += f"  • {cat}: {amount:.2f}\n"
        else:
            stats_text += "  No expenses yet\n"
        
        stats_text += "\n"
        
        # This month
        stats_text += f"<b>📈 This Month:</b>\n"
        stats_text += f"Total: <b>{month_stats['total']:.2f}</b> ({month_stats['count']} expenses)\n"
        if month_stats['by_category']:
            for cat, amount in sorted(month_stats['by_category'].items(), key=lambda x: x[1], reverse=True):
                stats_text += f"  • {cat}: {amount:.2f}\n"
        else:
            stats_text += "  No expenses yet\n"
        
        await message.answer(stats_text, parse_mode="HTML")
        
    except Exception as e:
        await message.answer(
            "❌ Error fetching statistics. Please try again later.",
            parse_mode="HTML"
        )


@router.message(ExpenseStates.waiting_for_category)
async def process_category(message: Message, state: FSMContext) -> None:
    """
    Handle category input when user previously sent only amount.
    
    Args:
        message: Incoming message object
        state: FSM context
    """
    if not is_user_allowed(message.from_user.id):
        return
    
    category = message.text.strip().lower()
    
    # Get stored amount from state
    data = await state.get_data()
    amount = data.get('amount')
    
    if not amount:
        await message.answer("❌ Session expired. Please send your expense again.")
        await state.clear()
        return
    
    try:
        # Create expense record
        expense = ExpenseInput(
            category=category,
            amount=amount,
            comment="",
            user_id=message.from_user.id
        )
        
        # Save to Google Sheets
        success = sheets_service.add_expense(expense)
        
        if success:
            await message.answer(
                f"✅ Expense saved!\n\n"
                f"Category: <b>{expense.category}</b>\n"
                f"Amount: <b>{expense.amount:.2f}</b>",
                parse_mode="HTML"
            )
        else:
            await message.answer("❌ Failed to save expense. Please try again.")
        
        await state.clear()
        
    except Exception as e:
        await message.answer(
            f"❌ Error: {str(e)}\n\n"
            "Please check your input and try again.",
            parse_mode="HTML"
        )
        await state.clear()


@router.message(F.text)
async def process_expense(message: Message, state: FSMContext) -> None:
    """
    Process expense input from user.
    
    Args:
        message: Incoming message object
        state: FSM context
    """
    if not is_user_allowed(message.from_user.id):
        return
    
    try:
        # Parse the message
        parsed = ParsedMessage.parse_from_text(message.text)
        
        # Case 1: Only amount provided, ask for category
        if parsed.amount is not None and parsed.category is None:
            await state.set_state(ExpenseStates.waiting_for_category)
            await state.update_data(amount=parsed.amount)
            
            categories_list = ", ".join(Config.DEFAULT_CATEGORIES[:5])
            await message.answer(
                f"💰 Amount: <b>{parsed.amount:.2f}</b>\n\n"
                f"Please send the category for this expense.\n\n"
                f"Examples: {categories_list}",
                parse_mode="HTML"
            )
            return
        
        # Case 2: Category and amount provided
        if parsed.category and parsed.amount:
            expense = ExpenseInput(
                category=parsed.category,
                amount=parsed.amount,
                comment=parsed.comment,
                user_id=message.from_user.id
            )
            
            # Save to Google Sheets
            success = sheets_service.add_expense(expense)
            
            if success:
                response = (
                    f"✅ <b>Expense saved!</b>\n\n"
                    f"Category: <b>{expense.category}</b>\n"
                    f"Amount: <b>{expense.amount:.2f}</b>"
                )
                if expense.comment:
                    response += f"\nComment: {expense.comment}"
                
                await message.answer(response, parse_mode="HTML")
            else:
                await message.answer("❌ Failed to save expense. Please try again.")
        else:
            await message.answer(
                "❌ Invalid format.\n\n"
                "Use: <code>category amount comment</code>\n"
                "Example: <code>food 2500 coffee</code>\n\n"
                "Or send /help for more info.",
                parse_mode="HTML"
            )
    
    except ValueError as e:
        await message.answer(
            f"❌ {str(e)}\n\n"
            "Use: <code>category amount comment</code>\n"
            "Example: <code>food 2500 coffee</code>",
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(
            "❌ An error occurred. Please try again or contact support.",
            parse_mode="HTML"
        )
