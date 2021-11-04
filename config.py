import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI') or 'mysql+mysqlconnector://root:root@localhost:3306/questionnaire'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
