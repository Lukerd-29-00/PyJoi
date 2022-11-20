import abc
from .. import PrimitiveSchema
import typing

class IIntSchema(PrimitiveSchema[int],abc.ABC):

    @abc.abstractmethod
    def max(self,new_max: int)->"IIntSchema":
        pass

    @abc.abstractmethod
    def min(self, new_max: int)->"IIntSchema":
        pass
    
    @abc.abstractmethod
    def multiple(self,new_base: int)->"IIntSchema":
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

    @abc.abstractmethod
    def validate(self, value: any) -> typing.Optional[int]:
        pass

    def optional(self)->"IIntSchema":
        return super(IIntSchema,self).optional()