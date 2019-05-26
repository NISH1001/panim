#!/usr/bin/env python3

import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')

from panim.spiral import SpiralAnimator
from panim.transformers import ZoomTransformer


def main():
    n = 800
    animator = SpiralAnimator(
        interval=1,
        clockwise=False,
        factor=0.1,
        nlimit=n
    )
    zoomer = ZoomTransformer(
        animobj=animator,
        factor=2000,
        nlimit=n)
    zoomer.animate(9000)
    zoomer.save("out/spiral-zoom.mp4")

if __name__ == "__main__":
    main()

