from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, TextAreaField, TimeField, \
    BooleanField, SubmitField, PasswordField, IntegerField, FieldList, \
    FormField, SelectField, DateTimeField, DateField, RadioField, SelectMultipleField, Field
from wtforms.fields.core import UnboundField

from wtforms.validators import email, length, input_required, data_required

from app import db
from app.models import type_model, test_model
from sqlalchemy import select, insert, update

sess = db.session                       # Объект сессии бд
stmt = select(type_model)               # Получение формулировки запроса
resp = sess.execute(stmt).scalars()     # Возвращает итератор по сырым значениям из объектов ответа Row
resp = [r for r in resp]                #
print(resp)
'''
answer_types = {
    t.id: {
        'name': t.name,
        'min_variants': t.min_variants,
        'max_variants': t.max_variants
    } for t in resp}
'''

variants = [(r.id, r.name) for r in resp]


class CreateQuestionField(FlaskForm):
    title           = StringField('Заголовок вопроса', validators=[input_required(), length(min=3, max=64)])
    text            = TextAreaField('Текст вопроса', validators=[length(max=512)])
    answer_type     = SelectField('Тип ответа', choices=variants, validators=[input_required()])
    variants        = FieldList(StringField('Вариант ответа', validators=[input_required()]), min_entries=1)

    button_add_variant     = SubmitField('+')

    def update_on_submit(self):
        if self.button_add_variant.data:
            self.add_variant()
            return True

    def add_variant(self):
        print('VARIANT ADDED')
        self.variants.append_entry()


class UserForm(FlaskForm):
    username    = StringField('Псевдоним', validators=[input_required(), length(min=3, max=64)])
    sex         = SelectField('Пол', choices=['МУЖ', 'ЖЕН'], validators=[input_required()])
    birth       = DateField('Дата рождения', validators=[input_required()])


class CreateTestForm(FlaskForm):
    title           = StringField('Название теста', validators=[input_required(), length(min=5, max=64)])
    author          = FormField(UserForm)

    questions       = FieldList(FormField(CreateQuestionField), min_entries=1)  # TODO there is only ONE question

    button_add_question    = SubmitField('Добавить вопрос')
    submit          = SubmitField('Отправить')

    def update_on_submit(self):
        # Check if add question button pressed
        if self.button_add_question.data:
            self.add_question()
            return True

        # Check if question block is updated
        for question in self.questions:
            if question.update_on_submit():
                return True

    def add_question(self):
        print('QUESTION APPENDED')
        question_block = FormField(CreateQuestionField)
        self.questions.append_entry(question_block)


# from wtforms.meta import DefaultMeta
# from wtforms.form import FormMeta
# from wtforms.fields.core import UnboundField
# Изучить данные классы, скорее всего есть возможность динамически создавать формы
class Answer:
    from wtforms.widgets import RadioInput, TextArea, CheckboxInput, html_params

    def __init__(self, answer_db, html_id: str, html_name: str):
        self.html_id = html_id
        self.html_name = html_name
        self.id = answer_db.id
        self.value = answer_db.value

    # Описание функции как widget объекта, с возможностью вызова, возвращает html,
    # radio  как пример
    def __call__(self, *args, **kwargs):
        return Markup('<input %s>' % self.html_params(id=self.html_id, type='radio', name=self.html_name, **kwargs))

    @property
    def response(self):
        from flask import request
        return request.form.get(self.html_name)


class Question:
    def __init__(self, question_db, html_id: str, result=False):
        self.html_id    = html_id
        self.id         = question_db.id
        self.title      = question_db.title
        self.type       = question_db.type
        self.text       = question_db.text

        if result:
            answers = self.__get_user_db_answers__(question_db.answers)
        else:
            answers = self.__get_prepared_db_answers__(question_db.answers)

        self.answers = []
        for i, answer_db in enumerate(answers):
            id_ = f'-{i}'
            if self.type.id == 1:
                id_ = ''
            elif self.type.id == 2: pass
            elif self.type.id == 3: pass
            answer = Answer(
                    answer_db, html_id + f'-answer-{i}',
                    html_id + f'-answer' + id_
            )

            self.answers.append(answer)

    @classmethod
    def __get_user_db_answers__(cls, all_answers):
        answers = []
        for answer in all_answers:
            if not answer.prepared:
                answers.append(answer)
        return answers

    @classmethod
    def __get_prepared_db_answers__(cls, all_answers):
        answers = []
        for answer in all_answers:
            if answer.prepared:
                answers.append(answer)
        return answers


class Test:
    def __init__(self, test_db, html_id='test-0', result=False):

        self.html_id        = html_id
        self.title          = test_db.title
        self.author_name    = test_db.author.name
        self.creation_date  = test_db.creation_date

        self.questions = [
            Question(
                question_db, self.html_id + f'-question-{i}', result=result
            ) for i, question_db in enumerate(test_db.questions)
        ]

        # from flask import request
        # self.username_input_label = 'Ваше имя'
        # self.username_input_html_id = f'{self.html_id}-username'
        # self.username = request.form.get(self.username_input_html_id)
