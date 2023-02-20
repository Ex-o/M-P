"""
Sender main page
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.data.pages import *

async def sender_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("My offers", callback_data=str(1))],
        [InlineKeyboardButton("Approves", callback_data=str(2))],
        [InlineKeyboardButton("Create offer", callback_data=str(3))],
        [InlineKeyboardButton("Cancel offer", callback_data=str(4))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Choose what you want to do", reply_markup=reply_markup
    )

    return SENDER_PAGE



