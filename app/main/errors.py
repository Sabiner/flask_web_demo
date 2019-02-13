# -*- coding: utf-8 -*-

from flask import url_for, render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@main.app_errorhandler(405)
def method_not_allowed(e):
    return render_template('error/405.html'), 405
