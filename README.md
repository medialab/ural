[![Build Status](https://github.com/medialab/ural/workflows/Tests/badge.svg)](https://github.com/medialab/ural/actions) [![DOI](https://zenodo.org/badge/133951636.svg)](https://zenodo.org/badge/latestdoi/133951636)

# Ural

A python helper library full of URL-related heuristics.

## Installation

You can install `ural` with pip with the following command:

```
pip install ural
```

## How to cite?

`ural` is published on [Zenodo](https://zenodo.org/) as [![DOI](https://zenodo.org/badge/133951636.svg)](https://zenodo.org/badge/latestdoi/133951636)

You can cite it thusly:

> Guillaume Plique, Jules Farjas, Oubine Perrin, Benjamin Ooghe-Tabanou, Martin Delabre, Pauline Breteau, Jean Descamps, Béatrice Mazoyer, Amélie Pellé, Laura Miguel, & César Pichon. Ural, a python helper library full of URL-related heuristics. (2018). Zenodo. https://doi.org/10.5281/zenodo.8160139

## Usage

*Generic functions*

* [canonicalize_url](#canonicalize_url)
* [could_be_html](#could_be_html)
* [could_be_rss](#could_be_rss)
* [ensure_protocol](#ensure_protocol)
* [fingerprint_hostname](#fingerprint_hostname)
* [fingerprint_url](#fingerprint_url)
* [force_protocol](#force_protocol)
* [format_url](#format_url)
* [get_domain_name](#get_domain_name)
* [get_hostname](#get_hostname)
* [get_fingerprinted_hostname](#get_fingerprinted_hostname)
* [get_normalized_hostname](#get_normalized_hostname)
* [has_special_host](#has_special_host)
* [has_valid_suffix](#has_valid_suffix)
* [has_valid_tld](#has_valid_tld)
* [infer_redirection](#infer_redirection)
* [is_homepage](#is_homepage)
* [is_shortened_url](#is_shortened_url)
* [is_special_host](#is_special_host)
* [is_typo_url](#is_typo_url)
* [is_url](#is_url)
* [is_valid_tld](#is_valid_tld)
* [links_from_html](#links_from_html)
* [normalize_hostname](#normalize_hostname)
* [normalize_url](#normalize_url)
* [should_follow_href](#should_follow_href)
* [should_resolve](#should_resolve)
* [split_suffix](#split_suffix)
* [strip_protocol](#strip_protocol)
* [urlpathsplit](#urlpathsplit)
* [urls_from_html](#urls_from_html)
* [urls_from_text](#urls_from_text)

*Utilities*

* [Upgrading suffixes and TLDs](#upgrading-suffixes-and-tlds)

*Classes*

* [HostnameTrieSet](#hostnametrieset)
  * [#.add](#hostnametrieset-add)
  * [#.match](#hostnametrieset-match)

*LRU-related functions* ([What on earth is a LRU?](#lru-explanation))

* [lru.url_to_lru](#lruurl_to_lru)
* [lru.lru_to_url](#lrulru_to_url)
* [lru.lru_stems](#lrulru_stems)
* [lru.canonicalized_lru_stems](#lrucanonicalized_lru_stems)
* [lru.normalized_lru_stems](#lrunormalized_lru_stems)
* [lru.fingerprinted_lru_stems](#lrufingerprinted_lru_stems)
* [lru.serialize_lru](#lruserialize_lru)
* [lru.unserialize_lru](#lruunserialize_lru)

*LRU-related classes*

* [LRUTrie](#lrutrie)
  * [#.set](#lrutrie-set)
  * [#.set_lru](#lrutrie-set_lru)
  * [#.match](#lrutrie-match)
  * [#.match_lru](#lrutrie-match_lru)

* [CanonicalizedLRUTrie](#canonicalizedlrutrie)
* [NormalizedLRUTrie](#normalizedlrutrie)
* [FingerprintedLRUTrie](#fingerprintedlrutrie)

*Platform-specific functions*

* [facebook](#facebook)
  * [has_facebook_comments](#has_facebook_comments)
  * [is_facebook_id](#is_facebook_id)
  * [is_facebook_full_id](#is_facebook_full_id)
  * [is_facebook_url](#is_facebook_url)
  * [is_facebook_post_url](#is_facebook_post_url)
  * [is_facebook_link](#is_facebook_link)
  * [convert_facebook_url_to_mobile](#convert_facebook_url_to_mobile)
  * [parse_facebook_url](#parse_facebook_url)
  * [extract_url_from_facebook_link](#extract_url_from_facebook_link)
* [google](#google)
  * [is_amp_url](#is_amp_url)
  * [is_google_link](#is_google_link)
  * [extract_url_from_google_link](#extract_url_from_google_link)
  * [extract_id_from_google_drive_url](#extract_id_from_google_drive_url)
  * [parse_google_drive_url](#parse_google_drive_url)
* [instagram](#instagram)
  * [is_instagram_post_shortcode](#is_instagram_post_shortcode)
  * [is_instagram_username](#is_instagram_username)
  * [is_instagram_url](#is_instagram_url)
  * [extract_username_from_instagram_url](#extract_username_from_instagram_url)
  * [parse_instagram_url](#parse_instagram_url)
* [telegram](#telegram)
  * [is_telegram_message_id](#is_telegram_message_id)
  * [is_telegram_url](#is_telegram_url)
  * [convert_telegram_url_to_public](#convert_telegram_url_to_public)
  * [extract_channel_name_from_telegram_url](#extract_channel_name_from_telegram_url)
  * [parse_telegram_url](#parse_telegram_url)
* [twitter](#twitter)
  * [is_twitter_url](#is_twitter_url)
  * [extract_screen_name_from_twitter_url](#extract_screen_name_from_twitter_url)
  * [parse_twitter_url](#parse_twitter_url)
* [youtube](#youtube)
  * [is_youtube_url](#is_youtube_url)
  * [is_youtube_channel_id](#is_youtube_channel_id)
  * [is_youtube_video_id](#is_youtube_video_id)
  * [parse_youtube_url](#parse_youtube_url)
  * [extract_video_id_from_youtube_url](#extract_video_id_from_youtube_url)
  * [normalize_youtube_url](#normalize_youtube_url)

---

### Differences between canonicalize_url, normalize_url & fingerprint_url

`ural` comes with three different url deduplication schemes, targeted to different use-cases and ordered hereafter by ascending aggressiveness:

1. [canonicalize_url](#canonicalize_url): we clean the url by performing some light preprocessing usually done by web browsers before hitting them, e.g. lowercasing the hostname, decoding punycode, ensuring we have a protocol, dropping leading and trailing whitespace etc. The clean url is guaranteed to still lead to the same place.
2. [normalize_url](#normalize_url): we apply more advanced preprocessing that will drop some parts of the url that are irrelevant to where the url leads, such as technical artifacts and SEO tricks. For instance, we will drop typical query items used by marketing campaigns, reorder the query items, infer some redirections, strip trailing slash or fragment when advisable etc. At that point, the url should be clean enough that one can perform meaningful statistical aggregation when counting them, all while ensuring with some good probability that the url still works and still leads to the same place, at least if the target server follows most common conventions.
3. [fingerprint_url](#fingerprint_url): we go a step further and we perform destructive preprocessing that cannot guarantee that the resulting url will still be valid. But the result might be even more useful for statistical aggregation, especially when counting urls from large platforms having multiple domains (e.g. `facebook.com`, `facebook.fr` etc.)

| Function         | Use-cases                            | Url validity           | Deduplication strength |
|------------------|--------------------------------------|------------------------|------------------------|
| canonicalize_url | web crawler                          | Technically the same   | +                      |
| normalize_url    | web crawler, statistical aggregation | Probably the same | ++                     |
| fingerprint_url  | statistical aggregation              | Potentially invalid    | +++                    |

*Example*

```python
from ural import canonicalize_url, normalize_url, fingerprint_url

url = 'https://www.FACEBOOK.COM:80/index.html?utc_campaign=3&id=34'

canonicalize_url(url)
>>> 'https://www.facebook.com/index.html?utc_campaign=3&id=34'
# The same url, cleaned up a little

normalize_url(url)
>>> 'facebook.com?id=34'
# Still a valid url, with implicit protocol, where all the cruft has been discarded

fingerprint_url(url, strip_suffix=True)
>>> 'facebook?id=34'
# Not a valid url anymore, but useful to match more potential
# candidates such as: http://facebook.co.uk/index.html?id=34
```

---

### canonicalize_url

Function returning a clean and safe version of the url by performing the same kind of preprocessing as web browsers.

For more details about this be sure to read [this](#differences-between-canonicalize_url-normalize_url--fingerprint_url) section of the docs.

```python
from ural import canonicalize_url

canonicalize_url('www.LEMONDE.fr')
>>> 'https://lemonde.fr'
```

*Arguments*

* **url** *string*: url to canonicalize.
* **quoted** *?bool* [`False`]: by default the function will unquote the url as much as possible all while keeping the url safe. If this kwarg is set to `True`, the function will instead quote the url as much as possible all while ensuring nothing will be double-quoted.
* **default_protocol** *?str* [`https`]: default protocol to add when the url has none.
* **strip_fragment** *?str* [`False`]: whether to strip the url's fragment.

---

### could_be_html

Function returning whether the url could return HTML.

```python
from ural import could_be_html

could_be_html('https://www.lemonde.fr')
>>> True

could_be_html('https://www.lemonde.fr/articles/page.php')
>>> True

could_be_html('https://www.lemonde.fr/data.json')
>>> False

could_be_html('https://www.lemonde.fr/img/figure.jpg')
>>> False
```

---

### could_be_rss

Function returning whether the given url could be a rss feed url.

```python
from ural import could_be_rss

could_be_rss('https://www.lemonde.fr/cyclisme/rss_full.xml')
>>> True

could_be_rss('https://www.lemonde.fr/cyclisme/')
>>> False

could_be_rss('https://www.ecorce.org/spip.php?page=backend')
>>> True

could_be_rss('https://feeds.feedburner.com/helloworld')
>>> True
```

---

### ensure_protocol

Function checking if the url has a protocol, and adding the given one if there is none.

```python
from ural import ensure_protocol

ensure_protocol('www.lemonde.fr', protocol='https')
>>> 'https://www.lemonde.fr'
```

*Arguments*

* **url** *string*: URL to format.
* **protocol** *string*: protocol to use if there is none in **url**. Is 'http' by default.

---

### fingerprint_hostname

Function returning a "fingerprinted" version of the given hostname by stripping subdomains irrelevant for statistical aggregation. Be warned that this function is even more aggressive than [normalize_hostname](#normalize_hostname) and that the resulting hostname might not be valid anymore.

For more details about this be sure to read [this](#differences-between-canonicalize_url-normalize_url--fingerprint_url) section of the docs.

```python
from ural import fingerprint_hostname

fingerprint_hostname('www.lemonde.fr')
>>> 'lemonde.fr'

fingerprint_hostname('fr-FR.facebook.com')
>>> 'facebook.com'

fingerprint_hostname('fr-FR.facebook.com', strip_suffix=True)
>>> 'facebook'
```

*Arguments*

* **hostname** *string*: target hostname.
* **strip_suffix** *?bool* [`False`]: whether to strip the hostname suffix such as `.com` or `.co.uk`. This can be useful to aggegate different domains of the same platform.

---

### fingerprint_url

Function returning a "fingerprinted" version of the given url that can be useful for statistical aggregation. Be warned that this function is even more aggressive than [normalize_url](#normalize_url) and that the resulting url might not be valid anymore.

For more details about this be sure to read [this](#differences-between-canonicalize_url-normalize_url--fingerprint_url) section of the docs.

```python
from ural import fingerprint_hostname

fingerprint_url('www.lemonde.fr/article.html')
>>> 'lemonde.fr/article.html'

fingerprint_url('fr-FR.facebook.com/article.html')
>>> 'facebook.com/article.html'

fingerprint_url('fr-FR.facebook.com/article.html', strip_suffix=True)
>>> 'facebook/article.html'
```

*Arguments*

* **url** *string*: target url.
* **strip_suffix** *?bool* [`False`]: whether to strip the hostname suffix such as `.com` or `.co.uk`. This can be useful to aggegate different domains of the same platform.
* **platform_aware** *?bool* [`False`]: whether to take some well-known platforms supported by `ural` such as facebook, youtube etc. into account when normalizing the url.

---

### force_protocol

Function force-replacing the protocol of the given url.

```python
from ural import force_protocol

force_protocol('https://www2.lemonde.fr', protocol='ftp')
>>> 'ftp://www2.lemonde.fr'
```

*Arguments*

* **url** *string*: URL to format.
* **protocol** *string*: protocol wanted in the output url. Is `'http'` by default.

---

### format_url

Function formatting a url given some typical parameters.

```python
from ural import format_url

format_url(
  'https://lemonde.fr',
  path='/article.html',
  args={'id': '48675'},
  fragment='title-2'
)
>>> 'https://lemonde.fr/article.html?id=48675#title-2'

# Path can be given as an iterable
format_url('https://lemonde.fr', path=['articles', 'one.html'])
>>> 'https://lemonde.fr/articles/one.html'

# Extension
format_url('https://lemonde.fr', path=['article'], ext='html')
>>> 'https://lemonde.fr/articles/article.html'

# Query args are formatted/quoted and/or skipped if None/False
format_url(
  "http://lemonde.fr",
  path=["business", "articles"],
  args={
    "hello": "world",
    "number": 14,
    "boolean": True,
    "skipped": None,
    "also-skipped": False,
    "quoted": "test=ok",
  },
  fragment="#test",
)
>>> 'http://lemonde.fr/business/articles?boolean&hello=world&number=14&quoted=test%3Dok#test'

# Query args can also be passed as a list of (key, value) pairs
format_url("http://lemonde.fr", args=[("id", "one"), ("name", "lucy")])
>>> "http://lemonde.fr?id=one&name=lucy

# Custom argument value formatting
def format_arg_value(key, value):
  if key == 'ids':
    return ','.join(value)

  return key

format_url(
  'https://lemonde.fr',
  args={'ids': [1, 2]},
  format_arg_value=format_arg_value
)
>>> 'https://lemonde.fr?ids=1%2C2'

# Formatter class
from ural import URLFormatter

formatter = URLFormatter('https://lemonde.fr', args={'id': 'one'})

formatter(path='/article.html')
>>> 'https://lemonde.fr/article.html?id=one'

# same as:
formatter.format(path='/article.html')
>>> 'https://lemonde.fr/article.html?id=one'

# Query arguments are merged
formatter(path='/article.html', args={"user_id": "two"})
>>> 'https://lemonde.fr/article.html?id=one&user_id=two'

# Easy subclassing
class MyCustomFormatter(URLFormatter):
  BASE_URL = 'https://lemonde.fr/api'

  def format_api_call(self, token):
    return self.format(args={'token': token})

formatter = MyCustomFormatter()

formatter.format_api_call('2764753')
>>> 'https://lemonde.fr/api?token=2764753'
```

*Arguments*

* **base_url** *str*: Base url.
* **path** *?str|list*: the url's path.
* **args** *?dict|list*: query arguments as a dictionary or a list of (key, value) pairs.
* **format_arg_value** *?callable*: function taking a query argument key and value and returning the formatted value.
* **fragment** *?str*: the url's fragment.
* **ext** *?str*: path extension such as `.html`.

---

### get_domain_name

Function returning an url's domain name. This function is of course tld-aware and will return `None` if no valid domain name can be found.

```python
from ural import get_domain_name

get_domain_name('https://facebook.com/path')
>>> 'facebook.com'
```

---

### get_hostname

Function returning the given url's full hostname. It can work on scheme-less urls.

```python
from ural import get_hostname

get_hostname('http://www.facebook.com/path')
>>> 'www.facebook.com'
```

---

### get_fingerprinted_hostname

Function returning the "fingerprinted" hostname of the given url by stripping subdomains irrelevant for statistical aggregation. Be warned that this function is even more aggressive than [get_normalized_hostname](#get_normalized_hostname) and that the resulting hostname might not be valid anymore.

For more details about this be sure to read [this](#differences-between-canonicalize_url-normalize_url--fingerprint_url) section of the docs.

```python
from ural import get_normalized_hostname

get_normalized_hostname('https://www.lemonde.fr/article.html')
>>> 'lemonde.fr'

get_normalized_hostname('https://fr-FR.facebook.com/article.html')
>>> 'facebook.com'

get_normalized_hostname('https://fr-FR.facebook.com/article.html', strip_suffix=True)
>>> 'facebook'
```

*Arguments*

* **url** *string*: target url.
* **strip_suffix** *?bool* [`False`]: whether to strip the hostname suffix such as `.com` or `.co.uk`. This can be useful to aggegate different domains of the same platform.

---

### get_normalized_hostname

Function returning the given url's normalized hostname, i.e. without usually irrelevant subdomains etc. Works a lot like [normalize_url](#normalize_url).

For more details about this be sure to read [this](#differences-between-canonicalize_url-normalize_url--fingerprint_url) section of the docs.

```python
from ural import get_normalized_hostname

get_normalized_hostname('http://www.facebook.com/path')
>>> 'facebook.com'

get_normalized_hostname('http://fr-FR.facebook.com/path')
>>> 'facebook.com'
```

*Arguments*

* **url** *str*: Target url.
* **infer_redirection** *bool* [`True`]: whether to attempt resolving common redirects by leveraging well-known GET parameters.
* **normalize_amp** *?bool* [`True`]: Whether to attempt to normalize Google AMP subdomains.

---

### has_special_host

Function returning whether the given url looks like it has a special host.

```python
from ural import has_special_host

has_special_host('http://104.19.154.83')
>>> True

has_special_host('http://youtube.com')
>>> False
```

---

### has_valid_suffix

Function returning whether the given url has a valid suffix as per [Mozzila's Public Suffix List](https://wiki.mozilla.org/Public_Suffix_List).

```python
from ural import has_valid_suffix

has_valid_suffix('http://lemonde.fr')
>>> True

has_valid_suffix('http://lemonde.doesnotexist')
>>> False

# Also works with hostnames
has_valid_suffix('lemonde.fr')
>>> True
```

---

### has_valid_tld

Function returning whether the given url has a valid Top Level Domain (TLD) as per [IANA's list](https://data.iana.org/TLD/tlds-alpha-by-domain.txt).

```python
from ural import has_valid_tld

has_valid_tld('http://lemonde.fr')
>>> True

has_valid_tld('http://lemonde.doesnotexist')
>>> False

# Also works with hostnames
has_valid_tld('lemonde.fr')
>>> True
```

---

### infer_redirection

Function attempting to find obvious clues in the given url that it is in fact a redirection and resolving the redirection automatically without firing any HTTP request. If nothing is found, the given url will be returned as-is.

The function is by default recursive and will attempt to infer redirections until none is found, but you can disable this behavior if you need to.

```python
from ural import infer_redirection

infer_redirection('https://www.google.com/url?sa=t&source=web&rct=j&url=https%3A%2F%2Fm.youtube.com%2Fwatch%3Fv%3D4iJBsjHMviQ&ved=2ahUKEwiBm-TO3OvkAhUnA2MBHQRPAR4QwqsBMAB6BAgDEAQ&usg=AOvVaw0i7y2_fEy3nwwdIZyo_qug')
>>> 'https://m.youtube.com/watch?v=4iJBsjHMviQ'

infer_redirection('https://test.com?url=http%3A%2F%2Flemonde.fr%3Fnext%3Dhttp%253A%252F%252Ftarget.fr')
>>> 'http://target.fr'

infer_redirection(
  'https://test.com?url=http%3A%2F%2Flemonde.fr%3Fnext%3Dhttp%253A%252F%252Ftarget.fr',
  recursive=False
)
>>> 'http://lemonde.fr?next=http%3A%2F%2Ftarget.fr'
```

---

### is_homepage

Function returning whether the given url is *probably* a website's homepage, based on its path.

```python
from ural import is_homepage

is_homepage('http://lemonde.fr')
>>> True

is_homepage('http://lemonde.fr/index.html')
>>> True

is_homepage('http://lemonde.fr/business/article5.html')
>>> False
```

---

### is_shortened_url

Function returning whether the given url is *probably* a shortened url. It works by matching the given url domain against most prominent shortener domains. So the result could be a false negative.

```python
from ural import is_shortened_url

is_shortened_url('http://lemonde.fr')
>>> False

is_shortened_url('http://bit.ly/1sNZMwL')
>>> True
```

---

### is_special_host

Function returning whether the given hostname looks like a special host.

```python
from ural import is_special_host

is_special_host('104.19.154.83')
>>> True

is_special_host('youtube.com')
>>> False
```

---

### is_typo_url

Function returning whether the given string is *probably* a typo error. This function doesn't test if the given string is a valid url. It works by matching the given url tld against most prominent typo-like tlds or by matching the given string against most prominent inclusive language terminations. So the result could be a false negative.

```python
from ural import is_typo_url

is_typo_url('http://dirigeants.es')
>>> True

is_typo_url('https://www.instagram.com')
>>> False
```

---

### is_url

Function returning whether the given string is a valid url.

```python
from ural import is_url

is_url('https://www2.lemonde.fr')
>>> True

is_url('lemonde.fr/economie/article.php', require_protocol=False)
>>> True

is_url('lemonde.falsetld/whatever.html', tld_aware=True)
>>> False
```

*Arguments*

* **string** *string*: string to test.
* **require_protocol** *bool* [`True`]: whether the argument has to have a protocol to be considered a url.
* **tld_aware** *bool* [`False`]: whether to check if the url's tld actually exists or not.
* **allow_spaces_in_path** *bool* [`False`]: whether the allow spaces in URL paths.
* **only_http_https** *bool* [`True`]: whether to only allow the `http` and `https` protocols.

---

### is_valid_tld

Function returning whether the given Top Level Domain (TLD) is valid as per [IANA's list](https://data.iana.org/TLD/tlds-alpha-by-domain.txt).

```python
from ural import is_valid_tld

is_valid_tld('.fr')
>>> True

is_valid_tld('com')
>>> True

is_valid_tld('.doesnotexist')
>>> False
```

---

### links_from_html

Function returning an iterator over the valid outgoing links present in given HTML text.

This is a variant of [urls_from_html](#urls_from_html) suited to web crawlers. It can deduplicate the urls, canonicalize them, join them with a base url and filter out things that should not be followed such as `mailto:` or `javascript:` href links etc. It will also skip any url equivalent to the given base url.

Note this function is able to work both on string and bytes seamlessly.

```python
from ural import links_from_html

html = b"""
<p>
  Hey! Check this site:
  <a href="https://medialab.sciencespo.fr/">médialab</a>
  And also this page:
  <a href="article.html">article</a>
  Or click on this:
  <a href="javascript:alert('hello');">link</a>
</p>
"""

for link in links_from_html('http://lemonde.fr', html):
    print(link)
>>> 'https://medialab.sciencespo.fr/'
>>> 'http://lemonde.fr/article.html'
```

*Arguments*

* **base_url** *string*: the HTML's url.
* **string** *string|bytes*: html string or bytes.
* **encoding** *?string* [`utf-8`]: if given binary, this encoding will be used to decode the found urls.
* **canonicalize** *?bool* [`False`]: whether to canonicalize the urls using [canonicalize_url](#canonicalize_url).
* **strip_fragment** *?bool* [`False`]: whether to strip the url fragments when using `canonicalize`.
* **unique** *?bool* [`False`]: whether to deduplicate the urls.

---

### normalize_hostname

Function normalizing the given hostname, i.e. without usually irrelevant subdomains etc. Works a lot like [normalize_url](#normalize_url).

For more details about this be sure to read [this](#differences-between-canonicalize_url-normalize_url--fingerprint_url) section of the docs.

```python
from ural import normalize_hostname

normalize_hostname('www.facebook.com')
>>> 'facebook.com'

normalize_hostname('fr-FR.facebook.com')
>>> 'facebook.com'
```

---

### normalize_url

Function normalizing the given url by stripping it of usually non-discriminant parts such as irrelevant query items or sub-domains etc.

This is a very useful utility when attempting to match similar urls written slightly differently when shared on social media etc.

For more details about this be sure to read [this](#differences-between-canonicalize_url-normalize_url--fingerprint_url) section of the docs.

```python
from ural import normalize_url

normalize_url('https://www2.lemonde.fr/index.php?utm_source=google')
>>> 'lemonde.fr'
```

*Arguments*

* **url** *string*: URL to normalize.
* **infer_redirection** *?bool* [`True`]: whether to attempt resolving common redirects by leveraging well-known GET parameters.
* **fix_common_mistakes** *?bool* [`True`]: whether to attempt to fix common URL mistakes.
* **normalize_amp** *?bool* [`True`]: whether to attempt to normalize Google AMP urls.
* **sort_query** *?bool* [`True`]: whether to sort query items.
* **strip_authentication** *?bool* [`True`]: whether to strip authentication.
* **strip_fragment** *?bool|str* [`'except-routing'`]: whether to strip the url's fragment. If set to `except-routing`, will only strip the fragment if the fragment is not deemed to be js routing (i.e. if it contains a `/`).
* **strip_index** *?bool* [`True`]: whether to strip trailing index.
* **strip_irrelevant_subdomains** *?bool* [`False`]: whether to strip irrelevant subdomains such as `www` etc.
* **strip_protocol** *?bool* [`True`]: whether to strip the url's protocol.
* **strip_trailing_slash** *?bool* [`True`]: whether to strip trailing slash.
* **quoted** *?bool* [`False`]: by default the function will unquote the url as much as possible all while keeping the url safe. If this kwarg is set to `True`, the function will instead quote the url as much as possible all while ensuring nothing will be double-quoted.
* **platform_aware** *?bool* [`False`]: whether to take some well-known platforms supported by `ural` such as facebook, youtube etc. into account when normalizing the url.

---

### should_follow_href

Function returning whether the given href should be followed (usually from a crawler's context). This means it will filter out anchors, and url having a scheme which is not http/https.

```python
from ural import should_follow_href

should_follow_href('#top')
>>> False

should_follow_href('http://lemonde.fr')
>>> True

should_follow_href('/article.html')
>>> True
```

---

### should_resolve

Function returning whether the given function looks like something you would want to resolve because the url will *probably* lead to some redirection.

It is quite similar to [is_shortened_url](#is_shortened_url) but covers more ground since it also deal with url patterns which are not shortened per se.

```python
from ural import should_resolve

should_resolve('http://lemonde.fr')
>>> False

should_resolve('http://bit.ly/1sNZMwL')
>>> True

should_resolve('https://doi.org/10.4000/vertigo.26405')
>>> True
```

---

### split_suffix

Function splitting a hostname or a url's hostname into the domain part and the suffix part (while respecting [Mozzila's Public Suffix List](https://wiki.mozilla.org/Public_Suffix_List)).

```python
from ural import split_suffix

split_suffix('http://www.bbc.co.uk/article.html')
>>> ('www.bbc', 'co.uk')

split_suffix('http://www.bbc.idontexist')
>>> None

split_suffix('lemonde.fr')
>>> ('lemonde', 'fr')
```

---

### strip_protocol

Function removing the protocol from the url.

```python
from ural import strip_protocol

strip_protocol('https://www2.lemonde.fr/index.php')
>>> 'www2.lemonde.fr/index.php'
```

*Arguments*

* **url** *string*: URL to format.

---

### urlpathsplit

Function taking a url and returning its path, tokenized as a list.

```python
from ural import urlpathsplit

urlpathsplit('http://lemonde.fr/section/article.html')
>>> ['section', 'article.html']

urlpathsplit('http://lemonde.fr/')
>>> []

# If you want to split a path directly
from ural import pathsplit

pathsplit('/section/articles/')
>>> ['section', 'articles']
```

---

### urls_from_html

Function returning an iterator over the urls present in the links of given HTML text.

Note this function is able to work both on string and bytes seamlessly.

```python
from ural import urls_from_html

html = """<p>Hey! Check this site: <a href="https://medialab.sciencespo.fr/">médialab</a></p>"""

for url in urls_from_html(html):
    print(url)
>>> 'https://medialab.sciencespo.fr/'
```

*Arguments*

* **string** *string|bytes*: html string or bytes.
* **encoding** *?string* [`utf-8`]: if given binary, this encoding will be used to decode the found urls.
* **errors** *?string* [`strict`]: policy on decode errors.

---

### urls_from_text

Function returning an iterator over the urls present in the string argument. Extracts only urls having a protocol.

Note that this function is somewhat markdown-aware, and punctuation-aware.

```python
from ural import urls_from_text

text = "Hey! Check this site: https://medialab.sciencespo.fr/, it looks really cool. They're developing many tools on https://github.com/"

for url in urls_from_text(text):
    print(url)

>>> 'https://medialab.sciencespo.fr/'
>>> 'https://github.com/'
```

*Arguments*

* **string** *string*: source string.

---

### Upgrading suffixes and TLDs

If you want to upgrade the package's data wrt Mozilla suffixes and IANA TLDs, you can do so either by running the following command:

```bash
python -m ural upgrade
```

or directly in your python code:

```python
from ural.tld import upgrade

upgrade()

# Or if you want to patch runtime only this time, or regularly
# (for long running programs or to avoid rights issues etc.):
upgrade(transient=True)
```

---

### HostnameTrieSet

Class implementing a hierarchic set of hostnames so you can efficiently query whether urls match hostnames in the set.

```python
from ural import HostnameTrieSet

trie = HostnameTrieSet()

trie.add('lemonde.fr')
trie.add('business.lefigaro.fr')

trie.match('https://liberation.fr/article1.html')
>>> False

trie.match('https://lemonde.fr/article1.html')
>>> True

trie.match('https://www.lemonde.fr/article1.html')
>>> True

trie.match('https://lefigaro.fr/article1.html')
>>> False

trie.match('https://business.lefigaro.fr/article1.html')
>>> True
```

<h4 id="hostnametrieset-add">#.add</h4>

Method add a single hostname to the set.

```python
from ural import HostnameTrieSet

trie = HostnameTrieSet()
trie.add('lemonde.fr')
```

*Arguments*

* **hostname** *string*: hostname to add to the set.

<h4 id="hostnametrieset-match">#.match</h4>

Method returning whether the given url matches any of the set's hostnames.

```python
from ural import HostnameTrieSet

trie = HostnameTrieSet()
trie.add('lemonde.fr')

trie.match('https://liberation.fr/article1.html')
>>> False

trie.match('https://lemonde.fr/article1.html')
>>> True
```

*Arguments*

* **url** *string|urllib.parse.SplitResult*: url to match.

---

### lru.url_to_lru

Function converting the given url to a serialized lru.

```python
from ural.lru import url_to_lru

url_to_lru('http://www.lemonde.fr:8000/article/1234/index.html?field=value#2')
>>> 's:http|t:8000|h:fr|h:lemonde|h:www|p:article|p:1234|p:index.html|q:field=value|f:2|'
```

*Arguments*

* **url** *string*: url to convert.
* **suffix_aware** *?bool*: whether to be mindful of suffixes when converting (e.g. considering "co.uk" as a single token).

---

### lru.lru_to_url

Function converting the given serialized lru or lru stems to a proper url.

```python
from ural.lru import lru_to_url

lru_to_url('s:http|t:8000|h:fr|h:lemonde|h:www|p:article|p:1234|p:index.html|')
>>> 'http://www.lemonde.fr:8000/article/1234/index.html'

lru_to_url(['s:http', 'h:fr', 'h:lemonde', 'h:www', 'p:article', 'p:1234', 'p:index.html'])
>>> 'http://www.lemonde.fr:8000/article/1234/index.html'
```

---

### lru.lru_stems

Function returning url parts in hierarchical order.

```python
from ural.lru import lru_stems

lru_stems('http://www.lemonde.fr:8000/article/1234/index.html?field=value#2')
>>> ['s:http', 't:8000', 'h:fr', 'h:lemonde', 'h:www', 'p:article', 'p:1234', 'p:index.html', 'q:field=value', 'f:2']
```

*Arguments*

* **url** *string*: URL to parse.
* **suffix_aware** *?bool*: whether to be mindful of suffixes when converting (e.g. considering "co.uk" as a single token).

---

### lru.canonicalized_lru_stems

Function canonicalizing the url and returning its parts in hierarchical order.

```python
from ural.lru import canonicalized_lru_stems

canonicalized_lru_stems('http://www.lemonde.fr/article/1234/index.html?field=value#2')
>>> ['s:http', 'h:fr', 'h:lemonde', 'p:article', 'p:1234', 'q:field=value', 'f:2']
```

*Arguments*

This function accepts the same arguments as [canonicalize_url](#canonicalize_url).

---

### lru.normalized_lru_stems

Function normalizing the url and returning its parts in hierarchical order.

```python
from ural.lru import normalized_lru_stems

normalized_lru_stems('http://www.lemonde.fr/article/1234/index.html?field=value#2')
>>> ['h:fr', 'h:lemonde', 'p:article', 'p:1234', 'q:field=value']
```

*Arguments*

This function accepts the same arguments as [normalize_url](#normalize_url).

---

### lru.fingerprinted_lru_stems

Function fingerprinting the url and returning its parts in hierarchical order.

```python
from ural.lru import fingerprinted_lru_stems

fingerprinted_lru_stems('http://www.lemonde.fr/article/1234/index.html?field=value#2', strip_suffix=True)
>>> ['h:lemonde', 'p:article', 'p:1234', 'q:field=value']
```

*Arguments*

This function accepts the same arguments as [fingerprint_url](#fingerprint_url).

---

### lru.serialize_lru

Function serializing lru stems to a string.

```python
from ural.lru import serialize_lru

serialize_lru(['s:https', 'h:fr', 'h:lemonde'])
>>> 's:https|h:fr|h:lemonde|'
```

---

### lru.unserialize_lru

Function unserializing stringified lru to a list of stems.

```python
from ural.lru import unserialize_lru

unserialize_lru('s:https|h:fr|h:lemonde|')
>>> ['s:https', 'h:fr', 'h:lemonde']
```

---

### LRUTrie

Class implementing a prefix tree (Trie) storing URLs hierarchically by storing them as LRUs along with some arbitrary metadata. It is very useful when needing to match URLs by longest common prefix.

Note that this class directly inherits from the `phylactery` library's [`TrieDict`](https://github.com/Yomguithereal/phylactery/blob/master/phylactery/triedict.py) so you can also use any of its methods.

```python
from ural.lru import LRUTrie

trie = LRUTrie()

# To respect suffixes
trie = LRUTrie(suffix_aware=True)
```

<h4 id="lrutrie-set">#.set</h4>

Method storing a URL in a LRUTrie along with its metadata.

```python
from ural.lru import LRUTrie

trie = LRUTrie()
trie.set('http://www.lemonde.fr', {'type': 'general press'})

trie.match('http://www.lemonde.fr')
>>> {'type': 'general press'}
```

*Arguments*

* **url** *string*: url to store in the LRUTrie.
* **metadata** *any*: metadata of the url.

<h4 id="lrutrie-set_lru">#.set_lru</h4>

Method storing a URL already represented as a LRU or LRU stems along with its metadata.

```python
from ural.lru import LRUTrie

trie = LRUTrie()

# Using stems
trie.set_lru(['s:http', 'h:fr', 'h:lemonde', 'h:www'], {'type': 'general press'})

# Using serialized lru
trie.set_lru('s:http|h:fr|h:lemonde|h:www|', {'type': 'general_press'})
```

*Arguments*

* **lru** *string|list*: lru to store in the Trie.
* **metadata** *any*: metadata to attach to the lru.

<h4 id="lrutrie-match">#.match</h4>

Method returning the metadata attached to the longest prefix match of your query URL. Will return `None` if no common prefix can be found.

```python
from ural.lru import LRUTrie

trie = LRUTrie()
trie.set('http://www.lemonde.fr', {'media': 'lemonde'})

trie.match('http://www.lemonde.fr')
>>> {'media': 'lemonde'}
trie.match('http://www.lemonde.fr/politique')
>>> {'media': 'lemonde'}

trie.match('http://www.lefigaro.fr')
>>> None
```

*Arguments*

* **url** *string*: url to match in the LRUTrie.

<h4 id="lrutrie-match_lru">#.match_lru</h4>

Method returning the metadata attached to the longest prefix match of your query LRU. Will return `None` if no common prefix can be found.

```python
from ural.lru import LRUTrie

trie = LRUTrie()
trie.set(['s:http', 'h:fr', 'h:lemonde', 'h:www'], {'media': 'lemonde'})

trie.match(['s:http', 'h:fr', 'h:lemonde', 'h:www'])
>>> {'media': 'lemonde'}
trie.match('s:http|h:fr|h:lemonde|h:www|p:politique|')
>>> {'media': 'lemonde'}

trie.match(['s:http', 'h:fr', 'h:lefigaro', 'h:www'])
>>> None
```

*Arguments*

* **lru** *string|list*: lru to match in the LRUTrie.

---

### CanonicalizedLRUTrie

The `CanonicalizedLRUTrie` is nearly identical to the standard [`LRUTrie`](#LRUTrie) except that it canonicalizes given urls before attempting any operation using the [`canonicalize_url`](#canonicalize_url) function.

Its constructor therefore takes the same arguments as the beforementioned function.

```python
from ural.lru import CanonicalizedLRUTrie

trie = CanonicalizedLRUTrie(strip_fragment=False)
```

---

### NormalizedLRUTrie

The `NormalizedLRUTrie` is nearly identical to the standard [`LRUTrie`](#LRUTrie) except that it normalizes given urls before attempting any operation using the [`normalize_url`](#normalize_url) function.

Its constructor therefore takes the same arguments as the beforementioned function.

```python
from ural.lru import NormalizedLRUTrie

trie = NormalizedLRUTrie(normalize_amp=False)
```

---

### FingerprintedLRUTrie

The `FingerprintedLRUTrie` is nearly identical to the standard [`LRUTrie`](#LRUTrie) except that it fingerprints given urls before attempting any operation using the [`fingerprint_url`](#fingerprint_url) function.

Its constructor therefore takes the same arguments as the beforementioned function.

```python
from ural.lru import FingerprintedLRUTrie

trie = FingerprintedLRUTrie(strip_suffix=False)
```

---

### Facebook

#### has_facebook_comments

Function returning whether the given url is pointing to a Facebook resource potentially having comments (such as a post, photo or video for instance).

```python
from ural.facebook import has_facebook_comments

has_facebook_comments('https://www.facebook.com/permalink.php?story_fbid=1354978971282622&id=598338556946671')
>>> True

has_facebook_comments('https://www.facebook.com/108824017345866/videos/311658803718223')
>>> True

has_facebook_comments('https://www.facebook.com/astucerie/')
>>> False

has_facebook_comments('https://www.lemonde.fr')
>>> False

has_facebook_comments('/permalink.php?story_fbid=1354978971282622&id=598338556946671', allow_relative_urls=True)
>>> True
```

#### is_facebook_id

Function returning whether the given string is a valid Facebook id or not.

```python
from ural.facebook import is_facebook_id

is_facebook_id('974583586343')
>>> True

is_facebook_id('whatever')
>>> False
```

#### is_facebook_full_id

Function returning whether the given string is a valid Facebook full post id or not.

```python
from ural.facebook import is_facebook_full_id

is_facebook_full_id('974583586343_9749757953')
>>> True

is_facebook_full_id('974583586343')
>>> False

is_facebook_full_id('whatever')
>>> False
```

#### is_facebook_url

Function returning whether given url is from Facebook or not.

```python
from ural.facebook import is_facebook_url

is_facebook_url('http://www.facebook.com/post/974583586343')
>>> True

is_facebook_url('https://fb.me/846748464')
>>> True

is_facebook_url('https://www.lemonde.fr')
>>> False
```

#### is_facebook_post_url

Function returning whether the given url is a Facebook post or not.

```python
from ural.facebook import is_facebook_post_url

is_facebook_post_url('http://www.facebook.com/post/974583586343')
>>> True

is_facebook_post_url('http://www.facebook.com')
>>> False

is_facebook_post_url('https://www.lemonde.fr')
>>> False
```

#### is_facebook_link

Function returning whether the given url is a Facebook redirection link.

```python
from ural.facebook import is_facebook_link

is_facebook_link('https://l.facebook.com/l.php?u=http%3A%2F%2Fwww.chaos-controle.com%2Farchives%2F2013%2F10%2F14%2F28176300.html&amp;h=AT0iUqJpUTMzHAH8HAXwZ11p8P3Z-SrY90wIXZhcjMnxBTHMiau8Fv1hvz00ZezRegqmF86SczyUXx3Gzdt_MdFH-I4CwHIXKKU9L6w522xwOqkOvLAylxojGEwrp341uC-GlVyGE2N7XwTPK9cpP0mQ8PIrWh8Qj2gHIIR08Js0mUr7G8Qe9fx66uYcfnNfTTF1xi0Us8gTo4fOZxAgidGWXsdgtU_OdvQqyEm97oHzKbWfXjkhsrzbtb8ZNMDwCP5099IMcKRD8Hi5H7W3vwh9hd_JlRgm5Z074epD_mGAeoEATE_QUVNTxO0SHO4XNn2Z7LgBamvevu1ENBcuyuSOYA0BsY2cx8mPWJ9t44tQcnmyQhBlYm_YmszDaQx9IfVP26PRqhsTLz-kZzv0DGMiJFU78LVWVPc9QSw2f9mA5JYWr29w12xJJ5XGQ6DhJxDMWRnLdG8Tnd7gZKCaRdqDER1jkO72u75-o4YuV3CLh4j-_4u0fnHSzHdVD8mxr9pNEgu8rvJF1E2H3-XbzA6F2wMQtFCejH8MBakzYtTGNvHSexSiKphE04Ci1Z23nBjCZFsgNXwL3wbIXWfHjh2LCKyihQauYsnvxp6fyioStJSGgyA9GGEswizHa20lucQF0S0F8H9-')
>>> True

is_facebook_link('https://lemonde.fr')
>>> False
```

#### convert_facebook_url_to_mobile

Function returning the mobile version of the given Facebook url. Will raise an exception if a non-Facebook url is given.

```python
from ural.facebook import convert_facebook_url_to_mobile

convert_facebook_url_to_mobile('http://www.facebook.com/post/974583586343')
>>> 'http://m.facebook.com/post/974583586343'
```

#### parse_facebook_url

Function parsing the given Facebook url.

```python
from ural.facebook import parse_facebook_url

# Importing related classes if you need to perform tests
from ural.facebook import (
  FacebookHandle,
  FacebookUser,
  FacebookGroup,
  FacebookPost,
  FacebookPhoto,
  FacebookVideo
)

parse_facebook_url('https://www.facebook.com/people/Sophia-Aman/102016783928989')
>>> FacebookUser(id='102016783928989')

parse_facebook_url('https://www.facebook.com/groups/159674260452951')
>>> FacebookGroup(id='159674260452951')

parse_facebook_url('https://www.facebook.com/groups/159674260852951/permalink/1786992671454427/')
>>> FacebookPost(id='1786992671454427', group_id='159674260852951')

parse_facebook_url('https://www.facebook.com/108824017345866/videos/311658803718223')
>>> FacebookVideo(id='311658803718223', parent_id='108824017345866')

parse_facebook_url('https://www.facebook.com/photo.php?fbid=10222721681573727')
>>> FacebookPhoto(id='10222721681573727')

parse_facebook_url('/annelaure.rivolu?rc=p&__tn__=R', allow_relative_urls=True)
>>> FacebookHandle(handle='annelaure.rivolu')

parse_facebook_url('https://lemonde.fr')
>>> None
```

#### extract_url_from_facebook_link

Function extracting target url from a Facebook redirection link.

```python
from ural.facebook import extract_url_from_facebook_link

extract_url_from_facebook_link('https://l.facebook.com/l.php?u=http%3A%2F%2Fwww.chaos-controle.com%2Farchives%2F2013%2F10%2F14%2F28176300.html&amp;h=AT0iUqJpUTMzHAH8HAXwZ11p8P3Z-SrY90wIXZhcjMnxBTHMiau8Fv1hvz00ZezRegqmF86SczyUXx3Gzdt_MdFH-I4CwHIXKKU9L6w522xwOqkOvLAylxojGEwrp341uC-GlVyGE2N7XwTPK9cpP0mQ8PIrWh8Qj2gHIIR08Js0mUr7G8Qe9fx66uYcfnNfTTF1xi0Us8gTo4fOZxAgidGWXsdgtU_OdvQqyEm97oHzKbWfXjkhsrzbtb8ZNMDwCP5099IMcKRD8Hi5H7W3vwh9hd_JlRgm5Z074epD_mGAeoEATE_QUVNTxO0SHO4XNn2Z7LgBamvevu1ENBcuyuSOYA0BsY2cx8mPWJ9t44tQcnmyQhBlYm_YmszDaQx9IfVP26PRqhsTLz-kZzv0DGMiJFU78LVWVPc9QSw2f9mA5JYWr29w12xJJ5XGQ6DhJxDMWRnLdG8Tnd7gZKCaRdqDER1jkO72u75-o4YuV3CLh4j-_4u0fnHSzHdVD8mxr9pNEgu8rvJF1E2H3-XbzA6F2wMQtFCejH8MBakzYtTGNvHSexSiKphE04Ci1Z23nBjCZFsgNXwL3wbIXWfHjh2LCKyihQauYsnvxp6fyioStJSGgyA9GGEswizHa20lucQF0S0F8H9-')
>>> 'http://www.chaos-controle.com/archives/2013/10/14/28176300.html'

extract_url_from_facebook_link('http://lemonde.fr')
>>> None
```

---

### Google

#### is_amp_url

Returns whether the given url is probably a Google AMP url.

```python
from ural.google import is_amp_url

is_amp_url('http://www.europe1.fr/sante/les-onze-vaccins.amp')
>>> True

is_amp_url('https://www.lemonde.fr')
>>> False
```

#### is_google_link

Returns whether the given url is a Google search link.

```python
from ural.google import is_google_link

is_google_link('https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=2ahUKEwjp8Lih_LnmAhWQlxQKHVTmCJYQFjADegQIARAB&url=http%3A%2F%2Fwww.mon-ip.com%2F&usg=AOvVaw0sfeZJyVtUS2smoyMlJmes')
>>> True

is_google_link('https://www.lemonde.fr')
>>> False
```

#### extract_url_from_google_link

Extracts the url from the given Google search link. This is useful to "resolve" the links scraped from Google's search results. Returns `None` if given url is not valid nor relevant.

```python
from ural.google import extract_url_from_google_link

extract_url_from_google_link('https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=2ahUKEwicu4K-rZzmAhWOEBQKHRNWA08QFjAAegQIARAB&url=https%3A%2F%2Fwww.facebook.com%2Fieff.ogbeide&usg=AOvVaw0vrBVCiIHUr5pncjeLpPUp')

>>> 'https://www.facebook.com/ieff.ogbeide'

extract_url_from_google_link('https://www.lemonde.fr')
>>> None
```

#### extract_id_from_google_drive_url

Extracts a file id from the given Google drive url. Returns `None` if given url is not valid nor relevant.

```python
from ural.google import extract_id_from_google_drive_url

extract_id_from_google_drive_url('https://docs.google.com/spreadsheets/d/1Q9sJtAb1BZhUMjxCLMrVASx3AoNDp5iV3VkbPjlg/edit#gid=0')
>>> '1Q9sJtAb1BZhUMjxCLMrVASx3AoNDp5iV3VkbPjlg'

extract_id_from_google_drive_url('https://www.lemonde.fr')
>>> None
```

#### parse_google_drive_url

Parse the given Google drive url. Returns `None` if given is not valid nor relevant.

```python
from ural.google import (
  parse_google_drive_url,
  GoogleDriveFile,
  GoogleDrivePublicLink
)

parse_google_drive_url('https://docs.google.com/spreadsheets/d/1Q9sJtAb1BZhUMjxCLMrVASx3AoNDp5iV3VkbPjlg/edit#gid=0')
>>> GoogleDriveFile('spreadsheets', '1Q9sJtAb1BZhUMjxCLMrVASx3AoNDp5iV3VkbPjlg')

parse_google_drive_url('https://www.lemonde.fr')
>>> None
```

---

### Instagram

#### is_instagram_post_shortcode

Function returning whether the given string is a valid Instagram post shortcode or not.

```python
from ural.instagram import is_instagram_post_shortcode

is_instagram_post_shortcode('974583By-5_86343')
>>> True

is_instagram_post_shortcode('whatever!!')
>>> False
```

#### is_instagram_username

Function returning whether the given string is a valid Instagram username or not.

```python
from ural.instagram import is_instagram_username

is_instagram_username('97458.3By-5_86343')
>>> True

is_instagram_username('whatever!!')
>>> False
```

#### is_instagram_url

Returns whether the given url is from Instagram.

```python
from ural.instagram import is_instagram_url

is_instagram_url('https://lemonde.fr')
>>> False

is_instagram_url('https://www.instagram.com/guillaumelatorre')
>>> True
```

#### extract_username_from_instagram_url

Return a username from the given Instagram url or `None` if we could not find one.

```python
from ural.instagram import extract_username_from_instagram_url

extract_username_from_instagram_url('https://www.instagram.com/martin_dupont/p/BxKRx5CHn5i/')
>>> 'martin_dupont'

extract_username_from_instagram_url('https://lemonde.fr')
>>> None

```

#### parse_instagram_url

Returns parsed information about the given Instagram url: either about the post, the user or the reel. If the url is an invalid Instagram url or if not an Instagram url, the function returns `None`.

```python
from ural.instagram import (
  parse_instagram_url,

  # You can also import the named tuples if you need them
  InstagramPost,
  InstagramUser,
  InstagramReel
)

parse_instagram_url('https://www.instagram.com/martin_dupont/p/BxKRx5CHn5i/')
>>> InstagramPost(id='BxKRx5CHn5i', name='martin_dupont')

parse_instagram_url('https://lemonde.fr')
>>> None

parse_instagram_url('https://www.instagram.com/p/BxKRx5-Hn5i/')
>>> InstagramPost(id='BxKRx5-Hn5i', name=None)

parse_instagram_url('https://www.instagram.com/martin_dupont')
>>> InstagramUser(name='martin_dupont')

parse_instagram_url('https://www.instagram.com/reels/BxKRx5-Hn5i')
>>> InstagramReel(id='BxKRx5-Hn5i')
```

*Arguments*

* **url** *str*: Instagram url to parse.

---

### Telegram

#### is_telegram_message_id

Function returning whether the given string is a valid Telegram message id or not.

```python
from ural.telegram import is_telegram_message_id

is_telegram_message_id('974583586343')
>>> True

is_telegram_message_id('whatever')
>>> False
```

#### is_telegram_url

Returns whether the given url is from Telegram.

```python
from ural.telegram import is_telegram_url

is_telegram_url('https://lemonde.fr')
>>> False

is_telegram_url('https://telegram.me/guillaumelatorre')
>>> True

is_telegram_url('https://t.me/s/jesstern')
>>> True
```

#### convert_telegram_url_to_public

Function returning the public version of the given Telegram url. Will raise an exception if a non-Telegram url is given.

```python
from ural.teglegram import convert_telegram_url_to_public

convert_telegram_url_to_public('https://t.me/jesstern')
>>> 'https://t.me/s/jesstern'
```

#### extract_channel_name_from_telegram_url

Return a channel from the given Telegram url or `None` if we could not find one.

```python
from ural.telegram import extract_channel_name_from_telegram_url

extract_channel_name_from_telegram_url('https://t.me/s/jesstern/345')
>>> 'jesstern'

extract_channel_name_from_telegram_url('https://lemonde.fr')
>>> None

```

#### parse_telegram_url

Returns parsed information about the given telegram url: either about the channel, message or user. If the url is an invalid Telegram url or if not a Telegram url, the function returns `None`.

```python
from ural.telegram import (
  parse_telegram_url,

  # You can also import the named tuples if you need them
  TelegramMessage,
  TelegramChannel,
  TelegramGroup
)

parse_telegram_url('https://t.me/s/jesstern/76')
>>> TelegramMessage(name='jesstern', id='76')

parse_telegram_url('https://lemonde.fr')
>>> None

parse_telegram_url('https://telegram.me/rapsocialclub')
>>> TelegramChannel(name='rapsocialclub')

parse_telegram_url('https://t.me/joinchat/AAAAAE9B8u_wO9d4NiJp3w')
>>> TelegramGroup(id='AAAAAE9B8u_wO9d4NiJp3w')
```

*Arguments*

* **url** *str*: Telegram url to parse.

---

### Twitter

#### is_twitter_url

Returns whether the given url is from Twitter.

```python
from ural.twitter import is_twitter_url

is_twitter_url('https://lemonde.fr')
>>> False

is_twitter_url('https://www.twitter.com/Yomguithereal')
>>> True

is_twitter_url('https://twitter.com')
>>> True
```

#### extract_screen_name_from_twitter_url

Extracts a normalized user's screen name from a Twitter url. If given an irrelevant url, the function will return `None`.


```python
from ural.twitter import extract_screen_name_from_twitter_url

extract_screen_name_from_twitter_url('https://www.twitter.com/Yomguithereal')
>>> 'yomguithereal'

extract_screen_name_from_twitter_url('https://twitter.fr')
>>> None
```

#### parse_twitter_url

Takes a Twitter url and returns either a `TwitterUser` namedtuple (contains a screen_name) if the given url is a link to a twitter user, a `TwitterTweet` namedtuple (contains a user_screen_name and an id) if the given url is a tweet's url, a `TwitterList` namedtuple (contains an id) or `None` if the given url is irrelevant.


```python
from ural.twitter import parse_twitter_url

parse_twitter_url('https://twitter.com/Yomguithereal')
>>> TwitterUser(screen_name='yomguithereal')

parse_twitter_url('https://twitter.com/medialab_ScPo/status/1284154793376784385')
>>> TwitterTweet(user_screen_name='medialab_scpo', id='1284154793376784385')

parse_twitter_url('https://twitter.com/i/lists/15512656222798157826')
>>> TwitterList(id='15512656222798157826')

parse_twitter_url('https://twitter.com/home')
>>> None
```

---

### Youtube

#### is_youtube_url

Returns whether the given url is from Youtube.

```python
from ural.youtube import is_youtube_url

is_youtube_url('https://lemonde.fr')
>>> False

is_youtube_url('https://www.youtube.com/watch?v=otRTOE9i51o')
>>> True

is_youtube_url('https://youtu.be/otRTOE9i51o)
>>> True
```

#### is_youtube_channel_id

Returns whether the given string is a formally valid Youtube channel id. Note that it won't validate the fact that this id actually refers to an existing channel or not. You will need to call YouTube servers for that.

```python
from ural.youtube import is_youtube_channel_id

is_youtube_channel_id('UCCCPCZNChQdGa9EkATeye4g')
>>> True

is_youtube_channel_id('@France24')
>>> False
```

#### is_youtube_video_id

Returns whether the given string is a formally valid YouTube video id. Note that it won't validate the fact that this id actually refers to an existing video or not. You will need to call YouTube servers for that.

```python
from ural.youtube import is_youtube_video_id

is_youtube_video_id('otRTOE9i51o')
>>> True

is_youtube_video_id('bDYTYET')
>>> False
```

#### parse_youtube_url

Returns parsed information about the given youtube url: either about the linked video, user or channel. If the url is an invalid Youtube url or if not a Youtube url, the function returns `None`.

```python
from ural.youtube import (
  parse_youtube_url,

  # You can also import the named tuples if you need them
  YoutubeVideo,
  YoutubeUser,
  YoutubeChannel,
  YoutubeShort,
)

parse_youtube_url('https://www.youtube.com/watch?v=otRTOE9i51o')
>>> YoutubeVideo(id='otRTOE9i51o')

parse_youtube_url('https://www.youtube.com/shorts/GINlKobb41w')
>>> YoutubeShort(id='GINlKobb41w')

parse_youtube_url('https://lemonde.fr')
>>> None

parse_youtube_url('http://www.youtube.com/channel/UCWvUxN9LAjJ-sTc5JJ3gEyA/videos')
>>> YoutubeChannel(id='UCWvUxN9LAjJ-sTc5JJ3gEyA', name=None)

parse_youtube_url('http://www.youtube.com/user/ojimfrance')
>>> YoutubeUser(id=None, name='ojimfrance')

parse_youtube_url('https://www.youtube.com/taranisnews')
>>> YoutubeChannel(id=None, name='taranisnews')
```

*Arguments*

* **url** *str*: Youtube url to parse.
* **fix_common_mistakes** *bool* [`True`]: Whether to fix common mistakes that can be found in Youtube urls as you can find them when crawling the web.

#### extract_video_id_from_youtube_url

Return a video id from the given Youtube url or `None` if we could not find one. Note that this will also work with Youtube shorts.

```python
from ural.youtube import extract_video_id_from_youtube_url

extract_video_id_from_youtube_url('https://www.youtube.com/watch?v=otRTOE9i51o')
>>> 'otRTOE9i51o'

extract_video_id_from_youtube_url('https://lemonde.fr')
>>> None

extract_video_id_from_youtube_url('http://youtu.be/afa-5HQHiAs')
>>> 'afa-5HQHiAs'
```

#### normalize_youtube_url

Returns a normalized version of the given Youtube url. It will normalize video, user and channel urls so you can easily match them.

```python
from ural.youtube import normalize_youtube_url

normalize_youtube_url('https://www.youtube.com/watch?v=otRTOE9i51o')
>>> 'https://www.youtube.com/watch?v=otRTOE9i51o'

normalize_youtube_url('http://youtu.be/afa-5HQHiAs')
>>> 'https://www.youtube.com/watch?v=afa-5HQHiAs'
```

---

## Miscellaneous

<h3 id="lru-explanation">About LRUs</h2>

*TL;DR*: a LRU is a hierarchical reordering of a URL so that one can perform meaningful prefix queries on URLs.

If you observe many URLs, you will quickly notice that they are not written in sound hierarchical order. In this URL, for instance:

```
http://business.lemonde.fr/articles/money.html?id=34#content
```

Some parts, such as the subdomain, are written in an "incorrect order". And this is fine, really, this is how URLs always worked.

But if what you really want is to match URLs, you will need to reorder them so that their order closely reflects the hierarchy of their targeted content. And this is exactly what LRUs are (that and also a bad pun on URL, since a LRU is basically a "reversed" URL).

Now look how the beforementioned URL could be splitted into LRU stems:

```python
[
  's:http',
  'h:fr',
  'h:lemonde',
  'h:business',
  'p:articles',
  'p:money.html',
  'q:id=34',
  'f:content'
]
```

And typically, this list of stems will be serialized thusly:

```
s:http|h:fr|h:lemonde|h:business|p:articles|p:money.html|q:id=34|f:content|
```

The trailing slash is added so that serialized LRUs can be *prefix-free*.
