import unittest
import PyJoi
from PyJoi.Stream import Exceptions as StreamExceptions
from .. import util

def is_int(value: any):
    if isinstance(value,int):
        return value
    else:
        raise util.TestException(None, "not an int")

class ListSchemaTest(unittest.TestCase):
    def test_has(self):
        Schema = PyJoi.list().has(util.SchemaMock(validate=is_int))
        s = Schema.validate([1,"2"])
        self.assertListEqual(s,[1,"2"])
        with self.assertRaises(StreamExceptions.RequiredItemNotFound):
            Schema.validate(["2","3","4"])

    def test_matches(self):
        Schema = PyJoi.list("lst").matches(util.SchemaMock(validate=is_int))
        s = Schema.validate([1,2])
        self.assertListEqual(s,[1,2])
        with self.assertRaises(util.TestException) as cm:
            Schema.validate([1,"2"])
        self.assertEqual(cm.exception.name,"lst") #Make sure the name of the anonymous schema is replaced with the list schema's name.

    def test_matches_refs(self):
        num = util.SchemaMock()
        R = PyJoi.Ref[int]("max")
        num._depends_on[R] = None
        R._schema = num
        def is_less(value: int)->int:
            if value <= R.value:
                return value
            else:
                raise util.TestException(None,"too large")
        num.validate = is_less
        Schema = PyJoi.Schema("schema",
            lst=PyJoi.list().matches(num),
            max=PyJoi.int()
        )
        s = Schema.validate({"max": 12, "lst": [11, 12, 10, 9]})
        self.assertEqual(s.max,12)
        self.assertListEqual(s.lst,[11,12,10,9])
        with self.assertRaises(util.TestException):
            Schema.validate({"max": -1, "lst": [11, 12, 10, 9]})