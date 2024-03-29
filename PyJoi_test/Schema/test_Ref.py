import unittest
import PyJoi
from PyJoi.Primitive.Numeric import Exceptions as IntExceptions

class TestRef(unittest.TestCase):

    def test_relative_resolution(self):
        schema = PyJoi.dict("schema",
            obj=PyJoi.dict(
                obj=PyJoi.dict(
                    value=PyJoi.int(),
                    value2=PyJoi.int().greater_than(PyJoi.Ref[int]("value"))
                ),
                value=PyJoi.int()
            ),
            value=PyJoi.int().greater_than(PyJoi.Ref[int]("obj.value")),
            value2=PyJoi.int().greater_than(PyJoi.Ref[int]("obj.obj.value"))
        )
        
        item = schema.validate(
            {
                "obj": {
                    "obj": {
                        "value": -5,
                        "value2": -4
                    },
                    "value": -3
                },
                "value": 3,
                "value2": -4
            }
        )
        self.assertEqual(item["obj"]["value"],-3)
        self.assertEqual(item["obj"]["obj"]["value"],-5)
        self.assertEqual(item["value"],3)
        self.assertEqual(item["value2"],-4)
        self.assertEqual(item["obj"]["obj"]["value2"],-4)

        with self.assertRaises(IntExceptions.InvalidSizeException):
            schema.validate(
                {
                    "obj": {
                        "obj": {
                            "value": -5,
                            "value2": -4
                        },
                        "value": -3
                    },
                    "value": -4,
                    "value2": -4
                }
            )
        
        with self.assertRaises(IntExceptions.InvalidSizeException):
            schema.validate(
                {
                    "obj": {
                        "obj": {
                            "value": -5,
                            "value2": -4
                        },
                        "value": -3
                    },
                    "value": 3,
                    "value2": -6 #Test that this is at least obj.obj.value.
                }
            )
        
        with self.assertRaises(IntExceptions.InvalidSizeException):
            schema.validate(
                {
                    "obj": {
                        "obj": {
                            "value": -5,
                            "value2": -6 #Test that this is at least obj.obj.value.
                        },
                        "value": -3
                    },
                    "value": 3,
                    "value2": -4
                }
            )

    def test_absolute_resolution(self):
        schema = PyJoi.dict("schema",
            min=PyJoi.int(),
            max_obj=PyJoi.dict(
                value=PyJoi.int()
            ),
            container=PyJoi.dict(
                value=PyJoi.int().greater_than(PyJoi.Ref[int](".min")).less_than(PyJoi.Ref[int](".max_obj.value")),
                subContainer=PyJoi.dict(
                    value=PyJoi.int().greater_than(PyJoi.Ref[int](".min")).less_than(PyJoi.Ref[int](".max_obj.value"))
                )
            )
        )

        item = schema.validate({
            "min": 1,
            "max_obj": {
                "value": 3
            },
            "container": {
                "value": 2,
                "subContainer": {
                    "value": 2
                }
            }
        })
        self.assertEqual(item["min"],1)
        self.assertEqual(item["max_obj"]["value"],3)
        self.assertEqual(item["container"]["value"],2)
        self.assertEqual(item["container"]["subContainer"]["value"],2)

        with self.assertRaises(IntExceptions.InvalidSizeException):
            schema.validate({
                "min": 1,
                "max_obj": {
                    "value": 1
                },
                "container": {
                    "value": 2, #Check that this fails if it's too large.
                    "subContainer": {
                        "value": 1
                    }
                }
            })

        with self.assertRaises(IntExceptions.InvalidSizeException):
            schema.validate({
                "min": 1,
                "max_obj": {
                    "value": 1
                },
                "container": {
                    "value": 0, #Check that this fails if it's too small.
                    "subContainer": {
                        "value": 1
                    }
                }
            })

        with self.assertRaises(IntExceptions.InvalidSizeException):
            schema.validate({
                "min": 1,
                "max_obj": {
                    "value": 1
                },
                "container": {
                    "value": 1, 
                    "subContainer": {
                        "value": 2 #Check that this fails if it's too big.
                    }
                }
            })

        with self.assertRaises(IntExceptions.InvalidSizeException):
            schema.validate({
                "min": 1,
                "max_obj": {
                    "value": 1
                },
                "container": {
                    "value": 1, 
                    "subContainer": {
                        "value": 0 #Check that this fails if it's too small.
                    }
                }
            })