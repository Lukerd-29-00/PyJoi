import PyJoi
from . import Common
import typing

def schema_factory(self: "StreamSchemaTest", name: typing.Optional[str] = None):
    return PyJoi.stream(name=name)

def list_factory(self: "StreamSchemaTest", iter: typing.Iterable)->typing.List:
    return list(iter)

class StreamSchemaTest(Common.StreamSchemaTest):
    @classmethod
    def setUpClass(cls):
        cls.schema_factory = schema_factory
        cls.instance_factory = list_factory
        cls.assertion = cls.assertListEqual