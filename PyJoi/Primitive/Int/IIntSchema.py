import abc
from .. import PrimitiveSchema

class IIntSchema(PrimitiveSchema[int],abc.ABC):
    def max(self,new_max: int)->"IIntSchema":
        pass

    def min(self, new_max: int)->"IIntSchema":
        pass
    
    def multiple(self,new_base: int)->"IIntSchema":
        pass

    def positive(self)->"IIntSchema":
        pass

    def negative(self)->"IIntSchema":
        pass

    def port(self)->"IIntSchema":
        pass

    def port_nonadmin(self)->"IIntSchema":
        pass

    def optional(self)->"IIntSchema":
        pass