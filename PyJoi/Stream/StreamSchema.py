""""""
from .. import AbstractSchema, Exceptions
import typing
from . import Exceptions as StreamExceptions
import itertools
from .. import SchemaSrc as Schema

T = typing.TypeVar("T")
A = typing.TypeVar("A")
class StreamSchema(typing.Generic[T],AbstractSchema.AbstractSchema[any,T,typing.Optional[str]]):
    """This is a schema designed to match any iterable object. Unlike other schemas, this will not return None if the iterable is empty or missing; the output will simply be an empty iterable. Note that a Ref to a StreamSchema instance is undefined behavior."""
    _has: typing.List[AbstractSchema.AbstractSchema]
    _matches: typing.Optional[AbstractSchema.AbstractSchema] = None

    def __init__(self,name: typing.Optional[str] = None, required: bool = True):
        """Initialize a StreamSchema."""
        super(StreamSchema,self).__init__(name,required=required)
        self._has = []
    
    def validate(self,iterable: any)->typing.Iterable[T]:
        """Validate some input using this schema. Note that this validate function is a generator, not a traditional function."""
        if iterable == None and self._required:
            raise Exceptions.MissingElementException(self._name,"Missing required list")
        elif iterable == None:
            return
        elif not isinstance(iterable,typing.Iterable):
            raise StreamExceptions.NotIterableException(self._name,"expected an iterable")
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
                    yield self._matches.validate(subitem) #The _matches schema is done last.
                except Exceptions.ValidationException as V:
                    raise type(V)(self._name,V.vmessage)
            else:
                yield subitem
        for found in hasFound:
            if not found:
                raise StreamExceptions.RequiredItemNotFound(self._name,f"No match for a required schema was found.")
        return

    def matches(self, schema: AbstractSchema.AbstractSchema[any,A,any])->"StreamSchema[A]":
        """Assert that the stream passed to validate must match the provided schema. Transformations supplied by .custom will be applied."""
        self._matches = schema
        schema._parent = self
        if isinstance(schema,Schema.Schema):
            schema._add_parent_refs()
        else:
            self._depends_on.update(schema._depends_on)
        return self
    
    def has(self, *schemas: AbstractSchema.AbstractSchema)->"StreamSchema[T]":
        """Assert that the stream contains at least one element matching the provided schema(s). Note that the error for this is thown only after iteration is complete."""
        self._has.extend(schemas)
        return self

    def optional(self)->"StreamSchema[T]":
        """If the schema is optional, a missing or null value will be interpreted as an empty iterable."""
        self._required = False
        return self