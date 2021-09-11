import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+mysqlconnector://vika:vika@localhost:3306/<db_name>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
