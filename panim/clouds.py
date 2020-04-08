#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix


def euclidean(p1, p2):
    return np.linalg.norm(p1 - p2)


def cloud2():
    s = 25
    w, h = s, s
    npoints = 10
    arr = np.zeros(h * w)
    indices = np.arange(len(arr))
    np.random.shuffle(indices)
    indices = indices[:npoints]
    arr[indices] = 255

    arr = np.reshape(arr, (h, w))

    ntile = 5
    tmp = np.tile(arr, ntile)
    stacked = [tmp for i in range(ntile)]
    tmp = np.vstack(stacked)
    arr = tmp.copy()
    h, w = arr.shape

    arr = arr.flatten()
    indices = np.where(arr == 255)[0]
    arr = np.reshape(arr, (h, w))
    indices2d = np.unravel_index(indices, (h, w))
    points = list(zip(indices2d[0], indices2d[1]))

    res = np.reshape(arr, (h, w)).copy()
    for r in range(h):
        for c in range(w):
            point = np.array([c, r])
            dist = min([euclidean(point, p) for p in points])
            dist = min(dist, 255)
            res[r, c] = dist

    # original
    plt.imshow(arr, cmap="gray")
    plt.show()

    # result
    plt.imshow(res, cmap="gray")
    plt.show()

    # inversion
    res = 255 - res
    plt.imshow(res, cmap="gray")
    plt.show()


def cloud1():
    s = 50
    w, h = s, s
    npoints = 10
    arr = np.zeros(h * w)
    indices = np.arange(len(arr))
    np.random.shuffle(indices)
    indices = indices[:npoints]
    arr[indices] = 255
    arr = np.reshape(arr, (h, w))

    indices2d = np.unravel_index(indices, (h, w))
    points = list(zip(indices2d[0], indices2d[1]))

    res = np.reshape(arr, (h, w)).copy()
    for r in range(h):
        for c in range(w):
            point = np.array([c, r])
            dist = min([euclidean(point, p) for p in points])
            dist = min(dist, 255)
            res[r, c] = dist

    # original
    plt.imshow(arr, cmap="gray")
    plt.show()

    # result
    plt.imshow(res, cmap="gray")
    plt.show()

    # inversion
    res = 255 - res
    plt.imshow(res, cmap="gray")
    plt.show()


def main():
    # cloud1()
    cloud2()


if __name__ == "__main__":
    main()
