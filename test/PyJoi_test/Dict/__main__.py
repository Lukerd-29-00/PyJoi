import unittest

suite = unittest.defaultTestLoader.discover("PyJoi_test.Dict","test_*")
runner = unittest.TextTestRunner()
runner.run(suite)