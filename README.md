[![Build Status](https://travis-ci.org/medialab/ural.svg)](https://travis-ci.org/medialab/ural)

# Ural

A helper library full of URL-related heuristics.

## Installation

You can install `ural` with pip with the following command:

```
pip install ural
```

## Usage

### Functions
* [ensure_protocol](#ensure_protocol)
* [force_protocol](#force_protocol)
* [is_url](#is_url)
* [lru_from_url](#lru_from_url)
* [normalize_url](#normalize_url)
* [normalized_lru_from_url](#normalized_lru_from_url)
* [strip_protocol](#strip_protocol)
* [urls_from_html](#urls_from_html)
* [urls_from_text](#urls_from_text)

### Classes
* [LRUTrie](#LRUTrie)
  * [set](#set)
  * [match](#match)
  * [values](#values)

---

### Functions

#### ensure_protocol

A function checking if the url has a protocol, and adding the given one if there is none.

```python
from ural import ensure_protocol

ensure_protocol('www2.lemonde.fr', protocol='https')
>>> 'https://www2.lemonde.fr'
```

*Arguments*

* **url** *string*: URL to format.
* **protocol** *string*: protocol to use if there is none in **url**. Is 'http' by default.

---

#### force_protocol

A function force-replacing the protocol of the given url.

```python
from ural import force_protocol

force_protocol('https://www2.lemonde.fr', protocol='ftp')
>>> 'ftp://www2.lemonde.fr'
```

*Arguments*

* **url** *string*: URL to format.
* **protocol** *string*: protocol wanted in the output url. Is `'http'` by default.

---

#### is_url

A function returning True if its argument is a url.

```python
from ural import is_url

is_url('https://www2.lemonde.fr')
>>> True
```

*Arguments*

* **string** *string*: string to test.
* **require_protocol** *boolean*: whether the argument has to have a protocol to be considered a url. Is `True` by default.

---

#### lru_from_url

Function returning url parts in hierarchical order.

```python
from ural import lru_from_url

lru_from_url('http://www.lemonde.fr:8000/article/1234/index.html?field=value#2')
>>> ['s:http', 't:8000', 'h:fr', 'h:lemonde', 'h:www', 'p:article', 'p:1234', 'p:index.html', 'q:field=value', 'f:2']
```

*Arguments*

* **url** *string*: URL to parse.

---

#### normalize_url

Function normalizing the given url by stripping it of usually non-discriminant parts such as irrelevant query items or sub-domains etc.

This is a very useful utility when attempting to match similar urls written slightly differently when shared on social media etc.

```python
from ural import normalize_url

normalize_url('https://www2.lemonde.fr/index.php?utm_source=google')
>>> 'lemonde.fr'
```

*Arguments*

* **url** *string*: URL to normalize.
* **sort_query** *boolean* [`True`]: whether to sort query items.
* **strip_authentication** *boolean* [`True`]: whether to strip authentication.
* **strip_index** *boolean* [`True`]: whether to strip trailing index.
* **strip_trailing_slash** *boolean* [`False`]: whether to strip trailing slash.

---

#### normalized_lru_from_url

Function normalizing url and returning its parts in hierarchical order.

```python
from ural import normalized_lru_from_url

normalized_lru_from_url('http://www.lemonde.fr:8000/article/1234/index.html?field=value#2')
>>> ['t:8000', 'h:fr', 'h:lemonde', 'h:www', 'p:article', 'p:1234', 'q:field=value']
```

*Arguments*

This function accepts the same arguments as [normalize_url](#normalize_url). 

---

#### strip_protocol

Function removing the protocol from the url.

```python
from ural import strip_protocol

strip_protocol('https://www2.lemonde.fr/index.php')
>>> 'www2.lemonde.fr/index.php'
```

*Arguments*

* **url** *string*: URL to format.

---

#### urls_from_html

A function returning an iterator over the urls present in the links of given HTML text.

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

#### urls_from_text

A function returning an iterator over the urls present in the string argument. Extracts only the urls with a protocol.

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

### Classes

#### LRUTrie

A class implementing a prefix tree (Trie) storing LRUs and their metadata, allowing to find the longest common prefix between two urls.

##### set

A function storing an url in a LRUTrie along with its metadata.

```python
from ural import LRUTrie

trie = LRUTrie()
trie.set('http://www.lemonde.fr', {'type': 'general press'})

trie.match('http://www.lemonde.fr')
>>> {'type': 'general press'}
```

*Arguments*

* **url** *string*: url to store in the LRUTrie.
* **metadata** *dict*: metadata of the url.

---

##### match

A function returning the metadata of the given url as it is stored in the LRUTrie.
If the exact given url doesn't exist in the LRUTrie, it returns the metadata of the longest common prefix, or `None` if there is no common prefix.

```python
from ural import LRUTrie

trie = LRUTrie()
trie.set('http://www.lemonde.fr', {'media': 'lemonde'})

trie.match('http://www.lemonde.fr')
>>> {'media': 'lemonde'}
trie.match('http://www.lemonde.fr/politique')
>>> {'media': 'lemonde'}
```

*Arguments*

* **url** *string*: url to match in the LRUTrie.

---

##### values

A function yielding the metadata of each url stored in the LRUTrie.

```python
from ural import LRUTrie

trie = LRUTrie()
trie.set('http://www.lemonde.fr', {'media' : 'lemonde'})
trie.set('http://www.lefigaro.fr', {'media' : 'lefigaro'})
trie.set('https://www.liberation.fr', {'media' : 'liberation'})

for value in trie.values():
  print(value)
>>> {'media': 'lemonde'}
>>> {'media': 'liberation'}
>>> {'media': 'lefigaro'}
```
