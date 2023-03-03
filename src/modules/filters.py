from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from ..data.pages import *
from ..utils.maps import get_ll_from_yandex_url
from ..db.utils import add_filter


async def filters_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Add new location", callback_data=str(1))],
        [InlineKeyboardButton("Delete location", callback_data=str(2))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Choose what you want to do", reply_markup=reply_markup
    )

    return FILTERS_PAGE


async def add_filter_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        'Alright, please share the link for the location you want to add (for example: https://yandex.ru/maps/-/CCUGNOeiXA)'
    )
    return FILTERS_ADD_PAGE


async def accept_filter_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    link = update.message.text
    user_id = update.effective_user.id
    lon, lat = await get_ll_from_yandex_url(link)

    add_filter(user_id, lat, lon, link)

    keyboard = [
        [InlineKeyboardButton("Add new location", callback_data=str(1))],
        [InlineKeyboardButton("Delete location", callback_data=str(2))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Your filter was successfully added', reply_markup=reply_markup)

    FILTERS_PAGE
