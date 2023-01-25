import PyJoi
import unittest
from PyJoi.Primitive.Bool import Exceptions

class TestBoolSchema(unittest.TestCase):
    def test_verifies_bool(self):
        self.assertEqual(PyJoi.bool().validate(True),True)
        with self.assertRaises(Exceptions.NotABoolException):
            PyJoi.bool().validate(3)
