from ural.utils import safe_urlsplit

homepage_paths = ['', '/', 'index', '/index', '/index.html', '/index.html/', '/index.aspx', 'index', 'home', '/home.html', '/home']


def is_homepage(url):
    url_tuple = safe_urlsplit(url)
    if url_tuple.path in homepage_paths:
        return True
    return False
