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


class TextAnswerForm(FlaskForm):
    input = TextAreaField()

class CheckAnswerForm(FlaskForm):
    value = BooleanField()

class ChoiceAnswerForm(FlaskForm):
    value = RadioField()

class GetTestedQuestionForm(FlaskForm):
    @classmethod
    def append_field(cls, name, field):
        setattr(cls, name, field)
        return cls


class GetTestedForm(FlaskForm):
    questions = FieldList(FormField(GetTestedQuestionForm))


def load_get_tested_form_from_db(test_id: int):
    sess = db.session
    stmt = select(test_model).where(test_model.id == test_id)
    resp = sess.execute(stmt).scalars().first()
    test_db = resp

    form = GetTestedForm()

    form.title = test_db.title
    form.author = test_db.author
    form.creation_date = test_db.creation_date


    for question_db in test_db.questions:
        # Чтобы поля класса не затирались (объект формы всегда приводится к определённому виду в методе append_entry())
        # необходимо либо добавлять объекты минуя этот метод, напрямую в entries, либо как здесь,
        # добавляя свойства объекта после его добавления в форму
        question = form.questions.append_entry()
        question.title = question_db.title
        question.type = question_db.type
        question.text = question_db.text

        GetTestedQuestionForm.answers = FieldList(FlaskForm(ChoiceAnswerForm))
        question.answers.append_entry(FlaskForm(ChoiceAnswerForm('sdf')))
        print(question.answers)

        '''
        if question_db.type.id == 1:
            print(question_db.type)
            GetTestedQuestionForm.answers = FieldList(RadioField())
        elif question_db.type.id == 2:
            print(question_db.type)
            GetTestedQuestionForm.answers = FieldList(BooleanField())

        elif question_db.type.id == 3:
            print(question_db.type)
            GetTestedQuestionForm.answers = FieldList(TextAreaField())
        for answer in question_db.answers:
            question.answers.append_entry().label = answer.value
        '''

        for answer in question.answers:
            print(answer)

    return form, test_db



