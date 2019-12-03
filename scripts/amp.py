with open('./scripts/data/amp-urls.txt') as f:
    for url in f:
        url = url.strip()[1:-1]
        print(url)
