import unittest

suite = unittest.defaultTestLoader.discover("PyJoi_test.Schema","test_*")
runner = unittest.TextTestRunner()
runner.run(suite)