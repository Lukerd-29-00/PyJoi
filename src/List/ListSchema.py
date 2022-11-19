from .. import Schema
import typing

class ListSchema(Schema):
    _starts_with: typing.Optional[typing.Tuple[Schema]] = None
    _ends_with: typing.Optional[typing.Tuple[Schema]] = None
    _matches: typing.Set[Schema]
    _has: typing.Set[Schema]
    _min_len: typing.Optional[int] = None
    _max_len: typing.Optional[int] = None

    def __init__(self, name: str, required: bool = True):
        super(ListSchema,self).__init__(name,required=required)
        self._matches = set()
        self._has = set()

    def starts_with(self, *schemas: Schema)->"ListSchema":
        self._starts_with = tuple(schemas)
        return self

    def ends_with(self, *schemas: Schema)->"ListSchema":
        self._ends_with = tuple(schemas)
        return self
    
    def matches(self, *schemas: Schema)->"ListSchema":
        self._matches = self._matches.union(schemas)
        return self
    
    def has(self, *schemas: Schema)->"ListSchema":
        for schema in schemas:
            if not schema.required:
                raise ValueError("Has schemas cannot be optional!")
        self._has = self._has.union(schemas)

    def optional(self)->"ListSchema":
        return super(ListSchema,self).optional()