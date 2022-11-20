import typing
import abc
from . import Ref
if typing.TYPE_CHECKING:
    from .SchemaSrc import Schema

class AbstractSchema(abc.ABC):
    _required: bool
    _parent: typing.Optional["Schema"] = None
    _root: "Schema"
    _depends_on: typing.Set[Ref.Ref]
    R = typing.TypeVar("R")

    def optional(self)->"AbstractSchema":
        """Indicates that this field is optional. An optional Schema will also accept empty objects. Any missing fields will be assigned to None."""
        self._required = False
        return self

    def _add_ref(self,ref: Ref.Ref)->None:
        #This is safe to do recursively because it only needs to be done when creating the Schema, so it's okay if it's slow.
        self._depends_on.add(ref)
        if not self._parent == self._root:
            path = str(ref).split(".")
            self._parent._add_ref(Ref.Ref("".join[path[:-1]]))

    def _get_ref_value(self,ref: Ref.Ref[R])->R:
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