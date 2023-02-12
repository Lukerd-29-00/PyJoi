from . import Schema
from .. import AbstractSchema
import typing
import itertools
from .. import Exceptions

T = typing.TypeVar("T")
class TupleSchema(typing.Generic[T],Schema.Schema[T]):
    def __init__(self, *args: "AbstractSchema.AbstractSchema", name: typing.Optional[str] = None):
        """Create a PyJoi Schema.
        
        Args:
            name: The optional name of the schema. If this Schema is nested within another one, its name will be inferred.
            required: Whether or not this schema is required for the enclosing object to be valid. Can be set to False with .optional().
        """
        self._fields = dict([(str(x), schema) for x, schema in zip(itertools.count(),args)])
        super(TupleSchema,self).__init__(name)

    def _validate(self, object: any) -> T:
        if object == None and not self._required:
            return None
        elif object == None:
            raise Exceptions.MissingObjectException(self._name,"missing required object")
        elif not isinstance(object,typing.Iterable):
            raise Exceptions.NotAnObjectException(self._name,"expected to be associated with an Iterable but encountered something else.")
        elif len(object) != len(self._fields):
            raise Exceptions.TupleWrongLengthException(self._name,f"Expected iterable of length {len(self._fields)}, got {len(object)}")
        data = super(TupleSchema,self)._validate(dict([(str(key), value) for key, value in zip(itertools.count(),object)]))
        output = []
        for i in range(len(object)):
            output.append(data[str(i)])
        return tuple(output)