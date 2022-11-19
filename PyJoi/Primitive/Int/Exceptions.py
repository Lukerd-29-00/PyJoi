from .. import Exceptions
import abc

class NotAnIntException(Exceptions.InvalidPrimitiveTypeException):
    pass

class InvalidSizeException(Exceptions.InvalidPrimitiveElementException,abc.ABC):
    pass

class TooSmallException(InvalidSizeException):
    pass

class TooBigException(InvalidSizeException):
    pass

class NonMultipleException(Exceptions.InvalidPrimitiveElementException):
    pass

class MissingIntException(Exceptions.MissingPrimitiveException):
    pass