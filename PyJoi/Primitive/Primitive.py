from .. import AbstractSchema
from . import Exceptions
import abc
import typing
import datetime

T = typing.TypeVar("T",int,str,float,datetime.datetime)
class PrimitiveSchema(AbstractSchema.AbstractSchema,abc.ABC,typing.Generic[T]):
    _blacklist: typing.Set[T]
    _whitelist: typing.Set[T]

    def __init__(self,name: str, required: bool = True):
        super(PrimitiveSchema,self).__init__(name,required)
        self._blacklist = set()
        self._whitelist = set()

    @abc.abstractmethod
    def validate(self,value: any)->T:
        pass

    @typing.overload
    def blacklist(self, item: T)->"PrimitiveSchema":
        pass
    @typing.overload
    def blacklist(self, items: typing.Iterable[T])->"PrimitiveSchema":
        pass
    def blacklist(self, items: typing.Union[T,typing.Iterable[T]], t: type)->"PrimitiveSchema":
        if self._whitelist:
            raise ValueError("Cannot blacklist items in a schema that already has a blacklist!")
        self._blacklist = self._blacklist.union([items] if isinstance(items,t) else items)
        return self

    def check_blacklist(self,value: T)->None:
        if self._blacklist and value in self._blacklist:
            raise Exceptions.BlackListedValueException(self.name,f"{value} in blacklist")

    @typing.overload
    def whitelist(self, item: T)->"PrimitiveSchema":
        pass
    @typing.overload
    def whitelist(self, items: typing.Iterable[T])->"PrimitiveSchema":
        pass
    def whitelist(self, items: typing.Union[T,typing.Iterable[T]], t: type)->"PrimitiveSchema":
        if self._blacklist:
            raise ValueError("Cannot blacklist items in a schema that already has a whitelist!")
        self._whitelist = self._whitelist.union([items] if isinstance(items,t) else items)
        return self

    def check_whitelist(self,value: T)->None:
        if self._whitelist and not value in self._whitelist:
            raise Exceptions.NonWhiteListedValueException(self.name,f"{value} not in whitelist")