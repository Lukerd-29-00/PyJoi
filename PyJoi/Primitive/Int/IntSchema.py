
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

    def max(self, new_max: typing.Union[int,Ref[int]])->"IIntSchema":
        if isinstance(new_max,int):
            self._checks.append(lambda value: self._check_size(value,new_max.__ge__))
        else:
            self._add_ref(new_max)
            self._checks.append(lambda value: self._check_size(value,new_max.value.__ge__))
        return self

    def min(self, new_min: typing.Union[int,Ref[int]])->"IIntSchema":
        if isinstance(new_min,int):
            self._checks.append(lambda value: self._check_size(value,new_min.__le__))
        else:
            self._add_ref(new_min)
            self._checks.append(lambda value: self._check_size(value,new_min.value.__le__))
        return self

    def multiple(self, base: typing.Union[int,Ref[int]])->"IIntSchema":
        if isinstance(base,int):
            self._checks.append(lambda value: self._check_multiple(value,base))
        else:
            self._add_ref(base)
            self._checks.append(lambda value: self._check_multiple(value,base.value))
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