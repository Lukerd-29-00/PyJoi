from .. import Primitive
import typing
from . import Exceptions

T = typing.TypeVar("T",bool,typing.Optional[bool])
class BoolSchema(typing.Generic[T],Primitive.PrimitiveSchema[T]):
    def _validate(self, value: any)->T:
        if not isinstance(value,bool) and value != None:
            raise Exceptions.NotABoolException(self._name,f"{value} is not a boolean.")
        return super(BoolSchema,self)._validate(value)

    if typing.TYPE_CHECKING:
        def optional(self)->"BoolSchema[typing.Optional[bool]]":
            pass

        def whitelist(self, *items: bool)->"BoolSchema[T]":
            pass
        
        def blacklist(self, *items: bool)->"BoolSchema[T]":
            pass