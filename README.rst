validator.py |Build Status| |PyPI version| |Bitdeli Badge|
==========================================================

A library for validating that dictionary values meet certain sets of
parameters. Much like form validators, but for dicts.

`Documentation <http://validatorpy.readthedocs.org/en/latest/index.html>`__
---------------------------------------------------------------------------

This README has some basic usage information, but more detailed
documentation may be found at
`ReadTheDocs <http://validatorpy.readthedocs.org/en/latest/index.html>`__.

Usage Example
-------------

First, install it from PyPI.

::

    pip install validator.py

.. code:: python


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

.. |Build Status| image:: https://travis-ci.org/mansam/validator.py.png?branch=master
   :target: https://travis-ci.org/mansam/validator.py
.. |PyPI version| image:: https://badge.fury.io/py/validator.py.png
   :target: http://badge.fury.io/py/validator.py
.. |Bitdeli Badge| image:: https://d2weczhvl823v0.cloudfront.net/mansam/validator.py/trend.png
   :target: https://bitdeli.com/free
