from .SchemaSrc import Schema
from .RefSrc import Ref
from .Primitive.Str import StrSchema
from .Primitive.Numeric.Int import IntSchema
from .Iterable.List.ListSchema import ListSchema
from .Iterable.IterableSchema import IterableSchema
from .Iterable.Set.SetSchema import SetSchema
from .Primitive.Bool import BoolSchema
import typing

def str(name: typing.Optional[str] = None)->StrSchema.StrSchema[str]:
    """Create a string schema."""
    return StrSchema.StrSchema(name)

def int(name: typing.Optional[str] = None)->IntSchema.IntSchema[int]:
    """Create an int schema."""
    return IntSchema.IntSchema(name)

def list(name: typing.Optional[str] = None)->ListSchema:
    return ListSchema(name)

def iterable(name: typing.Optional[str] = None)->IterableSchema:
    return IterableSchema(name)

def set(name: typing.Optional[str] = None)->SetSchema:
    return SetSchema(name)

def bool(name: typing.Optional[str] = None)->BoolSchema:
    return BoolSchema.BoolSchema(name)