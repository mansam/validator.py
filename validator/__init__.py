"""
validator.py

A library for validating that dictionary
values fit inside of certain sets of parameters.

Author: Samuel Lucidi <slucidi@newstex.com>

"""

__version__ = "0.4.0"

import re
from collections import defaultdict
from inspect import getargspec

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
    return in_lambda

def Not(validator):
    """
    Use to negate the requirement
    of another validator. Does not
    work with Required.

    """

    def not_lambda(value):
        return not validator(value)

    if validator.__name__ == "eq_lambda":
        not_lambda.err_message = "must not be equal to '%s'" % validator.value
    elif validator.__name__ == "truth_lambda":
        not_lambda.err_message = "must be False-equivalent value"
    elif validator.__name__ == "in_lambda":
        not_lambda.err_message = "must not be one of %s" % validator.collection
    elif validator.__name__ == "blank_lambda":
        not_lambda.err_message = "must not be blank"
    elif validator.__name__ == "range_lambda":
        not_lambda.err_message = "must not fall between %s and %s" % (validator.start, validator.end)
    elif validator.__name__ == "instanceof_lambda":
        not_lambda.err_message = "must not be an instance of %s or its subclasses" % validator.base_class
    elif validator.__name__ == "pattern_lambda":
        not_lambda.err_message = "must not match regex pattern %s" % validator.pattern
    elif validator.__name__ == "subclassof_lambda":
        not_lambda.err_message = "must not be a subclass of %s" % validator.base_class

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


def ArgSpec(*args, **kwargs):
    """
    Validate a function based on the given argspec
    # Example:
        validations = {
            "foo": [ArgSpec("a", "b", c", bar="baz")]
        }
        def pass_func(a, b, c, bar="baz"):
            pass
        def fail_func(b, c, a, baz="bar"):
            pass
        passes = {"foo": pass_func}
        fails = {"foo": fail_func}
    """
    def argspec_lambda(value):
        argspec = getargspec(value)
        argspec_kw_vals = ()
        if argspec.defaults != None:
            argspec_kw_vals = argspec.defaults
        kw_vals = {}
        arg_offset = 0
        arg_len = len(argspec.args) - 1
        for val in argspec_kw_vals[::-1]:
            kw_vals[argspec.args[arg_len - arg_offset]] = val
            arg_offset += 1
        if kwargs == kw_vals:
            if len(args) != arg_len - arg_offset + 1:
                return False
            index = 0
            for arg in args:
                if argspec.args[index] != arg:
                    return False
                index += 1
            return True
        return False
    argspec_lambda.err_message = "must match argspec ({0}) {{{1}}}".format(args, kwargs)
    return argspec_lambda

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
            # skip Required, since it was already
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
