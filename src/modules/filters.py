from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from ..data.pages import *
from ..utils.maps import get_point
from ..db.utils import add_filter, get_filters, delete_filter


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
        'Alright, please write the address where you want to add'
    )
    return FILTERS_ADD_PAGE


async def accept_filter_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    address = update.message.text
    user_id = update.effective_user.id
    point = await get_point(address)

    add_filter(user_id, point['lat'], point['lon'], point['formatted_address'])

    keyboard = [
        [InlineKeyboardButton("Add new location", callback_data=str(1))],
        [InlineKeyboardButton("Delete location", callback_data=str(2))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Your filter was successfully added', reply_markup=reply_markup)

    FILTERS_PAGE


async def delete_filter_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    filters = get_filters(user_id)

    keyboard = [[InlineKeyboardButton(filter['link'], callback_data=str(filter['id']))]
                for filter in filters]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        'Please select which filter you want to cancel!', reply_markup=reply_markup
    )
    return FILTERS_CANCEL_PAGE


async def confirm_delete_filter_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    delete_filter(query.data)

    keyboard = [
        [InlineKeyboardButton("Add new location", callback_data=str(1))],
        [InlineKeyboardButton("Delete location", callback_data=str(2))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Your filter was successfully deleted', reply_markup=reply_markup)

    FILTERS_PAGE
