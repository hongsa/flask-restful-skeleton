# -*- coding: utf-8 -*-
import uuid
from apps import db, app
from apps.models import User
import pytz
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta

today = datetime.today().date()
today_str = datetime.strftime(today, "%Y.%m.%d")

def get_current_time():
    return datetime.now(pytz.timezone('Asia/Seoul'))

def create_user(nickname, login_id, password):
    try:
        alreadyCreated = User.query.filter_by(login_id=login_id).first()
        if alreadyCreated:
            raise Exception("유저 아이디가 이미 존재합니다.", 409)
    except Exception as e:
        print(e)
        return e

    try:
        alreadyCreated = User.query.filter_by(nickname=nickname).first()
        if alreadyCreated:
            raise Exception("닉네임이 이미 사용중입니다.", 409)
    except Exception as e:
        print(e)
        return e

    try:
        newUser = User(str(nickname), login_id, str(password))
        db.session.add(newUser)
        db.session.commit()
        createdUser = User.query.filter_by(login_id=login_id).first()
    except Exception as e:
        print(e)
        return e

    try:
        payload = {
            "iss": "minsim.net",
            "user": {
                "id": createdUser.id,
                "login_id": login_id,
                "nickname": createdUser.nickname
            }
        }
        return {
            "id": createdUser.id,
            "nickname": createdUser.nickname,
            "login_id": createdUser.login_id,
            "token": str(unicode(jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256"), "utf-8")),
            "msg": "성공적으로 가입하셨습니다."
        }
    except Exception as e:
        print(e)
        return e


def login(login_id, password):
    login_user = None
    try:
        login_user = User.query.filter_by(login_id=login_id).first()
        if not login_user:
            raise Exception("유저 아이디가 존재하지 않습니다.", 409)

        '''
        기존 있는 datetime을 update는 aware - nonaware 호환 문제 발생
        강제로 + 9시간 함
        aware은 timezone 정보가 있는 거
        '''
        login_user.last_login = datetime.now() + timedelta(hours=9)
        db.session.add(login_user)
        db.session.commit()
        if not check_password_hash(login_user.password, password):
            raise Exception("잘못된 비밀번호입니다.", 409)
    except Exception as e:
        print(e)
        return e
    try:
        payload = {
            "iss": "minsim.net",
            "user": {
                "id": login_user.id,
                "login_id": login_user.login_id,
                "nickname": login_user.nickname,
            }
        }
    except Exception as e:
        print(e)
        return e
    else:
        return {
            "nickname": login_user.nickname,
            "id": login_user.id,
            "login_id": login_user.login_id,
            "token": str(unicode(jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256"), "utf-8")),
            "msg": "성공적으로 로그인 되었습니다."
        }


def update_user(user_id, data):
    try:
        target_user = User.query.filter_by(id=user_id).first()
        if not target_user:
            raise Exception(
                "id가 {} 인 유저가 존재하지 않습니다.".format(user_id), 404)
        target_user.fan = data['fan']
        db.session.commit()
    except Exception as e:
        print(e)
        return e
    return {
        "msg": "성공적으로 업데이트 되었습니다"
    }
