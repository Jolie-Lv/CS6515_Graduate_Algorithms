from modular_arithmatic import modular_exponential, euclid, ext_euclid, \
                               get_prime

class Receiver(object):
    def __init__(self, n = 8, k = 100, limit = 100):
        """
            args:
                n = number of bit for random numbers
                k = number of fermat tests
        """
        self.__p = None
        self.__q = None
        self.__e = None
        self.__d = None
        self.__generate_keys(n, k, limit)

    def public_key(self):
        return (self.__p*self.__q, self.__e)

    def decrypt(self, msg):
        return modular_exponential(msg, self.__d, self.__p*self.__q)

    def __generate_keys(self, n = 8, k = 100, limit = 100):
        """
            args:
                n = number of bit for random numbers
                k = number of fermat tests
                limit = the largest number for e (exclusive)
        """
        is_find = False
        while not is_find:
            self.__p = get_prime(n, k)
            self.__q = self.__p
            while self.__q == self.__p:
                self.__q = get_prime(n, k)

            self.__e = 3
            limit = limit if limit < (self.__p-1)*(self.__q-1) \
                          else (self.__p-1)*(self.__q-1)-1
            while self.__e < limit:
                if euclid(self.__e, (self.__p-1)*(self.__q-1)) == 1:
                    is_find = True
                    break
                self.__e += 2

            if is_find:
                self.__d = ext_euclid(self.__e, (self.__p-1)*(self.__q-1))[1]
                if self.__d < 0:
                    is_find = False

class Sender(object):
    def encrypt(self, N, e, msg):
        return modular_exponential(msg, e, N)
