import unittest
import PyJoi
from .. import Common
import typing
from PyJoi.Stream.Set import Exceptions as SetExceptions

def set_schema_factory(self: "SetSchemaTest", name: typing.Optional[str] = None):
    return PyJoi.set(name=name)

def set_factory(self: "SetSchemaTest", iter: typing.Iterable)->typing.Set:
    return set(iter)

class SetSchemaTest(Common.StreamSchemaTest):
    @classmethod
    def setUpClass(cls):
        cls.schema_factory = set_schema_factory
        cls.instance_factory = set_factory
        cls.assertion = cls.assertSetEqual

    def test_relaxed(self):
        Schema = PyJoi.set()
        s = Schema.validate([1,1,2])
        self.assertSetEqual(s,{1,2})
    
    def test_enforced(self):
        Schema = PyJoi.set().enforced()
        with self.assertRaises(SetExceptions.DuplicateException):
            Schema.validate([1,1,2])