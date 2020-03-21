import math

# class Complex(object):
#     def __init__(self, radius, n=1):
#         """
#             complex number in polar notation: (r, theta) = (r, 2*pi/n)
#             Args:
#                 radius = r
#                 n = 2*pi/theta
#         """
#         self.radius = radius
#         self.n = n
#
#     def __mul__(self, other):
#         # theta  = theta1+theta2
#         #        = 2*pi/n1+2*pi/n2
#         # 2*pi/n = 2*pi(1/n1+1/n2)
#         # n      = n1*n2/(n1+n2)
#         n1 = self.n
#         n2 = other.n
#         return Complex(self.radius*other.radius, float(n1*n2)/(n1+n2))
#
#     def __pow__(self, p):
#         # p*theta = p*2*pi/n
#         #         = 2*pi/(n/p)
#         return Complex(self.radius**p, (float(self.n)/p))
#
#     def __str__(self):
#         return '({},{})'.format(self.radius, 2*math.pi/self.n)

class Polynomial(object):
    def __init__(self, coeff):
        self.coeff = coeff

    def __mul__(self, other):
        """
            prepare values for A(x), B(x)
        """
        n = Polynomial.__pow_of_2(len(self.coeff)+len(other.coeff))
        w = complex(math.cos(2*math.pi/n),math.sin(2*math.pi/n))
        my_values = self.__fft(w, n)
        other_values = other.__fft(w, n)

        """
            calculate values for C(x)
        """
        c_values = [my_values[i]*other_values[i] for i in range(n)]
        tmp = Polynomial(c_values)

        """
            calculate coeff for C(x)
        """
        w = w**(n-1)
        tmp = tmp.__fft(w, n)
        return Polynomial([(c/n).real for c in tmp])

    def fft(self):
        n = Polynomial.__pow_of_2(len(self.coeff))
        w = complex(math.cos(2*math.pi/n),math.sin(2*math.pi/n))
        return self.__fft(w, n)

    def eval(self, x):
        ret = 0
        for i in range(len(self.coeff)):
            ret += self.coeff[i]*(x**i)

        return ret

    def eval_test(self):
        """
            for testing
        """
        n = Polynomial.__pow_of_2(len(self.coeff))
        w = complex(math.cos(2*math.pi/n),math.sin(2*math.pi/n))
        ret = [0]*n
        for i in range(n):
            ret[i] = self.eval(w**i)

        return ret

    def __fft(self, w, n):
        if n == 1:
            return [sum(self.coeff)]

        even = self.__get_interleaving(0).__fft(w**2, n/2)
        odd = self.__get_interleaving(1).__fft(w**2, n/2)

        ret = [0]*n
        for i in range(n/2):
            ret[i] = even[i]+(w**i)*odd[i]
            ret[n/2+i] = even[i]-(w**i)*odd[i]

        return ret

    def __get_interleaving(self, start):
        ret = []
        for i in range(start, len(self.coeff), 2):
            ret.append(self.coeff[i])
        return Polynomial(ret)

    @staticmethod
    def __pow_of_2(n):
        p = int(math.log(n,2))
        if 2**p < n:
            n = 2**(p+1)
        return n
