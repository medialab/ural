from ural.utils import safe_urlsplit
import re


def is_homepage(url):
    url_tuple = safe_urlsplit(url)
    if (url_tuple.path == '' or url_tuple.path == '/' or 'index' in url_tuple.path or 'home' in url_tuple.path or 'resultats-elections' in url_tuple.path) and (url_tuple.query == '' or url_tuple.fragment == ''):
        return True
    else:
        return False
