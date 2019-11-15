import re
from scripts.utils import Timer
from urllib.parse import urlsplit
from ural.patterns import DOMAIN_TEMPLATE

N = 1_000_000
URL = 'http://www.lemonde.fr:8000/article/1234/index.html?query=mobile#2'

with Timer('urlsplit'):
    for _ in range(N):
        parsed = urlsplit(URL)
        parsed.hostname

pattern = re.compile(DOMAIN_TEMPLATE % r'lemonde\.fr')
with Timer('regex'):
    for _ in range(N):
        parsed = pattern.match(URL)
