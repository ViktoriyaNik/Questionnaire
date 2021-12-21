from app import db
from sqlalchemy import select
from app.models import *


sess = db.session


class GeneralStatisticsData:
    def __init__(self):
        self.users = {
            'count': users_count,
            'mal_count': mal_count,
            'fem_count': fem_count
        }

        self.tests = {
            'count': tests_count,
            'question_count': questions_count,
            'answers_count': answers_count,
            'one_choice_answers_count': one_choice_answers_count,
            'any_choices_answers_count': any_choices_answers_count,
            'text_answers_count': text_answers_count
        }

        self.respondents = {
            'age_0_13':  respondents_age_0_13,
            'age_14_20': respondents_age_14_20,
            'age_21_35': respondents_age_21_35,
            'age_36_50': respondents_age_36_50,
            'age_51_70': respondents_age_51_70,
            'age_71_99': respondents_age_71_99
        }


def get_general_statistics():
    stmt = select(user_model)
    resp = sess.execute(stmt).scalars()
    users_db = [user_db for user_db in resp]

    users_count = len(users_db)
    fem_count = 0
    mal_count = 0
    for user_db in users_db:
        sex = user_db.sex.upper()
        if sex == 'FEM' or sex == 'ЖЕН':
            fem_count += 1
        else: mal_count += 1



'''
test_result
<id>, <test_id>, <user_id>, <completion_datetime>

create table `test_result` (
    `id` int not null auto_increment primary key,
    `test_id` int not null,
    `user_id` int not null,
    `completion_datetime` datetime not null,
    foreign key (`test_id`) references `test` (`id`) on delete cascade on update cascade,
    foreign key (`user_id`) references `user` (`id`) on delete cascade on update cascade
);
'''
