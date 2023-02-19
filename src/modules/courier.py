from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from .end import end_handler

COURIER_PAGE = 2


async def courier_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("YES", callback_data=str(3)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="ARE YOU SUREEEE?????", reply_markup=reply_markup
    )
    return COURIER_PAGE


COURIER_STATE = {
    COURIER_PAGE: [
        CallbackQueryHandler(end_handler, pattern="^" + str(3) + "$")
    ],
}