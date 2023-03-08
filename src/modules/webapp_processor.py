import json
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from src.db.utils import get_order_by_hash, set_order_details


async def custom_updates(request: Request) -> PlainTextResponse:
    order_json = await request.json()
    order = get_order_by_hash(order_json["orderId"])

    if len(order) == 0:
        return PlainTextResponse("Incorrect hash!")
    orders = [x for x in order_json["selections"].items() if x[1] > 0]

    order_id = order['id']
    set_order_details(order_id, json.dumps(orders))
    return PlainTextResponse("Thank you for the submission! It's being forwarded.")