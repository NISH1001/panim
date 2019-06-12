#!/usr/bin/env python3

import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')

from panim.spiral import SpiralAnimator, SpiralAnimator2
from panim.transformers import ZoomTransformer


def main():
    n = 25
    animator = SpiralAnimator(
        interval=50,
        clockwise=False,
        factor=0.1,
        nlimit=n
    )
    animator = SpiralAnimator2(
        interval=50,
        scale=0.4,
        nlimit=n,
        npoints=50,
        rot_factor=0.001
    )
    animator.animate(9000)
    animator.save("out/spiral2.mp4")
    return

    zoomer = ZoomTransformer(
        animobj=animator,
        factor=2000,
        nlimit=n)
    zoomer.animate(9000)
    zoomer.save("out/spiral-zoom.mp4")

if __name__ == "__main__":
    main()

