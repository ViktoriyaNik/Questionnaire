from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, TimeField,\
    BooleanField, SubmitField, PasswordField, IntegerField, FieldList, \
    FormField, SelectField, DateTimeField, DateField

from wtforms.validators import email, length, input_required, data_required

from app import db
from app.models import type_model
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


class QuestionVariantField(FlaskForm):
    variant = StringField('Вариант')


class QuestionField(FlaskForm):
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


class TestForm(FlaskForm):
    title           = StringField('Название теста', validators=[input_required(), length(min=5, max=64)])
    author_name     = StringField('Имя автора', validators=[input_required(), length(min=3, max=64)])
    author_sex      = SelectField('Пол автора', choices=['МУЖ', 'ЖЕН'], validators=[input_required()])
    author_birth    = DateField('Дата рождения', validators=[input_required()])

    questions       = FieldList(FormField(QuestionField), min_entries=1)  # TODO there is only ONE question

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
        question_block = FormField(QuestionField)
        self.questions.append_entry(question_block)
