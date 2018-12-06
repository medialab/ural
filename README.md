[![Build Status](https://travis-ci.org/medialab/ural.svg)](https://travis-ci.org/medialab/ural)

# Ural

A helper library full of URL-related heuristics.

## Installation

You can install `ural` with pip with the following command:

```
pip install ural
```

## Usage

- [Ural](#ural)
    - [Installation](#installation)
    - [Usage](#usage)
        - [ensure_protocol](#ensureprotocol)
        - [force_protocol](#forceprotocol)
        - [is_url](#isurl)
        - [normalize_url](#normalizeurl)
        - [strip_protocol](#stripprotocol)

### ensure_protocol

A function checking if the url has a protocol, and adding the given one if there is none.

```python
from ural import ensure_protocol

ensure_protocol('www2.lemonde.fr', protocol='https')
>>> 'https://www2.lemonde.fr'
```

_Arguments_

- **url** _string_: URL to format.
- **protocol** _string_: protocol to use if there is none in **url**. Is 'http' by default.

### force_protocol

A function force-replacing the protocol of the given url.

```python
from ural import force_protocol

force_protocol('https://www2.lemonde.fr', protocol='ftp')
>>> 'ftp://www2.lemonde.fr'
```

_Arguments_

- **url** _string_: URL to format.
- **protocol** _string_: protocol wanted in the output url. Is `'http'` by default.

### is_url

A function returning True if its argument is a url.

```python
from ural import is_url

is_url('https://www2.lemonde.fr')
>>> True
```

_Arguments_

- **string** _string_: string to test.
- **require_protocol** _bool_: whether the argument has to have a protocol to be considered a url. Is `True` by default.

### normalize_url

Function normalizing the given url by stripping it of usually non-discriminant parts such as irrelevant query items or sub-domains etc.

This is a very useful utility when attempting to match similar urls written slightly differently when shared on social media etc.

```python
from ural import normalize_url

normalize_url('https://www2.lemonde.fr/index.php#anchor')
>>> 'lemonde.fr'
```

_Arguments_

- **url** _string_: URL to normalize.
- **strip_trailing_slash** _boolean_ [`False`]: whether to strip trailing slash.
- **strip_index** _boolean_ [`True`]: Whether to drop index.xxxx at the end of the url.

### strip_protocol

Function removing the protocol from the url.

```python
from ural import strip_protocol

strip_protocol('https://www2.lemonde.fr/index.php')
>>> 'www2.lemonde.fr/index.php'
```

_Arguments_

- **url** _string_: URL to format.
