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
import json
import sys
import asyncio
from dataclasses import dataclass
from http import HTTPStatus

import uvicorn
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route

from telegram import __version__ as TG_VER, Update, PreCheckoutQuery
from telegram.constants import ParseMode

from src.db.utils import get_order_by_hash, get_temp_order, add_temp_offer
from src.modules.webapp_processor import WebhookUpdate, CustomContext, webhook_update

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

from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, CallbackContext, ExtBot, \
    TypeHandler, PreCheckoutQueryHandler

from src.modules.start import start_handler
from src.modules.help import help_handler
from src.data.states import *
from src.modules.create_offer import pre_checkout_handler, accept_payment_handler
from subprocess import Popen, PIPE

# Enable loggingccccccccccccccccccccccccccccccccccccccccccccccccccc
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ['TG_TOKEN']
PORT = int(os.environ.get('PORT', 5000))


async def main() -> None:
    """Set up the application and a custom webserver."""
    url = "https://boiling-ravine-21139.herokuapp.com"
    admin_chat_id = 123456
    port = PORT

    context_types = ContextTypes(context=CustomContext)
    # Here we set updater to None because we want our custom webhook server to handle the updates
    # and hence we don't need an Updater instance
    application = (
        Application.builder().token(TOKEN).updater(None).context_types(context_types).build()
    )
    # save the values in `bot_data` such that we may easily access them in the callbacks
    application.bot_data["url"] = url
    application.bot_data["admin_chat_id"] = admin_chat_id

    # register handlers
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
        CANCEL_OFFER_STATE |
        OFFER_APPROVAL_STATE |
        FILTERS_STATE,
        fallbacks=[CommandHandler("start", start_handler)],
    )
    application.add_handler(conv_handler)
    application.add_handler(TypeHandler(type=WebhookUpdate, callback=webhook_update))
    application.add_handler(PreCheckoutQueryHandler(callback=pre_checkout_handler))

    application.add_handler(MessageHandler(
            filters.SUCCESSFUL_PAYMENT & ~filters.COMMAND, accept_payment_handler
    ))

    # Pass webhook settings to telegram
    await application.bot.set_webhook(url=f"{url}/telegram")

    # Set up webserver
    async def telegram(request: Request) -> Response:
        """Handle incoming Telegram updates by putting them into the `update_queue`"""
        await application.update_queue.put(
            Update.de_json(data=await request.json(), bot=application.bot)
        )
        return Response()

    async def custom_updates(request: Request) -> PlainTextResponse:
        offer_json = await request.json()
        # offer = await get_order_by_hash(offer_json["orderId"])
        #
        # if len(offer) == 0:
        #     return PlainTextResponse("Incorrect hash!")

        # await application.update_queue.put(WebhookUpdate(user_id=offer_json["user_id"],
        #                                                  offer_id=offer["id"],
        #                                                  food_hash=offer_json["orderId"],
        #                                                  offer_details=offer_json["order"]))

        print(offer_json)
        await add_temp_offer(offer_json["orderId"], offer_json["userInfo"]["telegramAlias"], offer_json)
        return PlainTextResponse("Thank you!")

    async def health(_: Request) -> PlainTextResponse:
        """For the health endpoint, reply with a simple plain text message."""
        return PlainTextResponse(content="The bot is still running fine :)")

    starlette_app = Starlette(
        routes=[
            Route("/telegram", telegram, methods=["POST"]),
            Route("/healthcheck", health, methods=["GET"]),
            Route("/submitpayload", custom_updates, methods=["POST", "GET"]),
        ]
    )
    starlette_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=starlette_app,
            port=port,
            use_colors=False,
            host="0.0.0.0",
        )
    )

    # Run application and webserver together
    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()


if __name__ == "__main__":
    asyncio.run(main())
