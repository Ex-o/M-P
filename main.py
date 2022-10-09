from flask import request, Flask, jsonify, make_response
from db_context import DBConn

app = Flask(__name__)
dsn = "postgres://laggy:testpasswd123@127.0.0.1:5432/mnp"


def make_empty_resp():
    data = {'code': 'SUCCESS', 'message': 'Empty'}
    return make_response(jsonify(data), 200)


@app.route('/adduser', methods=['POST'])
def add_user():
    with DBConn(dsn) as db_ctx:
        db_ctx.execute(
            "INSERT INTO users (type, email, name, phone, country, address) VALUES(%s, %s, %s, %s, %s, %s)",
            (request.form['type'], request.form['email'], request.form['name'], request.form['phone'],
             request.form['country'], request.form['address']))
    return make_response()
