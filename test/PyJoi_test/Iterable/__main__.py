import unittest

suite = unittest.defaultTestLoader.discover("PyJoi_test.Iterable","test_*")
runner = unittest.TextTestRunner()
runner.run(suite)