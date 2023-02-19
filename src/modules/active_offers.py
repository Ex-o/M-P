from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from .end import end_handler
from ..utils.util import to_offer
from ..db.utils import get_offers

ACTIVE_OFFERS_PAGE = 11


async def active_offers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    user_id = update.effective_user.id

    offers = get_offers(user_id)

    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Go back", callback_data=str(1))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=to_offer(offers), reply_markup=reply_markup
    )

    return ACTIVE_OFFERS_PAGE


ACTIVE_OFFERS_STATE = {
    ACTIVE_OFFERS_PAGE: [
        CallbackQueryHandler(end_handler, pattern="^" + str(1) + "$"),
    ],
}