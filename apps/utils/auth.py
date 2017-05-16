# -*- coding: utf-8 -*-
from functools import wraps

from flask import request, g, jsonify
import jwt

from apps import app
# from entry import app


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(' > Starting authentication.. ')
        try:
            token = request.headers.get('Authorization', None)
        except:
            print('header get doesn\'t work.')
        print(request.headers)
        if token:
            print(' > token included.')
            if token.split()[0] == 'Bearer':
                token = token.split()[1]
            try:
                print('token: \n{}\n'.format(token))
                decoded = jwt.decode(token, app.config["SECRET_KEY"])
            except:
                return {'msg': "토큰 값이 유효하지 않습니다. 다시 로그인 하세요."}, 401
            else:
                print('decoded user: ', decoded['user'])
                g.current_user = decoded["user"]
                print('''
=============================================================
                        token is VALID
=====================authentication complete=================
''')
                return f(*args, **kwargs)
        return {'msg': "로그인을 하셔야 합니다."}, 401
    return decorated

def optional_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(' > Starting authentication.. ')
        try:
            token = request.headers.get('Authorization', None)
        except:
            print('header get doesn\'t work.')
        print(request.headers)
        
        if token:
            print(' > token included.')
            if token.split()[0] == 'Bearer':
                token = token.split()[1]
            try:
                print('token: \n{}\n'.format(token))
                decoded = jwt.decode(token, app.config["SECRET_KEY"])
            except:
                return f(*args, **kwargs)
            else:
                print('decoded user: ', decoded['user'])
                g.current_user = decoded["user"]
                print('current_user' in g)
                print('''
=============================================================
                        token is VALID
=====================authentication complete=================
''')
                return f(*args, **kwargs)
        return f(*args, **kwargs)
    return decorated


class InvalidUserError(Exception):
    pass
