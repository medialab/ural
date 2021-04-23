# =============================================================================
# Ural Shortened Url Testing Function
# =============================================================================
#
# Function testing whether the given url is probably a shortened url or not.
#
from phylactery import TrieDict

from ural.utils import safe_urlsplit, SplitResult

SHORTENER_DOMAINS = [
    'adec.co',
    'amn.st',
    'bddy.me',
    'bit.ly',
    'bitly.com',
    'buff.ly',
    'crwd.fr',
    'disq.us',
    'dlvr.it',
    'ebx.sh',
    'ed.gr',
    'fal.cn',
    'fb.me',
    'feedproxy.google.com',
    'flip.it',
    'frama.link',
    'fw.to',
    'gerd.fm',
    'goo.gl',
    'go.shr.lc',
    'ht.ly',
    'hubs.ly',
    'ift.tt',
    'io.webhelp.com',
    'is.gd',
    'j.mp',
    'lc.cx',
    'lnkd.in',
    'loom.ly',
    'mon.actu.io',
    'msft.social',
    'mtr.cool',
    'non.li',
    'owl.li',
    'ow.ly',
    'po.st',
    'sco.lt',
    'shar.es',
    'soc.fm',
    'spr.ly',
    'swll.to',
    't.co',
    'tinyurl.com',
    'tmblr.co',
    'trib.al',
    'twib.in',
    'u.afp.com',
    'urlz.fr',
    'wp.me',
    'wrld.bg',
    'xfru.it',
    'youtu.be',
    'zpr.io'
]

TRIE = TrieDict()

for domain in SHORTENER_DOMAINS:
    TRIE.set(reversed(domain.split('.')), True)


def is_shortened_url(url):
    if isinstance(url, SplitResult):
        parsed = url
    else:
        parsed = safe_urlsplit(url)

    if parsed.hostname is None:
        return False

    return bool(TRIE.longest(reversed(parsed.hostname.split('.'))))
