"""
validator.py

A library for validating that dictionary
values fit inside of certain sets of parameters.

Author: Samuel Lucidi <slucidi@newstex.com>

"""

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
    in_lambda.err_message = "must be one of %s" % collection
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
    elif validator.__name__ == "class_lambda":
        not_lambda.err_message = "must not be an instance of %s or its subclasses" % validator.base_class

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
    eq_lambda.err_message = "must be equal to '%s'" % obj
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

def Classy(base_class):
    """
    Use to specify that the
    value of the key being
    validated must be an instance
    of the passed in base class
    or its subclasses.

    # Example:
        validations = {
            "field": [Classy(basestring)]
        }
        passes = {"field": ""} # is a <'str'>, subclass of basestring
        fails  = {"field": str} # is a <'type'>


    """

    def class_lambda(value):
        return isinstance(value, base_class)

    class_lambda.base_class = base_class
    class_lambda.err_message = "must be an instance of %s or its subclasses" % base_class.__name__
    return class_lambda

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

    errors = {}
    for key in validation:
        if Required in validation[key]:
            if not Required(key, dictionary):
                errors[key] = "must be present"
                continue
        for v in validation[key]:
            if not v == Required:
                valid = v(dictionary[key])
                if not valid:
                    if not key in errors:
                        errors[key] = []
                    errors[key].append(v.err_message)
    if len(errors) > 0:
        return False, errors
    else:
        return True, {}