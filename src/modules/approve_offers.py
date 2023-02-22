from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from src.data.pages import *
from src.db.utils import get_needs_approval_list
from src.utils.util import to_approval


async def approve_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    # TODO: Remove other matches + verify it is my offer!
    await query.edit_message_text(
        f"Your offer [{context.user_data['offer_to_be_approved']}] is now approved!"
    )

    return ConversationHandler.END


async def confirm_approval_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    context.user_data['offer_to_be_approved'] = query.data
    keyboard = [
        [InlineKeyboardButton("Approve", callback_data=str(1))],
        [InlineKeyboardButton("Abort", callback_data=str(2))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        'Are you sure you want to approve this order?', reply_markup=reply_markup
    )

    return APPROVAL_CONFIRM_PAGE


async def get_approvals_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    approvals = get_needs_approval_list(user_id)

    if len(approvals) == 0:
        await query.edit_message_text(
            'There\'s nothing to approve yet!'
        )
        return ConversationHandler.END

    reply = ""
    context.user_data['approval_map'] = {}

    for idx, offer in enumerate(approvals, start=1):
        reply += f'{idx}. {to_approval(offer)}'
        context.user_data['approval_map'][idx] = offer['offer_id']

    keyboard = [[InlineKeyboardButton(f"Approve {x}",
                                      callback_data=str(context.user_data['approval_map'][x]))]
                for x in range(1, len(approvals) + 1)]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(reply, reply_markup=reply_markup)

    return GET_LIST_OF_OFFERS_PAGE
