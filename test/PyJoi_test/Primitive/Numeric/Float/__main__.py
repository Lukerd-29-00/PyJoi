import unittest

suite = unittest.defaultTestLoader.discover("PyJoi_test.Primitive.Numeric.Float","test_*")
runner = unittest.TextTestRunner()
runner.run(suite)