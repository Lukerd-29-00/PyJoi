from . import Exceptions
import typing
import re
from .IStringSchema import IStringSchema

HexPattern = re.compile(r"^(?:[a-f0-9][a-f0-9])*$")

PaddedB64Pattern = re.compile(r"^(?:[A-Za-z0-9\+/]{4})*(?:[A-Za-z0-9\+/]{2}[A-Za-z0-9\+/=]{2})?$")
UnpaddedB64Pattern = re.compile(r"^(?:[A-Za-z0-9\+/]{4})*(?:[A-Za-z0-9\+/]{2,3})?$")

PaddedUrlSafeB64Pattern = re.compile(r"^(?:[A-Za-z0-9\-_]{4})*(?:[A-Za-z0-9\-_]{2}[A-Za-z0-9\-_=]{2})?$")
UnPaddedUrlSafeB64Pattern = re.compile(r"^(?:[A-Za-z0-9\-_]{4})*(?:[A-Za-z0-9\-_]{2,3})?$")

class StringSchema(IStringSchema):
    __min_len: typing.Optional[int] = None
    __max_len: typing.Optional[int] = None
    __len: typing.Optional[int] = None
    __whitelist_regex: typing.Optional[re.Pattern] = None
    __blacklist_regex: typing.Optional[re.Pattern] = None
    __hex: bool = False

    def validate(self, value: any)->typing.Optional[str]:
        if value == None and not self._required:
            return value
        elif value == None:
            raise Exceptions.MissingStringException(self._name,"Encountered unexpected null/missing value for required string.")
        if not isinstance(value,str):
            raise Exceptions.NotAStringException(self._name,"Encounted non string value")
        if not self.__min_len is None and len(value) < self.__min_len:
            raise Exceptions.TooShortException(self._name,f"Encounted string of length {len(value)} but expected length to be >= {self.__min_len}")
        elif not self.__max_len is None and len(value) > self.__max_len:
            raise Exceptions.TooLongException(self._name,f"Encountered string of length {len(value)} but expected length to be <= {self.__max_len}")
        elif not self.__len is None and len(value) != self.__len:
            raise Exceptions.NonMatchingLengthException(self._name,f"Encountered string of length {len(value)} but expected {self.__len}")
        self.check_blacklist(value)
        self.check_whitelist(value)
        if self.__blacklist_regex and re.match(self.__blacklist_regex,value) != None:
            raise Exceptions.MatchesBlackistException(self._name,f"{value} matches blacklisted pattern {self.__blacklist_regex.pattern}")
        elif self.__whitelist_regex and re.match(self.__whitelist_regex,value) == None:
            raise Exceptions.NoWhiteListException(self._name,f"{value} fails to match whitelist pattern {self.__whitelist_regex.pattern}")
        elif self.__hex and re.match(HexPattern,value) == None:
            raise Exceptions.InvalidHexException(self._name,f"{value} is not a hexadecimal string.")
        return value

    def whitelist(self,items: typing.Union[str,typing.Iterable[str]])->"StringSchema":
        if self._blacklist or self.__blacklist_regex:
            raise ValueError("Cannot set a blacklist if a whitelist is present!")
        self._whitelist = self._whitelist.union(items if not isinstance(items,str) else [items])
        return self

    def blacklist(self, items: typing.Union[str,typing.Iterable[str]])->"StringSchema":
        if self._whitelist or self.__whitelist_regex:
            raise ValueError("Cannot set a blacklist if a whitelist is present!")
        self._blacklist = self._blacklist.union(items if not isinstance(items,str) else [items])
        return self

    def whitelist_pattern(self, pattern: str)->"StringSchema":
        if self._blacklist or self.__blacklist_regex:
            raise ValueError("Cannot set a whitelist pattern if a blacklist is present!")
        if self._whitelist:
            raise ValueError("Cannot set a whitelist pattern there is already a whitelist.")
        self.__whitelist_regex = re.compile(pattern)
        return self

    def blacklist_pattern(self, pattern: str)->"StringSchema":
        if self._whitelist or self.__whitelist_regex:
            raise ValueError("Cannot set a blacklist pattern if a whitelist is present!")
        self.__blacklist_regex = re.compile(pattern)
        return self

    def len(self,new_len: int)->"StringSchema":
        if not self.__max_len is None or not self.__min_len is None:
            raise ValueError("Cannot add length to a string schema that has length bounds already (min or max)")
        elif self.__hex and new_len % 2 == 1:
            raise ValueError("You can't restrict hexadecimal strings to an odd length.")
        self.__len = new_len
        return self
    
    def min_len(self,new_min: int)->"StringSchema":
        if self.__len != None:
            raise ValueError("Cannot add length bounds to a string schema that has a length set already!")
        self.__min_len = new_min
        return self

    def max_len(self, new_max: int)->"StringSchema":
        if self.__len != None:
            raise ValueError("Cannot add length bounds to a string schema that has a length set already!")
        self.__max_len = new_max
        return self

    def hex(self)->"StringSchema":
        self.__hex = True
        return self

    def base64(self)->"Base64Schema":
        return Base64Schema(self._name,self._required)

class Base64Schema(StringSchema):
    __padded: bool = True
    __urlsafe: bool = False

    def base64(self):
        raise ValueError("This is already base 64!")
    
    def urlsafe(self):
        self.__urlsafe = True
        return self
    
    def unpadded(self):
        self.__padded = False
        return self

    def validate(self,value: any)->typing.Optional[str]:
        value = super(Base64Schema,self).validate(value)
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