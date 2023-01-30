
import typing
from . import Exceptions as IntExceptions
from .. import Numeric
from ....RefSrc import Ref
class IntSchema(Numeric.Numeric):
    def _check_multiple(self,value: int,base: int):
        if value % base == 0:
            return value
        raise IntExceptions.NonMultipleException(self._name,f"Encountered {value}, not divisible by {base}")

    @typing.overload
    def whitelist(self,*items: int)->"IntSchema":
        pass
    @typing.overload
    def whitelist(self,items: typing.Iterable[int])->"IntSchema":
        pass
    def whitelist(self,*items: typing.Union[int,typing.Iterable[int]])->"IntSchema":
        return super(Numeric.Numeric,self).whitelist(items,primitive=int)

    @typing.overload
    def blacklist(self,*items: int)->"IntSchema":
        pass
    @typing.overload
    def blacklist(self,items: typing.Iterable[int])->"IntSchema":
        pass
    def blacklist(self,*items: typing.Union[int,typing.Iterable[int]])->"IntSchema":
        return super(Numeric.Numeric,self).blacklist(items,primitive=int)

    def validate(self, value: any)->typing.Optional[int]:
        if not isinstance(value,int) and value != None:
            raise IntExceptions.NotAnIntException(self._name,f"{value} is not an integer!")
        return super(Numeric.Numeric,self).validate(value) 

    def multiple(self, base: typing.Union[int,Ref[int]])->"IntSchema":
        if isinstance(base,int):
            self._checks.append(lambda value: self._check_multiple(value,base))
        else:
            self._add_ref(base)
            self._checks.append(lambda value: self._check_multiple(value,base.value))
        return self

    def port(self)->"IntSchema":
        bounds = (0,65535)
        self._checks.append(lambda value: self._check_size(value,lambda value: value >= bounds[0] and value <= bounds[1]))
        return self

    if typing.TYPE_CHECKING:
        def max(self, new_max: typing.Union[int,Ref[int]])->"IntSchema":
            pass

        def min(self, new_min: typing.Union[int,Ref[int]])->"IntSchema":
            pass