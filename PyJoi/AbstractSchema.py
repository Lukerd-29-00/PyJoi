import typing
import abc
T = typing.TypeVar("T")
class AbstractSchema(abc.ABC,typing.Generic[T]):
    name: str
    required: bool

    @typing.overload
    @abc.abstractmethod
    def __init__(self, required: bool = True):
        """Instantiate a Schema as part of another Schema."""
        pass

    @typing.overload
    @abc.abstractmethod
    def __init__(self,name: str, required: bool = True):
        pass

    @typing.overload
    @abc.abstractmethod
    def validate(self,object: typing.Dict[str,any])->typing.Optional[T]:
        """Validate some input using this schema."""
        pass

    @typing.overload
    @abc.abstractmethod
    def validate(self,value: T)->typing.Optional[T]:
        pass

    def optional(self)->"AbstractSchema[T]":
        """Indicates that this field is optional. An optional Schema will also accept empty objects. Any missing fields will be assigned to None."""
        self.required = False
        return self

    def __hash__(self)->int:
        return hash(self.name)