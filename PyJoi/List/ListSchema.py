""""""
from .. import AbstractSchema, Exceptions
import typing
from . import Exceptions as ListExceptions
import itertools

T = typing.TypeVar("T")
class ListSchema(typing.Generic[T],AbstractSchema.AbstractSchema[any,typing.List[T],typing.Optional[str]]):
    _has: typing.List[AbstractSchema.AbstractSchema]
    _matches: typing.Optional[AbstractSchema.AbstractSchema] = None

    def __init__(self,name: typing.Optional[str] = None, required: bool = True):
        super(ListSchema,self).__init__(name,required=required)
        self._has = []
    
    def validate(self,iterable: any)->typing.Optional[typing.List[T]]:
        if iterable == None and self._required:
            raise Exceptions.MissingElementException(self._name,"Missing required list")
        elif iterable == None:
            return None
        elif not isinstance(iterable,typing.Iterable):
            raise ListExceptions.NotIterableException(self._name,"expected an iterable")
        output = []
        hasFound = [False for _ in self._has]
        for item in iterable:
            subitem = item
            for i, schema in zip(itertools.count(0),self._has):
                try:
                    subitem = schema.validate(item) #Transformation will be performed according to the first schema in has that it happens to find that it matches. The behavior of multiple intersecting _has schemas with transformations is undefined.
                    hasFound[i] = True
                    break
                except Exceptions.ValidationException:
                    pass
            if self._matches != None:
                output.append(self._matches.validate(subitem)) #The _matches schema is done last.
            else:
                output.append(subitem)
        for found in hasFound:
            if not found:
                raise ListExceptions.RequiredItemNotFound(self._name,f"No match for a required schema was found.")
        return output

    def matches(self, schema: AbstractSchema.AbstractSchema)->"ListSchema[T]":
        self._matches = schema
        return self
    
    def has(self, *schemas: AbstractSchema.AbstractSchema)->"ListSchema[T]":
        self._has.extend(schemas)
        return self

    def optional(self)->"ListSchema[T]":
        self._required = False
        return self