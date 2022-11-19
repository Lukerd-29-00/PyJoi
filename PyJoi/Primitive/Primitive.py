from .. import AbstractSchema
from . import Exceptions
import abc
import typing
import datetime

T = typing.TypeVar("T",int,str,float,datetime.datetime)
class PrimitiveSchema(AbstractSchema.AbstractSchema,abc.ABC,typing.Generic[T]):
    _blacklist: typing.Set[T]
    _whitelist: typing.Set[T]

    def __init__(self,name: typing.Optional[str], required: bool = True):
        self.name = name
        self.required = required
        self._blacklist = set()
        self._whitelist = set()

    @abc.abstractmethod
    def validate(self,value: any)->typing.Optional[T]:
        pass

    def check_blacklist(self,value: T)->None:
        if self._blacklist and value in self._blacklist:
            raise Exceptions.BlackListedValueException(self.name,f"{value} in blacklist")

    def check_whitelist(self,value: T)->None:
        if self._whitelist and not value in self._whitelist:
            raise Exceptions.NonWhiteListedValueException(self.name,f"{value} not in whitelist")