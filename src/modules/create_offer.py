import os
import uuid

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import ContextTypes, ConversationHandler
from ..db.utils import set_offer, add_pending_food_offer, set_offer_status

from ..data.pages import *

PROVIDER_TEST_TOKEN = os.environ['PROVIDER_TEST_TOKEN']


async def create_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🔙 Go Back", callback_data="go_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        'Alright, please specify where you want to meet the courier in Innopolis', reply_markup=reply_markup
    )
    return MEETING_PLACE_PAGE


async def create_other_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🔙 Go Back", callback_data="go_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        'Alright, please specify where you want the courier to go', reply_markup=reply_markup
    )
    return OTHER_OFFER_PAGE


async def create_food_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    uid = uuid.uuid1()
    await add_pending_food_offer(update.effective_user.id, uid, "BGK", context.user_data['loc_source'])

    keyboard = [
        [InlineKeyboardButton("🔙 Go Back", callback_data="go_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"Go to https://hitchy-web.herokuapp.com/?orderId={uid} and submit your order!", reply_markup=reply_markup
    )
    return ORDER_TYPE_SELECT_PAGE


async def meeting_place_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data['loc_source'] = text

    keyboard = [
        [InlineKeyboardButton("🍔 Food", callback_data=str(1))],
        [InlineKeyboardButton("📙 Other (Specify details)", callback_data=str(2))],
        [InlineKeyboardButton("🔙 Go Back", callback_data="go_back")]
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
    await set_offer(loc_destination, loc_source, cost, user_id)

    await update.message.reply_invoice(provider_token=PROVIDER_TEST_TOKEN,
                                       title="PAY THIS TEST title",
                                       description="some description mafaka",
                                       currency="RUB",
                                       payload="ok, some payload",
                                       prices=[LabeledPrice(label="lable 1", amount=300 * 100),
                                               LabeledPrice(label="lable 2", amount=200 * 100)],
                                       need_shipping_address=True,
                                       start_parameter='wtf')

    return ConversationHandler.END


async def accept_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    offer_id = update.message.successful_payment.invoice_payload
    await set_offer_status(offer_id, 'paid')
    await context.bot.send_message(update.effective_user.id,
                                   "Payment Successful! We'll be showing your order to potential couriers now :)")
    return ConversationHandler.END


async def pre_checkout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pre_checkout_query_id = update.pre_checkout_query.id
    await context.bot.answerPreCheckoutQuery(pre_checkout_query_id=pre_checkout_query_id, ok=True)

    return ConversationHandler.END
