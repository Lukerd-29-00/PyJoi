from .SchemaSrc import Schema
from .RefSrc import Ref
from .Primitive.Str import StrSchema
from .Primitive.Numeric.Int import IntSchema
from .Primitive.Numeric.Float import FloatSchema
from .Iterable.List import ListSchema
from .Iterable import IterableSchema
from .Iterable.Set import SetSchema
from .Primitive.Bool import BoolSchema
import typing

def int(name: typing.Optional[str] = None)->IntSchema.IntSchema[int]:
    """Create an int schema."""
    return IntSchema.IntSchema(name)

def float(name: typing.Optional[str] = None)->FloatSchema.FloatSchema[float]:
    return FloatSchema.FloatSchema(name)

def list(name: typing.Optional[str] = None)->ListSchema.ListSchema[typing.List]:
    return ListSchema.ListSchema(name)

def iterable(name: typing.Optional[str] = None)->IterableSchema.IterableSchema[typing.Iterable]:
    return IterableSchema.IterableSchema(name)

def set(name: typing.Optional[str] = None)->SetSchema.SetSchema[typing.Set]:
    return SetSchema.SetSchema(name)

def bool(name: typing.Optional[str] = None)->BoolSchema.BoolSchema[bool]:
    return BoolSchema.BoolSchema(name)

def str(name: typing.Optional[str] = None)->StrSchema.StrSchema[str]:
    """Create a string schema."""
    return StrSchema.StrSchema(name)