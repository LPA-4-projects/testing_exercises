from typing import Mapping


def build_url(host_name: str, relative_url: str, get_params: Mapping[str, str] | None = None) -> str:
    get_params = get_params or {}
    querypart = ''
    if get_params:
        querypart = '?' + '&'.join([f'{k}={v}' for (k, v) in get_params.items()])
    return f'{host_name}/{relative_url}{querypart}'
