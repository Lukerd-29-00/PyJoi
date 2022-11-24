import abc
from .. import PrimitiveSchema
import typing
from ...RefSrc import Ref

class IIntSchema(PrimitiveSchema[int],abc.ABC):

    @typing.overload
    def whitelist(self,*items: int)->"IIntSchema":
        pass
    @typing.overload
    def whitelist(self,items: typing.Iterable[int])->"IIntSchema":
        pass
    def whitelist(self,*items: typing.Union[int,typing.Iterable[int]])->"IIntSchema":
        return super(IIntSchema,self).whitelist(items,primitive=int)

    @typing.overload
    def blacklist(self,*items: int)->"IIntSchema":
        pass
    @typing.overload
    def blacklist(self,items: typing.Iterable[int])->"IIntSchema":
        pass
    def blacklist(self,*items: typing.Union[int,typing.Iterable[int]])->"IIntSchema":
        return super(IIntSchema,self).blacklist(items,primitive=int)       

    @abc.abstractmethod
    def validate(self,value: any)->typing.Optional[int]:
        pass

    @abc.abstractmethod
    def max(self,new_max: typing.Union[Ref[int],int])->"IIntSchema":
        pass

    @abc.abstractmethod
    def min(self, new_max: typing.Union[Ref[int],int])->"IIntSchema":
        pass
    
    @abc.abstractmethod
    def multiple(self,new_base: typing.Union[Ref[int],int])->"IIntSchema":
        pass

    @abc.abstractmethod
    def positive(self)->"IIntSchema":
        pass

    @abc.abstractmethod
    def negative(self)->"IIntSchema":
        pass

    @abc.abstractmethod
    def port(self)->"IIntSchema":
        pass

    @abc.abstractmethod
    def port_nonadmin(self)->"IIntSchema":
        pass

    def optional(self)->"IIntSchema":
        return super(IIntSchema,self).optional()