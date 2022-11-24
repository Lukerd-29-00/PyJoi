
import typing
from . import Exceptions
from . import IIntSchema
from ...RefSrc import Ref
class IntSchema(IIntSchema.IIntSchema):

    def validate(self, value: any)->typing.Optional[int]:
        if not isinstance(value,int) and value != None:
            raise Exceptions.NotAnIntException(self._name,f"{value} is not an integer!")
        return super(IIntSchema.IIntSchema,self).validate(value) 

    def _check_size(self, value: int, comparator: typing.Callable[[int],bool])->int:
        if comparator(value):
            return value
        raise Exceptions.InvalidSizeException(self._name,f"{value} is outside the value bounds for this int schema!")

    def _check_multiple(self,value: int,base: int):
        if value % base == 0:
            return value
        raise Exceptions.NonMultipleException(self._name,f"Encountered {value}, not divisible by {base}")

    def max(self, new_max: int)->"IIntSchema":
        self._checks.append(lambda value: self._check_size(value,new_max.__ge__))
        return self

    def min(self, new_min: int)->"IIntSchema":
        self._checks.append(lambda value: self._check_size(value,new_min.__le__))
        return self

    def multiple(self, base: int)->"IIntSchema":
        self._checks.append(lambda value: self._check_multiple(value,base))
        return self

    def greater(self, ref: Ref[int])->"IIntSchema":
        self._add_ref(ref)
        self._checks.append(lambda value: self._check_size(value,ref.value.__lt__))
        return self

    def positive(self)->"IIntSchema":
        zero = 0
        self._checks.append(lambda value: self._check_size(value,zero.__le__))
        return self

    def negative(self)->"IIntSchema":
        mone = -1
        self._checks.append(lambda value: self._check_size(value,mone.__ge__))
        return self

    def port(self)->"IIntSchema":
        bounds = (0,65535)
        self._checks.append(lambda value: self._check_size(value,lambda value: value >= bounds[0] and value <= bounds[1]))
        return self
    
    def port_nonadmin(self)->"IIntSchema":
        bounds = (1024,65535)
        self._checks.append(lambda value: self._check_size(value,lambda value: value >= bounds[0] and value <= bounds[1]))
        return self