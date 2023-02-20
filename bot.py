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


import os
import logging

from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler

from src.modules.sender import SENDER_STATE
from src.modules.create_offer import CREATE_OFFER_STATE
from src.modules.start import start_handler, START_STATE
from src.modules.courier import COURIER_STATE
from src.modules.help import help_handler
from src.modules.get_list_of_offers import GET_LIST_OF_OFFERS_STATE
from src.modules.active_offers import ACTIVE_OFFERS_STATE
from src.modules.cancel_offer import CANCEL_OFFER_STATE

# Enable loggingccccccccccccccccccccccccccccccccccccccccccccccccccc
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ['TG_TOKEN']
PORT = int(os.environ.get('PORT', 5000))


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("help", help_handler))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_handler)],
        states=
        START_STATE |
        COURIER_STATE |
        SENDER_STATE |
        CREATE_OFFER_STATE |
        GET_LIST_OF_OFFERS_STATE |
        ACTIVE_OFFERS_STATE |
        CANCEL_OFFER_STATE,
        fallbacks=[CommandHandler("start", start_handler)],
    )
    application.add_handler(conv_handler)
    application.run_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=TOKEN,
                            webhook_url='https://boiling-ravine-21139.herokuapp.com/' + TOKEN)


if __name__ == "__main__":
    main()
