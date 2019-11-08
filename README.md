[![Build Status](https://travis-ci.org/medialab/ural.svg)](https://travis-ci.org/medialab/ural)

# Ural

A helper library full of URL-related heuristics.

## Installation

You can install `ural` with pip with the following command:

```
pip install ural
```

## Usage

*Generic functions*

* [ensure_protocol](#ensure_protocol)
* [get_domain_name](#get_domain_name)
* [force_protocol](#force_protocol)
* [is_url](#is_url)
* [normalize_url](#normalize_url)
* [strip_protocol](#strip_protocol)
* [urls_from_html](#urls_from_html)
* [urls_from_text](#urls_from_text)

*LRU-related functions* ([What on earth is a LRU?](#lru-explanation))

* [lru.lru_stems](#lrulru_stems)
* [lru.normalized_lru_stems](#lrunormalized_lru_stems)

*LRU-related classes*

* [NormalizedLRUTrie](#NormalizedLRUTrie)
  * [set](#set)
  * [match](#match)
  * [values](#values)

*Platform-specific functions*

* [facebook](#facebook)
  * [convert_facebook_url_to_mobile](#convert_facebook_url_to_mobile)
  * [extract_user_from_url](#extract_user_from_url)
* [youtube](#youtube)
  * [is_youtube_url](#is_youtube_url)
  * [is_youtube_video_id](#is_youtube_video_id)
  * [parse_youtube_url](#parse_youtube_url)
  * [extract_video_id_from_youtube_url](#extract_video_id_from_youtube_url)
  * [normalize_youtube_url](#normalize_youtube_url)

---

### ensure_protocol

Function checking if the url has a protocol, and adding the given one if there is none.

```python
from ural import ensure_protocol

ensure_protocol('www2.lemonde.fr', protocol='https')
>>> 'https://www2.lemonde.fr'
```

*Arguments*

* **url** *string*: URL to format.
* **protocol** *string*: protocol to use if there is none in **url**. Is 'http' by default.

---

### get_domain_name

Function returning an url's domain name. This function is of course tld-aware and will return `None` if no valid domain name can be found.

```python
from ural import get_domain_name

get_domain_name('https://facebook.com/path')
>>> 'facebook.com'
```

*Arguments*

* **url** *string*: Target url.

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

### is_url

Function returning True if its argument is a url.

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

### normalize_url

Function normalizing the given url by stripping it of usually non-discriminant parts such as irrelevant query items or sub-domains etc.

This is a very useful utility when attempting to match similar urls written slightly differently when shared on social media etc.

```python
from ural import normalize_url

normalize_url('https://www2.lemonde.fr/index.php?utm_source=google')
>>> 'lemonde.fr'
```

*Arguments*

* **url** *string*: URL to normalize.
* **sort_query** *bool* [`True`]: whether to sort query items.
* **strip_authentication** *bool* [`True`]: whether to strip authentication.
* **strip_fragment** *bool|str* [`'except-routing'`]: whether to strip the url's fragment. If set to `except-routing`, will only strip the fragment if the fragment is not deemed to be js routing (i.e. if it contains a `/`).
* **strip_index** *bool* [`True`]: whether to strip trailing index.
* **strip_lang_subdomains** *bool* [`False`]: whether to strip language subdomains (ex: 'fr-FR.lemonde.fr' to only 'lemonde.fr' because 'fr-FR' isn't a relevant subdomain, it indicates the language and the country).
* **strip_trailing_slash** *bool* [`False`]: whether to strip trailing slash.

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

### urls_from_html

Function returning an iterator over the urls present in the links of given HTML text.

```python
from ural import urls_from_html

html = """<p>Hey! Check this site: <a href="https://medialab.sciencespo.fr/">médialab</a></p>"""

for url in urls_from_html(html):
    print(url)
>>> 'https://medialab.sciencespo.fr/'
```

*Arguments*

* **string** *string*: html string.

---

### urls_from_text

Function returning an iterator over the urls present in the string argument. Extracts only the urls with a protocol.

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

### lru.lru_stems

Function returning url parts in hierarchical order.

```python
from ural.lru import lru_stems

lru_stems('http://www.lemonde.fr:8000/article/1234/index.html?field=value#2')
>>> ['s:http', 't:8000', 'h:fr', 'h:lemonde', 'h:www', 'p:article', 'p:1234', 'p:index.html', 'q:field=value', 'f:2']
```

*Arguments*

* **url** *string*: URL to parse.

---

### lru.normalized_lru_stems

Function normalizing url and returning its parts in hierarchical order.

```python
from ural.lru import normalized_lru_stems

normalized_lru_stems('http://www.lemonde.fr:8000/article/1234/index.html?field=value#2')
>>> ['t:8000', 'h:fr', 'h:lemonde', 'h:www', 'p:article', 'p:1234', 'q:field=value']
```

*Arguments*

This function accepts the same arguments as [normalize_url](#normalize_url).

---

### NormalizedLRUTrie

Class implementing a prefix tree (Trie) storing LRUs and their metadata, allowing to find the longest common prefix between two urls.

#### set

A method storing an url in a LRUTrie along with its metadata.

```python
from ural.lru import NormalizedLRUTrie

trie = NormalizedLRUTrie()
trie.set('http://www.lemonde.fr', {'type': 'general press'})

trie.match('http://www.lemonde.fr')
>>> {'type': 'general press'}
```

*Arguments*

* **url** *string*: url to store in the NormalizedLRUTrie.
* **metadata** *dict*: metadata of the url.

---

#### match

Method returning the metadata of the given url as it is stored in the NormalizedLRUTrie.
If the exact given url doesn't exist in the NormalizedLRUTrie, it returns the metadata of the longest common prefix, or `None` if there is no common prefix.

```python
from ural.lru import NormalizedLRUTrie

trie = NormalizedLRUTrie()
trie.set('http://www.lemonde.fr', {'media': 'lemonde'})

trie.match('http://www.lemonde.fr')
>>> {'media': 'lemonde'}
trie.match('http://www.lemonde.fr/politique')
>>> {'media': 'lemonde'}
```

*Arguments*

* **url** *string*: url to match in the NormalizedLRUTrie.

---

#### values

Method yielding the metadata of each url stored in the NormalizedLRUTrie.

```python
from ural.lru import NormalizedLRUTrie

trie = NormalizedLRUTrie()
trie.set('http://www.lemonde.fr', {'media' : 'lemonde'})
trie.set('http://www.lefigaro.fr', {'media' : 'lefigaro'})
trie.set('https://www.liberation.fr', {'media' : 'liberation'})

for value in trie.values():
  print(value)
>>> {'media': 'lemonde'}
>>> {'media': 'liberation'}
>>> {'media': 'lefigaro'}
```

---

### Facebook

#### convert_facebook_url_to_mobile

Function returning the mobile version of the given Facebook url. Will raise an exception if a non-Facebook url is given.

```python
from ural.facebook import convert_facebook_url_to_mobile

convert_facebook_url_to_mobile('http://www.facebook.com/post/974583586343')
>>> 'http://m.facebook.com/post/974583586343'
```

---

#### extract_user_from_url

Function extracting user information from a facebook user url.

```python
from ural.facebook import extract_user_from_url

extract_user_from_url('https://www.facebook.com/people/Sophia-Aman/102016783928989')
>>> FacebookUser(id='102016783928989', handle=None, url='https://www.facebook.com/profile.php?id=102016783928989)

extract_user_from_url('/annelaure.rivolu?rc=p&__tn__=R')
>>> FacebookUser(id=None, handle='annelaure.rivolu', url='https://www.facebook.com/annelaure.rivolu)
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

#### is_youtube_video_id

Returns whether the given string is a formally valid Youtube id. Note that it won't validate the fact that this id actually refers to an existing video or not. You will need to call Youtube servers for that.

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
  YoutubeChannel
)

parse_youtube_url('https://www.youtube.com/watch?v=otRTOE9i51o')
>>> YoutubeVideo(id='otRTOE9i51o')

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

Return a video id from the given Youtube url or `None` if we could not find one.

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

If you look closely to many URLs, you will quickly notice that they are not written in a sound hierarchical order. In this url, for instance:

```
http://business.lemonde.fr/articles/money.html?id=34#content
```

Some parts, such as the subdomain, are written in an "incorrect order". And this is fine, really, this is how urls always worked.

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
