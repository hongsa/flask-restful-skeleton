# -*- coding: utf-8 -*-
from apps import api
from .resources.main import UserSignUp, User

# USER API
# 1. signup : POST
api.add_resource(UserSignUp, '/api/users/signup')

# 2. login : GET, POST, PUT, DELETE
api.add_resource(User, '/api/users/<user_id>', '/api/users/login')
