import PyJoi
from PyJoi.Primitive.Numeric.Int import IntSchema
import typing
from PyJoi.Primitive.Numeric import Exceptions as NumericExceptions
from PyJoi.Primitive.Numeric.Int import Exceptions as IntExceptions
from .. import Common
from .... import util

class TestIntSchema(Common.TestNumericSchema[int,IntSchema.IntSchema]):
    instance2 = 2
    custom_fail = 6
    custom_success = 4

    def test_correct_input_type(self):
        super(TestIntSchema,self).test_correct_input_type()
        schema = PyJoi.int()
        self.assertIs(schema.validate(5.0),5)
        with self.assertRaises(IntExceptions.NotAnIntException):
            schema.validate(5.1)

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
            TestTuple,
            value=PyJoi.int().multiple(PyJoi.Ref("base")),
            base=PyJoi.int()
        )
        tup = s.validate({"value": 9, "base": 3})
        self.assertEqual(tup.value,9)
        self.assertEqual(tup.base,3)
        with self.assertRaises(IntExceptions.NonMultipleException):
            s.validate({"value": 1, "base": 3})

    def test_port(self):
        s = PyJoi.int().port()
        self.assertEqual(s.validate(0),0)
        self.assertEqual(s.validate(65535),65535)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(65536)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(-1)