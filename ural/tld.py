import codecs
from os.path import dirname, join

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

MOZILLA_PUBLIC_SUFFIX_LIST = "https://publicsuffix.org/list/public_suffix_list.dat"


def download_suffix_list(url):
    response = urlopen(url)

    try:
        data = response.read()
    finally:
        response.close()

    return data.decode("utf-8")


def suffix_list_iter(txt):
    in_private_section = False

    for line in txt.split("\n"):

        # Private section
        if "===BEGIN PRIVATE DOMAINS===" in line:
            in_private_section = True

        # Puny code version
        if "// xn--" in line:
            line = line.split()[1]

        line = line.strip()

        # Comments and paragraph breaks
        if not line or line[0] in ("/", "\n"):
            continue

        yield in_private_section, line


def upgrade_suffix_list(url=MOZILLA_PUBLIC_SUFFIX_LIST):
    txt = download_suffix_list(url)

    output_path = join(dirname(__file__), "tld_list.py")

    with codecs.open(output_path, "w", encoding="utf-8") as f:
        f.write("# coding: utf-8\n")
        f.write("from __future__ import unicode_literals\n\n")
        f.write("SUFFIXES = [\n")

        for private, tld in suffix_list_iter(txt):
            f.write('  (%s, "%s"),\n' % (1 if private else 0, tld))

        f.write("]\n")
