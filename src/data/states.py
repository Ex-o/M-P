from telegram.ext import CallbackQueryHandler, MessageHandler, filters

from ..modules.active_offers import active_offers_handler
from ..modules.cancel_offer import cancel_offer_handler, cancel_confirm_handler, destroy_offer_handler
from ..modules.courier import courier_handler
from ..modules.create_offer import create_offer_handler, meeting_place_handler, food_place_handler, payment_handler
from ..modules.end import end_handler
from ..data.pages import *
from ..modules.get_list_of_offers import get_list_of_offers_handler, ready_to_complete_handler
from ..modules.sender import sender_handler
from ..modules.approve_offers import get_approvals_handler, confirm_approval_handler, approve_offer_handler

START_STATE = {
    START_PAGE: [
        CallbackQueryHandler(courier_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(sender_handler, pattern="^" + str(2) + "$"),
    ]
}

SENDER_STATE = {
    SENDER_PAGE: [
        CallbackQueryHandler(end_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(get_approvals_handler, pattern="^" + str(2) + "$"),
        CallbackQueryHandler(create_offer_handler, pattern="^" + str(3) + "$"),
        CallbackQueryHandler(cancel_offer_handler, pattern="^" + str(4) + "$"),
    ]
}

COURIER_STATE = {
    COURIER_PAGE: [
        CallbackQueryHandler(get_list_of_offers_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(end_handler, pattern="^" + str(2) + "$"),
        CallbackQueryHandler(active_offers_handler, pattern="^" + str(3) + "$"),
    ],
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

GET_LIST_OF_OFFERS_STATE = {
    GET_LIST_OF_OFFERS_PAGE: [
        CallbackQueryHandler(ready_to_complete_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(get_list_of_offers_handler, pattern="^" + str(2) + "$"),
        CallbackQueryHandler(end_handler, pattern="^" + str(3) + "$"),
        CallbackQueryHandler(get_list_of_offers_handler, pattern="^" + str(4) + "$"),
    ],
}

ACTIVE_OFFERS_STATE = {
    ACTIVE_OFFERS_PAGE: [
        CallbackQueryHandler(end_handler, pattern="^" + str(1) + "$"),
    ],
}

CANCEL_OFFER_STATE = {
    CANCEL_OFFER_PAGE: [
        CallbackQueryHandler(cancel_confirm_handler, pattern="^(0|[1-9][0-9]*)$")
    ],
    CANCEL_CONFIRM_PAGE: [
        CallbackQueryHandler(destroy_offer_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(end_handler, pattern="^" + str(2) + "$"),
    ]
}

OFFER_APPROVAL_STATE = {
    GET_APPROVALS_PAGE: [
        CallbackQueryHandler(confirm_approval_handler, pattern="^(0|[1-9][0-9]*)$")
    ],
    APPROVAL_CONFIRM_PAGE: [
        CallbackQueryHandler(approve_offer_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(end_handler, pattern="^" + str(2) + "$"),
    ]
}