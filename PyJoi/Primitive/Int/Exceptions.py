from .. import Exceptions
import abc

class NotAnIntException(Exceptions.InvalidPrimitiveTypeException):
    pass

class InvalidSizeException(Exceptions.InvalidPrimitiveElementException):
    pass

class NonMultipleException(Exceptions.InvalidPrimitiveElementException):
    pass

class MissingIntException(Exceptions.MissingPrimitiveException):
    pass