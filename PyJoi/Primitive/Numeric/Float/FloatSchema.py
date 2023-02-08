from .. import NumericSchema
import typing
from .... import Ref
from . import Exceptions as FloatExceptions

T = typing.TypeVar("T",float,typing.Optional[float])
class FloatSchema(typing.Generic[T],NumericSchema.NumericSchema[T]):
    def _validate(self, value: any)->T:
        if not isinstance(value,int) and value != None and not isinstance(value,float):
            raise FloatExceptions.NotAFloatException(self._name,f"{value} is not an integer!")
        return super(NumericSchema.NumericSchema,self)._validate(value) 

    def __check_precision(self, value: float, precision: int):
        if value == round(value,precision):
            return value
        else:
            raise FloatExceptions.InvalidPrecisionException(self._name,f"{value} has more than {precision} decimal digits.")

    def precision(self, precision: typing.Union[int,Ref[int]])->"FloatSchema[T]":
        if isinstance(precision,int):
            if precision <= 0:
                raise ValueError("Precision must be a positive integer!")
            self._checks.append(lambda f: self.__check_precision(f,precision))
        else:
            self._add_ref(precision)
            self._checks.append(lambda f: self.__check_precision(f,precision.value))
        return self

    if typing.TYPE_CHECKING:
        def less_than(self,new_max: typing.Union[float,Ref[float]])->"FloatSchema[T]":
            pass

        def greater_than(self,new_min: typing.Union[float,Ref[float]])->"FloatSchema[T]":
            pass
    
        def optional(self)->"FloatSchema[typing.Optional[float]]":
            pass

        def whitelist(self,*items: typing.Union[float,typing.Iterable[float]])->"FloatSchema[T]":
            pass

        def blacklist(self,*items: typing.Union[float,typing.Iterable[float]])->"FloatSchema[T]":
            pass