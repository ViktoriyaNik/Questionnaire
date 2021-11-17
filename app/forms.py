from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, TimeField, BooleanField, SubmitField, PasswordField, IntegerField, FieldList, \
    FormField, SelectField, DateTimeField, DateField

from wtforms.validators import email, length, input_required, data_required


class QuestionVariantField(FlaskForm):
    variant = StringField('Вариант')


class QuestionField(FlaskForm):
    title   = StringField('Заголовок вопроса', validators=[input_required(), length(min=3, max=64)])
    text    = TextAreaField('Текст вопроса', validators=[length(max=512)])

    variants         = FieldList(FormField(QuestionVariantField), min_entries=1)


class TestForm(FlaskForm):
    title      = StringField('Название теста', validators=[input_required(), length(min=5, max=64)])
    author_name     = StringField('Имя автора', validators=[input_required(), length(min=3, max=64)])
    author_birth    = DateField('Дата рождения', validators=[input_required()])

    questions = FieldList(FormField(QuestionField), min_entries=1)  # TODO there is only ONE question
    # questions.append_entry(None)
