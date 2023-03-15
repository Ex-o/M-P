from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ..utils.util import to_offer
from ..db.utils import get_offers

from ..data.pages import *


async def active_offers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    user_id = update.effective_user.id

    offers = await get_offers(user_id)

    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🔙 Go Back", callback_data="go_back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=to_offer(offers), reply_markup=reply_markup
    )

    return ACTIVE_OFFERS_PAGE
