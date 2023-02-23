import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler

from ..db.utils import get_offers_since, get_user, update_last_offer_of_user, set_offer_match, get_own_offers
from ..utils.util import to_offer
from ..data.pages import *


def _get_filters():
    # TODO: implement logic, should return list of users places where he gonna visit
    return None


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

    filters = _get_filters()
    offers = get_offers_since(get_user(user.id)['last_offer'])

    if filters:
        offers = [offer for offer in offers if offer[0] in filters]

    offer = offers[0] if len(offers) > 0 else None

    if offer:
        update_last_offer_of_user(user.id, offer['id'])

    query = update.callback_query
    await query.answer()

    if len(offers) == 0:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Go back", callback_data=str(3))]])
        await query.edit_message_text(
            text='Oops, there is no offer for you now. Try again later.', reply_markup=reply_markup
        )
        return GET_LIST_OF_OFFERS_PAGE

    context.user_data['last_offer_id'] = offer['id']

    keyboard = [
        [InlineKeyboardButton("Ready to complete it", callback_data=str(1))],
        [InlineKeyboardButton("Skip offer", callback_data=str(2))],
        [InlineKeyboardButton("Go back", callback_data=str(3))],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=to_offer([offer]), reply_markup=reply_markup
    )

    return GET_LIST_OF_OFFERS_PAGE


async def ready_to_complete_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    user_id = user.id
    offer_id = context.user_data['last_offer_id']

    set_offer_match(user_id, offer_id)

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Continue to watch offers", callback_data=str(4)),
            InlineKeyboardButton("Go back", callback_data=str(3)),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Here are the details about the customer: TODO\nWhat next?", reply_markup=reply_markup
    )

