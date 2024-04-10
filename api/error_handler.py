from flask import jsonify

"""
The errors currently handled include
    400, 404, 401, 405, 500

The above list should be updated if an error handler is aded or removed
"""

def bad_request(e):
    return jsonify({
        'message': 'bad request: failed to decode JSON object',
        'status': False
    }), 400


def not_found(e):
    return jsonify({
        'message': 'not found: the resource you requested was not found on this server',
        'status': False
    }), 404


def unauthorised(e):
    return jsonify({
        'message': 'unauthorised: you do not have permission to access this resource',
        'status': False
    }), 401


def method_not_allowed(e):
    return jsonify({
        'message': 'method not allowed: the http method is not allowed for the requested endpoint',
        'status': False 
    }), 405


def server_error(e):
    return jsonify({
        'message': 'internal server error: an unexpected error occured',
        'status': False
    }), 500