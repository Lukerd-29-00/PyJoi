
import typing
from . import Exceptions as IntExceptions
from .. import NumericSchema
from ....RefSrc import Ref

T = typing.TypeVar("T",int,typing.Optional[int])

class IntSchema(typing.Generic[T],NumericSchema.NumericSchema[T]):
    def __init__(self, name: typing.Optional[str] = None):
        super(IntSchema,self).__init__(name)
        self._checks.append(lambda value: self.__check_int(value))

    def __check_int(self, value: any):
        if (isinstance(value,float) or isinstance(value,int)) and int(value) == value:
            return int(value)
        else:
            raise IntExceptions.NotAnIntException(self._name,f"{value} is not an integer!")

    def _check_multiple(self,value: int,base: int):
        if value % base == 0:
            return value
        raise IntExceptions.NonMultipleException(self._name,f"Encountered {value}, not divisible by {base}") 

    def multiple(self, base: typing.Union[int,Ref[int]])->"IntSchema[T]":
        if isinstance(base,int):
            self._checks.append(lambda value: self._check_multiple(value,base))
        else:
            self._add_ref(base)
            self._checks.append(lambda value: self._check_multiple(value,base.value))
        return self

    def port(self)->"IntSchema[T]":
        self._checks.append(lambda value: self._check_lower(value,65536))
        self._checks.append(lambda value: self._check_greater(value,-1))
        return self

    if typing.TYPE_CHECKING:
        def less_than(self, new_max: typing.Union[int,Ref[int]])->"IntSchema[T]":
            pass

        def greater_than(self, new_min: typing.Union[int,Ref[int]])->"IntSchema[T]":
            pass

        def optional(self)->"IntSchema[typing.Optional[int]]":
            pass

        def whitelist(self, *items: int)->"IntSchema[T]":
            pass

        def blacklist(self, *items: int)->"IntSchema[T]":
            pass