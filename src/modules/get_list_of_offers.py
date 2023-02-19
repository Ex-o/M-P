from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler

from ..db.utils import get_offers, get_user, update_last_offer_of_user, set_offer_match
from .end import end_handler

GET_LIST_OF_OFFERS_PAGE = 10


def _get_filters():
    # TODO: implement logic, should return list of users places where he gonna visit
    return None


def _to_str(filters):
    res = ""
    for filter in filters:
        res += 'Offer:\n' \
               f'Details: {filter[0]}\n' \
               f'Needs to be delivered to: {filter[1]}\n' \
               f'Pays: {filter[2]}\n\n'

    return res


async def get_list_of_offers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user

    filters = _get_filters()
    offers = get_offers(get_user(user.id)[2])

    if filters:
        offers = [offer for offer in offers if offer[0] in filters]

    offer = offers[0] if len(offers) > 0 else None

    if offer:
        update_last_offer_of_user(user.id, offer[3])

    query = update.callback_query
    await query.answer()

    if len(offers) == 0:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Ready to complete it", callback_data=str(1))]])
        await query.edit_message_text(
            text='Oops, there is no offer for you now. Try again later.', reply_markup=reply_markup
        )
        return GET_LIST_OF_OFFERS_PAGE

    context['last_offer_id'] = offer[3]

    keyboard = [
        [
            InlineKeyboardButton("Ready to complete it", callback_data=str(1)),
            InlineKeyboardButton("Skip offer", callback_data=str(2)),
            InlineKeyboardButton("Go back", callback_data=str(3)),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=_to_str([offer]), reply_markup=reply_markup
    )

    return GET_LIST_OF_OFFERS_PAGE


async def ready_to_complete_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    user_id = user.id
    offer_id = context['last_offer_id']

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

GET_LIST_OF_OFFERS_STATE = {
    GET_LIST_OF_OFFERS_PAGE: [
        CallbackQueryHandler(ready_to_complete_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(get_list_of_offers_handler, pattern="^" + str(2) + "$"),
        CallbackQueryHandler(end_handler, pattern="^" + str(3) + "$"),
        CallbackQueryHandler(get_list_of_offers_handler, pattern="^" + str(4) + "$"),
    ],
}