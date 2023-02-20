from telegram import Update
from telegram.ext import ContextTypes
from src.data.pages import *

from src.db.utils import get_active_sender_offers

CANCEL_OFFER_STATE = {
    CANCEL_OFFER_PAGE: []
}


async def cancel_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    active_offers = get_active_sender_offers(user_id)

    if len(active_offers) == 0:
        await query.edit_message_text(
            'You don\'t have any active offers!'
        )

    return SENDER_STATE

    await query.edit_message_text(
        'Alright, please specify where you want to meet the courier in Innopolis'
    )
    return CANCEL_OFFER_PAGE
