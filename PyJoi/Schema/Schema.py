import typing
from .. import Exceptions
from ..AbstractSchema import AbstractSchema
from collections import abc
import abc as abstract

def value_from_path(path: typing.List[str], data: typing.Dict[str,any]):
        item = data
        for part in path:
            if isinstance(item,dict):
                item = item[part]
            elif isinstance(item, tuple):
                item = item[int(part)]
            else:
                item = item._asdict()[part]
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

N = typing.TypeVar("N")
class OutputType(typing.Generic[N],typing.Protocol):
    def __call__(self, **kwargs)->N:
        pass


T = typing.TypeVar("T")
class Schema(typing.Generic[T],AbstractSchema[T],abstract.ABC):
    _fields: typing.Dict[str,"AbstractSchema"] = None
    _name: str
    _required: bool = True
    _values: typing.Dict[str,any]
    _output_type: typing.Optional[OutputType[T]]

    def __init__(self, name: typing.Optional[str] = None):
        """Create a PyJoi Schema.
        
        Args:
            name: The optional name of the schema. If this Schema is nested within another one, its name will be inferred.
            required: Whether or not this schema is required for the enclosing object to be valid. Can be set to False with .optional().
        """
        super(Schema,self).__init__(name)

        for k in self._fields.keys():
            self._fields[k]._name = k
            self._fields[k]._parent = self
            self._fields[k]._add_parent_refs()

        

    def _validate(self,object: typing.Dict[str,any])->typing.Dict:
        """Validate an object (Python dictionary from strings to anything that can be represented by another Schema).

        Args:
            object: The object being validated. Must be a dictionary or None.
        
        Returns:
            The dictionary put in, or None if the input was empty or None. An exception will be thrown if the validation fails.
        """
        if not self._fields:
            raise ValueError("Error: empty Schema encountered!") #TODO: Make these assertions so they can be optimized out for production.
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
        return data

    if typing.TYPE_CHECKING:
        def optional(self)->"Schema[typing.Optional[T]]":
            pass