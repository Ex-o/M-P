"""
Send a message when the command /start is issued.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ..data.pages import *

from ..utils.util import build_menu
from ..db.utils import register_user


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user

    if update.message is not None:
        await register_user(user.id, user.full_name, update.message.chat_id)

    button_list = [
        InlineKeyboardButton("Courier", callback_data=str(1)),
        InlineKeyboardButton("Sender", callback_data=str(2)),
    ]

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    if update.message is not None:
        await update.message.reply_text('Welcome', reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text('Welcome', reply_markup=reply_markup)
    return START_PAGE
