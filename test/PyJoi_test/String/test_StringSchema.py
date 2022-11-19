import unittest
import PyJoi
import typing
from PyJoi.Primitive.String import Exceptions



class TestStringSchema(unittest.TestCase):

    def test_optional_accepts_missing(self):
        value = PyJoi.Schema().string().optional().validate(None)
        self.assertIsNone(value)
        
    def test_required_rejects_missing(self):
        with self.assertRaises(Exceptions.MissingStringException) as cm:
            PyJoi.Schema().string().validate(None)

    def test_too_short_fails(self):
        with self.assertRaises(Exceptions.TooShortException):
            PyJoi.Schema().string().min_len(3).validate('hi')

    def test_too_long_fails(self):
        with self.assertRaises(Exceptions.TooLongException):
            PyJoi.Schema().string().max_len(3).validate("hello")

    



    
