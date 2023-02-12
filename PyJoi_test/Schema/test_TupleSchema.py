import unittest
import PyJoi
from unittest import mock
from .. import util
import typing
from PyJoi import Exceptions

class TestTupleSchema(unittest.TestCase):
    def test_name_attachment(self):
        m1 = util.SchemaMock()
        m2 = util.SchemaMock()
        m3 = util.SchemaMock()
        PyJoi.tuple(m1,m2,m3,name="schema")
        self.assertEqual(m1._name,"0")
        self.assertEqual(m2._name,"1")
        self.assertEqual(m3._name,"2")

    def test_calls_validate(self):
        m1 = util.SchemaMock(validate=mock.Mock(return_value=1))
        m2 = util.SchemaMock(validate=mock.Mock(return_value=2))
        schema = PyJoi.tuple[typing.Tuple[int,int]](m1,m2,name="schema")
        output = schema.validate([1, 2])
        self.assertTupleEqual(output,(1,2))
        m1.validate.assert_called_once_with(1)
        m2.validate.assert_called_once_with(2)

    def test_error_name_prepend(self):
        m1 = util.SchemaMock(validate=mock.Mock(side_effect=util.TestException("name","message")))
        schema = PyJoi.tuple(m1,name="schema")
        with self.assertRaises(util.TestException) as cm:
            schema.validate((1,))
        self.assertEqual(cm.exception.name,"schema.name")

    def test_requires_iterable(self):
        with self.assertRaises(Exceptions.NotAnObjectException):
            PyJoi.tuple(util.SchemaMock(),name="schema").validate(2)

    def test_optional(self):
        self.assertIsNone(PyJoi.tuple(util.SchemaMock(),name="schema").optional().validate(None))
        with self.assertRaises(Exceptions.MissingElementException):
            PyJoi.tuple(util.SchemaMock(),name="schema").validate(None)
    
    def test_length_requirement(self):
        schema = PyJoi.tuple(util.SchemaMock(),util.SchemaMock(),name="schema")
        with self.assertRaises(Exceptions.TupleWrongLengthException):
            schema.validate((1,))
        with self.assertRaises(Exceptions.TupleWrongLengthException):
            schema.validate((1, 2, 3))
        schema.validate((1,2))

    def test_relative_resolution(self):
        validate = mock.Mock()
        m1 = util.SchemaMock(validate=validate)
        m2 = util.SchemaMock(validate=validate)
        m2._add_ref(PyJoi.Ref("0"))
        schema = PyJoi.tuple(m1,m2,name="schema")
        schema.validate((1,2))
        self.assertListEqual([x[0][0] for x in validate.call_args_list],[1,2])
        self.assertIs(m2._depends_on[PyJoi.Ref("0")],validate.return_value)
        validate.reset_mock()

        m1 = util.SchemaMock(validate=validate)
        m1._add_ref(PyJoi.Ref("1"))
        m2 = util.SchemaMock(validate=validate)
        schema = PyJoi.tuple(m1,m2,name="schema")
        schema.validate((2, 1))
        self.assertListEqual([x[0][0] for x in validate.call_args_list],[1,2])
        validate.reset_mock()

        m1 = util.SchemaMock(validate=validate)
        m1._add_ref(PyJoi.Ref("1.0"))
        m2 = util.SchemaMock(validate=validate)
        schema = PyJoi.tuple(m1,PyJoi.tuple(m2),name="schema")
        schema.validate((2,(1,)))
        self.assertListEqual([x[0][0] for x in validate.call_args_list],[1,2])


    def test_absolute_resolution(self):
        validate = mock.Mock()
        m1 = util.SchemaMock(validate=validate)
        m2 = util.SchemaMock(validate=validate)
        m1._add_ref(PyJoi.Ref(".1"))
        schema = PyJoi.tuple(PyJoi.tuple(m1,name="inner_schema"),m2,name="schema")
        schema.validate(((2,),1))
        self.assertListEqual([x[0][0] for x in validate.call_args_list],[1,2])
        validate.reset_mock()

        m1 = util.SchemaMock(validate=validate)
        m2 = util.SchemaMock(validate=validate)
        m2._add_ref(PyJoi.Ref(".0.0"))
        schema = PyJoi.tuple(PyJoi.tuple(m1,name="inner_schema"),m2,name="schema")
        schema.validate(((1,),2))
        self.assertListEqual([x[0][0] for x in validate.call_args_list],[1,2])
