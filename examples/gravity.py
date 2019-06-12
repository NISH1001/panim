
#!/usr/bin/env python3

import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')

from panim.gravity import GravityAnimtor
# from panim.transformers import ZoomTransformer


def main():
    animator = GravityAnimtor(
        nlimit=15,
        time_length=1,
        l1=3, l2=3,
        m1=1, m2=1
    )
    animator.animate(200)
    animator.save("out/gravity.mp4")

if __name__ == "__main__":
    main()

