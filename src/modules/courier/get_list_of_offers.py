from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from ...db.utils import get_filters, get_offers_by_status, set_offer_match
from ...utils.util import to_offer, filter_offers
from ...data.pages import *


async def get_list_of_others_offers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user

    filters = await get_filters(user.id)
    offers = await get_offers_by_status('paid', user.id)
    offers = filter_offers(offers, filters)

    query = update.callback_query
    await query.answer()

    if len(offers) == 0:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Go Back", callback_data="go_back")]])
        await query.edit_message_text(
            text='Oops, there is no offer for you now. Try again later.', reply_markup=reply_markup
        )
        return GET_LIST_OF_OFFERS_PAGE

    page = context.user_data['page']
    left = min(len(offers) - 5, page * 5)
    left = max(left, 0)
    offers = offers[left:min(len(offers), left+5)]

    reply = ""

    for idx, offer in enumerate(offers, start=1):
        reply += f'{idx}. {to_offer([offer])}'

    keyboard = [[InlineKeyboardButton(f"Accept {x}",
                                      callback_data=str(offers[x-1]['id']))]
                for x in range(1, len(offers) + 1)]
    keyboard.append([InlineKeyboardButton('Previous page', callback_data='##Previous page##'),
                     InlineKeyboardButton('Next page', callback_data='##Next page##')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        'Please select which offer you want to get:\n' + reply, reply_markup=reply_markup
    )

    return GET_LIST_OF_OFFERS_PAGE


async def ready_to_complete_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    user_id = user.id
    offer_id = query.data
    await set_offer_match(user_id, offer_id)

    keyboard = [
        [
            InlineKeyboardButton("Accept more offers?", callback_data="accept_more"),
            InlineKeyboardButton("End", callback_data="end"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Here are the details about the customer: TODO\nWhat next?", reply_markup=reply_markup
    )

    return GET_LIST_OF_OFFERS_PAGE
