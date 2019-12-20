
#!/usr/bin/env python3

import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')

from panim.gravity import (
    PendulumAnimator,
    PendulumTipAnimator
)
# from panim.transformers import ZoomTransformer


def main():
    # animator = PendulumAnimator(
    #     nlimit=15,
    #     start_position=(0, 5),
    #     time_length=200,
    #     dt=0.05,
    #     l1=5, l2=5,
    #     m1=1, m2=1
    # )
    animator = PendulumTipAnimator(
        nlimit=15,
        start_position=(0, 5),
        time_length=250,
        dt=0.05,
        l1=5, l2=5,
        m1=1, m2=1
    )
    animator.animate(len(animator.y))
    animator.save("out/pendulum-tip-2.mp4")

if __name__ == "__main__":
    main()

