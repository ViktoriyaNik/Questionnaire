from werkzeug.security import generate_password_hash
from app import app, db
from flask import render_template, redirect, url_for, flash, request

from flask_login import current_user, login_user, login_required, logout_user

from app.forms import TestForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/create', methods=['POST', 'GET'])  # если ссылка в элементе <button>, то почему-то необходимо добавлять '/' вконце
def create():
    form = TestForm()

    if form.update_on_submit(): pass
    elif form.validate_on_submit():

        title = form.title.data
        author_name = form.author_name.data
        author_birth = form.author_birth.data

        print('Form is submitted...')
        print(title, author_name, author_birth, sep='\n')

        questions = []
        for question in form.questions:
            questions.append(question.title.data)
            questions.append(question.text.data)
            print(question.title.data)
            print(question.text.data)
            print(question.answer_type.data)
            variants = []
            for variant in question.variants:
                variants.append(variant.data)
                print(variant.data)

    return render_template('create.html', form=form, errors=form.errors)


from app.models import question, test, type, question_list, user
from sqlalchemy import insert, select
def save_test_to_db(form):
    sess = db.session

    title = form.title.data
    author_name = form.author_name.data
    author_birth = form.author_birth.data

    questions = []
    for question in form.questions:
        title = question.title
        text = question.text
        answer_type = question.answer_type

        stmt = insert(question).values(title=title, type=answer_type, text=text)

    if sess.execute(select(user).where(name=author_name)):
        pass


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
