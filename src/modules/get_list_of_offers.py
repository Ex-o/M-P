import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from ..db.utils import set_offer_match, get_own_offers
from ..utils.util import to_offer
from ..data.pages import *


async def get_list_of_own_offers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    offers = await get_own_offers(user_id)

    if len(offers) == 0:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Go back", callback_data=str(9999))]])
        await query.edit_message_text(
            text='You don\'t have any active offers! Go back and create some!', reply_markup=reply_markup
        )
        return SENDER_PAGE

    keyboard = [
        [InlineKeyboardButton("Go back", callback_data=str(9999))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=to_offer(offers), reply_markup=reply_markup
    )
    return SENDER_PAGE
