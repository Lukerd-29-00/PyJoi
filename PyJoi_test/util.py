from unittest import mock
from PyJoi import Exceptions
import PyJoi
from PyJoi import AbstractSchema

class TestException(Exceptions.ValidationException):
    pass

class SchemaMock(mock.Mock):
    def __init__(self, **kwargs):
        super(mock.Mock,self).__init__(**kwargs)
        self._depends_on = {}
        self._name = None

    def _add_ref(self,ref: PyJoi.Ref)->None:
        self._depends_on[ref] = AbstractSchema.empty
        ref._schema = self
    
    def _add_parent_refs(self):
        for ref in self._depends_on.keys():
            if ref.root == '' and self._parent != None:
                self._parent._add_parent_ref(ref)

    def _add_parent_ref(self, ref: PyJoi.Ref):
        self._add_ref(PyJoi.Ref(ref._path))
        if self._parent != None:
            self._parent._add_parent_ref(ref)