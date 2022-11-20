import unittest
import PyJoi
from PyJoi.Primitive.String import Exceptions
from PyJoi.Primitive import Exceptions as PrimitiveExceptions

class TestStringSchema(unittest.TestCase):
    def test_optional(self):
        self.assertIsNone(PyJoi.Schema().string().optional().validate(None))
        with self.assertRaises(Exceptions.MissingStringException):
            PyJoi.Schema().string().validate(None)

    def test_rejects_non_string(self):
        with self.assertRaises(Exceptions.NotAStringException):
            PyJoi.Schema().string().validate(1)

    def test_length_bounds(self):
        s = PyJoi.Schema().string().max_len(3)
        self.assertEqual(s.validate("hi"),"hi")
        with self.assertRaises(Exceptions.TooLongException):
            s.validate("hello")
        s = PyJoi.Schema().string().min_len(3)
        self.assertEqual(s.validate("hello"),"hello")
        with self.assertRaises(Exceptions.TooShortException):
            s.validate("hi")
        s = PyJoi.Schema().string().len(3)
        self.assertEqual(s.validate("cal"),"cal")
        with self.assertRaises(Exceptions.NonMatchingLengthException):
            s.validate("hi")
        with self.assertRaises(Exceptions.NonMatchingLengthException):
            s.validate("hello")

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

    def test_hex(self):
        s = PyJoi.Schema().string().hex()
        self.assertEqual(s.validate(b'\x00\xef'.hex()),b'\x00\xef'.hex())
        with self.assertRaises(Exceptions.NotHexException):
            s.validate('hi')
    
    def test_whitelist_regex(self):
        s = PyJoi.Schema().string().whitelist_pattern(r"a.")
        self.assertEqual(s.validate("ax"),"ax")
        with self.assertRaises(Exceptions.NoWhiteListException):
            s.validate("bx")
    
    def test_blacklist_regex(self):
        s = PyJoi.Schema().string().blacklist_pattern(r"a.")
        self.assertEqual(s.validate("by"),"by")
        with self.assertRaises(Exceptions.MatchesBlackistException):
            s.validate("ax")