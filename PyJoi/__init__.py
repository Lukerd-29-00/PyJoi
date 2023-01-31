from .SchemaSrc import Schema
from .RefSrc import Ref
from .Primitive.Str import StrSchema
from .Primitive.Numeric.Int.IntSchema import IntSchema
from .Iterable.List.ListSchema import ListSchema
from .Iterable.IterableSchema import IterableSchema
from .Iterable.Set.SetSchema import SetSchema
from .Primitive.Numeric.Int.IntSchema import IntSchema
from .Primitive.Bool import BoolSchema
import typing

def str(name: typing.Optional[str] = None)->StrSchema.StrSchema[str]:
    """Create a string schema."""
    return StrSchema.StrSchema(name)

def int(name: typing.Optional[str] = None)->IntSchema[int]:
    """Create an int schema."""
    return IntSchema(name)

def list(name: typing.Optional[str] = None)->ListSchema:
    return ListSchema(name)

def iterable(name: typing.Optional[str] = None)->IterableSchema:
    return IterableSchema(name)

def set(name: typing.Optional[str] = None)->SetSchema:
    return SetSchema(name)

def bool(name: typing.Optional[str] = None)->BoolSchema:
    return BoolSchema(name)