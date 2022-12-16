"""This is an object that helps items within a schema reference each other.

Refs paths are represented as teh objects that contain the value followed by the value separated by dots.

Example usage:
Schema("s",
    value1=Schema().something(Ref("s.value2")), or just "value2"
    value2=Schema()
)

Schema("s",

    object1=Schema(
        value=Schema().something(Ref("s.bound"))
    ),
    bound=Schema()
)

Schema("s",
    object1=Schema(
        value=Schema()
    ),
    bound=Schema().something(Ref("s.object1.bound")) or just "object1.bound"
)
"""
import typing
if typing.TYPE_CHECKING:
    from .AbstractSchema import AbstractSchema
#Indicates the type of the data this Ref object references.
T = typing.TypeVar("T")
class Ref(typing.Generic[T]):
    """Indicates another schema when passed as argument to some schema methods. Basically just a wrapper around the _path string attribute."""
    _path: str
    _schema: "AbstractSchema[any,any,str]"

    @property
    def value(self)->T:
        return self._schema._depends_on[self]
    
    @property
    def path(self)->typing.List[str]:
        return self._path.split('.')

    @property
    def root(self)->str:
        return self._path.split('.')[0]

    def __init__(self,path: str):
        self._path = path

    def __str__(self)->str:
        return self._path

    def __repr__(self)->str:
        return self._path

    def __eq__(self, other: "Ref")->str:
        return self._path == other._path
    
    def __hash__(self)->int:
        return hash(self._path)