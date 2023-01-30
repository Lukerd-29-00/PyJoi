from . import Exceptions
from .. import Exceptions as GenericExceptions
from .. import AbstractSchema
import typing
import abc
from .. import RefSrc

T = typing.TypeVar("T")

class PrimitiveSchema(typing.Generic[T],AbstractSchema.AbstractSchema[T],abc.ABC):
    R = typing.TypeVar("R") #I wish I could add R extends T, but python doesn't let me do that :(
    V = typing.TypeVar("V")
    _checks: typing.List[typing.Union[typing.Callable[[T],typing.Optional[T]],typing.Callable[[T],T]]]

    def __init__(self, name: typing.Optional[str] = None):
        super(PrimitiveSchema,self).__init__(name)
        self._checks = []

    def whitelist(self, items: typing.Union[T,typing.Iterable[T]],primitive: type)->"PrimitiveSchema[T]":
        if not isinstance(items[0],primitive) and len(items) > 1:
            raise ValueError("Cannot blacklist several iterables at once!")
        elif not isinstance(items[0],primitive):
            whitelist = set(items[0]) #this is faster if validation is done multiple times, since creating the set is o(n) but checking it is o(1).
            self._checks.append(lambda value: self._check_whitelist(value,whitelist))
        else:
            whitelist = set(items)
            self._checks.append(lambda value: self._check_whitelist(value,whitelist))
        return self

    def blacklist(self, items: typing.Union[str,typing.Iterable[str]],primitive: type)->"PrimitiveSchema[T]":
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

    def custom(self, func: typing.Callable, *refs: RefSrc.Ref)->'PrimitiveSchema':
        for r in refs:
            self._add_ref(r)
        self._checks.append(lambda v: func(self._name,v,*[r.value for r in refs]))
        return self
        
    def _validate(self,value: any)->T:
        subvalue = value
        for check in self._checks:
            if subvalue == None and self._required:
                raise GenericExceptions.MissingElementException(self._name,"Missing exepcted element, or got an unexpected null.")
            elif subvalue == None:
                return None
            subvalue = check(subvalue)
        if subvalue == None and self._required:
            raise GenericExceptions.MissingElementException(self._name,"Missing exepcted element, or got an unexpected null.")
        elif subvalue == None:
            return None
        return subvalue

    if typing.TYPE_CHECKING:
        def optional(self)->"PrimitiveSchema[typing.Optional[T]]":
            pass