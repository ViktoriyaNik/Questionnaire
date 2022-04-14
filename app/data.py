from app import db
from sqlalchemy import select
from app.models import *
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


__all__ = [
    'UsersStatisticsData',
    'QuestionsStatisticsData',
    'AnswersStatisticsData',
    'TestsStatisticsData',
    'GeneralStatisticsData',
    'get_users_statistics',
    'get_question_statistics',
    'get_answers_statistics',
    'get_tests_statistics',
    'get_general_statistics'
    ]

sess = db.session


def dec(val):
    return Decimal(str(val))


def get_age(born: date, at: date = date.today()):
    return at.year - born.year - ((at.month, at.day) < (born.month, born.day))


def to_percents(all: int, partial: int):
    return round(dec(100) * dec(partial / all if all != 0 else 1), 2)


def get_users_statistics(users_db=None):
    if not users_db:
        stmt = select(user_model)
        resp = sess.execute(stmt).scalars()
        users_db = [user_db for user_db in resp]

    count = len(users_db)
    fem_count = 0
    mal_count = 0

    age_0_13_count = 0
    age_14_20_count = 0
    age_21_35_count = 0
    age_36_50_count = 0
    age_51_70_count = 0
    age_71_99_count = 0
    for user_db in users_db:
        # calculate sex count
        sex = user_db.sex.upper()
        if sex == 'FEM' or sex == 'ЖЕН':
            fem_count += 1
        else: mal_count += 1

        # calculate ages count
        age = get_age(user_db.date_of_birth)
        if age < 14: age_0_13_count += 1
        elif age < 21: age_14_20_count += 1
        elif age < 36: age_21_35_count += 1
        elif age < 51: age_36_50_count += 1
        elif age < 71: age_51_70_count += 1
        elif age < 100: age_71_99_count += 1

    # define sex percentage
    fem_percentage = to_percents(count, fem_count)
    mal_percentage = to_percents(count, count - fem_count)

    # define ages percentage
    age_0_13_percentage = to_percents(count, age_0_13_count)
    age_14_20_percentage = to_percents(count, age_14_20_count)
    age_21_35_percentage = to_percents(count, age_21_35_count)
    age_36_50_percentage = to_percents(count, age_36_50_count)
    age_51_70_percentage = to_percents(count, age_51_70_count)
    age_71_99_percentage = to_percents(count, age_71_99_count)

    return UsersStatisticsData(
        count=count,
        fem_count=fem_count,
        mal_count=mal_count,
        fem_percentage=fem_percentage,
        mal_percentage=mal_percentage,

        age_0_13_count=age_0_13_count,
        age_14_20_count=age_14_20_count,
        age_21_35_count=age_21_35_count,
        age_36_50_count=age_36_50_count,
        age_51_70_count=age_51_70_count,
        age_71_99_count=age_71_99_count,

        age_0_13_percentage=age_0_13_percentage,
        age_14_20_percentage=age_14_20_percentage,
        age_21_35_percentage=age_21_35_percentage,
        age_36_50_percentage=age_36_50_percentage,
        age_51_70_percentage=age_51_70_percentage,
        age_71_99_percentage=age_71_99_percentage
    )


def get_question_statistics(questions_db=None):
    if not questions_db:
        stmt = select(question_model)
        resp = sess.execute(stmt).scalars()
        questions_db = [question_db for question_db in resp]

    questions_dto = QuestionsStatisticsData()
    questions_dto.count = len(questions_db)
    for question_db in questions_db:
        answ_type = question_db.type.id
        if answ_type == 1: questions_dto.one_choice_count += 1
        elif answ_type == 2: questions_dto.any_choices_count += 1
        elif answ_type == 3: questions_dto.text_answer_count += 1

    questions_dto.one_choice_percentage = to_percents(questions_dto.count, questions_dto.one_choice_count)
    questions_dto.any_choices_percentage = to_percents(questions_dto.count, questions_dto.any_choices_count)
    questions_dto.text_answer_percentage = to_percents(questions_dto.count, questions_dto.text_answer_count)
    return questions_dto


def get_answers_statistics(answers_db=None):
    if not answers_db:
        stmt = select(answer_model)
        resp = sess.execute(stmt).scalars()
        answers_db = [answer_db for answer_db in resp]

    answers_dto = AnswersStatisticsData()
    answers_dto.count = len(answers_db)
    for answer_db in answers_db:
        user_answer = answer_db.prepared
        if user_answer: answers_dto.prepared_count += 1
        else: answers_dto.user_count += 1
        answers_dto.responses_count += answer_db.count
    return answers_dto


def get_tests_statistics(tests_db=None):
    if not tests_db:
        stmt = select(test_model)
        resp = sess.execute(stmt).scalars()
        tests_db = [test_db for test_db in resp]

    tests_dto = TestsStatisticsData()
    tests_dto.count = len(tests_db)
    tests_dto.questions = get_question_statistics()
    return tests_dto


def get_general_statistics():
    general = GeneralStatisticsData()
    general.respondents = get_users_statistics()
    general.tests = get_tests_statistics()
    return general


@dataclass
class UsersStatisticsData:
    count: int = 0
    fem_count: int = 0
    mal_count: int = 0
    fem_percentage: float = 0
    mal_percentage: float = 0

    age_0_13_count: int = 0
    age_14_20_count: int = 0
    age_21_35_count: int = 0
    age_36_50_count: int = 0
    age_51_70_count: int = 0
    age_71_99_count: int = 0

    age_0_13_percentage: float = 0
    age_14_20_percentage: float = 0
    age_21_35_percentage: float = 0
    age_36_50_percentage: float = 0
    age_51_70_percentage: float = 0
    age_71_99_percentage: float = 0


@dataclass
class QuestionsStatisticsData:
    count: int = 0
    one_choice_count: int = 0
    any_choices_count: int = 0
    text_answer_count: int = 0

    one_choice_percentage: float = 0
    any_choices_percentage: float = 0
    text_answer_percentage: float = 0


@dataclass
class AnswersStatisticsData:
    count: int = 0
    prepared_count: int = 0
    user_count: int = 0
    responses_count: int = 0


@dataclass
class TestsStatisticsData:
    count: int = None
    questions: QuestionsStatisticsData = None
    answers: AnswersStatisticsData = None


@dataclass
class GeneralStatisticsData:
    respondents: UsersStatisticsData = None
    tests: TestsStatisticsData = None


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
