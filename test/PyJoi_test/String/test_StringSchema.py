import unittest
import PyJoi
from PyJoi.Primitive import String
import typing

class TestStringSchema(unittest.TestCase):

    def test_optional_accepts_none(self):
        class testtup(typing.NamedTuple):
            value: typing.Optional[str]
        s = PyJoi.Schema[testtup]("s",value=PyJoi.Schema("value").string().optional()).optional()
        validated = s.validate({})
        self.assertIsNone(validated)
