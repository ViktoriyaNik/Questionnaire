from app import db
from datetime import *


class Answer(db.Model):
    id          = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    value       = db.Column(db.String(1024), nullable=False)
    prepared    = db.Column(db.Boolean, nullable=False)


class Question(db.Model):
    id          = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    title       = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(512))


class Type(db.Model):
    id              = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(8))
    min_variants    = db.Column(db.SmallInteger, nullable=False)
    max_variants    = db.Column(db.SmallInteger, nullable=False)


class User(db.Model):
    id              = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(64), nullable=False)
    sex             = db.Column(db.String(3), nullable=False)
    date_of_birth   = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())

    tests = db.relationship('Test', backref='user', lazy=True, cascade='all, delete')

    @property
    def data(self):
        return f'{self.id}\t{self.name}\t{self.sex}\t{self.date_of_birth}'

    def __repr__(self):
        return self.data

    def __str__(self):
        return self.name


def test():
    s = db.session

    stmt = db.select(User)
    res = s.execute(stmt)
    res = [row[0] for row in res]
    return res


class Test(db.Model):
    id              = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    author_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creation_date   = db.Column(db.DateTime, nullable=False)

    #questions = db.relationship('Question', backref='test', lazy=True, cascade='all, delete')


result = db.Table(
    'result',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), nullable=False),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id'), nullable=False)
)


question_list = db.Table(
    'question_list',
    db.Column('test_id', db.Integer, db.ForeignKey('test.id'), nullable=False),  # TODO
    db.Column('type_id', db.Integer, db.ForeignKey('type.id'), nullable=False),  # TODO
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), nullable=False)
)
