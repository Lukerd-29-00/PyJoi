
import typing
from . import Exceptions
from . import IIntSchema
class IntSchema(IIntSchema.IIntSchema):
    _max: typing.Optional[int] = None
    _min: typing.Optional[int] = None
    _base: typing.Optional[int] = None

    def __set_condition(self,attr: str, bound: int):
        if self._whitelist:
            raise ValueError("Cannot add a bound to a schema with a whitelist!")
        elif self.__getattribute__(attr) != None:
            raise ValueError("Tried to set a bound that is already initialized. This can happen if you try something like .poitive().min(1), which is redundant.")
        self.__setattr__(attr,bound)
        if self._min != None and self._max != None and self._min > self._max:
            raise ValueError("Cannot set a maximum less than the minimum!")
        return self

    def max(self, new_max: int)->"IntSchema":
        return self.__set_condition("_max",new_max)

    def min(self, new_min: int)->"IntSchema":
        return self.__set_condition("_min",new_min)

    def multiple(self, base: int)->"IntSchema":
        return self.__set_condition("_base",base)

    def positive(self)->"IntSchema":
        return self.__set_condition("_min",0)

    def negative(self)->"IntSchema":
        return self.__set_condition("_max",-1)

    def port(self)->"IntSchema":
        self.__set_condition("_max",65535)
        return self.__set_condition("_min",0)
    
    def port_nonadmin(self)->"IntSchema":
        self.__set_condition("_max",65535)
        return self.__set_condition("_min",1024)

    def validate(self,value: any)->typing.Optional[int]:
        if value == None and not self.required:
            return None
        elif value == None:
            raise Exceptions.MissingIntException(self.name,"Missing required integer")
        elif not isinstance(value,int):
            raise Exceptions.NotAnIntException(self.name,"Found non-integer: the number may have been accidentally wrapped in quotes.")
        elif self._base != None and value % self._base != 0:
            raise Exceptions.NonMultipleException(self.name,f"{value} is not a multiple of {self._base}")
        elif self._max != None and value > self._max:
            raise Exceptions.TooSmallException(self.name,f"Expected value <= {self._max}, got {value}")
        elif self._min != None and value < self._min:
            raise Exceptions.TooBigException(self.name,f"Expected value >= {self._min}, got {value}")
        self.check_blacklist(value)
        self.check_whitelist(value)
        return value