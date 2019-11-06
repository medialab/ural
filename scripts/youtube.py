import csv

with open('./scripts/data/youtube-urls.csv') as f:
    reader = csv.reader(f)

    for line in reader:
        youtube_url = line[1]

        print(youtube_url)
