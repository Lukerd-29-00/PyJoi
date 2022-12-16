import unittest

suite = unittest.defaultTestLoader.discover("PyJoi_test.Stream","test_*")
runner = unittest.TextTestRunner()
runner.run(suite)