import typing
import abc
class AbstractSchema(abc.ABC):
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

    def optional(self)->"AbstractSchema":
        """Indicates that this field is optional. An optional Schema will also accept empty objects. Any missing fields will be assigned to None."""
        self.required = False
        return self

    def __hash__(self)->int:
        return hash(self.name)