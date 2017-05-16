# from secret_keys import CSRF_SECRET_KEY, SESSION_KEY
from datetime import timedelta

class Config(object):
    # Set secret keys for CSRF protection
    SECRET_KEY = "{secret password, using jwt}"
    # CSRF_SESSION_KEY = SESSION_KEY
    debug = True


class Production(Config):
    DEBUG = True
    CSRF_ENABLED = True
    ADMIN = "admin"
    # SQLALCHEMY_DATABASE_URI = "mysql://root:1111@0.0.0.0/used?charset=utf8"
    SQLALCHEMY_DATABASE_URI = "mysql://{account}:{password}@{ip_address}/{database_name}?charset=utf8"
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_TIMEOUT = 100
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_RECYCLE = 20
    migration_directory = 'migrations'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
