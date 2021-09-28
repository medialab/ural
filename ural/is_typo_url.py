# -*- coding: utf-8 -*-
# =============================================================================
# Ural URL Is Typo Url Function
# =============================================================================
#
# A function returning True if its argument is detected as typo.
#
from ural.strip_protocol import strip_protocol

ERROR_TLDS = {'cab', 'global', 'ren', 'gay', 'baby', 'gallery', 'red', 'tattoo', 'lincoln', 'ooo', 'new', 'barcelona', 'med', 'photos',
              'africa', 'film', 'sale', 'amazon', 'rip', 'love', 'py', 'android', 'video', 'kim', 'ro', 'ck', 'ba', 'day', 'bayern', 'mm',
              'luxe', 'blog', 'mo', 'gm', 'design', 'vote', 'pub', 'blue', 'bn', 'zip', 'style', 'nu', 'ml', 'mil', 'youtube', 'eco',
              'place', 'et', 'fk', 'ni', 'rent', 'bond', 'prod', 'post', 'berlin', 'protection', 'you', 'gh', 'by', 'clothing', 'ls', 'np',
              'sexy', 'il', 'ferrero', 'map', 'bom', 'bb', 'skin', 'bible', 'buy', 'market', 'ice', 'cfa',
              'group', 'office', 'meme', 'dm', 'vi', 'xxx', 'audio', 'dupont', 'cv', 'science', 'pharmacy', 'systems', 'ga', 'contact', 'family',
              'sport', 'gallup', 'zara', 'ms', 'cz', 'sj', 'maison', 'dj', 'hockey', 'pk', 'cash', 'ag',
              'cr', 'ink', 'website', 'mt', 'pr', 'bio', 'ses', 'lol', 'iq', 'norton', 'kh', 'la', 'hair', 'chat', 'wow', 'bo', 'mg', 'ss',
              'osaka', 'sh', 'ge', 'lifestyle', 'now', 'tel', 'mr', 'click', 'ping', 'earth', 'eus', 'shell', 'football', 'tours', 'surgery',
              'dot', 'mma', 'zero', 'ing', 'read', 'credit', 'mc', 'black', 'inc', 'tennis', 'author', 'like', 'social', 'mov', 'er', 'apple',
              'moi', 'google', 'suzuki', 'smile', 'able', 'xin', 'sm', 'sx', 'plus', 'ao', 'am', 'lk', 'no', 'box',
              'vision', 'gp', 'vu', 'name', 'delta', 've', 'quebec', 'lat', 'off', 'house', 'ltd', 'na', 'bs', 'bmw', 'game', 'rugby', 'mw',
              'total', 'aw', 'man', 'ceo', 'madrid', 'star', 'build', 'data', 'ye', 'pictures', 'gu', 'gle', 'baseball', 'je', 'car',
              'helsinki', 'buzz', 'im', 'kn', 'mu', 'sr', 'va', 'pa', 'sakura', 'fox', 'phone', 'sa', 'ki', 'tiffany', 'ps', 'rocher', 're',
              'men', 'beauty', 'boo', 'sy', 'pet', 'km', 'gb', 'open', 'pin', 'jo', 'zw', 'ne', 'so', 'ky', 'play',
              'pics', 'mtn', 'dvr'}

ERROR_INCLUSIVE = [u'é.es', 'eux.se', 's.es', 'eur.se', 'eu.r.se', 'ant.es', 'eu.x.se', 'eu.se', 'un.es', '.e.es',
                   'eux.ses', 'r.es', 'ois.es', 't.es', 'l.es', 'i.es', 'n.es', 'u.es']


def is_typo_url(link):
    """
    Function returning True if its argument is detected as url typo.

    Args:
        link (str): string to test.

    Returns:
        bool: True if the argument contains typo, False if not.

    """
    # tests if there is a '/' in the url except if it is at the end
    protocoleless_link = strip_protocol(link)
    slash_count = protocoleless_link.count("/")
    if slash_count > 1:
        return False
    elif slash_count == 1:
        if not protocoleless_link.endswith("/"):
            return False

    # tests if there is a ? in the url
    if '?' in protocoleless_link:
        return False

    # tests if '.co' is contained in the url
    if '.co.' in protocoleless_link:
        return False

    link = link.rstrip('/')
    _, tld = link.rsplit('.', 1)

    return (any(char.islower() for char in tld) and any(char.isupper() for char in tld)) or tld.lower() in ERROR_TLDS or is_inclusive_language(link)


def is_inclusive_language(link):
    """
    Function returning True if its argument contains inclusive language (in french)
    """
    for pattern in ERROR_INCLUSIVE:
        if link.lower().endswith(pattern):
            return True
    return False
