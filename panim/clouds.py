#!/usr/bin/env python3

"""
    Based on the algorithm described here:
        https://www.youtube.com/watch?v=4QOcCGI6xOU
"""


import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix


class CloudGenerator:
    def __init__(self, width=100, height=100, npoints=7):
        self.width, self.height = width, height
        self.npoints = npoints if npoints else self.width // 6
        self.array = np.zeros((self.height, self.width))

    def generate(self, npoints=None):
        h, w = self.height, self.width
        npoints = self.npoints if not npoints else npoints
        print(f"Generating clouds for npoint = {npoints}")
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
        return 255 - res

    def __str__(self):
        w, h, n = self.width, self.height, self.npoints
        return f"CloudGenerator = ({w}, {h}, {n})"

    def __repr__(self):
        return str(self)


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
    s = int(sys.argv[1])
    # s = 100
    w, h = s, s
    npoints = s // 6
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
    # cloud2()
    s = 100
    plt.style.use("dark_background")
    cg = CloudGenerator(width=s, height=s, npoints=25)
    img = cg.generate()
    plt.imshow(img, cmap="gray")
    plt.axis("off")
    plt.show()
    img = cv2.resize(img, None, fx=3, fy=3)
    plt.imshow(img, cmap="gray")
    plt.axis("off")
    plt.savefig("tmp/test00.png")
    plt.show()


if __name__ == "__main__":
    main()
