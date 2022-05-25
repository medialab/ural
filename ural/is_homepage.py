from ural.utils import safe_urlsplit


def is_homepage(url):
    url_tuple = safe_urlsplit(url)
    if url_tuple.path == '' or \
            url_tuple.path == ' ' \
                or url_tuple.path == '/' \
                    or url_tuple.path == 'index' \
                        or url_tuple.path == '/index' \
                            or url_tuple.path == '/index.html' \
                                or url_tuple.path =='/index.html/' \
                                    or url_tuple.path =='/index.aspx' \
                                        or url_tuple.path =='index' \
                                            or url_tuple.path =='home' \
                                                or url_tuple.path =='/home.html' \
                                                    or url_tuple.path == '/home':
        return True
    return False
