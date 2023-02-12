import unittest
from unittest import mock
import PyJoi
from PyJoi import Exceptions
import typing
from .. import util

class TestSchema(unittest.TestCase):
    def test_name_inference(self):
        m = mock.Mock()
        s = PyJoi.dict("s",
            a=m
        )
        self.assertEqual(m._name,"a")

    def test_optional(self):
        m = util.SchemaMock()
        s = PyJoi.dict("s",
            value=m
        )
        with self.assertRaises(Exceptions.MissingObjectException):
            s.validate(None)
        self.assertIsNone(s.optional().validate(None))

    def test_unknown_keys(self):
        self.assertIsNone(PyJoi.dict("schema",
            a=PyJoi.int().optional()
        ).validate({"b": 12})["a"])
        class TestTuple(typing.NamedTuple):
            a: int
        self.assertEqual(PyJoi.dict[TestTuple]("schema",TestTuple,a=PyJoi.int()).validate({"a": 2,"b": 12}).a,2)
    
    def test_error_name_prepend(self):
        sm = util.SchemaMock()
        sm.validate.side_effect = util.TestException("value","test")
        with self.assertRaises(util.TestException)as cm:
            PyJoi.dict("schema",
                value=sm
            ).validate({"value": "value"})
        self.assertEqual(cm.exception.name,"schema.value")

    def test_empty_schema_fails(self):
        with self.assertRaises(ValueError):
            PyJoi.dict("s").validate({"a": 1})

    def test_requires_dict(self):
        with self.assertRaises(Exceptions.NotAnObjectException):
            PyJoi.dict("S",a=util.SchemaMock()).validate(1)

    def test_union(self):
        m1 = util.SchemaMock(return_value=2)
        m2 = util.SchemaMock()
        schema = PyJoi.dict("schema",key=m1).union(m2)
        schema.validate({"key": 2})
        m1.validate.assert_called_once_with(2)
        m2.validate.assert_not_called()
        m1.reset_mock()
        m1.validate.side_effect = util.TestException("key","some error")
        m2.validate.return_value={"key": 2}
        data = {"key": 2}
        schema.validate({"key": 2})
        m1.validate.assert_called_once_with(2)
        m2.validate.assert_called_once_with(data)
