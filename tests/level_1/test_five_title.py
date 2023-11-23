import pytest
import random
import string

from functions.level_1.five_title import change_copy_item

ADD_COPY_TEXT = 'Copy of'


def get_copy_number(title: str) -> int:
    copy_number = title.rstrip(')').rsplit('(')[-1]
    return int(copy_number)


@pytest.fixture
def make_fake_title():
    def inner(length: int) -> str:
        return ''.join(random.choice(string.ascii_letters) for i in range(length))
    return inner


@pytest.fixture
def make_title_with_add_copy_text(make_fake_title):
    def inner(add_copy_text: str, length: int) -> str:
        title = make_fake_title(length)
        return f'{add_copy_text} {title}'
    return inner


@pytest.fixture
def make_copy_title(make_title_with_add_copy_text, faker):
    def inner(add_copy_text: str, length: int) -> str:
        title = make_title_with_add_copy_text(add_copy_text=add_copy_text, length=length)
        copy_number = faker.pyint(min_value=2)
        return f'{title} ({copy_number})'
    return inner


def test__change_copy_item__return_title_if_len_is_equal_max_main_item_title_length(make_fake_title):
    max_main_item_title_length: int = 10
    title: str = make_fake_title(max_main_item_title_length)

    copy_item = change_copy_item(title=title, max_main_item_title_length=max_main_item_title_length)
    assert copy_item == title


def test__change_copy_item__return_title_if_len_is_greater_than_max_main_item_title_length(make_fake_title):
    max_main_item_title_length: int = 10
    title: str = make_fake_title(max_main_item_title_length + 1)

    copy_item = change_copy_item(title=title, max_main_item_title_length=max_main_item_title_length)
    assert copy_item == title


def test__change_copy_item__works_correctly_with_default_max_main_item_title_length(make_fake_title):
    title: str = make_fake_title(100)

    copy_item = change_copy_item(title=title)
    assert copy_item == title, 'must return title without additional copy text'


def test__change_copy_item__return_title_with_additional_copy_text_if_not_start_with_add_copy_text(make_fake_title):
    additional_copy_text: str = ADD_COPY_TEXT
    title: str = make_fake_title(10)

    copy_item = change_copy_item(title=title)
    
    assert copy_item.startswith(additional_copy_text)
    assert not copy_item.strip().endswith('(2)')


def test__change_copy_item__return_title_with_copy_number_2_if_no_copy_number(make_title_with_add_copy_text):
    title: str = make_title_with_add_copy_text(add_copy_text=ADD_COPY_TEXT, length=10)

    copy_item = change_copy_item(title=title)
    assert copy_item.strip().endswith('(2)')


def test__change_copy_item__increase_copy_number(make_copy_title):
    title: str = make_copy_title(add_copy_text=ADD_COPY_TEXT, length=10)
    copy_number = get_copy_number(title)

    copy = change_copy_item(title=title)
    new_copy_number = get_copy_number(copy)
    
    assert new_copy_number == copy_number + 1
    