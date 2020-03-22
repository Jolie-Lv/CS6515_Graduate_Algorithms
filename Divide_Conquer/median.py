
def find_element_k(array, k, fast_select):
    if k > len(array):
        return None

    p = array[0]
    if fast_select and len(array) > 5:
        G = [array[i:i+5] for i in range(0,len(array),5)]
        m = []
        for subg in G:
            subg.sort()
            if len(subg) == 5:
                m.append(subg[2])
            else:
                m.append(subg[len(subg)/2])
        p = find_element_k(m, (len(m)+1)/2, fast_select)

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
        return find_element_k(ltp, k, fast_select)
    if k <= len(ltp)+len(eqp):
        return p
    return find_element_k(gtp, k-len(ltp)-len(eqp), fast_select)
