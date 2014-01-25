.. validator.py documentation master file, created by
   sphinx-quickstart on Fri Jan 24 01:02:35 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

validator.py | build status |
=============================

.. .. toctree::
..    :maxdepth: 2
   

About
-----

``validator.py`` is a tool for ensuring that data conforms to certain sets of rules, called validations. A validation is essentially a schema for a dictionary, containing a list of rules for each key/value pair in the dictionary you want to validate. This is intended to fill a similar use case to form validations in WTForms or Rails, but for general sources of data, not just web forms. To get right on with it, here's a quick example of what this is for and how it works:

.. code:: python


    from validator import Required, Not, Truthy, Blank, Range, Equals, In, validate

    # let's say that my dictionary needs to meet the following rules...
    rules = {
        "foo": [Required, Equals(123)], # foo must be exactly equal to 123
        "bar": [Required, Truthy()],    # bar must be equivalent to True
        "baz": [In(["spam", "eggs", "bacon"])], # baz must be one of these options
        "qux": [Not(Range(1, 100))] # qux must not be a number between 1 and 100 inclusive
    }

    # then this following dict would pass:
    passes = {
        "foo": 123,
        "bar": True, # or a non-empty string, or a non-zero int, etc...
        "baz": "spam",
        "qux": 101
    }
    >>> print validate(rules, passes)
    (True, {}) 

    # but this one would fail
    fails = {
        "foo": 321,
        "bar": False, # or 0, or [], or an empty string, etc...
        "baz": "barf",
        "qux": 99
    }
    >>> print validate(rules, fails)
    (False, {
     'foo': ["must be equal to 123"],
     'bar': ['must be True-equivalent value'],
     'baz': ["must be one of ['spam', 'eggs', 'bacon']"],
     'qux': ['must not fall between 1 and 100']
    })

Notice that the validation that passed just returned True and an empty ``dict``, but the one that failed returned a tuple with False and a ``dict`` with a list of related error messages for each key that failed. This lets you easily see exactly what failed in a human readable way.

Installation
------------
Stable releases can be installed via ``pip install validator.py``. Alternatively, you can get the latest sources or a release tarball from http://github.com/mansam/validator.py.

``validator.py`` is written with Python 2.7, but is tested with 2.6 and PyPy. It should also work with 2.5 and 3.x, though the tests currently won't run on 3.x.

Getting Started with Validations
--------------------------------

A validation (the set of rules used to test a dict) can be flat --consisting of just a single level of tests-- or it can contain additional conditionally nested validations. 

To create a validation, you insert a list of callables into a validation dictionary for each key/value pair in the dictionary you want to validate. When you call ``validate` with the validation and your dictionary, each of those callables will be called with the respective value in your dictionary as their argument. If the callable returns ``True``, then you're good to go. For example:

.. code:: python

    dictionary = {
		"foo": "bar"
	}
	validation = {
		"foo": [lambda x: x == "bar"] 
	}
	
	>>> validate(validation, dictionary)
	(True, {})
	# Success!

When ``validate`` got called in the example, the value of ``dictionary["foo"]`` got passed to lambda in the list, and ``since dictionary["foo"] == "bar"``, everything is good and the dictionary is considered valid!

Writing your own callables is helpful in some cases, but ``validator.py`` helpfully provides a wide range of validations that should cover most of the common use cases.

The ``Equals`` validator
------------------------

The ``Equals`` validator just checks that the dictionary value matches the parameter to ``Equals``. We use it to rewrite our previous example more succinctly:

.. code:: python

    dictionary = {
		"foo": "bar"
	}
	validation = {
		"foo": [Equals("bar")]
	}
	
	>>> validate(validation, dictionary)
	(True, {})
	# Success!

In the event that it fails, it explains so clearly:

.. code:: python

	>>> validate(validation, failure)
	(False, {"foo": ["must be equal to 'baz'"]})
	
The ``Required`` validator
--------------------------

By default, a key is considered optional. A key that's in the validation but isn't in the dictionary under test just gets silently skipped. To make sure that a key is present, use the ``Required`` validator. Adding the ``Required`` validator to the list of rules for a key ensures that the key must be present in the dictionary. Unlike most of the other validators that ``validator.py`` provides, ``Required`` shouldn't be written with parentheses.

.. code:: python

    dictionary = {
		"foo": "bar"
	}
	validation = {
		"foo": [Required, Equals("bar")]
	}
	
	>>> validate(validation, dictionary)
	(True, {})
	# Success!

In the event that a key is missing:

.. code:: python

    failure = {}
	>>> validate(validation, failure)
	(False, {"foo": ["is missing"]})

Conditional Validations
-----------------------

Available Validators
--------------------

.. |Build Status| image:: https://travis-ci.org/mansam/validator.py.png?branch=master
   :target: https://travis-ci.org/mansam/validator.py

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

