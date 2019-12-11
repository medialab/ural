import csv
from scripts.utils import Timer


class CSVLine(object):
    __slots__  = ('line', 'pos')

    def __init__(self, line):
        self.line = line
        self.pos = {'youtube_url': 1}

    def __getitem__(self, key):
        return self.line[1]


class SwiftCSVReader(object):
    def __init__(self, reader):
        self.reader = reader

    def __iter__(self):
        return self

    def __next__(self):
        try:
            line = next(self.reader)
            return CSVLine(line)
        except StopIteration:
            raise


with Timer('reader'):
    with open('./scripts/data/youtube-urls.csv') as f:
        for line in csv.reader(f):
            line[1]

with Timer('DictReader'):
    with open('./scripts/data/youtube-urls.csv') as f:
        for line in csv.DictReader(f):
            line['youtube_url']

with Timer('SwiftCSVReader'):
    with open('./scripts/data/youtube-urls.csv') as f:
        for line in SwiftCSVReader(csv.reader(f)):
            line['youtube_url']
