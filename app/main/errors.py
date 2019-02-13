# -*- coding: utf-8 -*-

from flask import request, jsonify
from flask import url_for, render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('error/404.html'), 404


@main.app_errorhandler(405)
def method_not_allowed(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'method not allowed'})
        response.status_code = 405
        return response
    return render_template('error/405.html'), 405
