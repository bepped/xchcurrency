from flask import jsonify, make_response

def bad_request(message):
    return make_response(jsonify(error=message), 400)


def not_found(message):
    return make_response(jsonify(error=message), 404)

