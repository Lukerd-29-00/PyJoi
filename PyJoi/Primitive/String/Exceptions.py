from .. import Exceptions
import abc

class MissingStringException(Exceptions.MissingPrimitiveException):
    """Thrown if the string is missing when it is required."""
    pass

class InvalidStringException(Exceptions.InvalidPrimitiveElementException,abc.ABC):
    """Thrown if a string is provided that does not match the schema."""
    pass

class NotAStringException(Exceptions.InvalidPrimitiveTypeException):
    pass

class IncorrectLengthException(InvalidStringException,abc.ABC):
    """Thrown if a string does not match a length rule of the schema"""
    pass

class MatchesBlackistException(Exceptions.BlackListedValueException):
    pass

class NoWhiteListException(Exceptions.NonWhiteListedValueException):
    pass

class TooShortException(IncorrectLengthException):
    pass

class TooLongException(IncorrectLengthException):
    pass

class NonMatchingLengthException(IncorrectLengthException):
    pass