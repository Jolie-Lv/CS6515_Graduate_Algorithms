def longest_increasing_subsequence(array):
    DP = [1]*len(array)

    for i in range(1, len(array)):
        for j in range(i):
            if array[i] > array[j]:
                DP[i] = max(DP[i], DP[j]+1)

    return max(DP)

def longest_common_subsequence(array1, array2):
    if len(array1) == 0 or len(array2) == 0:
        return 0

    DP = [[0 for j in range(len(array2))] for i in range(len(array1))]

    for i in range(len(array1)):
        if (i > 0 and DP[i-1][0] == 1) or array1[i] == array2[0]:
            DP[i][0] = 1

    for j in range(len(array2)):
        if (j > 0 and DP[0][j-1] == 1) or array1[0] == array2[j]:
            DP[0][j] = 1

    for i in range(1, len(array1)):
        for j in range(1, len(array2)):
            if array1[i] == array2[j]:
                DP[i][j] = DP[i-1][j-1]+1
            else:
                DP[i][j] = max(DP[i-1][j],DP[i][j-1])

    return DP[-1][-1]

def knapsack_no_repeat(items, values, W):
    n = len(items)
    DP = [[0 for j in range(W+1)] for i in range(n)]

    for j in range(W+1):
        if items[0] <= j:
            DP[0][j] = values[0]

    for i in range(1, n):
        for j in range(W+1):
            DP[i][j] = DP[i-1][j]
            if j >= items[i] and DP[i][j] < DP[i-1][j-items[i]]+values[i]:
                DP[i][j] = DP[i-1][j-items[i]]+values[i]

    return DP[-1][-1]

def knapsack_repeat(items, values, W):
    n = len(items)
    DP = [[0 for j in range(W+1)] for i in range(n)]

    for j in range(W+1):
        DP[0][j] = values[0]*(j/items[0])

    for i in range(1, n):
        for j in range(W+1):
            DP[i][j] = DP[i-1][j]
            if j >= items[i] and DP[i][j] < DP[i][j-items[i]]+values[i]:
                DP[i][j] = DP[i][j-items[i]]+values[i]

    return DP[-1][-1]

def chain_matrix_multiply(matrix_dim):
    n = len(matrix_dim)
    DP = [[float('inf') for j in range(n)] for i in range(n)]

    for i in range(n):
        DP[i][i] = 0

    for k in range(1, n):
        for i in range(n-k):
            for l in range(i, k+i):
                DP[i][k+i] = min(DP[i][k+i], DP[i][l]+DP[l+1][k+i]+ \
                                 matrix_dim[i][0]*matrix_dim[l][1]*matrix_dim[k+i][1])

    return DP[0][-1]
