import os

class Config(object):
    DEBUG = True
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI='postgresql://rsevey:Niner99~@localhost/harv_db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False