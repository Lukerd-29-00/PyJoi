from . import Exceptions
from .. import Exceptions as GenericExceptions
from .. import AbstractSchema
import typing
import datetime
import abc

T = typing.TypeVar("T",int,str,float,datetime.datetime)
class PrimitiveSchema(typing.Generic[T],AbstractSchema.AbstractSchema[any,T,typing.Optional[str]],abc.ABC):
    R = typing.TypeVar("R") #I wish I could add R extends T, but python doesn't let me do that :(
    _or: typing.Optional["PrimitiveSchema[R]"] = None
    _checks: typing.List[typing.Union[typing.Callable[[T],typing.Optional[T]],typing.Callable[[T],T]]]

    def __init__(self, name: typing.Optional[str] = None, required: bool = True):
        super(PrimitiveSchema,self).__init__(name,required=required)
        self._checks = []

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
        
    def validate(self,value: any)->typing.Optional[T]:
        subvalue = value
        try:
            for check in self._checks:
                if subvalue == None and self._required:
                    raise GenericExceptions.MissingElementException(self._name,"Missing exepcted element, or got an unexpected null.")
                elif subvalue == None:
                    return None
                subvalue = check(subvalue)
        except GenericExceptions.ValidationException as V:
            if self._or != None:
                return self._or.validate(value) #this is in fact type-safe as long as _or is assigned via the union method and assigned to something like this: a = Schema().int().union(...)
            raise V
        if subvalue == None and self._required:
            raise GenericExceptions.MissingElementException(self._name,"Missing exepcted element, or got an unexpected null.")
        elif subvalue == None:
            return None
        return subvalue

    def union(self, schema: 'PrimitiveSchema[R]')->'PrimitiveSchema[typing.Union[T,R]]':
        self._or = schema
        return self