import unittest
import PyJoi
import typing

class testtup(typing.NamedTuple):
    value: typing.Optional[str]

class TestStringSchema(unittest.TestCase):

    def test_optional_accepts_none(self):
        s = PyJoi.Schema[testtup]("s",value=PyJoi.Schema("value").string().optional()).optional()
        validated = s.validate(None)
        self.assertIsNone(validated)

    def test_optional_accepts_empty(self):
        s = PyJoi.Schema[testtup]("s",value=PyJoi.Schema("value").string().optional()).optional()
        validated = s.validate(None)
        self.assertIsNone(validated)
