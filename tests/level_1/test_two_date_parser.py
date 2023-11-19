import datetime
import pytest

from functions.level_1.two_date_parser import compose_datetime_from


@pytest.fixture
def make_time_str(faker) -> str:
    hours, minutes, _ = faker.time().split(':')
    return f'{hours}:{minutes}'


def test__compose_datetime_from__return_correct_datetime(make_time_str):
    now = datetime.date.today()

    time_str = make_time_str
    hours, minutes = time_str.split(':')
    time = datetime.time(hour=int(hours), minute=int(minutes))

    answer = compose_datetime_from(date_str='now', time_str=time_str)

    assert type(answer) == datetime.datetime
    assert answer.day == now.day
    assert answer.month == now.month
    assert answer.year == now.year
    assert answer.hour == time.hour
    assert answer.minute == time.minute


def test__compose_datetime_from__return_correct_datetime_for_tomorrow_date_str(make_time_str):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    time_str = make_time_str
    hours, minutes = time_str.split(':')
    time = datetime.time(hour=int(hours), minute=int(minutes))

    answer = compose_datetime_from(date_str='tomorrow', time_str=time_str)

    assert type(answer) == datetime.datetime
    assert answer.day == tomorrow.day
    assert answer.month == tomorrow.month
    assert answer.year == tomorrow.year
    assert answer.hour == time.hour
    assert answer.minute == time.minute
