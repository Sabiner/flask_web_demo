# -*- coding: utf-8 -*-

from flask import request, g, jsonify
from . import api
from .. import db
from ..models import Post, Permission
from authentication import auth


@api.route('/posts/', method=['POST'])
def new_post():
    """
    REST写法，POST请求创建新资源，并将其加入目标集合【/posts/】，状态码201
    :return: 新资源的JSON格式
    """
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())


@api.route('/posts/')
@auth.login_required
def get_posts():
    """
    REST写法，获得所有文章集合【/posts/】
    :return: 文章集合的JSON格式
    """
    posts = Post.query.all()
    return jsonify({'posts': [post.to_json() for post in posts]})


@api.route('/posts/<int:id>')
@auth.login_required
def get_post(id):
    """
    REST写法，获得指定ID对应的文章
    :param id: 
    :return: 
    """
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())
