#!/usr/bin/env python3

import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")

from panim.rain import RainAnimator


def main():
    r = RainAnimator(ndrops=50)
    r.animate(2000)
    r.save("out/rain.mp4")


if __name__ == "__main__":
    main()
