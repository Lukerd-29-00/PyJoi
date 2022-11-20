import unittest

suite = unittest.defaultTestLoader.discover("PyJoi_test.Int","test_*")
runner = unittest.TextTestRunner()
runner.run(suite)