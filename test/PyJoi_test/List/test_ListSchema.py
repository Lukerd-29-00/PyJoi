import unittest
import PyJoi
from PyJoi.Primitive.Int import Exceptions as IntExceptions
from PyJoi.List import Exceptions as ListExceptions

class ListSchemaTest(unittest.TestCase):

    def test_has(self):
        Schema = PyJoi.Schema().list().has(PyJoi.Schema().int())
        s = Schema.validate([1,"2"])
        self.assertListEqual(s,[1,"2"])
        with self.assertRaises(ListExceptions.RequiredItemNotFound):
            Schema.validate(["2","3","4"])

    def test_matches(self):
        Schema = PyJoi.Schema("lst").list().matches(PyJoi.Schema().int())
        s = Schema.validate([1,2])
        self.assertListEqual(s,[1,2])
        with self.assertRaises(IntExceptions.NotAnIntException) as cm:
            Schema.validate([1,"2"])
        self.assertEqual(cm.exception.name,"lst") #Make sure the name of the anonymous schema is replaced with the list schema's name.

    def test_matches_refs(self):
        Schema = PyJoi.Schema("schema",
            lst=PyJoi.Schema().list().matches(PyJoi.Schema().int().max(PyJoi.Ref("max"))), #We can reference 'max' directly because any non-object schemas in a list act as though they were elements of the list's parent for referencing purposes.
            max=PyJoi.Schema().int()
        )
        s = Schema.validate({"max": 12, "lst": [11, 12, 10, 9]})
        self.assertEqual(s.max,12)
        self.assertListEqual(s.lst,[11,12,10,9])
        with self.assertRaises(IntExceptions.InvalidSizeException):
            Schema.validate({"max": -1, "lst": [11, 12, 10, 9]})



