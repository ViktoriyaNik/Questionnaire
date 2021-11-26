from flask_wtf import FlaskForm
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


class CreateTestForm(FlaskForm):
    title           = StringField('Название теста', validators=[input_required(), length(min=5, max=64)])
    author_name     = StringField('Имя автора', validators=[input_required(), length(min=3, max=64)])
    author_sex      = SelectField('Пол автора', choices=['МУЖ', 'ЖЕН'], validators=[input_required()])
    author_birth    = DateField('Дата рождения', validators=[input_required()])

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


class Answer:
    def __init__(self, answer_db):
        self.value = answer_db.value


class Question:
    def __init__(self, question_db):
        self.title = question_db.title
        self.type = question_db.type
        self.text = question_db.text

        # Берёт все, не только которые были создыны автором TODO
        self.answers = [Answer(answer_db) for answer_db in question_db.answers]


class Test:
    def __init__(self, test_db):
        self.title = test_db.title
        self.author_name = test_db.author.name
        self.creation_date = test_db.creation_date

        self.questions = [Question(question_db) for question_db in test_db.questions]
