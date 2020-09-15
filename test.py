import numpy as np
from matplotlib.image import imread
import matplotlib.pyplot as plt
import os
from scipy import linalg

def SVD():
    A = imread('./five.png')
    X = np.mean(A, -1)

    img = plt.imshow(X)
    img.set_cmap('gray')

    U, S, VT = np.linalg.svd(X,full_matrices=False)
    S = np.diag(S)

    for r in (5, 20, 100):
        Xapprox = U[:, :r] @ S[0:r, :r] @ VT[:r, :]

        img = plt.imshow(Xapprox)
        img.set_cmap('gray')
        plt.show()

def main():
    SVD()
    # state = np.array([
    #     [1, 1, 1, 0],
    #     [0, 1, 1, 1],
    #     [1, 0, 1, 1],
    #     [1, 1, 0, 1],
    # ])
    # state = state @ state
    # state = 1/ np.sqrt(3) * state

    # p, l, u = linalg.lu(state)
    # print(p)
    # print(l)
    # print(u)

    # q, r = linalg.qr(state)
    # print(q)
    # print(r)

    # state = state @ state
    # print(state)

    


if __name__ == "__main__":
    main()
