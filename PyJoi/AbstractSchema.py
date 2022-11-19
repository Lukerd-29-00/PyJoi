import typing
import abc

class AbstractSchema(abc.ABC):
    name: str
    required: bool
    V = typing.TypeVar("V",str,int,typing.Set,typing.List,float)

    @typing.overload
    @abc.abstractmethod
    def __init__(self,name: str, required: bool = True):
        """Instantiate a Schema with just a name"""
        pass

    @typing.overload
    @abc.abstractmethod
    def __init__(self,name: str, required: bool = True, **kwargs: typing.Dict[str,"AbstractSchema"]):
        """Instantiate a schema with a name and the schema's shape."""
        pass

    def string(self):
        """Create a string schema."""
        from .Primitive.String.StringSchema import StringSchema
        return StringSchema(self.name,required=self.required)

    def int(self):
        """Create an int schema."""
        from .Primitive.Int.IntSchema import IntSchema
        return IntSchema(self.name,required=self.required)

    @abc.abstractmethod
    def optional(self)->"AbstractSchema":
        """Indicate that this field is not required for the input to be valid."""
        pass

    @typing.overload
    @abc.abstractmethod
    def validate(self,value: V)->V:
        pass

    @typing.overload
    @abc.abstractmethod
    def validate(self,object: typing.Dict[str,any])->typing.NamedTuple:
        """Validate some input using this schema."""
        pass

    def optional(self)->"AbstractSchema":
        """Indicates that this field is optional. An optional Schema will also accept empty objects. Any missing fields will be assigned to None."""
        self.required = False
        return self

    def __hash__(self)->int:
        return hash(self.name)