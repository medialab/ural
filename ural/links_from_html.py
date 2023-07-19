from ural.canonicalize_url import canonicalize_url
from ural.urls_from_html import urls_from_html
from ural.should_follow_href import should_follow_href
from ural.is_url import is_url
from ural.utils import urljoin
from ural.patterns import PROTOCOL_RE


def links_from_html(
    base_url,
    html_body,
    encoding="utf-8",
    canonicalize=False,
    unique=False,
    strip_fragment=False,
):
    already_seen = set()

    if canonicalize:
        base_url = canonicalize_url(base_url, strip_fragment=strip_fragment)

    # NOTE: urls_from_html strips urls, no need to redo it
    for url in urls_from_html(html_body, encoding=encoding, errors="replace"):

        # Empty url is basically self
        if not url:
            continue

        if not should_follow_href(url):
            continue

        # urllib.parse.urljoin lowercases protocol...
        if not PROTOCOL_RE.match(url):
            url = urljoin(base_url, url)

        if not is_url(
            url,
            require_protocol=True,
            tld_aware=True,
            allow_spaces_in_path=True,
            only_http_https=True,
        ):
            continue

        if canonicalize:
            url = canonicalize_url(url, strip_fragment=strip_fragment)

        if url == base_url:
            continue

        if unique:
            if url in already_seen:
                continue

            already_seen.add(url)

        yield url
