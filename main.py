from flask import Blueprint
from flask import request, Flask, current_app

from db_context import DBConn
from utils import make_empty_resp, log_debug

route_blueprint = Blueprint('route_blueprint', __name__)


def create_app():
    app = Flask(__name__)
    app.config.update({
        'DSN': "postgres://laggy:testpasswd123@127.0.0.1:5432/mnp"
    })
    app.register_blueprint(route_blueprint)

    return app


@route_blueprint.route('/adduser', methods=['POST'])
def add_user():
    with DBConn(current_app.config['DSN']) as db_ctx:
        data = request.get_json()
        db_ctx.execute(
            "INSERT INTO users (type, email, name, phone, country, address) VALUES(%s, %s, %s, %s, %s, %s)",
            (data['type'], data['email'], data['name'], data['phone'],
             data['country'], data['address']))
        log_debug(data)

    return make_empty_resp()
