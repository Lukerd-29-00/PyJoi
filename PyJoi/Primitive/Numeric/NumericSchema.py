import abc
from .. import PrimitiveSchema
import typing
from ...RefSrc import Ref
from . import Exceptions

T = typing.TypeVar("T",int,float,typing.Optional[int],typing.Optional[float])
class NumericSchema(typing.Generic[T],PrimitiveSchema[T],abc.ABC):
    def _check_lower(self, value: typing.Union[float,int], constant: typing.Union[float, int])->T:
        if value < constant:
            return value
        else:
            raise Exceptions.InvalidSizeException(self._name,f"{value} >= {constant}")

    def _check_greater(self, value: typing.Union[float,int], constant: typing.Union[float,int])->T:
        if value > constant:
            return value
        else:
            raise Exceptions.InvalidSizeException(self._name,f"{value} <= {constant}")

    def less_than(self, new_max: typing.Union[float,Ref[float],int,Ref[int]])->"NumericSchema[T]":
        if isinstance(new_max,int) or isinstance(new_max,float):
            self._checks.append(lambda value: self._check_lower(value,new_max))
        else:
            self._add_ref(new_max)
            self._checks.append(lambda value: self._check_lower(value,new_max.value))
        return self

    def greater_than(self, new_min: typing.Union[float,Ref[float],int,Ref[int]])->"NumericSchema[T]":
        if isinstance(new_min,int) or isinstance(new_min,float):
            self._checks.append(lambda value: self._check_greater(value, new_min))
        else:
            self._add_ref(new_min)
            self._checks.append(lambda value: self._check_greater(value, new_min.value))
        return self
    
    def positive(self)->"NumericSchema[T]":
        self._checks.append(lambda value: self._check_greater(value, 0))
        return self

    def negative(self)->"NumericSchema[T]":
        self._checks.append(lambda value: self._check_lower(value,0))
        return self