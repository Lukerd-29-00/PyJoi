import typing
from . import Exceptions
from .AbstractSchema import AbstractSchema
import collections
from collections import abc

def value_from_path(path: typing.List[str], data: typing.Dict[str,any]):
        item = data
        for i in range(len(path)):
            item = item[path[i]]
            if i != len(path)-1:
                item = dict(item._asdict())
        return item

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
        self._contains.add(item)

    def prepend(self, item: S)->None:
        if not item in self._contains:
            self._list = [item] + self._list
        self._contains.add(item)

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
        super(Schema,self).__init__(name,required=required)
        if kwargs:
            self._fields = dict(kwargs)
            for k in self._fields.keys():
                self._fields[k]._name = k
                self._fields[k]._parent = self
                self._fields[k]._add_parent_refs()

    def primary_key(self, *keys: str)->"Schema[T]":
        self._primary_key = set(keys)



    def validate(self,object: typing.Optional[typing.Dict[str,any]])->typing.Optional[T]:
        """Validate an object (Python dictionary from strings to anything that can be represented by another Schema).

        Args:
            object: The object being validated. Must be a dictionary or None.
        
        Returns:
            The dictionary put in, or None if the input was empty or None. An exception will be thrown if the validation fails.
        """
        if not self._fields:
            raise ValueError("Error: empty Schema encountered!") #TODO: Make these assertions so they can be optimized out for production.
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
                if self._parent != None and ref.path[0] == '':
                    self._fields[key]._depends_on[ref] = self._depends_on[ref] #Inject any values from resolved refs injected from above.
                else:
                    Keys.append(ref.path[0] if ref.path[0] != '' else ref.path[1])                
            Keys.append(key)
        data = {}
        try:
            for key in Keys:
                for dep in self._fields[key]._depends_on.keys():
                    if dep.root != '' or self._parent == None:
                        path = dep.path
                        self._fields[key]._depends_on[dep] = value_from_path(path if path[0] != '' else path[1:],data)
                data[key] = self._fields[key].validate(None if not key in object.keys() else object[key])
        except Exceptions.ValidationException as V:
            raise type(V)(f"{self._name}.{V.name}",V.vmessage)
        for value in data.values():
            if value != None:
                return nt(**data)
        if self._required:
            raise Exceptions.EmptyObjectException(self._name,"required object was empty!")
        else:
            return None

    def optional(self)->"Schema[T]":
        return super(Schema,self).optional()