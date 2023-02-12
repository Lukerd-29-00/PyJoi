import unittest

suite1 = unittest.defaultTestLoader.discover("PyJoi_test.Primitive","test_*")
suite2 = unittest.defaultTestLoader.discover("PyJoi_test.Iterable","test_*")
suite3 = unittest.defaultTestLoader.discover("PyJoi_test.Schema","test_*")
runner = unittest.TextTestRunner()
runner.run(suite1)
runner.run(suite2)
runner.run(suite3)