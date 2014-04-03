from validator import *
from validator.ext import *

class BaseClass(object):
    pass

class SubClass(BaseClass):
    pass

class TestValidator(object):

    def test_argspec_validator(self):
        def truth_func(a, b, c):
            pass
        def false_func(c, b, a):
            pass
        def truth_kw_func(a, b, c, d=1):
            pass
        def false_kw_func(a, b, c, d=2):
            pass

        validator = {
            "truthiness": [ArgSpec('a', 'b', 'c')],
            "falsiness": [Not(ArgSpec('a', 'b', 'c'))],
        }
        kw_validator = {
            "truthiness": [ArgSpec('a', 'b', 'c', d=1)],
            "falsiness": [Not(ArgSpec('a', 'b', 'c', d=1))],
        }
        values = {
            "truthiness": truth_func,
            "falsiness": false_func,
        }
        values_kw = {
            "truthiness": truth_kw_func,
            "falsiness": false_kw_func,
        }
        assert validate(validator, values)[0]
        assert validate(kw_validator, values_kw)[0]

    def test_truthy_validator(self):
        validator = {
            "truthiness": [Truthy()],
            "falsiness": [Not(Truthy())]
        }
        str_value = {
            "truthiness": "test",
            "falsiness": ""
        }
        int_value = {
            "truthiness": 1,
            "falsiness": 0
        }
        bool_value = {
            "truthiness": True,
            "falsiness": False
        }
        assert validate(validator, str_value)[0]
        assert validate(validator, int_value)[0]
        assert validate(validator, bool_value)[0]

    def test_required_validator(self):
        validator = {
            "truthiness": [Required],
            "falsiness": []
        }
        str_value = {
            "truthiness": "test"
        }
        int_value = {
            "truthiness": 1
        }
        bool_value = {
            "truthiness": True
        }
        assert validate(validator, str_value)[0]
        assert validate(validator, int_value)[0]
        assert validate(validator, bool_value)[0]

    def test_blank_validator(self):
        validator = {
            "truthiness": [Blank()],
            "falsiness": [Not(Blank())]
        }
        str_value = {
            "truthiness": "",
            "falsiness": "not_blank"
        }
        int_value = {
            "truthiness": 1,
            "falsiness": 0
        }
        bool_value = {
            "truthiness": True,
            "falsiness": False
        }
        assert validate(validator, str_value)[0]
        assert not validate(validator, int_value)[0]
        assert not validate(validator, bool_value)[0]

    def test_in_validator(self):
        validator = {
            "truthiness": [Truthy()],
            "falsiness": [Not(Truthy())]
        }
        str_value = {
            "truthiness": "test",
            "falsiness": ""
        }
        int_value = {
            "truthiness": 1,
            "falsiness": 0
        }
        bool_value = {
            "truthiness": True,
            "falsiness": False
        }
        assert validate(validator, str_value)[0]
        assert validate(validator, int_value)[0]
        assert validate(validator, bool_value)[0]

    def test_equals_validator(self):
        validator = {
            "truthiness": [Truthy()],
            "falsiness": [Not(Truthy())]
        }
        str_value = {
            "truthiness": "test",
            "falsiness": ""
        }
        int_value = {
            "truthiness": 1,
            "falsiness": 0
        }
        bool_value = {
            "truthiness": True,
            "falsiness": False
        }
        assert validate(validator, str_value)[0]
        assert validate(validator, int_value)[0]
        assert validate(validator, bool_value)[0]

    def test_not_validator(self):
        validator = {
            "test_truthy":  [Not(Truthy())],
            "test_equals":  [Not(Equals("one"))],
            "test_not_not": [Not(Not(Truthy()))],
            "test_in":      [Not(In(['one', 'two']))],
            "test_range":   [Not(Range(1, 10))],
            "test_pattern": [Not(Pattern("\d\d\d"))]
        }
        test_case = {
            "test_truthy": False,
            "test_equals": "two",
            "test_not_not": True,
            "test_in": "three",
            "test_range": 11,
            "test_pattern": "abc"
        }
        assert validate(validator, test_case)[0]

    def test_range_validator(self):
        validator = {
            "in_range": [Range(1, 10)],
            "out_of_range": [Not(Range(1, 10))],
            "exclusive_in_range": [Range(1, 10, inclusive=False)],
            "exclusive_out_of_range": [Not(Range(1, 10, inclusive=False))]
        }
        test_case = {
            "in_range": 1,
            "out_of_range": 11,
            "exclusive_in_range": 2,
            "exclusive_out_of_range": 1
        }
        assert validate(validator, test_case)[0]

    def test_instanceof_validator(self):
        validator = {
            "classy": [Required, InstanceOf(SubClass)],
            "subclassy": [Required, InstanceOf(BaseClass)],
            "not_classy": [Required, Not(InstanceOf(SubClass))],
            "not_subclassy": [Required, Not(InstanceOf(BaseClass))]
        }
        test_case = {
            "classy": SubClass(),
            "subclassy": BaseClass(),
            "not_classy": object(),
            "not_subclassy": 3
        }
        assert validate(validator, test_case)[0]

    def test_subclassof_validator(self):
        validator = {
            "is_subclass": [Required, SubclassOf(BaseClass)],
            "not_subclass": [Required, Not(SubclassOf(BaseClass))],
        }
        test_case = {
            "is_subclass": SubClass,
            "not_subclass": int
        }
        assert validate(validator, test_case)[0]

    def test_pattern_validator(self):
        validator = {
            "match": [Required, Pattern('\d\d\%')],
            "no_match": [Required, Not(Pattern('\d\d\%'))]
        }
        test_case = {
            "match": "39%",
            "no_match": "ab%"
        }
        assert validate(validator, test_case)[0]

    def test_conditional_validator(self):
        passes = {
            "if_true_passes": [Required, If(Equals(1), Then({"dependent_passes": [Equals(1)]}))],
            "if_false_passes": [Required, If(Equals(1), Then({"dependent_fails": [Equals(1)]}))],
        }
        fails = {
            "if_true_fails": [Required, If(Equals(1), Then({"dependent_fails": [Equals(1)]}))]
        }
        test_case = {
            "if_true_passes": 1,
            "if_false_passes": 2,
            "if_true_fails": 1,
            "dependent_passes": 1,
            "dependent_fails": 2
        }
        assert validate(passes, test_case)[0]
        assert not validate(fails, test_case)[0]

    def test_nested_validations(self):
        passes = {
            "foo": [Required, Equals(1)],
            "bar": [
                Required,
                {
                    "baz": [Required, Equals(2)],
                    "qux": [Required, {
                        "quux": [Required, Equals(3)]
                    }]
                }
            ]
        }
        fails = {
            "foo": [Required, Equals(2)],
            "bar": [
                Required,
                {
                    "baz": [Required, Equals(3)],
                    "qux": [Required, {
                        "quux": [Required, Equals(4)]
                    }]
                }
            ]
        }
        test_case = {
            "foo": 1,
            "bar": {
                "baz": 2,
                "qux": {
                    "quux": 3
                }
            }
        }
        assert validate(passes, test_case)[0]
        assert not validate(fails, test_case)[0]

    def test_optional_validations(self):
        optional_validation = {
            "foo": [Equals(1)],
            "bar": [{
                "baz": [Equals(2)],
                "qux": [Equals(3)]
            }]
        }
        test_case = {
            "bar": {"baz":2}
        }
        assert validate(optional_validation, test_case)[0]

    def test_contains_validator(self):
        validation = {
            "foo": [Required, Contains("1")],
            "qux": [Required, Not(Contains("1"))]
        }
        test_case_list = {
            "foo": ["1", "2", "3"],
            "qux": ["2", "3", "4"]
        }
        test_case_dict = {
            "foo": {"1": "one", "2": "two"},
            "qux": {"2": "two", "3": "three"}
        }
        test_case_substring = {
            "foo": "test1case",
            "qux": "barbaz"
        }
        assert validate(validation, test_case_list)[0]
        assert validate(validation, test_case_dict)[0]
        assert validate(validation, test_case_substring)[0]

    def test_length_validator(self):
        passes = {
            "foo": [Required, Length(5), Length(1, maximum=5)],
            "bar": [Required, Length(0, maximum=10)]
        }
        fails = {
            "foo": [Required, Length(8), Length(1, maximum=11)],
            "bar": [Required, Length(0, maximum=3)]
        }
        test_case = {
            "foo": "12345",
            "bar": "12345",
        }
        assert validate(passes, test_case)[0]
        assert not validate(fails, test_case)[0]

