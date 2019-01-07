[![Build Status](https://travis-ci.org/medialab/ural.svg)](https://travis-ci.org/medialab/ural)

# Ural

A helper library full of URL-related heuristics.

## Installation

You can install `ural` with pip with the following command:

```
pip install ural
```

## Usage

* [ensure_protocol](#ensure_protocol)
* [force_protocol](#force_protocol)
* [is_url](#is_url)
* [normalize_url](#normalize_url)
* [strip_protocol](#strip_protocol)
* [urls_from_html](#urls_from_html)
* [urls_from_text](#urls_from_text)

---

### ensure_protocol

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

### force_protocol

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

### is_url

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
* **sort_query** *boolean* [`True`]: whether to sort query items.
* **strip_authentication** *boolean* [`True`]: whether to strip authentication.
* **strip_index** *boolean* [`True`]: whether to strip trailing index.
* **strip_trailing_slash** *boolean* [`False`]: whether to strip trailing slash.

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

### urls_from_text

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
