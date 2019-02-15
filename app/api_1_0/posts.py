# -*- coding: utf-8 -*-

from flask import request, g, jsonify, url_for, current_app
from . import api
from .. import db
from ..models import Post, Permission
from authentication import auth
from decorators import permission_required
from errors import forbidden


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    """
    REST写法，POST请求创建新资源，并将其加入目标集合【/posts/】，状态码201
    :return: 新资源的JSON格式
    """
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    # 服务器为新资源指派URL，并在响应的Location首部中返回
    return jsonify(post.to_json()), 201, {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api.route('/posts/')
@auth.login_required
def get_posts():
    """
    REST写法，获得所有文章集合【/posts/】
    :return: 文章集合的JSON格式
    """
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


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


@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
    """
    PUT请求用来更新现有资源
    :param id: 资源ID
    :return: 
    """
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())
