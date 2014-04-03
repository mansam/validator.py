# The MIT License (MIT)

# Copyright (c) 2014 Samuel Lucidi

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
validator.py

A library for validating that dictionary
values fit inside of certain sets of parameters.

Author: Samuel Lucidi <sam@samlucidi.com>

"""

__version__ = "0.8.0"

import re
from collections import defaultdict

def _isstr(s):
    """
    Python 2/3 compatible check to see
    if an object is a string type.

    """

    try:
        return isinstance(s, basestring)
    except NameError:
        return isinstance(s, str)

def In(collection):
    """
    Use to specify that the
    value of the key being
    validated must exist
    within the collection
    passed to this validator.

    # Example:
        validations = {
            "field": [In([1, 2, 3])]
        }
        passes = {"field":1}
        fails  = {"field":4}

    """

    def in_lambda(value):
        return (value in collection)

    in_lambda.collection = collection
    in_lambda.err_message = "must be one of %r" % collection
    in_lambda.not_message = "must not be one of %r" % collection
    return in_lambda

def Not(validator):
    """
    Use to negate the requirement
    of another validator. Does not
    work with Required.

    """

    def not_lambda(value):
        result = validator(value)
        not_lambda.err_message = getattr(validator, "not_message", "failed validation")
        not_lambda.not_message = getattr(validator, "err_message", "failed validation")
        return not result

    return not_lambda

def Range(start, end, inclusive=True):

    def range_lambda(value):
        if inclusive:
            return start <= value <= end
        else:
            return start < value < end
    range_lambda.start = start
    range_lambda.end = end
    range_lambda.err_message = "must fall between %s and %s" % (start, end)
    range_lambda.not_message = "must not fall between %s and %s" % (start, end)
    return range_lambda

def Equals(obj):
    """
    Use to specify that the
    value of the key being
    validated must be equal to
    the value that was passed
    to this validator.

    # Example:
        validations = {
            "field": [Equals(1)]
        }
        passes = {"field":1}
        fails  = {"field":4}

    """

    def eq_lambda(value):
        return value == obj

    eq_lambda.value = obj
    eq_lambda.err_message = "must be equal to %r" % obj
    eq_lambda.not_message = "must not be equal to %r" % obj
    return eq_lambda

def Blank():
    """
    Use to specify that the
    value of the key being
    validated must be equal to
    the empty string.

    This is a shortcut for saying
    Equals("").

    # Example:
        validations = {
            "field": [Blank()]
        }
        passes = {"field":""}
        fails  = {"field":"four"}

    """

    def blank_lambda(value):
        return value == ""
    blank_lambda.err_message = "must be an empty string"
    blank_lambda.not_message = "must not be an empty string"
    return blank_lambda

def Truthy():
    """
    Use to specify that the
    value of the key being
    validated must be truthy,
    i.e. would cause an if statement
    to evaluate to True.

    # Example:
        validations = {
            "field": [Truthy()]
        }
        passes = {"field": 1}
        fails  = {"field": 0}


    """

    def truth_lambda(value):
        if value:
            return True
        else:
            return False
    truth_lambda.err_message = "must be True-equivalent value"
    truth_lambda.not_message = "must be False-equivalent value"
    return truth_lambda

def Required(field, dictionary):
    """
    When added to a list of validations
    for a dictionary key indicates that
    the key must be present. This
    should not be called, just inserted
    into the list of validations.

    # Example:
        validations = {
            "field": [Required, Equals(2)]
        }

    By default, keys are considered
    optional and their validations
    will just be ignored if the field
    is not present in the dictionary
    in question.

    """

    return (field in dictionary)

def InstanceOf(base_class):
    """
    Use to specify that the
    value of the key being
    validated must be an instance
    of the passed in base class
    or its subclasses.

    # Example:
        validations = {
            "field": [InstanceOf(basestring)]
        }
        passes = {"field": ""} # is a <'str'>, subclass of basestring
        fails  = {"field": str} # is a <'type'>

    """

    def instanceof_lambda(value):
        return isinstance(value, base_class)

    instanceof_lambda.base_class = base_class
    instanceof_lambda.err_message = "must be an instance of %s or its subclasses" % base_class.__name__
    instanceof_lambda.not_message = "must not be an instance of %s or its subclasses" % base_class.__name__
    return instanceof_lambda

def SubclassOf(base_class):
    """
    Use to specify that the
    value of the key being
    validated must be a subclass
    of the passed in base class.

    # Example:
        validations = {
            "field": [SubclassOf(basestring)]
        }
        passes = {"field": str} # is a subclass of basestring
        fails  = {"field": int}
    """

    def subclassof_lambda(class_):
        return issubclass(class_, base_class)

    subclassof_lambda.base_class = base_class
    subclassof_lambda.err_message = "must be a subclass of %s" % base_class.__name__
    subclassof_lambda.not_message = "must not be a subclass of %s" % base_class.__name__
    return subclassof_lambda

def Pattern(pattern):
    """
    Use to specify that the
    value of the key being
    validated must match the
    pattern provided to the
    validator.

    # Example:
        validations = {
            "field": [Pattern('\d\d\%')]
        }
        passes = {"field": "30%"}
        fails  = {"field": "30"}

    """

    compiled = re.compile(pattern)

    def pattern_lambda(value):
        return compiled.match(value)
    pattern_lambda.pattern = pattern
    pattern_lambda.err_message = "must match regex pattern %s" % pattern
    pattern_lambda.not_message = "must not match regex pattern %s" % pattern
    return pattern_lambda

def Then(validation):
    """
    Special validator for use as
    part of the If rule.
    If the conditional part of the validation
    passes, then this is used to apply another
    set of dependent rules.

    # Example:
        validations = {
            "foo": [If(Equals(1), Then({"bar": [Equals(2)]}))]
        }
        passes = {"foo": 1, "bar": 2}
        also_passes = {"foo": 2, "bar": 3}
        fails = {"foo": 1, "bar": 3}
    """

    def then_lambda(dictionary):
        return validate(validation, dictionary)

    return then_lambda


def If(validator_lambda, then_lambda):
    """
    Special conditional validator.
    If the validator passed as the first
    parameter to this function passes,
    then a second set of rules will be
    applied to the dictionary.

    # Example:
        validations = {
            "foo": [If(Equals(1), Then({"bar": [Equals(2)]}))]
        }
        passes = {"foo": 1, "bar": 2}
        also_passes = {"foo": 2, "bar": 3}
        fails = {"foo": 1, "bar": 3}
    """

    def if_lambda(value, dictionary):
        conditional = False
        dependent = None
        if validator_lambda(value):
            conditional = True
            dependent = then_lambda(dictionary)
        return conditional, dependent

    return if_lambda

    
def Length(minimum, maximum=0):
    """
    Use to specify that the
    value of the key being
    validated must have at least
    `minimum` elements and optionally
    at most `maximum` elements.

    At least one of the parameters
    to this validator must be non-zero, 
    and neither may be negative.

    # Example:
        validations = {
            "field": [Length(0, maximum=5)]
        }
        passes = {"field": "hello"}
        fails  = {"field": "hello world"}

    """

    if not minimum and not maximum:
        raise ValueError("Length must have a non-zero minimum or maximum parameter.")
    if minimum < 0 or maximum < 0:
        raise ValueError("Length cannot have negative parameters.")

    err_messages = {
        "maximum": "must be at most {0} {1} in length",
        "minimum": "must be at least {0} {1} in length",
        "range": "must{0}be between {1} and {2} {3} in length"
    }

    def length_lambda(value):

        # this is all a crufty hack to set an
        # appropriate error message.
        if _isstr(value):
            length_lambda.unit = "characters"
        else:
            length_lambda.unit = "elements"
        if minimum and maximum:
            err_msg = err_messages["range"].format(' ', minimum, maximum, length_lambda.unit)
            not_msg = err_messages["range"].format(' not ', minimum, maximum, length_lambda.unit)
        elif minimum:
            err_msg = err_messages["minimum"].format(minimum, length_lambda.unit)
            not_msg = err_messages["maximum"].format(minimum - 1, length_lambda.unit)
        elif maximum:
            err_msg = err_messages["maximum"].format(maximum, length_lambda.unit)
            not_msg = err_messages["minimum"].format(maximum + 1, length_lambda.unit)
        else:
            # this should not be possible
            assert False

        length_lambda.err_message = err_msg
        length_lambda.not_message = not_msg
        # the actual test starts here
        if maximum:
            return minimum <= len(value) <= maximum
        else:
            return minimum <= len(value)

    return length_lambda

def Contains(contained):
    """
    Use to ensure that the value of the key
    being validated contains the value passed
    into the Contains validator. Works with
    any type that supports the 'in' syntax.

    # Example:
        validations = {
            "field": [Contains(3)]
        }
        passes = {"field": [1, 2, 3]}
        fails  = {"field": [4, 5, 6]}

    """

    def contains_lambda(value):
        return contained in value

    contains_lambda.err_message = "must contain {0}".format(contained)
    contains_lambda.not_message = "must not contain {0}".format(contained)
    return contains_lambda

def validate(validation, dictionary):
    """
    Validate that a dictionary passes a set of
    key-based validators. If all of the keys
    in the dictionary are within the parameters
    specified by the validation mapping, then
    the validation passes.

    :param validation: a mapping of keys to validators
    :type validation: dict

    :param dictionary: dictionary to be validated
    :type dictionary: dict

    :return: a tuple containing a bool indicating
    success or failure and a mapping of fields
    to error messages.

    """

    errors = defaultdict(list)
    for key in validation:
        if Required in validation[key]:
            if not Required(key, dictionary):
                errors[key] = "must be present"
                continue
        for v in validation[key]:
            # don't break on optional keys
            if key in dictionary:
                # Ok, need to deal with nested
                # validations.
                if isinstance(v, dict):
                    valid, nested_errors = validate(v, dictionary[key])
                    if nested_errors:
                        errors[key].append(nested_errors)
                    continue
                # Done with that, on to the actual
                # validating bit.
                # Skip Required, since it was already
                # handled before this point.
                if not v == Required:
                    # special handling for the
                    # If(Then()) form
                    if v.__name__ == "if_lambda":
                        conditional, dependent = v(dictionary[key], dictionary)
                        # if the If() condition passed and there were errors
                        # in the second set of rules, then add them to the
                        # list of errors for the key with the condtional
                        # as a nested dictionary of errors.
                        if conditional and dependent[1]:
                            errors[key].append(dependent[1])
                    # handling for normal validators
                    else:
                        valid = v(dictionary[key])
                        if not valid:
                            msg = getattr(v, "err_message", "failed validation")
                            errors[key].append(msg)
    if len(errors) > 0:
        return False, dict(errors)
    else:
        return True, {}
