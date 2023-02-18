#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from db_utils import register_user
from db_context import DBConn

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, \
    CallbackQueryHandler
import os

from src.utils.util import build_menu

# Enable loggingccccccccccccccccccccccccccccccccccccccccccccccccccc
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ['TG_TOKEN']
PORT = int(os.environ.get('PORT', 5000))



# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info("/Start command was issued")
    logger.debug("I AM A DEBUG")
    button_list = [
        InlineKeyboardButton("Courier", callback_data=str(1)),
        InlineKeyboardButton("Sender", callback_data=str(2)),
    ]

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    await update.message.reply_text('Welcome', reply_markup=reply_markup)
    return 1
    # await update.message.reply_html(
    #     rf"Hi {user.mention_html()}!",
    #     reply_markup=ForceReply(selective=True),
    # )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Khaled got ice cream, YAY!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text('Farhod got ice cream, YAY!')


async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("YES", callback_data=str(3)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="ARE YOU SUREEEE?????", reply_markup=reply_markup
    )
    return 2


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="OKKK!")
    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            1: [
                CallbackQueryHandler(one, pattern="^" + str(1) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(2) + "$"),
            ],
            2: [
                CallbackQueryHandler(end, pattern="^" + str(3) + "$")
            ]
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=TOKEN,
                            webhook_url='https://boiling-ravine-21139.herokuapp.com/' + TOKEN)


if __name__ == "__main__":
    main()
