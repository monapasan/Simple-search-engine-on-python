import numpy as np
from scipy.sparse import csc_matrix
from pprint import pprint


def toMatrix(struct):
    col = []
    # there is no important reason for this
    # but anyway make it sorted
    sKs = sorted(struct.keys())
    # sKs- sort keys from link structur
    # mK - mainKey
    # cK - childKey
    for mK in sKs:
        col.append([struct[mK][cK] if cK in struct[mK] else 0 for cK in sKs])
    matrix = np.array(col)
    # pprint(pageRank(np.full((2, 2), (0.25, 0.75), dtype=np.float)))
    # TEST: k =
    # np.array([[0,1,1,1,0],[0,0,1,0,1],[0,0,0,1,1],[0,0,1,0,0],[0,0,0,0,0]])
    # pprint(pageRank(M))
    return matrix


def pageRank(matrix, d = 0.95, delta = 0.04):

    t = 1 - d
    n = matrix.shape[0]
    # sparse Matrix
    sparseM = csc_matrix(matrix, dtype = np.float)
    # sum of all values in a row
    rsums = np.array(sparseM.sum(axis = 1))[:, 0]
    # original value / sum values in a row
    sparseM.data /= rsums[sparseM.indices]
    adjazentM = sparseM.toarray()
    # if the whole row give the sum = 0
    # we have to change it to 1/n
    adjazentM[rsums == 0] = np.full_like(adjazentM[rsums == 0], 1 / n)
    # exclude zeros and generate new values, because we don't want have zeros
    for v in np.nditer(adjazentM, op_flags=['readwrite']):
        # from lesson
        v[...] = v * d + t / n
    # TODO: formatiing
    # step 0
    step = 0
    pr = np.full(n, 1 / n, dtype = np.float)
    calcDelta = delta + 1
    while(calcDelta > delta):
        # next Probability. Empty for now
        nextProb = np.full(n, 0, dtype = np.float)
        nextProb = pr.dot(adjazentM)
        calcDelta = np.sum(np.abs(nextProb - pr))
        # print(calcDelta)
        step += 1
        pr = nextProb
    return pr.round(decimals=4)
