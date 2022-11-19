from .. import Exceptions
import abc

class MissingPrimitiveException(Exceptions.MissingElementException,abc.ABC):
    """Thrown if a primitive value was expected but not found."""
    pass

class InvalidPrimitiveElementException(Exceptions.InvalidElementException,abc.ABC):
    """Thrown if a primitive value does not match the PrmitiveSchema provided."""
    pass

class InvalidPrimitiveTypeException(Exceptions.InvalidTypeException):
    """Thrown if the type of the value provided does not match the schema."""
    pass

class BlackListedValueException(Exceptions.ValidationException):
    """Thrown if a primitive element has a value excluded by a blacklist."""
    pass

class NonWhiteListedValueException(Exceptions.ValidationException):
    """Thrown if a value from outside a whitelist is found."""
    pass