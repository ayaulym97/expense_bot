"""
Main bot module for Expense Tracker Bot.
Initializes and runs the Telegram bot with aiogram 3.x.
"""

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import CommandStart

from config import Config
from handlers import router


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    """
    Actions to perform on bot startup.
    
    Args:
        bot: Bot instance
    """
    logger.info("Bot is starting...")
    logger.info(f"Allowed users: {Config.ALLOWED_USERS}")
    
    # Set bot commands
    from aiogram.types import BotCommand
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="stats", description="View statistics"),
        BotCommand(command="categories", description="List categories"),
        BotCommand(command="help", description="Get help"),
    ]
    await bot.set_my_commands(commands)
    logger.info("Bot commands set successfully")


async def on_shutdown(bot: Bot) -> None:
    """
    Actions to perform on bot shutdown.
    
    Args:
        bot: Bot instance
    """
    logger.info("Bot is shutting down...")
    await bot.session.close()


async def main() -> None:
    """
    Main function to initialize and run the bot.
    """
    # Validate configuration
    if not Config.validate():
        logger.error("Configuration validation failed. Exiting.")
        sys.exit(1)
    
    # Initialize bot with default properties
    bot = Bot(
        token=Config.TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Initialize dispatcher
    dp = Dispatcher()
    
    # Register routers
    dp.include_router(router)
    
    # Register startup and shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Add middleware for access control
    @dp.message.middleware()
    async def access_control_middleware(handler, event: Message, data: dict):
        """
        Middleware to check if user is allowed to use the bot.
        
        Args:
            handler: Next handler in chain
            event: Incoming message
            data: Additional data
            
        Returns:
            Result of handler or None if user is not allowed
        """
        user_id = event.from_user.id
        
        if user_id not in Config.ALLOWED_USERS:
            logger.warning(f"Unauthorized access attempt from user {user_id}")
            # Silently ignore messages from unauthorized users
            return None
        
        return await handler(event, data)
    
    # Start polling
    try:
        logger.info("Starting bot polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Error during polling: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
