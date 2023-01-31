import unittest
import PyJoi
from PyJoi.Iterable import Exceptions as StreamExceptions
from .. import util
from PyJoi.Iterable import IterableSchema
import typing
import abc

class SchemaFactory(typing.Protocol):
    def __call__(self, name: typing.Optional[str] = None)->IterableSchema.IterableSchema:
        pass

def is_int(value: any):
    if isinstance(value,int):
        return value
    else:
        raise util.TestException(None, "not an int")

class IterableSchemaTest(unittest.TestCase,abc.ABC):
    schema_factory: SchemaFactory
    instance_factory: typing.Callable[[typing.Iterable],typing.Iterable]
    assertion: typing.Callable[[typing.Iterable],None]

    @abc.abstractclassmethod
    def setUpClass(cls):
        pass

    def test_has(self):
        Schema = self.schema_factory().has(util.SchemaMock(validate=is_int))
        s = Schema.validate([1,"2"])
        self.assertion(self.instance_factory(s),self.instance_factory([1,"2"]))
        with self.assertRaises(StreamExceptions.RequiredItemNotFound):
            self.instance_factory(Schema.validate(["2","3","4"]))

    def test_matches(self):
        Schema = self.schema_factory("lst").matches(util.SchemaMock(validate=is_int))
        s = Schema.validate([1,2])
        self.assertion(self.instance_factory(s),self.instance_factory([1,2]))
        with self.assertRaises(util.TestException) as cm:
            self.instance_factory(Schema.validate([1,"2"]))
        self.assertEqual(cm.exception.name,"lst") #Make sure the name of the anonymous schema is replaced with the list schema's name.

    def test_matches_refs(self):
        num = util.SchemaMock()
        R = PyJoi.Ref[int]("max") #We can reference this key directly because a schema in .matches is treated as though it was at the level of the enclosing steam schema.
        num._depends_on[R] = None
        R._schema = num
        def is_less(value: int)->int:
            if value <= R.value:
                return value
            else:
                raise util.TestException(None,"too large")
        num.validate = is_less
        mx = util.SchemaMock()
        mx.validate.return_value = 12
        Schema = PyJoi.Schema("schema",
            lst=self.schema_factory().matches(num), #We can reference 'max' directly because any non-object schemas in a list act as though they were elements of the list's parent for referencing purposes.
            max=mx
        )
        s = Schema.validate({"max": 12, "lst": [11, 12, 10, 9]})
        self.assertEqual(s.max,12)
        self.assertion(self.instance_factory(s.lst),self.instance_factory([11,12,10,9]))
        mx.validate.return_value = -1
        with self.assertRaises(util.TestException):
            next(Schema.validate({"max": -1, "lst": [11, 12, 10, 9]}).lst)