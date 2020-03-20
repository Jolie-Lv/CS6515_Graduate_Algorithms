def fast_integer_multiplication(x, y):
    xbit = count_bits(x)
    ybit = count_bits(y)
    if xbit == 0 or ybit == 0:
        return 0
    if xbit == 1 and ybit == 1:
        return 1

    n = max(xbit, ybit)
    n = n if n%2 == 0 else n+1

    xL = x>>(n/2)
    xR = x-(xL<<(n/2))
    yL = y>>(n/2)
    yR = y-(yL<<(n/2))

    multL = fast_integer_multiplication(xL,yL)
    multR = fast_integer_multiplication(xR,yR)
    multC = fast_integer_multiplication(xL+xR,yL+yR)

    return (multL<<n)+((multC-multL-multR)<<(n/2))+multR

def count_bits(x):
    bit = 0
    while x > 0:
        bit += 1
        x >>= 1

    return bit
