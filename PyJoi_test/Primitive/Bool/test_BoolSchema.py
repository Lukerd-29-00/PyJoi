import PyJoi
from PyJoi.Primitive.Bool import BoolSchema
from .. import Common
import typing
from ... import util

class TestBoolSchema(Common.PrimitiveSchemaTest[bool,bool,BoolSchema.BoolSchema]):
    instance1 = True
    instance2 = False
    output_instance = True
    noninstance = "True"
    custom_fail = False
    custom_success = True

    def schema_factory(self, name: typing.Optional[str] = None) -> BoolSchema.BoolSchema[bool]:
        return PyJoi.bool()
    
    def _custom_check(self, name: str, x: bool)->bool:
        if x:
            return x
        else:
            raise util.TestException(name,f"{x} is not True.")

    def _custom_check_ref(self, name: str, x: bool, y: bool)->bool:
        if x and (not y):
            return x
        else:
            raise util.TestException(name,f"{x} is not true or {y} is not False.")