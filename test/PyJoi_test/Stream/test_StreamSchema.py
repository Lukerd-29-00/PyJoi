import unittest
import PyJoi
from PyJoi.Primitive.Numeric import Exceptions as NumericExceptions
from PyJoi.Stream import Exceptions as StreamExceptions
from .. import util

def is_int(value: any):
    if isinstance(value,int):
        return value
    else:
        raise util.TestException(None, "not an int")

class StreamSchemaTest(unittest.TestCase):
    def test_has(self):
        Schema = PyJoi.stream().has(util.SchemaMock(validate=is_int))
        s = Schema.validate([1,"2"])
        self.assertListEqual(list(s),[1,"2"])
        with self.assertRaises(StreamExceptions.RequiredItemNotFound):
            set(Schema.validate(["2","3","4"]))

    def test_matches(self):
        Schema = PyJoi.stream("lst").matches(util.SchemaMock(validate=is_int))
        s = Schema.validate([1,2])
        self.assertListEqual(list(s),[1,2])
        with self.assertRaises(util.TestException) as cm:
            set(Schema.validate([1,"2"]))
        self.assertEqual(cm.exception.name,"lst") #Make sure the name of the anonymous schema is replaced with the list schema's name.

    def test_matches_refs(self):
        num = util.SchemaMock()
        R = PyJoi.Ref[int]("max") #We can reference this key directly because a schema in .matches is treated as though it was at the level of the enclosing steam schema.
        num._depends_on[R] = None
        R._schema = num
        def is_less(value: int)->int:
            if value <= R.value:
                return value
            else:
                raise util.TestException(None,"too large")
        num.validate = is_less
        mx = util.SchemaMock()
        mx.validate.return_value = 12
        Schema = PyJoi.Schema("schema",
            lst=PyJoi.stream().matches(num), #We can reference 'max' directly because any non-object schemas in a list act as though they were elements of the list's parent for referencing purposes.
            max=mx
        )
        s = Schema.validate({"max": 12, "lst": [11, 12, 10, 9]})
        self.assertEqual(s.max,12)
        self.assertListEqual(list(s.lst),[11,12,10,9])
        mx.validate.return_value = -1
        with self.assertRaises(util.TestException):
            next(Schema.validate({"max": -1, "lst": [11, 12, 10, 9]}).lst)