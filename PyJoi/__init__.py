from .SchemaSrc import Schema
from .RefSrc import Ref
from .Primitive.String.StringSchema import StringSchema as StringSchemaConstructor
from .Primitive.String import StringSchema
from .Primitive.Int.IntSchema import IntSchema as IntSchemaConstructor
from .Stream.List.ListSchema import ListSchema
from .Stream.StreamSchema import StreamSchema
from .Stream.Set.SetSchema import SetSchema
from .Primitive.Int import IntSchema
from .Primitive.Bool import BoolSchema
import typing

def string(name: typing.Optional[str] = None)->"StringSchema":
    """Create a string schema."""
    return StringSchemaConstructor(name)

def int(name: typing.Optional[str] = None)->"IntSchema":
    """Create an int schema."""
    return IntSchemaConstructor(name)

def list(name: typing.Optional[str] = None)->"ListSchema":
    return ListSchema(name)

def stream(name: typing.Optional[str] = None)->"StreamSchema":
    return StreamSchema(name)

def set(name: typing.Optional[str] = None)->"SetSchema":
    return SetSchema(name)

def bool(name: typing.Optional[str] = None)->"BoolSchema":
    return BoolSchema(name)