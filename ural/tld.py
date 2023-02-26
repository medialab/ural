# =============================================================================
# Ural TLD-related Functions
# =============================================================================
#
# Some useful links:
#   - https://wiki.mozilla.org/Public_Suffix_List
#   - https://publicsuffix.org/list/public_suffix_list.dat
#   - https://www.iana.org/domains/root/db
#   - https://data.iana.org/TLD/tlds-alpha-by-domain.txt
#   - http://en.wikipedia.org/wiki/List_of_Internet_top-level_domains
#
# NOTE: there is a debate about what is or is not a TLD per se. This is a very
# interesting topic and one should note that the current module follows an
# "operational" definition of a what a TLD is, but not the purist idea of what
# it actually is actually supposed to be (according to IANA at least). Our
# definition is in line with Mozilla's one wrt domain attribution and the
# problem we are trying to address is usually to obtain the accurate domain name
# from a given url, which is not trivial and means you MUST rely on an exhaustive
# and maintained list of current possibilities (as represented by Mozilla's
# public suffix list).
#
# For instance, let's observe the following url:
#   https://www.whatever.co.uk/section/article.html
#
# What we need to extract from this url is what is colloquially known as a
# domain name: "whatever.co.uk"
#
# So we will consider this url TLD as being: ".co.uk", while a purist would
# argue that the actual TLD is ".uk".
#
import codecs
from os.path import dirname, join

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import ural.tld_data as tld_data
from ural.classes.suffix_trie import SuffixTrie
from ural.exceptions import TLDUpgradeError
from ural.utils import attempt_to_decode_idna, safe_urlsplit

MOZILLA_PUBLIC_SUFFIX_LIST = "https://publicsuffix.org/list/public_suffix_list.dat"
IANA_TLD_URL = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"

SUFFIX_TRIE = SuffixTrie()
TLD_SET = set()


def download(url):
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


def get_suffix_lists(txt):
    public_list = []
    private_list = []

    for private, suffix in suffix_list_iter(txt):
        if private:
            private_list.append(suffix)
        else:
            public_list.append(suffix)

    return public_list, private_list


def parse_tlds(txt):
    tlds = []

    for line in txt.split("\n"):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        tlds.append(attempt_to_decode_idna(line.lower()))

    return tlds


def refresh():
    global SUFFIX_TRIE
    global TLD_TRIE

    SUFFIX_TRIE = SuffixTrie()

    for suffix in tld_data.PUBLIC_SUFFIXES:
        SUFFIX_TRIE.add(suffix, private=False)

    for suffix in tld_data.PRIVATE_SUFFIXES:
        SUFFIX_TRIE.add(suffix, private=True)

    for tld in tld_data.TLDS:
        TLD_SET.add(tld)


refresh()


def upgrade(transient=False):
    try:
        mozilla_txt = download(MOZILLA_PUBLIC_SUFFIX_LIST)
        iana_txt = download(IANA_TLD_URL)

        output_path = join(dirname(__file__), "tld_data.py")

        public, private = get_suffix_lists(mozilla_txt)
        tlds = parse_tlds(iana_txt)

        tld_data.PUBLIC_SUFFIXES = public
        tld_data.PRIVATE_SUFFIXES = private
        tld_data.TLDS = tlds

        refresh()

        if transient:
            return

        with codecs.open(output_path, "w", encoding="utf-8") as f:
            f.write("# coding: utf-8\n")
            f.write("from __future__ import unicode_literals\n\n")
            f.write("PUBLIC_SUFFIXES = [\n")
            for suffix in public:
                f.write('  "%s",\n' % suffix)
            f.write("]\n\n")
            f.write("PRIVATE_SUFFIXES = [\n")
            for suffix in private:
                f.write('  "%s",\n' % suffix)
            f.write("]\n\n")
            f.write("TLDS = [\n")
            for tld in tlds:
                f.write('  "%s",\n' % tld)
            f.write("]\n")

    except Exception as reason:
        raise TLDUpgradeError("Could not upgrade TLD lists", reason=reason)


def get_domain_name(url):
    """
    Function returning the given url's domain name as a string. This function
    is of course TLD aware.

    Args:
        url (string): Target url.

    Returns:
        str: the url's domain name.

    """
    return SUFFIX_TRIE.extract_domain_name(url)


def has_valid_suffix(url):
    return SUFFIX_TRIE.has_valid_domain_name(url)


def split_suffix(url):
    return SUFFIX_TRIE.split(url)


def is_valid_tld(tld):
    tld = attempt_to_decode_idna(tld.lstrip(".").lower())

    return tld in TLD_SET


def has_valid_tld(url):
    parsed = safe_urlsplit(url)

    if not parsed.hostname:
        return False

    last_part = parsed.hostname.rsplit(".", 1)[-1]

    return is_valid_tld(last_part)
