import json
from dataclasses import dataclass

from starlette.requests import Request
from starlette.responses import PlainTextResponse
from telegram.ext import CallbackContext, ExtBot, ConversationHandler

from src.db.utils import set_offer_details

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

    await context.bot.send_message(update.user_id, "THANKS FOR MAKING ORDER NIGGA")

    return ConversationHandler.END