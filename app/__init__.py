# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

#初始化数据库
db = SQLAlchemy(app)

# 初始化flask-Login
lm = LoginManager()
lm.setup_app(app)



from app import views,models