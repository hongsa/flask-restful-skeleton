# -*- coding:utf-8 -*-
from apps import db
import pytz
import datetime
from werkzeug.security import generate_password_hash

def get_current_time():
    return datetime.datetime.now(pytz.timezone('Asia/Seoul'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    nickname = db.Column(db.String(255), index=True, unique=True)
    created = db.Column(db.DATETIME, default=get_current_time)
    last_login = db.Column(db.DATETIME, default=get_current_time)

    def __init__(self, nickname, login_id, password):
        self.login_id = login_id
        self.nickname = nickname
        self.password = generate_password_hash(password)
        print(self)
