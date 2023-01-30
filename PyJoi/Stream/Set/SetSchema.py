""""""
from .. import StreamSchema
from ... import AbstractSchema
import typing
from . import Exceptions

T = typing.TypeVar("T",bound=typing.Union[typing.Set,typing.Optional[typing.Set]])
A = typing.TypeVar("A")
class SetSchema(typing.Generic[T],StreamSchema.StreamSchema[T]):
    _enforced: bool = False
    
    def _validate(self,iterable: any)->T:
        if self._enforced:
            stream = super(SetSchema,self)._validate(iterable)
            output = set()
            for item in stream:
                if item in output:
                    raise Exceptions.DuplicateException(self._name,"Error: duplicate element detected.")
                output.add(item)
            return output
        return set(super(SetSchema,self)._validate(iterable))

    def enforced(self)->"SetSchema[T]":
        self._enforced = True
        return self
    
    #This saves an unnecessary function call to just call super.
    if typing.TYPE_CHECKING:
        def matches(self, schema: AbstractSchema.AbstractSchema[A])->"SetSchema[typing.Set[A]]":
            pass
    
        def has(self, *schemas: AbstractSchema.AbstractSchema)->"SetSchema[T]":
            pass

        def optional(self)->"SetSchema[typing.Optional[T]]":
            pass