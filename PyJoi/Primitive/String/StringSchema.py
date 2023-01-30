from . import Exceptions
import typing
import re
from .. import PrimitiveSchema

T = typing.TypeVar("T",str,typing.Optional[str])

HexPattern = re.compile(r"^(?:[a-f0-9][a-f0-9])*$")

PaddedB64Pattern = re.compile(r"^(?:[A-Za-z0-9\+/]{4})*(?:[A-Za-z0-9\+/]{2}[A-Za-z0-9\+/=]{2})?$")
UnpaddedB64Pattern = re.compile(r"^(?:[A-Za-z0-9\+/]{4})*(?:[A-Za-z0-9\+/]{2,3})?$")

PaddedUrlSafeB64Pattern = re.compile(r"^(?:[A-Za-z0-9\-_]{4})*(?:[A-Za-z0-9\-_]{2}[A-Za-z0-9\-_=]{2})?$")
UnPaddedUrlSafeB64Pattern = re.compile(r"^(?:[A-Za-z0-9\-_]{4})*(?:[A-Za-z0-9\-_]{2,3})?$")

class StringSchema(typing.Generic[T],PrimitiveSchema[T]):
    def _matches(self,string: str, pattern: re.Pattern)->str:
        if re.match(pattern,string) != None:
            return string
        raise Exceptions.NoWhiteListException(self._name,f"String {string} does not match pattern {pattern.pattern}")

    def _not_matches(self, string: str, pattern: re.Pattern)->str:
        if re.match(pattern,string) == None:
            return string
        raise Exceptions.MatchesBlackistException(self._name,f"String {string} matches blacklisted pattern {pattern.pattern}")

    def whitelist_pattern(self, pattern: str)->"StringSchema[T]":
        whitelist_regex = re.compile(pattern)
        self._checks.append(lambda value: self._matches(value,whitelist_regex))
        return self

    def blacklist_pattern(self, pattern: str)->"StringSchema[T]":
        blacklist_regex = re.compile(pattern)
        self._checks.append(lambda value: self._not_matches(value,blacklist_regex))
        return self

    def _check_len(self, string: str, comparator: typing.Callable[[int],bool])->str:
        if comparator(len(string)):
            return string
        raise Exceptions.NonMatchingLengthException(self._name,f"String {string} has an incorrect length of {len(string)}")

    def len(self,new_len: int)->"StringSchema[T]":
        self._checks.append(lambda value: self._check_len(value,new_len.__eq__))
        return self
    
    def min_len(self,new_min: int)->"StringSchema[T]":
        self._checks.append(lambda value: self._check_len(value,new_min.__le__))
        return self

    def max_len(self, new_max: int)->"StringSchema[T]":
        self._checks.append(lambda value: self._check_len(value,new_max.__ge__))
        return self

    def hex(self)->"StringSchema[T]":
        self._checks.append(lambda value: self._matches(value,HexPattern))
        return self

    def base64(self)->"Base64Schema[T]":
        return Base64Schema(self._name)

    def _validate(self,value: any)->T:
        if not isinstance(value,str) and value != None:
            raise Exceptions.NotAStringException(self._name,f"expected a string, got {value}")
        return super(StringSchema,self)._validate(value)

    if typing.TYPE_CHECKING:
        def optional(self)->"StringSchema[typing.Optional[str]]":
            pass

        def whitelist(self,*items: str)->"StringSchema[T]":
            pass

        def blacklist(self,*items: str)->"StringSchema[T]":
            pass

B = typing.TypeVar("B",str,typing.Optional[str])

class Base64Schema(typing.Generic[B],StringSchema[B]):
    __padded: bool = True
    __urlsafe: bool = False

    def __init__(self,name: typing.Optional[str] = None):
        super(Base64Schema,self).__init__(name)
        self._checks.append(lambda value: self._check(value))

    def base64(self):
        raise ValueError("This is already base 64!")
    
    def urlsafe(self)->"Base64Schema[B]":
        self.__urlsafe = True
        return self
    
    def unpadded(self)->"Base64Schema[B]":
        self.__padded = False
        return self

    def _check(self,value: str)->str:
        if value == None:
            return value
        elif self.__padded and self.__urlsafe and re.match(PaddedUrlSafeB64Pattern,value) == None:
            raise Exceptions.InvalidBase64Exception(self._name,f"{value} is invalid urlsafe base64")
        elif self.__padded and not self.__urlsafe and re.match(PaddedB64Pattern,value) == None:
            raise Exceptions.InvalidBase64Exception(self._name,f"{value} is invalid base64")
        elif not self.__padded and self.__urlsafe and re.match(UnPaddedUrlSafeB64Pattern,value) == None:
            raise Exceptions.InvalidBase64Exception(self._name,f"{value} is invalid unpadded urlsafe base64")
        elif not self.__padded and not self.__urlsafe and re.match(UnpaddedB64Pattern,value) == None:
            raise Exceptions.InvalidBase64Exception(self._name,f"{value} is invalid unpadded base64")
        return value

    if typing.TYPE_CHECKING:
        def whitelist(self,*items: str)->"Base64Schema[B]":
            pass

        def blacklist(self,*items: str)->"Base64Schema[B]":
            pass

        def len(self,new_len: int)->"Base64Schema[B]":
            pass
    
        def min_len(self,new_min: int)->"Base64Schema[B]":
            pass

        def max_len(self, new_max: int)->"Base64Schema[B]":
            pass

        def whitelist_pattern(self, pattern: str)->"Base64Schema[B]":
            pass

        def blacklist_pattern(self, pattern: str)->"Base64Schema[B]":
            pass

        def optional(self)->"Base64Schema[typing.Optional[str]]":
            pass