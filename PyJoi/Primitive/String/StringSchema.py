from . import Exceptions
import typing
import re
from .IStringSchema import IStringSchema

HexPattern = re.compile(r"^(?:[a-f0-9][a-f0-9])*$")

class StringSchema(IStringSchema):
    __min_len: typing.Optional[int] = None
    __max_len: typing.Optional[int] = None
    __len: typing.Optional[int] = None
    __whitelist_regexes: typing.Set[re.Pattern]
    __blacklist_regexes: typing.Set[re.Pattern]

    def __init__(self, name: typing.Optional[str], required: bool = True):
        super(StringSchema,self).__init__(name,required=required)
        self.__whitelist_regexes = set()
        self.__blacklist_regexes = set()

    def validate(self, value: any)->str:
        if value == None and not self.required:
            return value
        elif value == None:
            raise Exceptions.MissingStringException(self.name,"Encountered unexpected null/missing value for required string.")
        if not isinstance(value,str):
            raise Exceptions.NotAStringException(self.name,"Encounted non string value")
        if not self.__min_len is None and len(value) < self.__min_len:
            raise Exceptions.TooShortException(self.name,f"Encounted string of length {len(value)} but expected length to be >= {self.__min_len}")
        elif not self.__max_len is None and len(value) > self.__max_len:
            raise Exceptions.TooLongException(self.name,f"Encountered string of length {len(value)} but expected length to be <= {self.__max_len}")
        elif not self.__len is None and len(value) != self.__len:
            raise Exceptions.NonMatchingLengthException(self.name,f"Encountered string of length {len(value)} but expected {self.__len}")
        self.check_blacklist(value)
        self.check_whitelist(value)
        if self.__blacklist_regexes:
            for pattern in self.__blacklist_regexes:
                if not re.match(pattern,value) is None:
                    raise Exceptions.MatchesBlackistException(self.name,f"{value} matches blacklisted pattern {pattern.pattern}")
        if self.__whitelist_regexes:
            found = False
            for pattern in self.__whitelist_regexes:
                if not re.match(pattern,value) is None:
                    found = True
                    break
            if not found:
                raise Exceptions.NoWhiteListException(self.name,f"{value} fails to match any whitelisted pattern.")
        return value

    def whitelist(self,items: typing.Union[str,typing.Iterable[str]])->"StringSchema":
        if self.__blacklist_regexes:
            raise ValueError("Cannot set a whitelist if a blacklist is present!")
        return super(StringSchema,self).whitelist(items)

    def blacklist(self, items: typing.Union[str,typing.Iterable[str]])->"StringSchema":
        if self.__whitelist_regexes:
            raise ValueError("Cannot set a blacklist if a whitelist is present!")
        return super(StringSchema,self).blacklist(items)

    def whitelist_patterns(self, patterns: typing.Union[str,typing.Iterable[str]])->"StringSchema":
        if self._blacklist or self.__blacklist_regexes:
            raise ValueError("Cannot set a whitelist pattern if a blacklist is present!")
        self.__whitelist_regexes = self.__whitelist_regexes.union(patterns if not isinstance(patterns,str) else [patterns])
        return self

    def blacklist_patterns(self, patterns: typing.Union[typing.Iterable[str],str])->"StringSchema":
        if self._whitelist or self.__whitelist_regexes:
            raise ValueError("Cannot set a blacklist pattern if a whitelist is present!")
        self.__blacklist_regexes = self.__blacklist_regexes.union(patterns if not isinstance(patterns,str) else [patterns])
        return self

    def len(self,new_len: int)->"StringSchema":
        if not self.__max_len is None or not self.__min_len is None:
            raise ValueError("Cannot add length to a string schema that has length bounds already (min or max)")
        elif HexPattern in self.__whitelist_regexes and new_len % 2 == 1:
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
        if self.__len != None and self.__len % 2 == 1:
            raise ValueError("Cannot require hex from an odd-length string!")
        elif self._blacklist or self.__blacklist_regexes:
            raise ValueError("Cannot set a whitelist pattern if a blacklist is present!")
        self.__whitelist_regexes.add(HexPattern)
        return self