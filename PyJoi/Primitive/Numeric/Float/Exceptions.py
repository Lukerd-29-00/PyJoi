from ... import Exceptions

class InvalidPrecisionException(Exceptions.InvalidPrimitiveElementException):
    pass

class NotAFloatException(Exceptions.InvalidPrimitiveTypeException):
    pass