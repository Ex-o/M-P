from telegram.ext import CallbackQueryHandler, MessageHandler, filters

from ..modules.active_offers import active_offers_handler
from ..modules.cancel_offer import cancel_offer_handler, cancel_confirm_handler, destroy_offer_handler
from ..modules.courier import courier_handler
from ..modules.create_offer import meeting_place_handler, food_place_handler, \
    payment_handler, create_offer_handler, create_food_offer_handler, create_other_offer_handler, accept_payment_handler
from ..modules.end import end_handler
from ..data.pages import *
from ..modules.get_list_of_offers import get_list_of_own_offers_handler
from ..modules.courier.get_list_of_offers import get_list_of_others_offers_handler, ready_to_complete_handler
from ..modules.sender import sender_handler
from ..modules.approve_offers import get_approvals_handler, confirm_approval_handler, approve_offer_handler
from ..modules.filters import filters_handler, add_filter_handler, accept_filter_handler, delete_filter_handler, \
    confirm_delete_filter_handler

START_STATE = {
    START_PAGE: [
        CallbackQueryHandler(courier_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(sender_handler, pattern="^" + str(2) + "$"),
    ]
}

SENDER_STATE = {
    SENDER_PAGE: [
        CallbackQueryHandler(get_list_of_own_offers_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(get_approvals_handler, pattern="^" + str(2) + "$"),
        CallbackQueryHandler(create_offer_handler, pattern="^" + str(3) + "$"),
        CallbackQueryHandler(cancel_offer_handler, pattern="^" + str(4) + "$"),
        CallbackQueryHandler(end_handler, pattern="^" + str(9999) + "$")
    ]
}

COURIER_STATE = {
    COURIER_PAGE: [
        CallbackQueryHandler(get_list_of_others_offers_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(filters_handler, pattern="^" + str(2) + "$"),
        CallbackQueryHandler(active_offers_handler, pattern="^" + str(3) + "$"),
    ],
}

CREATE_OFFER_STATE = {
    ORDER_TYPE_SELECT_PAGE: [
        CallbackQueryHandler(create_food_offer_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(create_other_offer_handler, pattern="^" + str(2) + "$"),
    ],
    MEETING_PLACE_PAGE: [
        MessageHandler(
            filters.TEXT & ~filters.COMMAND, meeting_place_handler
        )
    ],
    OTHER_OFFER_PAGE: [
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
        CallbackQueryHandler(ready_to_complete_handler, pattern="^(0|[1-9][0-9]*)$"),
        CallbackQueryHandler(get_list_of_others_offers_handler, pattern="^(accept_more|go_back)$"),
        CallbackQueryHandler(end_handler, pattern="^end$"),
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
        CallbackQueryHandler(confirm_approval_handler, pattern="^((0|[1-9][0-9]*)#(0|[1-9][0-9]*))$")
    ],
    APPROVAL_CONFIRM_PAGE: [
        CallbackQueryHandler(approve_offer_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(end_handler, pattern="^" + str(2) + "$"),
    ]
}

FILTERS_STATE = {
    FILTERS_PAGE: [
        CallbackQueryHandler(add_filter_handler, pattern="^" + str(1) + "$"),
        CallbackQueryHandler(delete_filter_handler, pattern="^" + str(2) + "$"),
    ],
    FILTERS_ADD_PAGE: [
        MessageHandler(
            filters.TEXT & ~filters.COMMAND, accept_filter_handler
        )
    ],
    FILTERS_CANCEL_PAGE: [
        CallbackQueryHandler(confirm_delete_filter_handler, pattern="^(0|[1-9][0-9]*)$")
    ]
}