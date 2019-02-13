# -*- coding: utf-8 -*-

from flask import Blueprint
from ..models import Permission

main = Blueprint('main', __name__)

import views
import errors


@main.app_context_processor
def inject_permissions():
    """
    让变量在所有模板中全局可访问
    app_context_processor是上下文处理器，避免了每次调用render_template时都要多添加一个模板参数
    :return: 
    """
    return dict(Permission=Permission)
