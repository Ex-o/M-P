from telegram import Update
from telegram.ext import ContextTypes

from src.db.utils import get_temp_order

async def get_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""

    offer = await get_temp_order(update.message.text)
    await update.message.reply_text(offer[0]["order_json"])

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Khaled got ice cream, YAY!")