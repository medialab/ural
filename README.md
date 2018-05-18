[![Build Status](https://travis-ci.org/Yomguithereal/ural.svg)](https://travis-ci.org/Yomguithereal/ural)

# Ural

A helper library full of URL-related heuristics.

## Installation

You can install `ural` with pip with the following command:

```
pip install ural
```

## Usage

* [normalize_url](#normalize_url)

### normalize_url

Function normalizing the given url by stripping it of usually non-discriminant parts such as irrelevant query items or sub-domains etc.

This is a very useful utility when attempting to match similar urls written slightly differently when shared on social media etc.

```python
from ural import normalize_url

url('https://www2.lemonde.fr/index.php#anchor')
>>> 'lemonde.fr'
```

*Arguments*

* **url** *string*: URL to normalize.


todo: ensure protocol
