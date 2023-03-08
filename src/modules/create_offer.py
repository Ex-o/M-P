import os
import uuid

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import ContextTypes, ConversationHandler
from ..db.utils import set_offer

from ..data.pages import *


PROVIDER_TEST_TOKEN = os.environ['PROVIDER_TEST_TOKEN']


async def create_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        'Alright, please specify where you want to meet the courier in Innopolis'
    )
    return MEETING_PLACE_PAGE


async def create_other_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        'Alright, please specify where you want the courier to go'
    )
    return OTHER_OFFER_PAGE


async def create_food_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=f"Go to https://hitchy-web.herokuapp.com/?orderId={uuid.uuid1()} and submit your order!"
    )
    return ConversationHandler.END


async def meeting_place_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data['loc_source'] = text

    keyboard = [
        [InlineKeyboardButton("🍔 Food", callback_data=str(1))],
        [InlineKeyboardButton("📙 Other (Specify details)", callback_data=str(2))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        text="Choose your offer type", reply_markup=reply_markup
    )
    return ORDER_TYPE_SELECT_PAGE


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

    await update.message.reply_invoice(provider_token=PROVIDER_TEST_TOKEN,
                                                  title="PAY THIS TEST title",
                                                  description="some description mafaka",
                                                  currency="RUB",
                                                  payload="ok, some payload",
                                                  prices=[LabeledPrice(label="lable 1", amount=300 * 100),
                                                          LabeledPrice(label="lable 2", amount=200 * 100)])

    return PAYMENT_PAGE_2


async def accept_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        'Thanks for ' + update.message.invoice.title + ' payment braza'
    )
