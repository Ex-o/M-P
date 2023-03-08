import json
from dataclasses import dataclass

from starlette.requests import Request
from starlette.responses import PlainTextResponse
from telegram.ext import CallbackContext, ExtBot

from src.db.utils import get_order_by_hash, set_order_details

@dataclass
class WebhookUpdate:
    """Simple dataclass to wrap a custom update type"""

    user_id: int
    order_id: str
    order_details: str


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


async def webhook_update(update: WebhookUpdate, context: CustomContext) -> None:
    orders = [x for x in update.order_details.items() if x[1] > 0]
    set_order_details(update.order_id, json.dumps(orders))

    await context.bot.send_message(update.user_id, "THANKS FOR MAKING ORDER NIGGA")