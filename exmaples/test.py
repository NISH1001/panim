#!/usr/bin/env python3

import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

from  panim.box import (
    BoxSizeAnimator
)
from panim.spiral import (
    SpiralAnimator
)

def main():
    animator = BoxSizeAnimator(
        interval=5,
        size=50,
        factor=-0.05,
        toggle=True,
        line_width=3,
        title='Phasing Out - Paradox'
    )
    animator.animate(50)
    animator.save("out/box.mp4")

    animator = SpiralAnimator(
        interval=1,
        clockwise=False,
        factor=0.1,
        title="Test"
    )
    animator.animate(50)
    animator.save("out/spiral.mp4")

if __name__ == "__main__":
    main()

