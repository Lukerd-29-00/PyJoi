""""""
from .. import StreamSchema
from ... import AbstractSchema
import typing
from . import Exceptions

T = typing.TypeVar("T")
A = typing.TypeVar("A")
class SetSchema(typing.Generic[T],StreamSchema.StreamSchema[T]):
    _enforced: bool = False
    
    def validate(self,iterable: any)->typing.Set[T]:
        if self._enforced:
            stream = super(SetSchema,self).validate(iterable)
            output = set()
            for item in stream:
                if item in output:
                    raise Exceptions.DuplicateException(self._name,"Error: duplicate element detected.")
                output.add(item)
            return output
        return set(super(SetSchema,self).validate(iterable))

    def enforced(self):
        self._enforced = True
        return self
    
    #This saves an unnecessary function call to just call super.
    if typing.TYPE_CHECKING:
        def matches(self, schema: AbstractSchema.AbstractSchema[any,A,any])->"SetSchema[A]":
            pass
    
        def has(self, *schemas: AbstractSchema.AbstractSchema)->"SetSchema[T]":
            pass

        def optional(self)->"SetSchema[T]":
            pass