import csv
from ural import normalize_url

with open('./scripts/data/tricky.csv') as f:
    reader = csv.DictReader(f)

    for line in reader:
        if not line['expanded_links']:
            continue

        for url in line['expanded_links'].split('|'):
            try:
                normalize_url(url)
            except Exception as e:
                print(e, url)
