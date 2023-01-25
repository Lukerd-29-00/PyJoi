from .. import Primitive
import typing
from . import Exceptions
class BoolSchema(Primitive.PrimitiveSchema[bool]):

    def validate(self, value: any)->typing.Optional[bool]:
        if not isinstance(value,bool) and value != None:
            raise Exceptions.NotABoolException(self._name,f"{value} is not a boolean.")
        return super(BoolSchema,self).validate(value)