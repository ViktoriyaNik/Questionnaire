from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, BooleanField, SubmitField, PasswordField, IntegerField, FieldList, \
    FormField, SelectField, DateTimeField
from wtforms.validators import DataRequired, EqualTo, Email


class TestForm(FlaskForm):
    pass


class QuestionField(FlaskForm):
    question_title = StringField('Заголовок')
