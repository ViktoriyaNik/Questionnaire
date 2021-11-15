from app import db


class Answer(db.Model):
    id          = db.Colummn(db.Integer, nullable=False, auto_increment=True, primary_key=True)
    value       = db.Column(db.String(1024), nullable=False)
    prepared    = db.Column(db.Boolean, nullable=False)


class Question(db.Model):
    id          = db.Column(db.Integer, nullable=False, auto_increment=True)
    title       = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(512))


class Test(db.Model):
    id = db.Column(db.Integer, nullable=False, auto_increment=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    creation_date = db.Column(db.Datetime, nullable=False)


question_list = db.Table(
    'question_list',
    db.Column('test_id', db.Integer, db.ForeignKey()) # TODO
)
