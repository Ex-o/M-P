from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.data.pages import *


async def courier_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Get list of offers", callback_data=str(1))],
        [InlineKeyboardButton("Edit filters", callback_data=str(2))],
        [InlineKeyboardButton("Get your active offers", callback_data=str(3))],
        [InlineKeyboardButton("🔙 Go Back", callback_data="go_back")],
    ]
    context.user_data['page'] = 0
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Choose what you want to do", reply_markup=reply_markup
    )

    return COURIER_PAGE
