from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.data.pages import *
from src.db.utils import get_needs_approval_list
from src.utils.util import to_approval


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
        reply += f'{idx} {to_approval(offer)}'

    await query.edit_message_text(reply)

    return GET_LIST_OF_OFFERS_PAGE
