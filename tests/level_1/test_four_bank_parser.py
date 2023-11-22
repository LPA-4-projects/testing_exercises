import datetime
import random
import pytest
import string
from decimal import Decimal

from functions.level_1.four_bank_parser import BankCard, SmsMessage, Expense, parse_ineco_expense


@pytest.fixture
def payment_amount(faker):
    return faker.pydecimal(right_digits=2, positive=True, min_value=0.01)


@pytest.fixture
def person(faker):
    return f'{faker.first_name()} {faker.last_name()}'


@pytest.fixture
def spent_in_place(faker):
    return faker.pystr()


@pytest.fixture
def spent_at_time(faker):
    spent_at_date = faker.date(pattern='%d.%m.%y')
    spent_at_time = faker.time(pattern='%H:%M')
    return f'{spent_at_date} {spent_at_time}'


@pytest.fixture
def make_sms_text():
    def inner(amount: Decimal, card_number: str, spent_at: str, spent_in: str):
        return f'Payment {amount} AMD, {card_number} {spent_at} {spent_in} authcode xxxxxxx'
    return inner


@pytest.fixture
def make_number_as_string():
    def inner(length: int) -> str:
        return ''.join(random.choice(string.digits) for i in range(length))
    return inner


@pytest.fixture
def make_card_number(make_number_as_string):
    def inner(last_digits: str | None = None) -> str:
        last_digits = last_digits or make_number_as_string(length=4)
        number = make_number_as_string(length=12)
        return f'{number}{last_digits}'
    return inner


@pytest.fixture
def make_card(faker):
    def inner(last_digits: str | None = None, owner: str | None = None) -> BankCard:
        return BankCard(
            last_digits=last_digits or str(faker.pyint(min_value=1000, max_value=9999)),
            owner=owner or f'{faker.first_name()} {faker.last_name()}',
        )
    return inner


@pytest.fixture
def make_cards(person, make_number_as_string):
    def inner(count: int) -> list[BankCard]:
        return [
            BankCard(
                last_digits=make_number_as_string(length=4),
                owner=person,
            )
            for i in range(count)
        ]
    return inner


def test__parse_ineco_expense__return_correct_data_structure(
    faker,
    make_card,
    make_card_number,
    payment_amount,
    person,
    spent_in_place,
    spent_at_time,
    make_sms_text,
):
    card: BankCard = make_card()
    card_number: str = make_card_number(card.last_digits)
    amount: Decimal = payment_amount
    spent_in: str = spent_in_place
    spent_at: str = spent_at_time

    sms = SmsMessage(
        text=make_sms_text(amount=amount, card_number=card_number, spent_at=spent_at, spent_in=spent_in),
        author=person,
        sent_at=faker.date_time(),
    )

    expense = parse_ineco_expense(sms=sms, cards=[card])

    assert type(expense) == Expense
    assert expense.amount == amount
    assert expense.card.last_digits == card.last_digits
    assert expense.card.owner == card.owner
    assert expense.spent_in == spent_in
    assert expense.spent_at == datetime.datetime.strptime(spent_at, '%d.%m.%y %H:%M')


def test__parse_ineco_expense__can_choose_the_right_card(
    faker,
    make_cards,
    make_card_number,
    payment_amount,
    person,
    spent_in_place,
    spent_at_time,
    make_sms_text,
):
    cards: list[BankCard] = make_cards(count=3)
    card_number: str = make_card_number(cards[0].last_digits)
    amount = payment_amount
    spent_in = spent_in_place
    spent_at = spent_at_time
    sms = SmsMessage(
        text=make_sms_text(amount=amount, card_number=card_number, spent_at=spent_at, spent_in=spent_in),
        author=person,
        sent_at=faker.date_time(),
    )

    expense = parse_ineco_expense(sms=sms, cards=cards)

    assert expense.card.last_digits == cards[0].last_digits
