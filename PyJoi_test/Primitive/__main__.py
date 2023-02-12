import unittest

suite = unittest.defaultTestLoader.discover("PyJoi_test.Primitive","test_*")
runner = unittest.TextTestRunner()
runner.run(suite)