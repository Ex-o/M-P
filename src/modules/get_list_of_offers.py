import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from ..db.utils import get_user, update_last_offer_of_user, set_offer_match, get_own_offers, \
    get_filters, get_offers_by_status
from ..utils.util import to_offer, filter_offers
from ..data.pages import *


async def get_list_of_own_offers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    offers = get_own_offers(user_id)

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


async def get_list_of_others_offers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user

    filters = await get_filters(user.id)
    offers = get_offers_by_status('paid', user.id)

    offers = filter_offers(offers, filters)

    query = update.callback_query
    await query.answer()

    if len(offers) == 0:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Go back", callback_data="go_back")]])
        await query.edit_message_text(
            text='Oops, there is no offer for you now. Try again later.', reply_markup=reply_markup
        )
        return GET_LIST_OF_OFFERS_PAGE

    reply = ""
    context.user_data['pending_offers'] = {}

    for idx, offer in enumerate(offers, start=1):
        reply += f'{idx}. {to_offer([offer])}'
        context.user_data['pending_offers'][idx] = offer['id']

    keyboard = [[InlineKeyboardButton(f"Accept {x}",
                                      callback_data=str(context.user_data['pending_offers'][x]))]
                for x in range(1, len(offers) + 1)]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        'Please select which offer you want to get:', reply_markup=reply_markup
    )

    return GET_LIST_OF_OFFERS_PAGE


async def ready_to_complete_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    user_id = user.id
    offer_id = query.data
    set_offer_match(user_id, offer_id)

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

