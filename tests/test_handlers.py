from db_context import DBConn
from utils import log_debug


def test_add_users(client, get_db):
    users_number = 5
    req_data = {
        "type": "user",
        "email": "test@test.com",
        "phone": "+700000000",
        "name": "test",
        "country": "test",
        "address": "test"
    }

    for i in range(users_number):
        resp = client.post("/adduser", json=req_data)
        assert resp.status_code == 200

    dsn = get_db.dsn
    with DBConn(dsn) as db_ctx:
        db_ctx.execute("SELECT * FROM users")
        db_rows = db_ctx.fetchall()
        log_debug(db_rows)
        assert len(db_rows) == users_number
