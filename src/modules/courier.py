from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from .end import end_handler
from .get_list_of_offers import get_list_of_offers_handler
from .active_offers import active_offers_handler

from src.data.pages import *

async def courier_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Get list of offers", callback_data=str(1))],
        [InlineKeyboardButton("Edit filters", callback_data=str(2))],
        [InlineKeyboardButton("Get your active offers", callback_data=str(3))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Choose what you want to do", reply_markup=reply_markup
    )

    return COURIER_PAGE
