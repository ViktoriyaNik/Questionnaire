from werkzeug.security import generate_password_hash
from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app import forms
from flask_login import current_user, login_user, login_required, logout_user


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/create/')  # если ссылка в элементе <button>, то почему-то необходимо добавлять '/' вконце
def create():
    return render_template('create.html')


@app.route('/questionnaire/', defaults={'test_id': None})
@app.route('/questionnaire/<test_id>')
def questionnaire(test_id):
    if  test_id:
        return render_template('questionnaire.html', test_id=test_id)
    else:
        return render_template('questionnaire.html', test_id=test_id, questionnaire_list=['test0', 'test1', 'test2', 'test3'])


@app.route('/statistics/<test_id>')
def statistics(test_id):
    return render_template('statistics.html', test_id=test_id)
