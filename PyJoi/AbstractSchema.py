import typing
import abc
from .RefSrc import Ref
from . import Exceptions
if typing.TYPE_CHECKING:
    from .SchemaSrc import Schema

class Empty():
    """This is here as the initial value assigned to each ref before being resolved at runtime. This makes it so that an UnresolvedRefError is raised if the ref is not resolved before its value is needed."""
    def __bool__(self):
        return False
    def __getattr__(self, __name: str)->None:
        raise Exceptions.UnresolvedRefError("Empty ref was used!")

empty = Empty() #This is used instead of None for initial dependency values in order to raise this custom error if an invalid ref is invoked.

V = typing.TypeVar("V")
class AbstractSchema(abc.ABC,typing.Generic[V]):
    _name: typing.Optional[str]
    _required: bool = True
    _parent: typing.Optional["Schema"] = None
    _depends_on: typing.Dict[Ref,any]
    _or: typing.Optional["AbstractSchema"] = None
    T = typing.TypeVar("T")

    def __init__(self, name: str):
        self._name = name
        self._depends_on = {}

    def optional(self)->"AbstractSchema[typing.Optional[V]]":
        """Indicates that this field is optional. An optional Schema will also accept empty objects. Any missing fields will be assigned to None."""
        self._required = False
        return self

    def _add_ref(self,ref: Ref)->None:
        self._depends_on[ref] = empty
        ref._schema = self
    
    def _add_parent_refs(self):
        for ref in self._depends_on.keys():
            if ref.root == '' and self._parent != None:
                self._parent._add_parent_ref(ref)

    def _add_parent_ref(self, ref: Ref):
        self._add_ref(Ref(ref._path))
        if self._parent != None:
            self._parent._add_parent_ref(ref)
    
    def union(self, schema: 'AbstractSchema[T]')->'AbstractSchema[typing.Union[T,V]]':
        self._or = schema
        return self
    
    @abc.abstractmethod
    def _validate(self, value: any)->V:
        pass

    def validate(self, value: any)->V:
        try:
            return self._validate(value)
        except Exceptions.ValidationException as V:
            if self._or != None:
                return self._or.validate(value)
            else:
                raise V

