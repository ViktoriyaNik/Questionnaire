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
    print('Count of questions:', len(form.questions))
    print('Count of variants in question 1:', len(form.questions[0].variants))
    if form.update_on_submit(): pass
    elif form.validate_on_submit():
        save_test_to_db(form)
    return render_template('create.html', form=form, errors=form.errors)


from app.models import question_model, answer_model, test_model, type_model, user_model
from sqlalchemy import insert, select, exists
def save_test_to_db(form):
    sess = db.session
    #try:
    test_title      = form.title.data
    author_name     = form.author_name.data
    author_sex      = form.author_sex.data
    author_birth    = form.author_birth.data

    # Если такой пользователь существует, взять из бд, если нет - создать
    if sess.query(exists().where(user_model.name == author_name)).scalar():
        stmt = select(user_model).where(user_model.name == author_name)
        author_db = sess.execute(stmt).scalar()
    else:
        author_db = user_model(name=author_name, sex=author_sex, date_of_birth=author_birth)
        sess.add(author_db)
        sess.commit()

    test_db         = test_model(title=test_title, author=author_db)

    questions = []
    for question_form in form.questions:
        question_title          = question_form.title.data
        question_text           = question_form.text.data
        question_answer_type    = question_form.answer_type.data

        question_db             = question_model(
            type_id=question_answer_type,
            test=test_db,
            title=question_title,
            text=question_text if question_text else None)

        sess.add(question_db)
        sess.commit()

        for variant in question_form.variants:
            answer_value    = variant.data

            answer_db        = answer_model(value=answer_value, prepared=True)
            question_db.answers.append(answer_db)
            sess.add(answer_db)
            sess.commit()

    #except Exception:
    #    print('Error while adding changes to Data Base!')
    #    sess.rollback()


@app.route('/tests')
@app.route('/tests/<test_id>')
def tests(test_id=None):
    if  test_id:
        return render_template('tests.html', test_id=test_id)
    else:
        sess = db.session
        stmt = select(test_model)
        resp = sess.execute(stmt).scalars()
        test_list = [r for r in resp]
        return render_template('tests.html', test_id=test_id,
                               test_list=test_list
                               #[
                               #    test_model(id=1, title='Тестовое название 1', author_id=1, creation_date='2021-11-11'),
                               #    test_model(id=2, title='Тестовое название 2', author_id=2, creation_date='2021-11-11'),
                               #    test_model(id=3, title='Тестовое название 3', author_id=1, creation_date='2021-11-11')]
                               )


@app.route('/statistics')
@app.route('/statistics/<test_id>')
def statistics(test_id=None):
    return render_template('statistics.html', test_id=test_id)
