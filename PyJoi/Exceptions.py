import abc

class ValidationException(Exception,abc.ABC):
    name: str
    vmessage: str
    def __init__(self,name: str, message: str):
        self.name = name
        self.vmessage = message
        super(ValidationException,self).__init__(f"Validation failed: {name}: {message}")

class InvalidElementException(ValidationException,abc.ABC):
    """Thrown if an element is non-None, nonempty but does not match the schema."""
    pass

class EmptyElementException(ValidationException,abc.ABC):
    """Thrown if an element is not None but is empty (e.g. {} or []). Note that a dict with no recognized keys will also be considered "empty"."""
    pass

class MissingElementException(ValidationException,abc.ABC):
    """Thrown if an element that was expected was either missing or null."""
    pass

class InvalidTypeException(ValidationException,abc.ABC):
    """Thrown if the value provided does not match the schema's type."""
    pass

class EmptyObjectException(EmptyElementException):
    """Thrown if a Schema object is passed an empty Dict to validate()."""
    pass

class MissingObjectException(MissingElementException):
    """Thrown if a Dict was expected under a key but not found."""
    pass

class ObjectMissingKeyException(InvalidElementException):
    """Thrown by Schema.validate if a key that was expected was not found or mapped to something empty."""
    pass

class ObjectIncorrectKeyException(InvalidElementException):
    """Thrown by Schema.validate if a key is mapped to a nonempty value that does not match the schema somehow."""
    pass

class ObjectContainsWrongTypeException(ObjectMissingKeyException):
    """Thrown by Schema.validate if a key is mapped to a value of the wrong type."""
    pass

class NotAnObjectException(InvalidTypeException):
    """Thrown by Schema.validate if the value provided is not a Dict."""
    pass
