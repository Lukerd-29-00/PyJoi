from .. import Exceptions

class NotIterableException(Exceptions.InvalidTypeException):
    pass

class RequiredItemNotFound(Exceptions.InvalidElementException):
    pass

class EmptyIterableException(Exceptions.EmptyElementException):
    pass