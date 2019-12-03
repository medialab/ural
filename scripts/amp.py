from ural.normalize_url import normalize_url
from ural.ensure_protocol import ensure_protocol

with open('./scripts/data/amp-urls.txt') as f:
    for url in f:
        url = url.strip()[1:-1]
        url = normalize_url(url)
        print(ensure_protocol(url))
