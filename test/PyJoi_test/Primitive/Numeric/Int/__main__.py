import unittest

suite = unittest.defaultTestLoader.discover("PyJoi_test.Primitive.Numeric.Int","test_*")
runner = unittest.TextTestRunner()
runner.run(suite)