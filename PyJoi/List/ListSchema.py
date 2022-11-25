""""""
from .. import AbstractSchema, Exceptions
import typing
from . import Exceptions as ListExceptions
import itertools
from .. import SchemaSrc as Schema

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
        if not zip([1],iterable) and self._required: #The zip expression is used to determine if the iterable is empty. Depending on the iterable, this may be considerably computationally easier than calling len(), and will never be much worse.
            raise ListExceptions.EmptyListException(self._name,"required list was empty.")
        elif not zip([1],iterable):
            return None
        output = []
        hasFound = [False for _ in self._has]
        for item in iterable:
            subitem = item
            for i, schema in zip(itertools.count(0),self._has):
                try:
                    schema._depends_on = dict([(k, self._depends_on[k]) for k in schema._depends_on.keys()])
                    subitem = schema.validate(item) #Transformation will be performed according to the first schema in has that it happens to find that it matches. The behavior of multiple intersecting _has schemas with transformations is undefined.
                    hasFound[i] = True
                    break
                except Exceptions.ValidationException:
                    pass
            if self._matches != None:
                self._matches._depends_on = dict([(k, self._depends_on[k]) for k in self._matches._depends_on.keys()])
                try:
                    output.append(self._matches.validate(subitem)) #The _matches schema is done last.
                except Exceptions.ValidationException as V:
                    raise type(V)(self._name,V.vmessage)
            else:
                output.append(subitem)
        for found in hasFound:
            if not found:
                raise ListExceptions.RequiredItemNotFound(self._name,f"No match for a required schema was found.")
        return output

    def matches(self, schema: AbstractSchema.AbstractSchema)->"ListSchema[T]":
        if not isinstance(schema,Schema.Schema):
            self._depends_on.update(schema._depends_on)
        self._matches = schema
        return self
    
    def has(self, *schemas: AbstractSchema.AbstractSchema)->"ListSchema[T]":
        self._has.extend(schemas)
        return self

    def optional(self)->"ListSchema[T]":
        self._required = False
        return self