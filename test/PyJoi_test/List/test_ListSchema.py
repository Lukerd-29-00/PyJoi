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

    def test_list_matches(self):
        Schema = PyJoi.Schema().list().matches(PyJoi.Schema().int())
        s = Schema.validate([1,2])
        self.assertListEqual(s,[1,2])
        with self.assertRaises(IntExceptions.NotAnIntException):
            Schema.validate([1,"2"])

