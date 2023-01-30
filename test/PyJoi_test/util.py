from unittest import mock
from PyJoi import Exceptions

class TestException(Exceptions.ValidationException):
    pass

class SchemaMock(mock.Mock):
    def __init__(self, **kwargs):
        super(mock.Mock,self).__init__(**kwargs)
        self._depends_on = {}