from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from pages import *

from src.db.utils import get_active_sender_offers

CANCEL_OFFER_STATE = []


async def cancel_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    active_offers = get_active_sender_offers(user_id)

    if len(active_offers) == 0:
        await query.edit_message_text(
            'You don\'t have any active offers!'
        )

    return START_PAGE

    await query.edit_message_text(
        'Alright, please specify where you want to meet the courier in Innopolis'
    )
    return CANCEL_OFFER_PAGE
