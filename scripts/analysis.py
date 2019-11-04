import csv
from urllib.parse import urlsplit, parse_qsl
from collections import Counter
from tqdm import tqdm

from ural import normalize_url

TOP = 50

FRAGMENTS = Counter()
QUERIES = Counter()
QUERIES_COMBO = Counter()

with open('./scripts/data/urls.csv') as f:
    for line in tqdm(f, desc='Reading urls'):
        url = line.strip()[1:-1]
        url = normalize_url(url, strip_protocol=False)
        parsed = urlsplit(url)

        FRAGMENTS[parsed.fragment] += 1

        if parsed.query:
            for name, value in parse_qsl(parsed.query):
                QUERIES[name] += 1
                QUERIES_COMBO['%s=%s' % (name, value)] += 1

def report(name, counter):
    print()

    title = 'Top %i %s:' % (TOP, name)
    print(title)
    print('-' * len(title))

    for record in counter.most_common(TOP):
        print('  • %s - %i' % record)

    print()

report('fragments', FRAGMENTS)
report('queries', QUERIES)
report('queries combo', QUERIES_COMBO)
