#!/usr/bin/env python3

import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")
plt.axis("off")

from panim.spiral import SpiralAnimator, SpiralAnimator2
from panim.transformers import ZoomTransformer, TransformerPipeline, RotationTransformer


def disappointment():
    rotation_angle = 0.05
    n = 75
    animator = SpiralAnimator2(
        interval=50,
        scale=0.4,
        nlimit=n,
        npoints=75,
        factor=0.001,
    )
    zoomer = ZoomTransformer(animobj=animator, factor=1000, nlimit=n)
    rotator = RotationTransformer(animobj=animator, factor=rotation_angle)

    animator = TransformerPipeline(animobj=animator, transformers=[zoomer, rotator])
    # animator.animate(100)
    animator.animate(fps=30, timespan=5)
    animator.save("out/spiral2.mp4")


def test():
    n = 300
    rotation_angle = 0.01
    animator = SpiralAnimator(interval=50, clockwise=False, factor=0.1, nlimit=n)

    zoomer = ZoomTransformer(animobj=animator, factor=175, nlimit=n)
    rotator = RotationTransformer(animobj=animator, factor=rotation_angle)

    animator = TransformerPipeline(animobj=animator, transformers=[zoomer, rotator])
    animator.animate(9000)
    animator.save("out/spiral-zoom.mp4")


def main():
    disappointment()
    # test()


if __name__ == "__main__":
    main()
