import typing
import abc
from .. import PrimitiveSchema

class IStringSchema(PrimitiveSchema[str],abc.ABC):

    @typing.overload
    @abc.abstractmethod
    def whitelist_patterns(self, pattern: str)->"IStringSchema":
        """Whitelist a regular expression."""
        pass

    @typing.overload
    @abc.abstractmethod
    def whitelist_patterns(self, patterns: typing.Iterable[str])->"IStringSchema":
        """Whitelist several regular expressions; the string only needs to match one."""
        pass

    @typing.overload
    @abc.abstractmethod
    def blacklist_patterns(self, pattern: str)->"IStringSchema":
        """Blacklist a regular expression."""
        pass

    @typing.overload
    @abc.abstractmethod
    def blacklist_patterns(self, patterns: typing.Iterable[str])->"IStringSchema":
        """Blacklist several regular expressions."""
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