#!/usr/bin/env python3

import cv2

from panim.clouds import CloudGenerator
import matplotlib.pyplot as plt

plt.style.use("dark_background")
plt.axis("off")


def main():
    s = 200
    cg = CloudGenerator(width=s, height=s, npoints=0)
    img = cg.generate()
    img = cv2.resize(img, None, fx=3, fy=3)
    plt.imshow(img, cmap="gray")
    plt.axis("off")
    plt.savefig("tmp/test00.png")
    print(plt.rcParams["figure.figsize"])
    pass


if __name__ == "__main__":
    main()
