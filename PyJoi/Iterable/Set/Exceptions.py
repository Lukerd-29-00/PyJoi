from ... import Exceptions

class DuplicateException(Exceptions.InvalidElementException):
    """Indicates that a set schema encountered a duplicate."""
    pass