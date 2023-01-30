import abc
from .. import PrimitiveSchema
import typing
from ...RefSrc import Ref
from . import Exceptions

class Numeric(PrimitiveSchema,abc.ABC):
    def _check_size(self, value: int, comparator: typing.Callable[[typing.Union[int,float]],bool])->int:
        if comparator(value):
            return value
        raise Exceptions.InvalidSizeException(self._name,f"{value} is outside the value bounds for this int schema!")

    def max(self, new_max: typing.Union[float,Ref[float],int,Ref[int]])->"Numeric":
        if isinstance(new_max,int):
            self._checks.append(lambda value: self._check_size(value,new_max.__ge__))
        else:
            self._add_ref(new_max)
            self._checks.append(lambda value: self._check_size(value,new_max.value.__ge__))
        return self

    def min(self, new_min: typing.Union[float,Ref[float],int,Ref[int]])->"Numeric":
        if isinstance(new_min,int):
            self._checks.append(lambda value: self._check_size(value,new_min.__le__))
        else:
            self._add_ref(new_min)
            self._checks.append(lambda value: self._check_size(value,new_min.value.__le__))
        return self
    
    def positive(self)->"Numeric":
        zero = 0
        self._checks.append(lambda value: self._check_size(value,zero.__le__))
        return self

    def negative(self)->"Numeric":
        zero = 0
        self._checks.append(lambda value: self._check_size(value,zero.__gt__))
        return self

    if typing.TYPE_CHECKING:
        def optional(self)->"Numeric":
            pass

        def custom(self, func: typing.Callable, *refs: Ref)->"Numeric":
            pass

