import unittest
import PyJoi
from PyJoi import Exceptions
from PyJoi.Primitive.Int import Exceptions as IntExceptions
import typing

class TestSchema(unittest.TestCase):
    def test_name_inference(self):
        s = PyJoi.Schema("s",
            a=PyJoi.int()
        )
        self.assertEqual(s._fields["a"]._name,"a")

    def test_optional(self):
        s = PyJoi.Schema("s",
            value=PyJoi.int().optional()
        )
        with self.assertRaises(Exceptions.MissingObjectException):
            s.validate(None)
        with self.assertRaises(Exceptions.EmptyObjectException):
            s.validate({"value": None})
        self.assertIsNone(s.optional().validate(None))
        self.assertIsNone(s.validate({"value": None}))

    def test_unknown_keys(self):
        self.assertIsNone(PyJoi.Schema("schema",
            a=PyJoi.int().optional()
        ).optional().validate({"b": 12}))
        with self.assertRaises(Exceptions.EmptyObjectException) as cm:
            PyJoi.Schema("schema",
                a=PyJoi.int().optional()
            ).validate({"b": 12})
        class TestTuple(typing.NamedTuple):
            a: int
        self.assertEqual(PyJoi.Schema[TestTuple]("schema",a=PyJoi.int()).validate({"a": 2,"b": 12}).a,2)
        self.assertEqual(cm.exception.name,"schema")
    
    def test_error_name_prepend(self):
        with self.assertRaises(IntExceptions.NotAnIntException)as cm:
            PyJoi.Schema("schema",
                value=PyJoi.int()
            ).validate({"value": "value"})
        self.assertEqual(cm.exception.name,"schema.value")

    def test_kwargs_needs_name(self):
        with self.assertRaises(ValueError):
            PyJoi.Schema(a=PyJoi.int()).validate({"a": 1})

    def test_empty_schema_fails(self):
        with self.assertRaises(ValueError):
            PyJoi.Schema("s").validate({"a": 1})

    def test_requires_dict(self):
        with self.assertRaises(Exceptions.NotAnObjectException):
            PyJoi.Schema("S",a=PyJoi.int()).validate(1)