import unittest

suite = unittest.defaultTestLoader.discover("PyJoi_test.Set","test_*")
runner = unittest.TextTestRunner()
runner.run(suite)