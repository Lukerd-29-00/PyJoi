import typing
from . import Exceptions
from .AbstractSchema import AbstractSchema
import collections

class Schema(AbstractSchema):
    __fields: typing.Optional[typing.Dict[str,"Schema"]] = None
    name: str
    required: bool

    def __init__(self, name: str, required: bool = True, **kwargs: typing.Optional[typing.Dict[str,"Schema"]]):
        if kwargs:
            self.__nt = collections.namedtuple(name,kwargs.keys())
            self.__fields = dict(kwargs)
        self.required = required
        self.name = name

    def validate(self,object: typing.Dict[str,any])->typing.NamedTuple:
        if object == None and not self.required:
            return None
        elif object == None:
            raise Exceptions.MissingObjectException(self.name,"missing required object")
        elif not isinstance(object,typing.Dict):
            raise Exceptions.NotAnObjectException(self.name,"expected to be associated with an object but encountered something else.")
        try:
            data = dict([(key, self.__fields[key].validate(None if object is None or not key in object.keys() else object[key])) for key in self.__fields.keys()])
        except Exceptions.ValidationException as V:
            raise type(V)(f"{self.name}.{V.name}",V.vmessage)
        s = set(data.values())
        if len(s) == 1 and None in s and not self.required:
            return None
        elif len(s) == 1 and None in s:
            raise Exceptions.EmptyObjectException(self.name,"Required object is empty.")
        return self.__nt(**data)