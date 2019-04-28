#!/usr/bin/env python3


import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

from panim.lsystem import (
    LSystemAnimator,
    BranchedLSystemAnimator
)


def main():
    # angle = 30
    # iteration = 4
    # rule = {
    #     'F': 'F[-F][+F]'
    # }

    angle = 22
    iteration = 4
    rule = {
        'F': 'FF[++F][-FF]'
    }

    axiom = 'F'

    animator = BranchedLSystemAnimator(
        interval=20,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle
    )
    animator.animate(len(animator.coords))
    animator.save("out/tree.mp4")

if __name__ == "__main__":
    main()

