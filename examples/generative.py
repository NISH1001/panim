#!/usr/bin/env python3

import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')

from panim.generative import (
    GenerativeArt,
    GenerativeArt2,
    GenerativeArt3,
    GenerativeArt4
)
from panim.flow import (
    FlowAnimator
)
from panim.transformers import ZoomTransformer


def main():
    animator = GenerativeArt4(
        width=640,
        height=320
    )
    # animator = FlowAnimator(
    #     nlines = 75,
    #     npoints = 90,
    #     perspective=150
    # )
    animator.animate(5000)
    animator.save("out/random4.mp4", fps=24)

if __name__ == "__main__":
    main()
