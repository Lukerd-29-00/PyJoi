import unittest
import PyJoi
import typing
from PyJoi.Primitive.Int import Exceptions as IntExceptions

class TestRef(unittest.TestCase):

    def test_relative_resolution(self):
        schema = PyJoi.Schema("schema",
            obj=PyJoi.Schema(
                obj=PyJoi.Schema(
                    value=PyJoi.Schema().int(),
                    value2=PyJoi.Schema().int().min(PyJoi.Ref[int]("value"))
                ),
                value=PyJoi.Schema().int()
            ),
            value=PyJoi.Schema().int().min(PyJoi.Ref[int]("obj.value")),
            value2=PyJoi.Schema().int().min(PyJoi.Ref[int]("obj.obj.value"))
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
        self.assertEqual(item.obj.value,-3)
        self.assertEqual(item.obj.obj.value,-5)
        self.assertEqual(item.value,3)
        self.assertEqual(item.value2,-4)
        self.assertEqual(item.obj.obj.value2,-4)

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
        schema = PyJoi.Schema("schema",
            min=PyJoi.Schema().int(),
            max_obj=PyJoi.Schema(
                value=PyJoi.Schema().int()
            ),
            container=PyJoi.Schema(
                value=PyJoi.Schema().int().min(PyJoi.Ref[int](".min")).max(PyJoi.Ref[int](".max_obj.value")),
                subContainer=PyJoi.Schema(
                    value=PyJoi.Schema().int().min(PyJoi.Ref[int](".min")).max(PyJoi.Ref[int](".max_obj.value"))
                )
            )
        )

        item = schema.validate({
            "min": 1,
            "max_obj": {
                "value": 1
            },
            "container": {
                "value": 1,
                "subContainer": {
                    "value": 1
                }
            }
        })
        self.assertEqual(item.min,1)
        self.assertEqual(item.max_obj.value,1)
        self.assertEqual(item.container.value,1)
        self.assertEqual(item.container.subContainer.value,1)

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


