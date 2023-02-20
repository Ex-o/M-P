"""
Sender main page
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from .end import end_handler
from .create_offer import create_offer_handler
from .cancel_offer import cancel_offer_handler
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


SENDER_STATE = {
    SENDER_PAGE: [
        CallbackQueryHandler(end_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(end_handler, pattern="^" + str(2) + "$"),
        CallbackQueryHandler(create_offer_handler, pattern="^" + str(3) + "$"),
        CallbackQueryHandler(cancel_offer_handler, pattern="^" + str(4) + "$"),
    ]
}
