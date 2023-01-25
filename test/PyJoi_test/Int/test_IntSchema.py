import unittest
import PyJoi
import typing
from PyJoi.Primitive.Int import Exceptions
from PyJoi.Primitive import Exceptions as PrimitiveExceptions
from PyJoi import Exceptions as BaseExceptions

class TestIntSchema(unittest.TestCase):

    def test_optional(self):
        s = PyJoi.Schema().int()
        with self.assertRaises(BaseExceptions.MissingElementException):
            s.validate(None)
        self.assertIsNone(s.optional().validate(None))

    def test_rejects_non_int(self):
        with self.assertRaises(Exceptions.NotAnIntException):
            PyJoi.Schema().int().validate("1")
    
    def test_whitelist(self):
        self.assertEqual(PyJoi.Schema().int().whitelist(1).validate(1),1)
        self.assertEqual(PyJoi.Schema().int().whitelist([1,2]).validate(2),2)
        self.assertEqual(PyJoi.Schema().int().whitelist([1,2]).validate(1),1)
        with self.assertRaises(PrimitiveExceptions.NonWhiteListedValueException):
            PyJoi.Schema().int().whitelist(1).validate(2)
        with self.assertRaises(PrimitiveExceptions.NonWhiteListedValueException):
            PyJoi.Schema().int().whitelist([1,2]).validate(3)

    def test_blacklist(self):
        s = PyJoi.Schema().int().blacklist(1)
        self.assertEqual(s.validate(2),2)
        with self.assertRaises(PrimitiveExceptions.BlackListedValueException):
            s.validate(1)
        s = PyJoi.Schema().int().blacklist([1,2])
        self.assertEqual(s.validate(3),3)
        with self.assertRaises(PrimitiveExceptions.BlackListedValueException):
            s.validate(1)
        with self.assertRaises(PrimitiveExceptions.BlackListedValueException):
            s.validate(2)

    def test_multiple(self):
        s = PyJoi.Schema().int().multiple(3)
        self.assertEqual(s.validate(3),3)
        self.assertEqual(s.validate(6),6)
        self.assertEqual(s.validate(3*2**15),3*2**15)
        with self.assertRaises(Exceptions.NonMultipleException):
            s.validate(4)
        class TestTuple(typing.NamedTuple):
            value: int
            base: int
        s = PyJoi.Schema[TestTuple]("s",
            value=PyJoi.Schema().int().multiple(PyJoi.Ref("base")),
            base=PyJoi.Schema().int()
        )
        tup = s.validate({"value": 9, "base": 3})
        self.assertEqual(tup.value,9)
        self.assertEqual(tup.base,3)
        with self.assertRaises(Exceptions.NonMultipleException):
            s.validate({"value": 1, "base": 3})

    def test_max(self):
        s = PyJoi.Schema().int().max(3)
        self.assertEqual(s.validate(3),3)
        self.assertEqual(s.validate(-1),-1)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate(4)
        class TestTuple(typing.NamedTuple):
            value: int
            value2: int
        s = PyJoi.Schema[TestTuple]("s",
            value=PyJoi.Schema().int().max(PyJoi.Ref("value2")),
            value2=PyJoi.Schema().int()
        )
        tup = s.validate({"value": 1, "value2": 1})
        self.assertEqual(tup.value,1)
        self.assertEqual(tup.value2,1)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate({"value": 3, "value2": 2})
    
    def test_min(self):
        s = PyJoi.Schema().int().min(3)
        self.assertEqual(s.validate(3),3)
        self.assertEqual(s.validate(2**16),2**16)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate(2)
        class TestTuple(typing.NamedTuple):
            value: int
            value2: int
        s = PyJoi.Schema[TestTuple]("s",
            value=PyJoi.Schema().int().min(PyJoi.Ref("value2")),
            value2=PyJoi.Schema().int()
        )
        tup = s.validate({"value": 3, "value2": 2})
        self.assertEqual(tup.value,3)
        self.assertEqual(tup.value2,2)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate({"value": 1,"value2": 2})

    def test_postiive(self):
        s = PyJoi.Schema().int().positive()
        self.assertEqual(s.validate(0),0)
        self.assertEqual(s.validate(25),25)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate(-3)

    def test_negative(self):
        s = PyJoi.Schema().int().negative()
        self.assertEqual(s.validate(-10),-10)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate(0)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate(35)
    
    def test_port(self):
        s = PyJoi.Schema().int().port()
        self.assertEqual(s.validate(0),0)
        self.assertEqual(s.validate(65535),65535)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate(65536)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate(-1)
        s = PyJoi.Schema().int().port_nonadmin()
        self.assertEqual(s.validate(1024),1024)
        self.assertEqual(s.validate(65535),65535)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate(65536)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate(1023)
    
    def test_custom(self):
        def lt_five(name: str, x: int)->int:
            if x < 5:
                return x
            else:
                raise Exceptions.InvalidSizeException(name,f"{x} is not less than 5.")
        s = PyJoi.Schema().int().custom(lt_five)
        self.assertEqual(s.validate(4),4)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate(5)
        def less_than(name: str, x: int, y: int)->int:
            if x < y:
                return x
            else:
                raise Exceptions.InvalidSizeException(name,f"{x} is not less than {y}.")
        s = PyJoi.Schema("s",
            less=PyJoi.Schema().int().custom(less_than,PyJoi.Ref("more")),
            more=PyJoi.Schema().int()
        )
        self.assertEqual(s.validate({"less": 3, "more": 5}).less,3)
        with self.assertRaises(Exceptions.InvalidSizeException):
            s.validate({"less": 5, "more": 5})