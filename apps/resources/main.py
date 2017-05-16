# -*- coding: utf-8 -*-
from flask import g, json, make_response, request
from flask_restful import Resource
from apps import dao
import json
from apps.utils.auth import requires_auth


class UserSignUp(Resource):

    def post(self):
        try:
            data = request.json
            nickname = data['nickname']
            login_id = data['login_id']
            password = data['password']
        except Exception as e:
            return make_response(json.dumps({"msg": "잘못된 요청입니다."}), 400)
        response = dao.create_user(
            nickname, login_id, password)
        if isinstance(response, Exception):
            return errorHandler(response)
        return make_response(json.dumps(response), 201)


class User(Resource):

    def post(self):
        try:
            data = request.json
            login_id = data['login_id']
            password = str(data['password'])
        except Exception as e:
            return make_response(json.dumps({"msg": "잘못된 요청입니다."}), 400)
        response = dao.login(login_id, password)
        if isinstance(response, Exception):
            return errorHandler(response)
        return make_response(json.dumps(response))
        # return make_response(json.dumps(response))

    @requires_auth
    def put(self, user_id):
        if not user_id:
            return make_response(json.dumps({"msg": "유저 아이디가 없습니다."}), 400)
        try:
            data = request.json
        except Exception as e:
            print(e)
            return make_response(json.dumps({"msg": "잘못된 요청입니다."}), 400)
        try:
            if g.current_user["id"] != int(user_id):
                raise Exception("유저아이디와 토큰이 일치하지 않습니다.")
        except Exception as e:
            print(e)
            return make_response(json.dumps({"msg": e.args[0]}), 400)

        response = dao.update_user(user_id, data)
        if isinstance(response, Exception):
            return errorHandler(response)
        return make_response(json.dumps(response))



def errorHandler(response):
    if len(response.args) == 1:
        return make_response(json.dumps({
            "msg": response.args[0]
        }), 400)
    elif len(response.args) > 1:
        return make_response(json.dumps({"msg": response.args[0]}), response.args[1])
    else:
        return make_response(json.dumps({"msg": '오류가 발생했습니다.'}), 400)

def validate_necessary(key, data, data_type, necessary=True):
    if not key in data:
        raise Exception("{}가 데이터로 오지 않았습니다.".format(key), 400)
    else:
        try :
            if data_type == int or data_type == str or data_type == bool:
                data[key] = data_type(data[key])
            if type(data[key]) != data_type:
                raise Exception()
        except Exception as e:
            print e
            raise Exception("{}의 타입이 {}가 아닙니다.".format(key, str(data_type)), 400)
