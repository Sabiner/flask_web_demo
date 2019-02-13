# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError
from flask_pagedown.fields import PageDownField

from ..models import Role, User, Post


class NameForm(Form):
    name = StringField("What's your name?", validators=[Required()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')

    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        Required(),
        Regexp(r'^[a-zA-Z][a-zA-Z0-9_.]*$', 0, 'Username must have obly letters, numbers, dots or underscores')
    ])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already redisted.')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField('Submit')
