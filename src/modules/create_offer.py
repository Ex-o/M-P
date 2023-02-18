from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler

MEETING_PLACE_PAGE = 4
FOOD_PAGE = 5
PAYMENT_PAGE = 6


async def create_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        'Alright, please specify where you want to meet the courier in Innopolis'
    )
    return MEETING_PLACE_PAGE


async def metting_place_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
    text = update.message.text
    context.user_data['cost'] = text

    await update.message.reply_text(
        'Thank you for your offer, your offer is successfully added'
    )

    return ConversationHandler.END


CREATE_OFFER_STATE = {
    MEETING_PLACE_PAGE: [
        MessageHandler(
            filters.TEXT & ~filters.COMMAND, metting_place_handler
        )
    ],
    FOOD_PAGE: [
        MessageHandler(
            filters.TEXT & ~filters.COMMAND, food_place_handler
        )
    ],
    PAYMENT_PAGE: [
        MessageHandler(
            filters.TEXT & ~filters.COMMAND, payment_handler
        )
    ]
}
