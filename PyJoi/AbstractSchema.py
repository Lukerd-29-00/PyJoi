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
    _depends_on: typing.Dict[Ref,any]
    R = typing.TypeVar("R")

    def __init__(self,name: typing.Optional[str] = None, required: bool = True):
        self._name = name
        self._required = required
        self._depends_on = {}

    def optional(self)->"AbstractSchema[T,V,N]":
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