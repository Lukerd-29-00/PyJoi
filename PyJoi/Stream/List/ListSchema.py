""""""
from .. import StreamSchema
from ... import AbstractSchema
import typing

T = typing.TypeVar("T")
A = typing.TypeVar("A")
class ListSchema(typing.Generic[T],StreamSchema.StreamSchema[T]):
    
    def validate(self,iterable: any)->typing.List[T]:
        return list(super(ListSchema,self).validate(iterable))

    if typing.TYPE_CHECKING:
        def matches(self, schema: AbstractSchema.AbstractSchema[any,A,any])->"ListSchema[A]":
            pass
    
        def has(self, *schemas: AbstractSchema.AbstractSchema)->"ListSchema[T]":
            pass

        def optional(self)->"ListSchema[T]":
            pass