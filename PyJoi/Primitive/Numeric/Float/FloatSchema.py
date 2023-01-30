from .. import Numeric
import typing
from .... import Ref

T = typing.TypeVar("T",float,typing.Optional[float])
class FloatSchema(typing.Generic[T],Numeric.Numeric[T]):
    @typing.overload
    def whitelist(self,*items: float)->"FloatSchema[T]":
        pass
    @typing.overload
    def whitelist(self,items: typing.Iterable[float])->"FloatSchema[T]":
        pass
    def whitelist(self,*items: typing.Union[float,typing.Iterable[float]])->"FloatSchema[T]":
        return super(Numeric.Numeric,self).whitelist(items,primitive=float)

    @typing.overload
    def blacklist(self,*items: float)->"FloatSchema[T]":
        pass
    @typing.overload
    def blacklist(self,items: typing.Iterable[float])->"FloatSchema[T]":
        pass
    def blacklist(self,*items: typing.Union[float,typing.Iterable[float]])->"FloatSchema[T]":
        return super(Numeric.Numeric,self).blacklist(items,primitive=float)

    if typing.TYPE_CHECKING:
        def max(self,new_max: typing.Union[float,Ref[float]])->"FloatSchema[T]":
            pass

        def min(self,new_min: typing.Union[float,Ref[float]])->"FloatSchema[T]":
            pass
    
        def optional(self)->"FloatSchema[typing.Optional[float]]":
            pass