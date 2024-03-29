from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from ..data.pages import *

from ..db.utils import get_active_sender_offers, delete_offer


async def destroy_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    await delete_offer(context.user_data['offer_to_be_cancelled'])

    await query.edit_message_text(
        f"Your offer [{context.user_data['offer_to_be_cancelled']}] is now deleted!"
    )

    return ConversationHandler.END


async def cancel_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    context.user_data['offer_to_be_cancelled'] = query.data
    keyboard = [
        [InlineKeyboardButton("Cancel", callback_data=str(1))],
        [InlineKeyboardButton("Abort", callback_data=str(2))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        'Are you sure you want to cancel this order?', reply_markup=reply_markup
    )

    return CANCEL_CONFIRM_PAGE


async def cancel_offer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    active_offers = await get_active_sender_offers(user_id)

    if len(active_offers) == 0:
        await query.edit_message_text(
            'You don\'t have any active offers!'
        )
        return None

    keyboard = [[InlineKeyboardButton(f"{x['loc_destination']} -> {x['loc_source']}", callback_data=str(x['id']))]
                for x in active_offers]

    keyboard.append([InlineKeyboardButton("🔙 Go Back", callback_data="go_back")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        'Please select which offer you want to cancel!', reply_markup=reply_markup
    )
    return CANCEL_OFFER_PAGE
