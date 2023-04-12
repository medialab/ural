from ebbe import Timer
from ural.utils import safe_urlsplit
from urllib.parse import urlunsplit


def add_param_by_splitting(url, key, value):
    param = "{}={}".format(key, value)

    fragment = None
    query = None

    if "#" in url:
        url, fragment = url.rsplit("#", 1)

    if "?" in url:
        url, query = url.rsplit("?", 1)

    if query:
        query += "&" + param
    elif query is not None:
        query = param

    url += "?" + query

    if fragment is not None:
        url += "#" + fragment

    return url


def add_param_by_urlsplit(url, key, value):
    param = "{}={}".format(key, value)

    splitted = safe_urlsplit(url)

    query = splitted.query

    if query:
        query += "&" + param
    else:
        query = param

    return urlunsplit(
        (
            splitted.scheme,
            splitted.netloc,
            splitted.path,
            splitted.query,
            splitted.fragment,
        )
    )


N = 100_000

with Timer("split"):
    for _ in range(N):
        add_param_by_splitting(
            "http://www.lemonde.fr/path/to/article.html?test#ok", "hello", "world"
        )

with Timer("split"):
    for _ in range(N):
        add_param_by_urlsplit(
            "http://www.lemonde.fr/path/to/article.html?test#ok", "hello", "world"
        )
