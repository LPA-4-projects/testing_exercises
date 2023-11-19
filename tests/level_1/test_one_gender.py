import pytest

from functions.level_1.one_gender import genderalize


def test__genderalize__return_male_verb_if_male(faker):
    verb_male = faker.pystr()
    verb_female = faker.pystr()
    gender = 'male'

    answer = genderalize(
        verb_male=verb_male,
        verb_female=verb_female,
        gender=gender,
    )

    assert answer == verb_male


def test__genderalize__return_female_verb_if_female(faker):
    verb_male = faker.pystr()
    verb_female = faker.pystr()
    gender = 'female'

    answer = genderalize(
        verb_male=verb_male,
        verb_female=verb_female,
        gender=gender,
    )

    assert answer == verb_female


@pytest.mark.xfail
def test__genderalize__raise_error_if_wrong_gender_word(faker):
    verb_male = faker.pystr()
    verb_female = faker.pystr()
    gender = 'alien'

    with pytest.raises(ValueError):
        genderalize(
            verb_male=verb_male,
            verb_female=verb_female,
            gender=gender,
        )
