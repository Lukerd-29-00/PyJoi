import unittest
import PyJoi
from PyJoi.Primitive.String import Exceptions
from PyJoi.Primitive import Exceptions as PrimitiveExceptions

class TestStringSchema(unittest.TestCase):
    def test_optional_accepts_missing(self):
        value = PyJoi.Schema().string().optional().validate(None)
        self.assertIsNone(value)
        
    def test_required_rejects_missing(self):
        with self.assertRaises(Exceptions.MissingStringException) as cm:
            PyJoi.Schema().string().validate(None)

    def test_too_short_fails(self):
        with self.assertRaises(Exceptions.TooShortException):
            PyJoi.Schema().string().min_len(3).validate('hi')

    def test_too_long_fails(self):
        with self.assertRaises(Exceptions.TooLongException):
            PyJoi.Schema().string().max_len(3).validate("hello")

    def test_inside_range_accepted(self):
        value = PyJoi.Schema().string().min_len(3).max_len(10).validate("hello")
        self.assertEqual(value,"hello")

    def test_accepts_in_whitelist(self):
        value = PyJoi.Schema().string().whitelist("hi").validate("hi")
        self.assertEqual(value,"hi")
        s = PyJoi.Schema().string().whitelist(["hi","hello"])
        self.assertEqual(s.validate("hi"),"hi")
        self.assertEqual(s.validate("hello"),"hello")

    def test_whitelist_rejects_outsiders(self):
        with self.assertRaises(PrimitiveExceptions.NonWhiteListedValueException):
            PyJoi.Schema().string().whitelist("hi").validate("hello")
        s = PyJoi.Schema().string().whitelist(["hi", "hello"])
        with self.assertRaises(PrimitiveExceptions.NonWhiteListedValueException):
            s.validate("yes")

    def test_blacklist_accepts_outsiders(self):
        value = PyJoi.Schema().string().blacklist("hi").validate("hello")
        self.assertEqual(value,"hello")
        value = PyJoi.Schema().string().blacklist(["hi", "hello"]).validate("yes")
        self.assertEqual(value,"yes")

    def test_blacklist_rejects_outsiders(self):
        with self.assertRaises(PrimitiveExceptions.BlackListedValueException):
            PyJoi.Schema().string().blacklist("hi").validate("hi")
        s = PyJoi.Schema().string().blacklist(["hi","hello"])
        with self.assertRaises(PrimitiveExceptions.BlackListedValueException):
            s.validate("hi")
        with self.assertRaises(PrimitiveExceptions.BlackListedValueException):
            s.validate("hello")


    

    

    



    
