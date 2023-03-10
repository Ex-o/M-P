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
    menu = get_menu_items([x[0] for x in offers])

    quantified_menu = []
    for x in menu:
        tmp = next(y for y in offers if y["id"] == x[0])
        quantified_menu.append([x["title"], x["price"], tmp[1]])

    await context.bot.send_invoice(update.user_id, provider_token=PROVIDER_TEST_TOKEN,
                                   title=f"Your order: {update.food_hash}",
                                   description="Please complete the payment to proceed",
                                   currency="RUB",
                                   payload=str(update.offer_id),
                                   prices=[LabeledPrice(label=f"x{x[2]} {x[0]}",
                                                        amount=x[1] * x[2] * 100)
                                           for x in quantified_menu],
                                   need_shipping_address=False,
                                   start_parameter='wtf')

    return ConversationHandler.END
