from . import Schema
from .. import AbstractSchema, Exceptions
import typing

T = typing.TypeVar("T")
class DictSchema(typing.Generic[T],Schema.Schema[T]):
    def __init__(self, name: typing.Optional[str] = None, output_type: typing.Optional[Schema.OutputType[T]] = None, **kwargs: "AbstractSchema.AbstractSchema"):
        self._fields = kwargs
        self._output_type = output_type
        super(DictSchema,self).__init__(name)
    
    def _validate(self, object: any)->T:
        if object == None and not self._required:
            return None
        elif object == None:
            raise Exceptions.MissingObjectException(self._name,"Missing required dict!")
        elif not isinstance(object,typing.Dict):
            raise Exceptions.NotAnObjectException(self._name,"Expected a dictionary object, but got something else!")
        data = super(DictSchema,self)._validate(object)
        if self._output_type == None:
            return data
        else:
            return self._output_type(**data)