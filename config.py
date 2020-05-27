import os
from dotenv import load_dotenv


class Config(object):
    DEBUG = True
    SECRET_KEY = os.getenv("SKEY")
    SQLALCHEMY_DATABASE_URI= os.getenv("POSTGRES_CONNECT")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
