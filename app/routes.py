import datetime

from app import app, db
from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_user, login_required, logout_user

from app.forms import CreateTestForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    form = CreateTestForm()
    if form.update_on_submit(): pass
    elif form.validate_on_submit():
        save_test_to_db(form)
        return redirect(url_for('tests'))
    return render_template('create.html', form=form, errors=form.errors)


# Если такой пользователь существует, взять из бд, если нет - создать
def create_user_if_not_exists(user_name: str, user_sex: str, user_birth: datetime.date, sess=db.session):
    if sess.query(exists().where(user_model.name == user_name)).scalar():
        stmt = select(user_model).where(user_model.name == user_name)
        author_db = sess.execute(stmt).scalar()
    else:
        author_db = user_model(name=user_name, sex=user_sex, date_of_birth=user_birth)
        sess.add(author_db)
        sess.commit()
    return author_db


from app.models import question_model, answer_model, test_model, type_model, user_model, result_model
from sqlalchemy import insert, select, exists
def save_test_to_db(form):
    sess = db.session
    #try:
    test_title      = form.title.data
    author_name     = form.author.username.data
    author_sex      = form.author.sex.data
    author_birth    = form.author.birth.data

    author_db = create_user_if_not_exists(author_name, author_sex, author_birth, sess)

    test_db = test_model(title=test_title, author=author_db)

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
@app.route('/tests/<test_id>', methods=['POST', 'GET'])
def tests(test_id=None):
    from app.forms import Test

    if test_id:
        sess = db.session
        stmt = select(test_model).where(test_model.id == test_id)
        test_db = sess.execute(stmt).scalars().first()
        test = Test(test_db)

        if request.method == 'POST':
            user_db = create_user_if_not_exists('test_respondent', 'Mal', datetime.date(2000, 11, 11))
            sess.add(user_db)
            sess.commit()
            for question in test.questions:
                stmt = select(question_model).where(question_model.id == question.id)
                question_db = sess.execute(stmt).scalars().first()
                print('html_id:', question.html_id)
                for answer in question.answers:
                    # print('\thtml_id:', answer.html_id)
                    print('\thtml_name:', answer.html_name)
                    print('\tvalue:', answer.response)

                    stmt = select(answer_model).where(answer_model.id == answer.id)
                    answer_db = sess.execute(stmt).scalars().first()
                    if answer.response:
                        if question.type.id == 3:  # TODO Добавить возможность не отвечать в виде текста
                            answer_db.count += 1
                            answer_db = answer_model(question=question_db, value=answer.response, prepared=False)
                            sess.add(answer_db)
                            sess.commit()
                        else:
                            if int(answer.response) == int(answer_db.id):
                                answer_db.count += 1
                            sess.commit()
                    user_db.answers.append(answer_db)

        return render_template('test.html', test=test)
    else:
        sess = db.session
        stmt = select(test_model)
        resp = sess.execute(stmt).scalars()
        test_list = [r for r in resp]

        # По идее test_id отсюда можно убрать
        return render_template('tests.html', test_id=test_id, test_list=test_list)


@app.route('/statistics')
@app.route('/statistics/<test_id>')
def statistics(test_id=None):
    from app.forms import Test
    sess = db.session
    if test_id:
        stmt = select(test_model).where(test_model.id == test_id)
        test_db = sess.execute(stmt).scalars().first()
        test = Test(test_db, result=True)
        return render_template('statistics.html', test=test)
    else:

        return render_template('statistics.html', test_id=test_id)
