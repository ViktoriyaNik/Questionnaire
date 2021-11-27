from app import db
from datetime import *


result = db.Table(
    'result',
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id'), nullable=False),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class Answer(db.Model):
    id          = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    value       = db.Column(db.String(1024), nullable=False)
    prepared    = db.Column(db.Boolean, nullable=False)
    count       = db.Column(db.Integer, nullable=False, default=0)


class Question(db.Model):
    id          = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    type_id     = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    test_id     = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    title       = db.Column(db.String(64), nullable=False)
    text        = db.Column(db.String(512))

    # Relationships
    answers     = db.relationship('Answer', backref='question', lazy='dynamic', cascade='all, delete')  # TODO invalid cascade


class Type(db.Model):
    id              = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(32))
    min_variants    = db.Column(db.SmallInteger, nullable=False)
    max_variants    = db.Column(db.SmallInteger, nullable=False)

    # Relationships
    questions       = db.relationship('Question', backref='type', cascade='all, delete')


class User(db.Model):
    id              = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(64), nullable=False, unique=True)
    sex             = db.Column(db.String(3), nullable=False)
    date_of_birth   = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())

    # Relationships
    tests           = db.relationship('Test', backref='author', cascade='all, delete')
    answers         = db.relationship('Answer', secondary=result, backref=db.backref('user', cascade='all, delete'))

    @property
    def data(self):
        return f'{self.id}\t{self.name}\t{self.sex}\t{self.date_of_birth}'

    def __repr__(self):
        return self.data

    def __str__(self):
        return self.name


class Test(db.Model):
    id              = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    title           = db.Column(db.String(64), nullable=False, unique=True)
    author_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creation_date   = db.Column(db.DateTime, default=datetime.utcnow().date(), nullable=False)

    # Relationships
    questions       = db.relationship('Question', backref='test', lazy='dynamic', cascade='all, delete')


# Приведение названий моделей к именам таблиц в базе данных

test_model      = Test
user_model      = User
type_model      = Type
question_model  = Question
answer_model    = Answer
result_model    = result
