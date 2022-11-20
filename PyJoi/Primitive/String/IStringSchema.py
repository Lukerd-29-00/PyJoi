import abc
from .. import PrimitiveSchema

class IStringSchema(PrimitiveSchema[str],abc.ABC):

    @abc.abstractmethod
    def whitelist_pattern(self, pattern: str)->"IStringSchema":
        """Whitelist a regular expression."""
        pass

    @abc.abstractmethod
    def blacklist_pattern(self, pattern: str)->"IStringSchema":
        """Blacklist a regular expression."""
        pass

    @abc.abstractmethod
    def len(self,new_len: int)->"IStringSchema":
        """Set the length of the desired string; the validation will succeed iff the length matches this value."""
        pass
    
    @abc.abstractmethod
    def min_len(self,new_min: int)->"IStringSchema":
        """Set the minimum length for a string."""
        pass

    @abc.abstractmethod
    def max_len(self, new_max: int)->"IStringSchema":
        """Sets the maximum length for a string."""
        pass

    @abc.abstractmethod
    def hex(self)->"IStringSchema":
        """Match hex strings; expects an even-length of a-f0-9"""
        pass

    def optional(self)->"IStringSchema":
        """Indicates that this string is optional."""
        return super(IStringSchema,self).optional()

    def base64(self)->"IBase64Schema":
        pass

class IBase64Schema(IStringSchema,abc.ABC):

    @abc.abstractmethod
    def unpadded(self)->"IBase64Schema":
        pass
    
    @abc.abstractmethod
    def urlsafe(self)->"IBase64Schema":
        pass