from functions.level_1.three_url_builder import build_url


def test__build_url__can_build_url_with_params():
    url = 'https://yandex.ru/search?text=pytest_testdox+configure&lr=213&clid=2270455&win=414'
    host = 'https://yandex.ru'
    path = 'search'
    params = {
        'text': 'pytest_testdox+configure',
        'lr': '213',
        'clid': '2270455',
        'win': '414',
    }

    answer = build_url(
        host_name=host,
        relative_url=path,
        get_params=params,
    )

    assert answer == url


def test__build_url__can_build_url_without_params():
    url = 'https://yandex.ru/search'
    host = 'https://yandex.ru'
    path = 'search'

    answer = build_url(
        host_name=host,
        relative_url=path,
        get_params=None,
    )

    assert answer == url
