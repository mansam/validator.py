from validator import *

class TestValidator(object):

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
            "test_range":   [Not(Range(1, 10))]
        }
        test_case = {
            "test_truthy": False,
            "test_equals": "two",
            "test_not_not": True,
            "test_in": "three",
            "test_range": 11
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

    def test_classy_validator(self):
        validator = {
            "classy": [Required, Classy(unicode)],
            "subclassy": [Required, Classy(basestring)],
            "not_classy": [Required, Not(Classy(unicode))],
            "not_subclassy": [Required, Not(Classy(basestring))]
        }
        test_case = {
            "classy": u"unicode_string",
            "subclassy": u"unicode_string",
            "not_classy": r'raw_string',
            "not_subclassy": 3
        }
        assert validate(validator, test_case)[0]