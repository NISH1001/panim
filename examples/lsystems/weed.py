#!/usr/bin/env python3


import sys
import time
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

from panim.lsystem import (
    LSystemAnimator,
    BranchedLSystemAnimator
)


def weed():
    angle = 22.5
    axiom = 'F'
    rule = {
        'F': 'FF-[XY]+[XY]',
        'X': '+FY',
        'Y': '-FX'
    }
    iteration = 5
    animator = BranchedLSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(0, -30),
        nlimit=30
    )
    animator.animate(len(animator.coords))
    animator.save("out/weeds/weed.mp4")



def main():
    start = time.time()
    weed()
    # algae2()
    end = time.time()
    print("Time Taken :: {} seconds".format(end-start))


if __name__ == "__main__":
    main()
