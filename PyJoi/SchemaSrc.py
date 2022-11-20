import typing
from . import Exceptions
from .AbstractSchema import AbstractSchema
from .Primitive.String.StringSchema import StringSchema as StringSchemaConstructor
from .Primitive.String import StringSchema
from .Primitive.Int.IntSchema import IntSchema as IntSchemaConstructor
from .Primitive.Int import IntSchema
import collections

T = typing.TypeVar("T",bound=typing.NamedTuple)
class Schema(typing.Generic[T],AbstractSchema):
    _fields: typing.Optional[typing.Dict[str,"Schema"]] = None
    _name: typing.Optional[str]
    _required: bool

    def __init__(self, name: typing.Optional[str] = None, required: bool = True, **kwargs: typing.Optional[typing.Dict[str,"Schema"]]):
        """Create a PyJoi Schema.
        
        Args:
            name: The optional name of the schema. If this Schema is nested within another one, its name will be inferred.
            required: Whether or not this schema is required for the enclosing object to be valid. Can be set to False with .optional().
        """
        if kwargs:
            self.__nt = collections.namedtuple(name,kwargs.keys())
            self._fields = dict(kwargs)
            for k in self._fields.keys():
                self._fields[k]._name = k
        self._required = required
        self._name = name

    def string(self)->StringSchema:
        """Create a string schema."""
        if self._fields != None:
            raise ValueError("Cannot create string schema from an object schema with parameters!")
        return StringSchemaConstructor(self._name,required=self._required)

    def int(self)->IntSchema:
        """Create an int schema."""
        return IntSchemaConstructor(self._name,required=self._required)

    def validate(self,object: typing.Optional[typing.Dict[str,any]])->typing.Optional[T]:
        """Validate an object (Python dictionary from strings to anything that can be represented by another Schema).

        Args:
            object: The object being validated. Must be a dictionary or None.
        """
        if not self._fields:
            raise ValueError("Error: empty Schema encountered!")
        elif self._name == None:
            raise ValueError("Error: Schema has no name!")
        elif object == None and not self._required:
            return None
        elif object == None:
            raise Exceptions.MissingObjectException(self._name,"missing required object")
        elif not isinstance(object,typing.Dict):
            raise Exceptions.NotAnObjectException(self._name,"expected to be associated with an object but encountered something else.")
        try:
            data = dict([(key, self._fields[key].validate(None if object is None or not key in object.keys() else object[key])) for key in self._fields.keys()])
        except Exceptions.ValidationException as V:
            raise type(V)(f"{self._name}.{V.name}",V.vmessage)
        s = set(data.values())
        if len(s) == 1 and None in s and not self._required:
            return None
        elif len(s) == 1 and None in s:
            raise Exceptions.EmptyObjectException(self._name,"Required object is empty.")
        return self.__nt(**data)

    def optional(self)->"Schema":
        return super(Schema,self).optional()