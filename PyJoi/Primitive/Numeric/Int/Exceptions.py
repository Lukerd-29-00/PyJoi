from ... import Exceptions
class NotAnIntException(Exceptions.InvalidPrimitiveTypeException):
    pass

class NonMultipleException(Exceptions.InvalidPrimitiveElementException):
    pass

class MissingIntException(Exceptions.MissingPrimitiveException):
    pass
