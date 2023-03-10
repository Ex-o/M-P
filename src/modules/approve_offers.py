from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from ..data.pages import *
from ..db.utils import get_needs_approval_list, delete_other_matches
from ..utils.util import to_approval


async def approve_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    offer_id, user_id = query.data.split('#')

    delete_other_matches(offer_id, user_id)
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

    for idx, offer in enumerate(approvals, start=1):
        reply += f'{idx}. {to_approval(offer)}'

    keyboard = [[InlineKeyboardButton(f"Approve {x}", callback_data=str(
        str(approvals[x]['offer_id']) + '#' + str(approvals[x]['user_id'])))]
                for x in range(len(approvals))]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(reply, reply_markup=reply_markup)
    return GET_APPROVALS_PAGE
