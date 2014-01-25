validator.py [![Build Status](https://travis-ci.org/mansam/validator.py.png?branch=master)](https://travis-ci.org/mansam/validator.py)
============

A library for validating that dictionary values meet certain sets of parameters. Much like form validators, but for dicts.

## Documentation

This README has some basic usage information, but more detailed documentation may be found at [ReadTheDocs](http://validatorpy.readthedocs.org/en/latest/index.html).

## Usage Example

First, install it from PyPI.

    pip install validator.py


```python

from validator import Required, Not, Truthy, Blank, Range, Equals, In, validate

# let's say that my dictionary needs to meet the following rules...
rules = {
    "foo": [Required, Equals(123)],
    "bar": [Required, Truthy()],
    "baz": [In(["spam", "eggs", "bacon"])],
    "qux": [Not(Range(1, 100))] # by default, Range is inclusive
}

# then this following dict would pass:
passes = {
    "foo": 123,
    "bar": True, # or a non-empty string, or a non-zero int, etc...
    "baz": "spam",
    "qux": 101
}
print validate(rules, passes)
# (True, {}) 

# but this one would fail
fails = {
    "foo": 321,
    "bar": False, # or 0, or [], or an empty string, etc...
    "baz": "barf",
    "qux": 99
}
print validate(rules, fails)
# (False,
#  {
#  'foo': ["must be equal to '123'"],
#  'bar': ['must be True-equivalent value'],
#  'baz': ["must be one of ['spam', 'eggs', 'bacon']"],
#  'qux': ['must not fall between 1 and 100']
#  })
```
