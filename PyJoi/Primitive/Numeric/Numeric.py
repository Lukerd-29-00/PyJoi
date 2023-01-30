import abc
from .. import PrimitiveSchema
import typing
from ...RefSrc import Ref
from . import Exceptions

T = typing.TypeVar("T",int,float,typing.Optional[int],typing.Optional[float])
class Numeric(typing.Generic[T],PrimitiveSchema[T],abc.ABC):

    def _check_size(self, value: int, comparator: typing.Callable[[T],bool])->T:
        if comparator(value):
            return value
        raise Exceptions.InvalidSizeException(self._name,f"{value} is outside the value bounds for this int schema!")

    def max(self, new_max: typing.Union[float,Ref[float],int,Ref[int]])->"Numeric[T]":
        if isinstance(new_max,int):
            self._checks.append(lambda value: self._check_size(value,new_max.__ge__))
        else:
            self._add_ref(new_max)
            self._checks.append(lambda value: self._check_size(value,new_max.value.__ge__))
        return self

    def min(self, new_min: typing.Union[float,Ref[float],int,Ref[int]])->"Numeric[T]":
        if isinstance(new_min,int):
            self._checks.append(lambda value: self._check_size(value,new_min.__le__))
        else:
            self._add_ref(new_min)
            self._checks.append(lambda value: self._check_size(value,new_min.value.__le__))
        return self
    
    def positive(self)->"Numeric[T]":
        zero = 0
        self._checks.append(lambda value: self._check_size(value,zero.__le__))
        return self

    def negative(self)->"Numeric[T]":
        zero = 0
        self._checks.append(lambda value: self._check_size(value,zero.__gt__))
        return self

    if typing.TYPE_CHECKING:
        def optional(self)->"Numeric[typing.Optional[T]]":
            pass