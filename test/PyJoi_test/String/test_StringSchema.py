import unittest
import PyJoi
from PyJoi.Primitive.String import Exceptions
from PyJoi.Primitive import Exceptions as PrimitiveExceptions
from PyJoi import Exceptions as TopExceptions
class TestStringSchema(unittest.TestCase):
    def test_optional(self):
        self.assertIsNone(PyJoi.Schema().string().optional().validate(None))
        with self.assertRaises(TopExceptions.MissingElementException):
            PyJoi.Schema().string().validate(None)

    def test_rejects_non_string(self):
        with self.assertRaises(Exceptions.NotAStringException):
            PyJoi.Schema().string().validate(1)

    def test_length_bounds(self):
        s = PyJoi.Schema().string().max_len(3)
        self.assertEqual(s.validate("hi"),"hi")
        with self.assertRaises(Exceptions.NonMatchingLengthException):
            s.validate("hello")
        s = PyJoi.Schema().string().min_len(3)
        self.assertEqual(s.validate("hello"),"hello")
        with self.assertRaises(Exceptions.NonMatchingLengthException):
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
        with self.assertRaises(Exceptions.NoWhiteListException):
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

    def test_padded_base64(self):
        s = PyJoi.Schema().string().base64()
        self.assertEqual(s.validate("AB/+"),"AB/+")
        self.assertEqual(s.validate("ABCDaA=="),"ABCDaA==")
        self.assertEqual(s.validate("ABCDaXQ="),"ABCDaXQ=")
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate('Èb==') #Sanity check
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate("ABCDA") #Check that a string of length 1 mod 4 is rejected.
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate("-BCDaXQ=") #Check that - is not allowed.
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate("_BCDaXQ=") #Check that _ is not allowed.
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate("ABCDab") #Check that padding is required.
        self.assertEqual(s.urlsafe().validate("AB-_"),"AB-_")
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate("+B-_") #Check that + is not allowed.
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate("/B-_") #Check that / is not allowed.
        
    def test_unpadded_base64(self):
        s = PyJoi.Schema().string().base64().unpadded()
        self.assertEqual(s.validate("AB/+"),"AB/+")
        self.assertEqual(s.validate("ABCDaA"),"ABCDaA")
        self.assertEqual(s.validate("ABCDaXQ"),"ABCDaXQ")
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate('Èw') #Basic sanity check
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate("ABCDA") #Check that a string of length 1 mod 4 is rejected.
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate("-BCDAA") #Test that - is not allowed
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate("_BCDAA") #Test that _ is not allowed
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate("ABCDaA==") #Test that padding is not allowed
        self.assertEqual(s.urlsafe().validate("AB-_"),"AB-_")
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate("/BCD")
        with self.assertRaises(Exceptions.InvalidBase64Exception):
            s.validate("+BCD")