# -*- coding: utf-8 -*-

from flask import g
from flask_httpauth import HTTPBasicAuth
from flask import jsonify

from ..models import User, AnonymousUser
from .errors import unauthorized, forbidden
from . import api

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    """
    为API添加用户认证。如果password值为''，则按照令牌方式进行认证，否则按照email和password认证
    :param email: 邮箱
    :param password: 密码
    :return: 可访问/不可访问
    """
    if email_or_token == '':
        # 匿名用户，尚未登录
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.token_used = False
    g.current_user = user
    return user.verity_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    """
    想要在API访问前加login_required监护。
    为了让api蓝本中的所有API都一次性加上监护，可以用before_request修饰器应用到整个蓝本
    :return: 
    """
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})
