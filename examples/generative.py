#!/usr/bin/env python3

import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")

from panim.generative import (
    GenerativeArt,
    RandomlyVanishingPixelArt,
    CloudGenerativeArt,
)

from panim.experiments import RowArt

from panim.flow import FlowAnimator
from panim.transformers import ZoomTransformer


def main():
    # animator = RandomlyVanishingPixelArt(
    #     width=800,
    #     height=600,
    #     # gray=False
    # )

    # animator = RowArt(width=800, height=600,)
    animator = CloudGenerativeArt(width=200, height=200)
    animator.animate(100)
    animator.save("out/clouds/test.mp4", fps=10)

    # animator = FlowAnimator(
    #     nlines = 75,
    #     npoints = 90,
    #     perspective=150
    # )
    # animator.animate(1500)
    # animator.save("out/random5.mp4", fps=24)


if __name__ == "__main__":
    main()
