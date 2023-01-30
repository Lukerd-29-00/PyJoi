import unittest

suite = unittest.defaultTestLoader.discover("PyJoi_test.Bool","test_*")
runner = unittest.TextTestRunner()
runner.run(suite)