from db_context import .DBConn as db


def register_user(telegram_id):
    with db as db_ctx:
        db_ctx.execute(
            f"INSERT INTO users (id) VALUES({telegram_id})")


def set_offer(loc_destination, loc_source, cost):
    with db as db_ctx:
        db_ctx.execute(
            "INSERT INTO offers (loc_destination, loc_source, cost) "
            f"VALUES({loc_destination}, {loc_source}, {cost})")
