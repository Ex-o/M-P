from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ..utils.util import to_offer
from ..db.utils import get_active_offers

from ..data.pages import *


async def _show_offers_page(query, offers) -> int:
    if len(offers) == 0:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Go Back", callback_data="go_back")]])
        await query.edit_message_text(
            text='You don\'t have any active offers yet!\n\n'
                 ''
                 'Hint: Try to get matches in `Get list of offers`', reply_markup=reply_markup
        )
        return ACTIVE_OFFERS_PAGE

    reply = ""

    for idx, offer in enumerate(offers, start=1):
        reply += f'{idx}. {to_offer([offer])}'

    keyboard = [[InlineKeyboardButton(f"Open {x}",
                                      callback_data=str(offers[x - 1]['id']))]
                for x in range(1, len(offers) + 1)]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        'Please select which offer you want to update:\n' + reply, reply_markup=reply_markup
    )

    return ACTIVE_OFFERS_PAGE


async def active_offers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    offers = await get_active_offers(user_id)

    return await _show_offers_page(query, offers)


async def active_offers_update_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    # TODO: update status of the matched_offer
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Go Back", callback_data="go_back_2")]])

    await query.edit_message_text(
        text="TODO", reply_markup=reply_markup
    )

    return ACTIVE_OFFERS_PAGE
