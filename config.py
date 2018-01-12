#coding:utf-8


CSRF_ENABLED = True
SECRET_KEY = 'chen_h'


import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

'''
SQLALCHEMY_DATABASE_URI 是 Flask-SQLAlchemy 扩展需要的，该变量存储我们数据库文件的路径。
SQLALCHEMY_MIGRATE_REPO 是文件夹，我们将会把 SQLAlchemy-migrate 数据文件存储在这里。
'''