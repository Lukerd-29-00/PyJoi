from .AbstractSchema import AbstractSchema
from . import Ref
import typing
import abc
from . import Exceptions


T = typing.TypeVar("T")
class NonObjectSchema(typing.Generic[T],AbstractSchema,abc.ABC):
    Ps = typing.ParamSpec("Ps")
       
    R = typing.TypeVar("R") #I wish I could add R extends T, but python doesn't let me do that :(
    _or: typing.Optional["NonObjectSchema[R]"] = None
    _checks: typing.List[typing.Union[typing.Callable[[T],typing.Optional[T]],typing.Callable[[T],T]]]
    _name: typing.Optional[str]

    def __init__(self):
        self._checks = []

    def validate(self,value: any)->typing.Optional[T]:
        subvalue = value
        try:
            for check in self._checks:
                if subvalue == None and self._required:
                    raise Exceptions.MissingElementException(self._name,"Missing exepcted element, or got an unexpected null.")
                elif subvalue == None:
                    return None
                subvalue = check(subvalue)
        except Exceptions.ValidationException as V:
            if self._or != None:
                return self._or.validate(value) #this is in fact type-safe as long as _or is assigned via the union method and assigned to something like this: a = Schema().int().union(...)
            raise V
        if subvalue == None and self._required:
            raise Exceptions.MissingElementException(self._name,"Missing exepcted element, or got an unexpected null.")
        elif subvalue == None:
            return None
        return subvalue

    def union(self, schema: 'NonObjectSchema[R]')->'NonObjectSchema[typing.Union[T,R]]':
        self._or = schema
        return self