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
    GenerativeArt
)
from panim.transformers import ZoomTransformer


def main():
    animator = GenerativeArt(
        width=640,
        height=320
    )
    animator.animate(2500)
    animator.save("out/generative.mp4", fps=7)

if __name__ == "__main__":
    main()

