import unittest

from modular_arithmatic import modular_exponential, euclid, ext_euclid

class TestRA(unittest.TestCase):

    def test_modular_arithmatic(self):
        self.assertTrue(modular_exponential(456, 34, 9) == (456**34)%9)

    def test_euclid(self):
        self.assertTrue(euclid(3,15) == 3)

    def test_ext_euclid(self):
        self.assertTrue(ext_euclid(3,14)[1] == 5)

if __name__ == '__main__':
    unittest.main()
