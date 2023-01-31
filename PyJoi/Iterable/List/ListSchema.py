""""""
from .. import IterableSchema
from ... import AbstractSchema
import typing

T = typing.TypeVar("T",bound=typing.Union[typing.List,typing.Optional[typing.List]])
A = typing.TypeVar("A")
class ListSchema(typing.Generic[T],IterableSchema.IterableSchema[T]):
    def _validate(self,iterable: any)->T:
        return list(super(ListSchema,self)._validate(iterable))

    if typing.TYPE_CHECKING:
        def matches(self, schema: AbstractSchema.AbstractSchema[A])->"ListSchema[typing.List[A]]":
            pass
    
        def has(self, *schemas: AbstractSchema.AbstractSchema)->"ListSchema[T]":
            pass

        def optional(self)->"ListSchema[typing.Optional[T]]":
            pass