# -*- coding: utf-8 -*-

import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Role


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.form_validate'))
        self.assertTrue('Stranger' in response.get_data(as_text=True))

    def test_register_and_login(self):
        email = 'john@example.com'
        username = 'john'
        # 注册新用户
        response = self.client.post('/auth/register', data={
            'email': email,
            'username': username,
            'password': '123',
            'password2': '123'
        })
        self.assertTrue(response.status_code == 302)

        # 使用新注册用户登陆
        response = self.client.post('/auth/login', data={
            'email': email,
            'password': '123'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search(r'Hello,\s+john', data))
        self.assertTrue('You have not confirmed your account yet.' in data)

        # 发送确认令牌
        user = User.query.filter_by(email=email).first()
        token = user.generate_confirmation_token()
        response = self.client.get('/auth/confirm/%s' % token, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have confirmed your account' in data)

        # 登出
        response = self.client.get('/auth/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out' in data)
