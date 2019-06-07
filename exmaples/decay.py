
#!/usr/bin/env python3

import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')

from panim.decay import ExponentialDecay
# from panim.transformers import ZoomTransformer


def main():
    n = 800
    animator = ExponentialDecay(
        nlimit=30
    )
    animator.animate(5500)
    animator.save("out/decay.mp4")

if __name__ == "__main__":
    main()

