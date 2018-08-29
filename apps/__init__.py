# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import sys
from flask_restful import Api
from flask_cors import CORS
from sqlalchemy import create_engine

# reload(sys)
# sys.setdefaultencoding('utf-8')

app = Flask('apps')
CORS(app)
app.config.from_object('apps.settings.Production')
app.debug = True
api = Api(app)

# sqlalchemy 통해 raw sql 이용함
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], convert_unicode=True, echo=False, max_overflow=30, pool_size=10, pool_recycle=7200)


db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


from. import controllers
from. import models
from. import dao
