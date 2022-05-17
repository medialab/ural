from ural.utils import safe_urlsplit


def is_homepage(url):
    url_tuple = safe_urlsplit(url)
    if url_tuple.path == '':
        return True
    else:
        return False
