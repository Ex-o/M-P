from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler

from ..db.utils import get_offers
from .end import end_handler

GET_LIST_OF_OFFERS_PAGE = 10


def _get_filters():
    # TODO: implement logic, should return list of users places where he gonna visit
    return None


def _get_offers():
    return get_offers()


def _to_str(filters):
    res = ""
    for filter in filters:
        res += 'Offer:\n' \
               f'Details: {filter[0]}\n' \
               f'Needs to be delivered to: {filter[1]}\n' \
               f'Pays: {filter[2]}\n\n'

    return res


async def get_list_of_offers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    filters = _get_filters()
    offers = _get_offers()

    if filters:
        offers = [offer for offer in offers if offer[0] in filters]

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Done", callback_data=str(1)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=_to_str(offers), reply_markup=reply_markup
    )

    return GET_LIST_OF_OFFERS_PAGE

GET_LIST_OF_OFFERS_STATE = {
    GET_LIST_OF_OFFERS_PAGE: [
        CallbackQueryHandler(end_handler, pattern="^" + str(1) + "$"),
    ],
}
