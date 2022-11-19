from . import Schema
import typing

class tst2():
    x: str

class tst(typing.NamedTuple):
    s: str
    a: typing.Optional[tst2]
    b: int

class MySchema(Schema):
    def validate(self, other: typing.Dict[str,any])->tst:
        return super(MySchema,self).validate(other)

if __name__ == "__main__":
    schema = MySchema("tst",
        s=Schema("s").string().hex(),
        a=Schema("a",
            x=Schema("x").string()
        ).optional(),
        b=Schema("b").int().positive()
    )
    t = schema.validate({"s": "ab", "b": 0})
    print(t.s)
    print(t.a)
    print(t.b)