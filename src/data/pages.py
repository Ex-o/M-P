from telegram.ext import CallbackQueryHandler, MessageHandler, filters

from src.modules.cancel_offer import cancel_offer_handler
from src.modules.create_offer import create_offer_handler, meeting_place_handler, food_place_handler, payment_handler
from src.modules.end import end_handler

START_PAGE = 1
COURIER_PAGE = 2
SENDER_PAGE = 3
MEETING_PLACE_PAGE = 4
FOOD_PAGE = 5
PAYMENT_PAGE = 6
CANCEL_OFFER_PAGE = 7

GET_LIST_OF_OFFERS_PAGE = 10
ACTIVE_OFFERS_PAGE = 11

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