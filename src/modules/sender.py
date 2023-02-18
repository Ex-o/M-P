"""
Sender main page
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from ..utils.util import build_menu

SENDER_PAGE = 3


async def SenderHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    button_list = [
        InlineKeyboardButton("My offers", callback_data=str(1)),
        InlineKeyboardButton("Approves", callback_data=str(2)),
        InlineKeyboardButton("Create offer", callback_data=str(3)),
        InlineKeyboardButton("Cancel offer", callback_data=str(4)),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=4))
    await update.message.reply_text('Choose what you want to do', reply_markup=reply_markup)
    return SENDER_PAGE
