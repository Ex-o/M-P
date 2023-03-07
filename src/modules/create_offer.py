import uuid

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from ..db.utils import set_offer

from ..data.pages import *


async def create_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🍔 Food", callback_data=str(1))],
        [InlineKeyboardButton("📙 Other (Specify details)", callback_data=str(2))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Choose your offer type", reply_markup=reply_markup
    )
    return ORDER_TYPE_SELECT_PAGE


async def create_food_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=f"Go to https://hitchy-web.herokuapp.com/?orderId={uuid.uuid1()} and submit your order!"
    )
    return ConversationHandler.END

async def create_other_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        'Alright, please specify where you want to meet the courier in Innopolis'
    )
    return MEETING_PLACE_PAGE


async def meeting_place_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data['loc_source'] = text

    await update.message.reply_text(
        'Please specify from where you want to get your food and the list of foods respectively :)'
    )
    return FOOD_PAGE


async def food_place_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data['loc_destination'] = text

    await update.message.reply_text(
        'How much you are ready to play?'
    )
    return PAYMENT_PAGE


async def payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    loc_destination = context.user_data['loc_destination']
    loc_source = context.user_data['loc_source']
    cost = update.message.text
    user_id = update.effective_user.id

    set_offer(loc_destination, loc_source, cost, user_id)

    await update.message.reply_text(
        'Thank you for your offer, your offer is successfully added'
    )

    return ConversationHandler.END

