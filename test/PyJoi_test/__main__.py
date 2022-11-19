import unittest
suite = unittest.defaultTestLoader.discover("PyJoi","test_*")
unittest.TextTestRunner().run(suite)