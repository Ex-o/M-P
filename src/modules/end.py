from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


async def end_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="OKKK!")
    return ConversationHandler.END
