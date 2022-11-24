import typing
from . import Exceptions
from .AbstractSchema import AbstractSchema
from .Primitive.String.StringSchema import StringSchema as StringSchemaConstructor
from .Primitive.String import StringSchema
from .Primitive.Int.IntSchema import IntSchema as IntSchemaConstructor
from .List.ListSchema import ListSchema
from .Primitive.Int import IntSchema
import collections
from collections import abc
from .RefSrc import Ref

S = typing.TypeVar("S",bound=abc.Hashable)
class OrderedSet(typing.Generic[S]):
    _list: typing.List[S]
    _contains: typing.Set[S]

    def __init__(self,startWith: typing.Iterable[S] = []):
        self._contains = set()
        self._list = []
        for item in startWith:
            self.append(item)
    
    def append(self, item: S)->None:
        if not item in self._contains:
            self._contains.add(item)
            self._list.append(item)

    def clear(self)->None:
        self._contians = set()
        self._list.clear()

    def copy(self)->"OrderedSet[S]":
        return OrderedSet(self._list)

    def extend(self, newItems: typing.Iterable[S])->None:
        for item in newItems:
            if not item in self._contains:
                self._list.append(item)
        self._contains = self._contains.union(newItems)

    def __contains__(self, item: S)->bool:
        return item in self._contains

    def index(self,item: S)->int:
        return self._list.index(item)

    def insert(self,item: S, index: int)->None:
        if not item in self._contains:
            self._list.insert(item,index)

    def prepend(self, item: S)->None:
        if not item in self._contains:
            self._list = [item] + self._list

    def __getitem__(self,index: int)->S:
        return self._list[index]

    def __str__(self)->str:
        return f"{{{str(self._list)[1:-1]}}}"

    def __repr__(self)->str:
        return f"{{{str(self._list)[1:-1]}}}"

    def __iter__(self)->typing.Iterator[S]:
        return iter(self._list)

T = typing.TypeVar("T",bound=typing.NamedTuple)
class Schema(typing.Generic[T],AbstractSchema[typing.Optional[typing.Dict[str,any]],T,str]):
    _fields: typing.Dict[str,"AbstractSchema"] = None
    _name: str
    _required: bool = True
    _values: typing.Dict[str,any]

    def __init__(self, name: typing.Optional[str] = None, required: bool = True, **kwargs: "AbstractSchema"):
        """Create a PyJoi Schema.
        
        Args:
            name: The optional name of the schema. If this Schema is nested within another one, its name will be inferred.
            required: Whether or not this schema is required for the enclosing object to be valid. Can be set to False with .optional().
        """
        super(Schema,self).__init__()
        if kwargs:
            self._fields = dict(kwargs)
            for k in self._fields.keys():
                self._fields[k]._name = k
                self._fields[k]._parent = self
                self._fields[k]._add_parent_refs()
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

    def list(self)->ListSchema:
        return ListSchema(self._name,self._required)

    def _resolve_dependency_chain(self, ref: Ref, chain: OrderedSet)->None:
        for dependency in self._fields[ref._path]._depends_on.keys():
            if len(dependency._path.split('.')) == 1:
                self._resolve_dependency_chain(dependency,chain)
        chain.append(ref._path)

    def validate(self,object: typing.Optional[typing.Dict[str,any]])->typing.Optional[T]:
        """Validate an object (Python dictionary from strings to anything that can be represented by another Schema).

        Args:
            object: The object being validated. Must be a dictionary or None.
        
        Returns:
            The dictionary put in, or None if the input was empty or None. An exception will be thrown if the validation fails.
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
            raise Exceptions.NotAnObjectException(self._name,"expected to be associated with a dictionary but encountered something else.")
        nt = collections.namedtuple(self._name,self._fields.keys())
        Keys = OrderedSet[str]()
        for key in self._fields.keys():
            for ref in self._fields[key]._depends_on.keys():
                if len(ref._path.split('.')) == 1:
                    self._resolve_dependency_chain(ref,Keys)
                else:
                    pathComponents = (".".join(ref._path.split('.')[:-1]), ref._path.split('.')[-1])
                    self._fields[key]._depends_on[ref] = self._depends_on[Ref(pathComponents[0])].__getattribute__(pathComponents[1])
            Keys.append(key)
        data = {}
        try:
            for key in Keys:
                for dep in self._fields[key]._depends_on.keys():
                    if len(ref._path.split('.')) == 1:
                        self._fields[key]._depends_on[dep] = data[dep._path]
                data[key] = self._fields[key].validate(None if not key in object.keys() else object[key])
        except Exceptions.ValidationException as V:
            raise type(V)(f"{self._name}.{V.name}",V.vmessage)
        s = set(data.values())
        if len(s) == 1 and None in s and not self._required:
            return None
        elif len(s) == 1 and None in s:
            raise Exceptions.EmptyObjectException(self._name,"Required object is empty.")
        return nt(**data)

    def optional(self)->"Schema[T]":
        return super(Schema,self).optional()