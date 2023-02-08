from .. import Common
import typing
from PyJoi.Primitive.Numeric import NumericSchema, Exceptions as NumericExceptions
import PyJoi
from ... import util

O = typing.TypeVar("O",int,float)
S = typing.TypeVar("S",bound=NumericSchema.NumericSchema)

class TestNumericSchema(typing.Generic[O,S],Common.PrimitiveSchemaTest[typing.Union[int,float],O,S]):
    instance1 = 5.0
    noninstance = "2"
    output_instance = 5.0 #Either int or float will return something equal to five, even though they are different types.

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

    def test_max(self):
        s = self.schema_factory().max(3)
        self.assertEqual(s.validate(2),2)
        self.assertEqual(s.validate(-1),-1)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(4)
        class TestTuple(typing.NamedTuple):
            value: int
            value2: int
        s = PyJoi.Schema[TestTuple]("s", 
            TestTuple,
            value=PyJoi.int().max(PyJoi.Ref("value2")),
            value2=PyJoi.int()
        )
        tup = s.validate({"value": 0, "value2": 1})
        self.assertEqual(tup.value,0)
        self.assertEqual(tup.value2,1)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate({"value": 3, "value2": 2})
    
    def test_min(self):
        s = self.schema_factory().min(3)
        self.assertEqual(s.validate(4),4)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(2)
        class TestTuple(typing.NamedTuple):
            value: int
            value2: int
        s = PyJoi.Schema[TestTuple]("s",
            TestTuple,
            value=self.schema_factory().min(PyJoi.Ref("value2")),
            value2=self.schema_factory()
        )
        tup = s.validate({"value": 3, "value2": 2})
        self.assertEqual(tup.value,3)
        self.assertEqual(tup.value2,2)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate({"value": 1,"value2": 2})

    def test_postiive(self):
        s = self.schema_factory().positive()
        self.assertEqual(s.validate(25),25)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(-3)

    def test_negative(self):
        s = self.schema_factory().negative()
        self.assertEqual(s.validate(-10),-10)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(0)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(35)
