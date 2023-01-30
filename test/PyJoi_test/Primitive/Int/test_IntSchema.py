import unittest
import PyJoi
from PyJoi.Primitive.Numeric.Int import IntSchema
import typing
from PyJoi.Primitive.Numeric import Exceptions as NumericExceptions
from PyJoi.Primitive.Numeric.Int import Exceptions as IntExceptions
from .. import Common
from ... import util

class TestIntSchema(Common.PrimitiveSchemaTest[int,int,IntSchema.IntSchema]):
    instance1 = 1
    instance2 = 2
    output_instance = 1
    noninstance = "1"
    custom_fail = 6
    custom_success = 4

    def schema_factory(self, name: typing.Optional[str] = None)->"IntSchema[int]":
        return PyJoi.int(name)

    def _custom_check(self, name: str, x: int) -> int:
        if x < 5:
            return x
        else:
            raise util.TestException(name,f"{x} is not less than 5.")

    def _custom_check_ref(self, name: str, x: int, y: int) -> int:
        if x < y:
                return x
        else:
            raise util.TestException(name,f"{x} is not less than {y}.")

    def test_multiple(self):
        s = PyJoi.int().multiple(3)
        self.assertEqual(s.validate(3),3)
        self.assertEqual(s.validate(6),6)
        self.assertEqual(s.validate(3*2**15),3*2**15)
        with self.assertRaises(IntExceptions.NonMultipleException):
            s.validate(4)
        class TestTuple(typing.NamedTuple):
            value: int
            base: int
        s = PyJoi.Schema[TestTuple]("s",
            value=PyJoi.int().multiple(PyJoi.Ref("base")),
            base=PyJoi.int()
        )
        tup = s.validate({"value": 9, "base": 3})
        self.assertEqual(tup.value,9)
        self.assertEqual(tup.base,3)
        with self.assertRaises(IntExceptions.NonMultipleException):
            s.validate({"value": 1, "base": 3})

    def test_max(self):
        s = PyJoi.int().max(3)
        self.assertEqual(s.validate(3),3)
        self.assertEqual(s.validate(-1),-1)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(4)
        class TestTuple(typing.NamedTuple):
            value: int
            value2: int
        s = PyJoi.Schema[TestTuple]("s",
            value=PyJoi.int().max(PyJoi.Ref("value2")),
            value2=PyJoi.int()
        )
        tup = s.validate({"value": 1, "value2": 1})
        self.assertEqual(tup.value,1)
        self.assertEqual(tup.value2,1)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate({"value": 3, "value2": 2})
    
    def test_min(self):
        s = PyJoi.int().min(3)
        self.assertEqual(s.validate(3),3)
        self.assertEqual(s.validate(2**16),2**16)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(2)
        class TestTuple(typing.NamedTuple):
            value: int
            value2: int
        s = PyJoi.Schema[TestTuple]("s",
            value=PyJoi.int().min(PyJoi.Ref("value2")),
            value2=PyJoi.int()
        )
        tup = s.validate({"value": 3, "value2": 2})
        self.assertEqual(tup.value,3)
        self.assertEqual(tup.value2,2)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate({"value": 1,"value2": 2})

    def test_postiive(self):
        s = PyJoi.int().positive()
        self.assertEqual(s.validate(0),0)
        self.assertEqual(s.validate(25),25)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(-3)

    def test_negative(self):
        s = PyJoi.int().negative()
        self.assertEqual(s.validate(-10),-10)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(0)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(35)
    
    def test_port(self):
        s = PyJoi.int().port()
        self.assertEqual(s.validate(0),0)
        self.assertEqual(s.validate(65535),65535)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(65536)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(-1)