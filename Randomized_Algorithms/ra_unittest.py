import unittest

from modular_arithmatic import modular_exponential, euclid, ext_euclid, \
                               get_prime
from rsa import Receiver, Sender

class TestRA(unittest.TestCase):

    def test_modular_arithmatic(self):
        self.assertTrue(modular_exponential(456, 34, 9) == (456**34)%9)

    def test_euclid(self):
        self.assertTrue(euclid(3,15) == 3)

    def test_ext_euclid(self):
        self.assertTrue(ext_euclid(3,14)[1] == 5)

    def test_prime(self):
        r = get_prime()
        is_prime = True
        for n in range(2, int(r**0.5)+1):
            if r%n == 0:
                is_prime = False
                break
        self.assertTrue(is_prime)

    def test_rsa(self):
        receiver = Receiver()
        N, e = receiver.public_key()

        sender = Sender()
        original_msg = 45
        msg = sender.encrypt(N,e,original_msg)
        msg = receiver.decrypt(msg)

        self.assertTrue(original_msg == msg)

if __name__ == '__main__':
    unittest.main()
