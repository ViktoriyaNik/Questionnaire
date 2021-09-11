from werkzeug.security import generate_password_hash
from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app import forms
from flask_login import current_user, login_user, login_required, logout_user

@app.route('/')
@app.route('/index')
def index():
    return '<h1>Прувет, медвед!</h1> <div><img src="http://risovach.ru/upload/2015/11/mem/medved-iz-kustov_97135269_orig_.png"></div>'
