import json
import os
from dataclasses import dataclass

from starlette.requests import Request
from starlette.responses import PlainTextResponse
from telegram import LabeledPrice
from telegram.ext import CallbackContext, ExtBot, ConversationHandler

from src.db.utils import set_offer_details, get_menu_items

PROVIDER_TEST_TOKEN = os.environ['PROVIDER_TEST_TOKEN']

@dataclass
class WebhookUpdate:
    """Simple dataclass to wrap a custom update type"""

    user_id: int
    offer_id: int
    food_hash: str
    offer_details: str


class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    """
    Custom CallbackContext class that makes `user_data` available for updates of type
    `WebhookUpdate`.
    """

    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "CustomContext":
        if isinstance(update, WebhookUpdate):
            return cls(application=application, user_id=update.user_id)
        return super().from_update(update, application)


async def webhook_update(update: WebhookUpdate, context: CustomContext):
    offers = [x for x in update.offer_details.items() if x[1] > 0]
    set_offer_details(update.offer_id, json.dumps(offers))
    menu = get_menu_items([x[0] for x in update.offer_details.items()])

    await context.bot.send_invoice(update.user_id, provider_token=PROVIDER_TEST_TOKEN,
                                                  title="PAY THIS TEST title",
                                                  description="some description mafaka",
                                                  currency="RUB",
                                                  payload="ok, some payload",
                                                  prices=[LabeledPrice(label=x["title"], amount=x["price"] * 100)
                                                          for x in menu],
                                       need_shipping_address=True,
                                       start_parameter='wtf')

    return ConversationHandler.END
