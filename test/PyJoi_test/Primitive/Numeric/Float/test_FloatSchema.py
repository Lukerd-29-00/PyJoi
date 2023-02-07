from .. import Common
import typing
from PyJoi.Primitive.Numeric.Float import FloatSchema
from .... import util
import PyJoi
from PyJoi.Primitive.Numeric import Exceptions as NumericExceptions
from PyJoi.Primitive.Numeric.Float import Exceptions as FloatExceptions
from unittest import mock

class TestFloatSchema(Common.TestNumericSchema[float,FloatSchema.FloatSchema]):
    instance2 = 2
    custom_fail = 6.1
    custom_success = 4.56

    def schema_factory(self, name: typing.Optional[str] = None) -> FloatSchema.FloatSchema[float]:
        return PyJoi.float()

    def test_max(self):
        super(TestFloatSchema,self).test_max()
        s = PyJoi.float().max(3.2)
        self.assertEqual(s.validate(3.1),3.1)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(4.3)
    
    def test_min(self):
        super(TestFloatSchema,self).test_min()
        s = PyJoi.float().min(3.2)
        self.assertEqual(s.validate(3.3),3.3)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(2.3)

    def test_postiive(self):
        super(TestFloatSchema,self).test_postiive()
        s = PyJoi.float().positive()
        self.assertEqual(s.validate(25.2),25.2)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(-3.1)

    def test_negative(self):
        super(TestFloatSchema,self).test_negative()
        s = PyJoi.float().negative()
        self.assertEqual(s.validate(-25.2),-25.2)
        with self.assertRaises(NumericExceptions.InvalidSizeException):
            s.validate(3.1)
    
    def test_precision(self):
        s = PyJoi.float().precision(2)
        self.assertEqual(s.validate(2.22),2.22)
        self.assertEqual(s.validate(2.2),2.2)
        with self.assertRaises(FloatExceptions.InvalidPrecisionException):
            s.validate(2.222)
        s = PyJoi.Schema("s",
            precision=util.SchemaMock(validate=mock.Mock(return_value=2)),
            value=PyJoi.float().precision(PyJoi.Ref[int]("precision"))
        )
        v = s.validate({"precision": 2, "value": 2.22})
        self.assertEqual(v.value,2.22)
        with self.assertRaises(FloatExceptions.InvalidPrecisionException):
            s.validate({"precision": 2, "value": 2.222})