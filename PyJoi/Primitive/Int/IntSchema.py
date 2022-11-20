
import typing
from . import Exceptions
from . import IIntSchema
class IntSchema(IIntSchema.IIntSchema):

    def validate(self, value: any)->typing.Optional[int]:
        if not isinstance(value,int):
            raise Exceptions.MissingIntException(self._name,f"{value} is not an integer!")
        return super(IntSchema,self).validate(value)

    def whitelist(self, items: typing.Union[typing.Iterable[int],int]):
        if self._blacklist:
            raise ValueError("Cannot have both whitelist and blacklist")
        self._whitelist = self._whitelist.union(items if not isinstance(items,int) else [items])
        return self

    def _check_size(self, value: int, comparator: typing.Callable[[int],bool])->int:
        if comparator(value):
            return value
        raise Exceptions.InvalidSizeException(self._name,f"{value} is outside the value bounds for this int schema!")

    def _check_multiple(self,value: int,base: int):
        if value % base == 0:
            return value
        raise Exceptions.NonMultipleException(self._name,f"Encountered {value}, not divisible by {base}")

    def blacklist(self, items: typing.Union[typing.Iterable[int],int]):
        self._blacklist = self._blacklist.union(items if not isinstance(items,int) else [items])
        return self

    def max(self, new_max: int)->"IntSchema":
        self._checks.append(lambda value: self._check_size(value,new_max.__ge__))
        return self

    def min(self, new_min: int)->"IntSchema":
        self._checks.append(lambda value: self._check_size(value,new_min.__le__))
        return self

    def multiple(self, base: int)->"IntSchema":
        self._checks.append(lambda value: self._check_size(value,base))
        return self

    def positive(self)->"IntSchema":
        zero = 0
        self._checks.append(lambda value: self._check_size(value,zero.__le__))
        return self

    def negative(self)->"IntSchema":
        mone = -1
        self._checks.append(lambda value: self._check_size(value,mone.__ge__))
        return self

    def port(self)->"IntSchema":
        bounds = (0,65535)
        self._checks.append(lambda value: self._check_size(value,lambda value: value >= bounds[0] and value <= bounds[1]))
        return self
    
    def port_nonadmin(self)->"IntSchema":
        bounds = (1024,65535)
        self._checks.append(lambda value: self._check_size(value,lambda value: value >= bounds[0] and value <= bounds[1]))
        return self