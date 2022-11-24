import unittest

suite = unittest.defaultTestLoader.discover("PyJoi_test.List","test_*")
runner = unittest.TextTestRunner()
runner.run(suite)