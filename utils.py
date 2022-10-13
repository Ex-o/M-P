import logging

from flask import jsonify, make_response

LOGGER = logging.getLogger(__name__)


def log_debug(msg):
    LOGGER.debug(msg)


def make_empty_resp():
    data = {'code': 'SUCCESS', 'message': 'Empty'}
    return make_response(jsonify(data), 200)
