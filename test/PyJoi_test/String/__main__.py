import unittest

suite = unittest.defaultTestLoader.discover("PyJoi_test.String","test_*")
runner = unittest.TextTestRunner()
runner.run(suite)