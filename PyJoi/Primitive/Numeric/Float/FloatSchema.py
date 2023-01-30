from .. import Numeric
import typing
from .... import Ref

class FloatSchema(Numeric.Numeric):
    @typing.overload
    def whitelist(self,*items: float)->"FloatSchema":
        pass
    @typing.overload
    def whitelist(self,items: typing.Iterable[float])->"FloatSchema":
        pass
    def whitelist(self,*items: typing.Union[float,typing.Iterable[float]])->"FloatSchema":
        return super(Numeric.Numeric,self).whitelist(items,primitive=float)

    @typing.overload
    def blacklist(self,*items: float)->"FloatSchema":
        pass
    @typing.overload
    def blacklist(self,items: typing.Iterable[float])->"FloatSchema":
        pass
    def blacklist(self,*items: typing.Union[float,typing.Iterable[float]])->"FloatSchema":
        return super(Numeric.Numeric,self).blacklist(items,primitive=float)

    if typing.TYPE_CHECKING:
        def max(self,new_max: typing.Union[float,Ref[float]]):
            pass

        def min(self,new_min: typing.Union[float,Ref[float]]):
            pass