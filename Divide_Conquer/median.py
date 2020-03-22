def median(array, k):
    if k > len(array):
        return None

    p = array[0]
    ltp = []
    eqp = []
    gtp = []

    for a in array:
        if a < p:
            ltp.append(a)
        elif a > p:
            gtp.append(a)
        else:
            eqp.append(a)

    if k <= len(ltp):
        return median(ltp, k)
    if k <= len(ltp)+len(eqp):
        return p
    return median(gtp, k-len(ltp)-len(eqp))
