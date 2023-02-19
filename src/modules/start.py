"""
Send a message when the command /start is issued.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from ..utils.util import build_menu
from .sender import sender_handler
from .courier import courier_handler

START_PAGE = 1


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    button_list = [
        InlineKeyboardButton("Courier", callback_data=str(1)),
        InlineKeyboardButton("Sender", callback_data=str(2)),
    ]

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    await update.message.reply_text('Welcome', reply_markup=reply_markup)
    return START_PAGE


START_STATE = {
    START_PAGE: [
        CallbackQueryHandler(courier_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(sender_handler, pattern="^" + str(2) + "$"),
    ]
}
