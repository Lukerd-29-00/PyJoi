import typing
from . import Exceptions
from .AbstractSchema import AbstractSchema
from .Primitive.String.StringSchema import StringSchema as StringSchemaConstructor
from .Primitive.String import StringSchema
from .Primitive.Int.IntSchema import IntSchema as IntSchemaConstructor
from .Primitive.Int import IntSchema
import collections

T = typing.TypeVar("T",bound=typing.NamedTuple)
class Schema(typing.Generic[T],AbstractSchema[T]):
    _fields: typing.Optional[typing.Dict[str,"Schema"]] = None
    name: typing.Optional[str]
    required: bool

    @typing.overload
    def __init__(self, required: bool = True):
        """Instantiate with some parent schema"""
        pass

    @typing.overload
    def __init__(self,name: str, required: bool = True, **kwargs: typing.Dict[str,"AbstractSchema"]):
        """Instantiate a schema with a name and the schema's shape."""
        pass

    def __init__(self, name: typing.Optional[str] = None, required: bool = True, **kwargs: typing.Optional[typing.Dict[str,"Schema"]]):
        if name == None and kwargs:
            raise TypeError("Must have a name to add keyword arguments!")
        elif kwargs:
            self.__nt = collections.namedtuple(name,kwargs.keys())
            self._fields = dict(kwargs)
            for k in self._fields.keys():
                self._fields[k].name = k
        self.required = required
        self.name = name

    def string(self)->StringSchema:
        """Create a string schema."""
        if self._fields != None:
            raise ValueError("Cannot create string schema from an object schema with parameters!")
        return StringSchemaConstructor(self.name,required=self.required)

    def int(self)->IntSchema:
        """Create an int schema."""
        return IntSchemaConstructor(self.name,required=self.required)

    def validate(self,object: typing.Dict[str,any])->typing.Optional[T]:
        if object == None and not self.required:
            return None
        elif object == None:
            raise Exceptions.MissingObjectException(self.name,"missing required object")
        elif not isinstance(object,typing.Dict):
            raise Exceptions.NotAnObjectException(self.name,"expected to be associated with an object but encountered something else.")
        try:
            data = dict([(key, self._fields[key].validate(None if object is None or not key in object.keys() else object[key])) for key in self._fields.keys()])
        except Exceptions.ValidationException as V:
            raise type(V)(f"{self.name}.{V.name}",V.vmessage)
        s = set(data.values())
        if len(s) == 1 and None in s and not self.required:
            return None
        elif len(s) == 1 and None in s:
            raise Exceptions.EmptyObjectException(self.name,"Required object is empty.")
        return self.__nt(**data)