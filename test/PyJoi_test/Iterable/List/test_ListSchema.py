import unittest
import PyJoi
from PyJoi.Iterable import Exceptions as StreamExceptions
from .. import Common
import typing

def list_schema_factory(self: "ListSchemaTest", name: typing.Optional[str] = None):
    return PyJoi.list(name=name)

def list_factory(self: "ListSchemaTest", iter: typing.Iterable)->typing.List:
    return list(iter)

class ListSchemaTest(Common.IterableSchemaTest):
    @classmethod
    def setUpClass(cls):
        cls.schema_factory = list_schema_factory
        cls.instance_factory = list_factory
        cls.assertion = cls.assertListEqual