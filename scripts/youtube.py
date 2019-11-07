import csv
from ural.youtube import is_youtube_url

with open('./scripts/data/youtube-urls.csv') as f:
    reader = csv.reader(f)
    next(reader)

    for line in reader:
        youtube_url = line[1]

        # if not is_youtube_url(youtube_url):
        #     print(youtube_url)
