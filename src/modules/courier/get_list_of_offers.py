import math

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from ...db.utils import get_filters, get_offers_by_status, set_offer_match
from ...utils.util import to_offer, filter_offers
from ...data.pages import *


async def _show_offers_page(query, offers, page) -> int:
    if len(offers) == 0:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Go Back", callback_data="go_back")]])
        await query.edit_message_text(
            text='Oops, there is no offer for you now. Try again later.', reply_markup=reply_markup
        )
        return GET_LIST_OF_OFFERS_PAGE

    left = max(min(len(offers) - 5, page * 5), 0)
    offers = offers[left:min(len(offers), left + 5)]

    reply = ""

    for idx, offer in enumerate(offers, start=1):
        reply += f'{idx}. {to_offer([offer])}'

    keyboard = [[InlineKeyboardButton(f"Accept {x}",
                                      callback_data=str(offers[x - 1]['id']))]
                for x in range(1, len(offers) + 1)]
    keyboard.append([InlineKeyboardButton('Previous page', callback_data='##Previous page##'),
                     InlineKeyboardButton('Next page', callback_data='##Next page##')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        'Please select which offer you want to get:\n' + reply, reply_markup=reply_markup
    )

    return GET_LIST_OF_OFFERS_PAGE


async def get_list_of_others_offers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user

    offers = filter_offers(
        await get_offers_by_status('paid', user.id),
        await get_filters(user.id),
    )

    query = update.callback_query
    await query.answer()

    context.user_data['page'] = min(max(0, context.user_data['page']), math.floor((len(offers) - 1) / 5))

    return await _show_offers_page(query, offers, context.user_data['page'])


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


async def next_page_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user

    offers = filter_offers(
        await get_offers_by_status('paid', user.id),
        await get_filters(user.id),
    )

    query = update.callback_query
    await query.answer()

    context.user_data['page'] += 1
    context.user_data['page'] = max(0, min(context.user_data['page'], math.floor((len(offers) - 1) / 5)))

    return await _show_offers_page(query, offers, context.user_data['page'])


async def prev_page_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user

    offers = filter_offers(
        await get_offers_by_status('paid', user.id),
        await get_filters(user.id),
    )

    query = update.callback_query
    await query.answer()

    context.user_data['page'] -= 1
    context.user_data['page'] = max(0, min(context.user_data['page'], math.floor((len(offers) - 1) / 5)))

    return await _show_offers_page(query, offers, context.user_data['page'])
