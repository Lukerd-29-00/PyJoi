import unittest
import typing
from unittest import mock
import unittest
import abc
from PyJoi import Primitive
from PyJoi import Exceptions
from .. import util
from PyJoi.Primitive import Exceptions as PrimitiveExceptions
import PyJoi

T = typing.TypeVar("T",bound=Primitive.PrimitiveSchema)

class SchemaFactory(typing.Generic[T],typing.Protocol):
    def __call__(self, name: typing.Optional[str] = None)->T:
        pass

I = typing.TypeVar("I") #Type required for an input to be valid (assuming non-optional). For example, this would be int for an int schema test.
O = typing.TypeVar("O") #Type output by the schema.
S = typing.TypeVar("S",bound=Primitive.PrimitiveSchema)

class PrimitiveSchemaTest(typing.Generic[I,O,S],unittest.TestCase,abc.ABC):
    instance1: I
    instance2: I #Needs two in order to test the whitelist method. Ensure instance1 != instance2.
    output_instance: O #The expected output value of validate(instance1)
    noninstance: any #Can be anything not of type I.
    custom_fail: I
    custom_success: I

    @abc.abstractmethod
    def schema_factory(self, name: typing.Optional[str] = None)->S:
        pass

    def test_correct_input_type(self):
        self.assertEqual(self.schema_factory().validate(self.instance1),self.output_instance)
        with self.assertRaises(Exceptions.InvalidTypeException):
            self.schema_factory().validate(self.noninstance)

    def test_optional(self):
        with self.assertRaises(Exceptions.MissingElementException):
            self.schema_factory().validate(None)
        self.assertIsNone(self.schema_factory().optional().validate(None))

    def test_union(self):
        mk = util.SchemaMock(validate=mock.Mock(return_value=self.noninstance))
        schema = self.schema_factory().union(mk)
        self.assertEqual(schema.validate(self.instance1),self.output_instance)
        mk.validate.assert_not_called()
        self.assertIs(schema.validate(self.noninstance),self.noninstance)
        mk.validate.assert_called_once_with(self.noninstance)

    def test_whitelist(self):
        schema = self.schema_factory().whitelist(self.instance1)
        self.assertEqual(schema.validate(self.instance1),self.output_instance)
        with self.assertRaises(PrimitiveExceptions.NonWhiteListedValueException):
            schema.validate(self.instance2)

    def test_blacklist(self):
        schema = self.schema_factory()
        self.assertEqual(schema.validate(self.instance1),self.output_instance)
        with self.assertRaises(PrimitiveExceptions.BlackListedValueException):
            schema.blacklist(self.instance1).validate(self.instance1)

    @abc.abstractmethod
    def _custom_check(self, name: str, x: I)->O:
        pass

    @abc.abstractmethod
    def _custom_check_ref(self, name: str, x: I, y: I)->O: #Function that returns x if x = custom_succeed an y = custom_fail, and raises TestException for the other way around.
        pass

    def test_custom(self):            
        s = self.schema_factory().custom(self._custom_check)
        self.assertEqual(s.validate(self.custom_success),self.custom_success)
        with self.assertRaises(util.TestException):
            s.validate(self.custom_fail)
            
        s = PyJoi.dict("s",
            x=self.schema_factory().custom(self._custom_check_ref,PyJoi.Ref[I]("y")),
            y=self.schema_factory()
        )
        self.assertEqual(s.validate({"x": self.custom_success, "y": self.custom_fail})["x"],self.custom_success)
        with self.assertRaises(util.TestException):
            s.validate({"x": self.custom_fail, "y": self.custom_success})