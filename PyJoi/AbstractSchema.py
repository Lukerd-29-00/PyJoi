import typing
import abc
from .RefSrc import Ref
if typing.TYPE_CHECKING:
    from .SchemaSrc import Schema

T = typing.TypeVar("T")
V = typing.TypeVar("V")
N = typing.TypeVar("N",str,typing.Optional[str])
class AbstractSchema(abc.ABC,typing.Generic[T,V,N]):
    _name: N
    _required: bool
    _parent: typing.Optional["Schema"] = None
    _root: "Schema"
    _depends_on: typing.Dict[Ref,any]
    R = typing.TypeVar("R")

    def __init__(self):
        self._depends_on = {}

    def optional(self)->"AbstractSchema":
        """Indicates that this field is optional. An optional Schema will also accept empty objects. Any missing fields will be assigned to None."""
        self._required = False
        return self

    def _add_ref(self,ref: Ref)->None:
        self._depends_on[ref] = None
        ref._schema = self
    
    def _add_parent_refs(self):
        for ref in self._depends_on.keys():
            self._add_parent_ref(ref)

    def _add_parent_ref(self, ref: Ref):
        path = str(ref).split('.')
        if len(path) > 1:
            self._parent._add_ref(Ref(".".join(path[:-1])))
        
        
    @abc.abstractmethod
    def validate(self, value: T)->typing.Optional[V]:
        pass

    def _get_ref_value(self,ref: Ref[R])->R:
        parent = self._parent
        node = self
        path = str(ref).split(".")
        i = len(path)-1
        #We do this iteratively instead of recursively because it is performed during validation, so recursion would be a problematic waste of time and memory.
        for target in path[::-1]:
            if target in parent._fields.keys() or parent == None:
                break
            parent = parent._parent
            i -= 1
        if parent == None:
            raise ValueError(f"{path} not found in schema {self._root._name}")
        node = parent
        for target in path[i+1:]:
            try:
                if target in node._fields.keys():
                    node = node._fields[target]
                else:
                    raise ValueError(f"{path} not found in schema {self._root._name}")
            except AttributeError:
                raise ValueError(f"{path} not found in schema {self._root._name}")
        return node._parent._values[target[-1]]