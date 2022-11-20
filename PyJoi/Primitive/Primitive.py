from .. import NonObjectSchema
from . import Exceptions
import typing
import datetime

T = typing.TypeVar("T",int,str,float,datetime.datetime)
class PrimitiveSchema(typing.Generic[T],NonObjectSchema.NonObjectSchema[T]):

    def __init__(self,name: typing.Optional[str], required: bool = True):
        super(PrimitiveSchema,self).__init__()
        self._name = name
        self._required = required

    def whitelist(self, items: typing.Union[T,typing.Iterable[T]],primitive: type)->"PrimitiveSchema":
        if not isinstance(items[0],primitive) and len(items) > 1:
            raise ValueError("Cannot blacklist several iterables at once!")
        elif not isinstance(items[0],primitive):
            whitelist = set(items[0]) #this is faster if validation is done multiple times, since creating the set is o(n) but checking it is o(1).
            self._checks.append(lambda value: self._check_whitelist(value,whitelist))
        else:
            whitelist = set(items)
            self._checks.append(lambda value: self._check_whitelist(value,whitelist))
        return self

    def blacklist(self, items: typing.Union[str,typing.Iterable[str]],primitive: type)->"PrimitiveSchema":
        if not isinstance(items[0],primitive) and len(items) > 1:
            raise ValueError("Cannot blacklist several iterables at once!")
        elif not isinstance(items[0],primitive):
            blacklist = set(items[0]) #this is faster if validation is done multiple times, since creating the set is o(n) but checking it is o(1).
            self._checks.append(lambda value: self._check_blacklist(value,blacklist))
        else:
            blacklist = set(items)
            self._checks.append(lambda value: self._check_blacklist(value,blacklist))
        return self

    def _check_blacklist(self,value: T, blacklist: typing.Set[T])->str:
        if value in blacklist:
            raise Exceptions.BlackListedValueException(self._name,f"{value} in blacklist")
        return value

    def _check_whitelist(self,value: T, whitelist: typing.Set[T])->str:
        if not value in whitelist:
            raise Exceptions.NonWhiteListedValueException(self._name,f"{value} not in whitelist")
        return value