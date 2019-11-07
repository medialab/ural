import csv
from ural.youtube import is_youtube_url, parse_youtube_url

BLACKLIST = {
    'https://www.youtube.com',
    'http://www.youtube.com',
    'https://youtube.com',
    'http://youtube.com',
    'http://www.youtube.com/watch',
    'https://gaming.youtube.com',
    'https://music.youtube.com',
    'https://studio.youtube.com',
    'http://www.youtube.com/channels/paid_channels',
    'https://www.youtube.com/watch?v%3D',
    'https://www.youtube.com/watch',
    'https://youtu.be'
}

BLACKLISTED_PATTERNS = [
    '/creators/',
    '/vi/',
    '/yt/',
    '/t/',
    '/feed/',
    'img.youtube'
]

with open('./scripts/data/youtube-urls.csv') as f:
    reader = csv.reader(f)
    next(reader)

    for line in reader:
        youtube_url = line[1]

        # if 'youtu.be' not in youtube_url:
        #     continue

        if youtube_url in BLACKLIST:
            continue

        if any(p in youtube_url for p in BLACKLISTED_PATTERNS):
            continue

        # if not is_youtube_url(youtube_url):
        #     print(youtube_url)

        result = parse_youtube_url(youtube_url)

        if result is None:
            print(youtube_url)
