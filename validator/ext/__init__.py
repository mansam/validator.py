"""
Extensions.
Additional validators that are a little more complex than the defaults or
that otherwise don't fit into the base part of the module.

"""

from validator import Pattern
from inspect import getargspec
import string

def ArgSpec(*args, **kwargs):
    """
    Validate a function based on the given argspec.

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
    # as little sense as negating this makes, best to just be consistent.
    argspec_lambda.not_message = "must not match argspec ({0}) {{{1}}}".format(args, kwargs)
    return argspec_lambda