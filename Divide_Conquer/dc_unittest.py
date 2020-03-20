import unittest

from fast_integer_multiplication import fast_integer_multiplication

class TestDP(unittest.TestCase):

    def test_fast_integer_mult(self):
        self.assertTrue(fast_integer_multiplication(1234,56678) == 1234*56678)

if __name__ == '__main__':
    unittest.main()
