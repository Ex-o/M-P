from telegram.ext import CallbackQueryHandler, MessageHandler, filters

from src.modules.cancel_offer import cancel_offer_handler, cancel_confirm_handler, destroy_offer_handler
from src.modules.create_offer import create_offer_handler, meeting_place_handler, food_place_handler, payment_handler
from src.modules.end import end_handler
from src.data.pages import *

SENDER_STATE = {
    SENDER_PAGE: [
        CallbackQueryHandler(end_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(end_handler, pattern="^" + str(2) + "$"),
        CallbackQueryHandler(create_offer_handler, pattern="^" + str(3) + "$"),
        CallbackQueryHandler(cancel_offer_handler, pattern="^" + str(4) + "$"),
    ]
}

CREATE_OFFER_STATE = {
    MEETING_PLACE_PAGE: [
        MessageHandler(
            filters.TEXT & ~filters.COMMAND, meeting_place_handler
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

CANCEL_OFFER_STATE = {
    CANCEL_OFFER_PAGE : [
        CallbackQueryHandler(cancel_confirm_handler, pattern="^(0|[1-9][0-9]*)$")
    ],
    CANCEL_CONFIRM_PAGE : [
        CallbackQueryHandler(destroy_offer_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(end_handler, pattern="^" + str(2) + "$"),
    ]
}