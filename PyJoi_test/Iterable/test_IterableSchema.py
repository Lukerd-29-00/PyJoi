import PyJoi
from . import Common
import typing

def schema_factory(self: "IterableSchemaTest", name: typing.Optional[str] = None):
    return PyJoi.iterable(name=name)

def list_factory(self: "IterableSchemaTest", iter: typing.Iterable)->typing.List:
    return list(iter)

class IterableSchemaTest(Common.IterableSchemaTest):
    @classmethod
    def setUpClass(cls):
        cls.schema_factory = schema_factory
        cls.instance_factory = list_factory
        cls.assertion = cls.assertListEqual