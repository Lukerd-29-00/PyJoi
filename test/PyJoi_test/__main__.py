import unittest
suite = unittest.defaultTestLoader.discover("PyJoi_test","test_*")
unittest.TextTestRunner().run(suite)