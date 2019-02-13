# -*- coding: utf-8 -*-

from flask import jsonify


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def method_not_allowed(message):
    response = jsonify({'error': 'method not allowed', 'message': message})
    response.status_code = 405
    return response
