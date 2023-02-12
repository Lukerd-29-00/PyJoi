import PyJoi
from PyJoi.Primitive.Str import Exceptions
from PyJoi.Primitive.Str import StrSchema
from .. import Common
import typing
from ... import util

class TestStrSchema(Common.PrimitiveSchemaTest[str,str,StrSchema.StrSchema]):
    instance1 = "hello"
    instance2 = "world"
    output_instance = "hello"
    noninstance = 2
    custom_fail = "hello"
    custom_success = "ab"

    def schema_factory(self, name: typing.Optional[str] = None)->StrSchema.StrSchema[str]:
        return PyJoi.str()

    def _custom_check(self, name: str, x: str) -> str:
        if len(x) < 3:
            return x
        else:
            raise util.TestException(name,f"{x} is at least 3 characters.")

    def _custom_check_ref(self, name: str, x: str, y: str) -> str:
        if len(x) < len(y):
            return x
        else:
            raise util.TestException(name,f"{x} is at least {len(y)} characters.")

    def test_length_bounds(self):
        s = PyJoi.str().max_len(3)
        self.assertEqual(s.validate("hi"),"hi")
        with self.assertRaises(Exceptions.NonMatchingLengthException):
            s.validate("hello")
        s = PyJoi.str().min_len(3)
        self.assertEqual(s.validate("hello"),"hello")
        with self.assertRaises(Exceptions.NonMatchingLengthException):
            s.validate("hi")
        s = PyJoi.str().len(3)
        self.assertEqual(s.validate("cal"),"cal")
        with self.assertRaises(Exceptions.NonMatchingLengthException):
            s.validate("hi")
        with self.assertRaises(Exceptions.NonMatchingLengthException):
            s.validate("hello")

    def test_hex(self):
        s = PyJoi.str().hex()
        self.assertEqual(s.validate(b'\x00\xef'.hex()),b'\x00\xef'.hex())
        with self.assertRaises(Exceptions.NoWhiteListException):
            s.validate('hi')
    
    def test_whitelist_regex(self):
        s = PyJoi.str().whitelist_pattern(r"a.")
        self.assertEqual(s.validate("ax"),"ax")
        with self.assertRaises(Exceptions.NoWhiteListException):
            s.validate("bx")
    
    def test_blacklist_regex(self):
        s = PyJoi.str().blacklist_pattern(r"a.")
        self.assertEqual(s.validate("by"),"by")
        with self.assertRaises(Exceptions.MatchesBlackistException):
            s.validate("ax")

    def test_padded_base64(self):        
        s = PyJoi.str().base64()
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
        s = PyJoi.str().base64().unpadded()
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

    def test_encoding(self):
        s = PyJoi.str().encoding("utf-8")
        self.assertEqual(s.validate(b"abc"),'abc')
        self.assertEqual(s.validate("abc"),"abc")
        with self.assertRaises(Exceptions.NotAStringException):
            PyJoi.str().validate(b"abc")