#!/usr/bin/env python3

import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)


from panim.lsystem import (
    LSystemAnimator
)

def main():
    axiom = 'L'
    rule = {
        'L': '-RF+LFL+FR-',
        'R': '+LF-RFR-FL+'
    }
    angle = 90

    animator = LSystemAnimator(interval=50, iteration=5, rule=rule, axiom=axiom, turn_angle=angle)
    animator.animate(len(animator.coords))
    # animator.animate(500)
    animator.save("out/hilbert.mp4")

if __name__ == "__main__":
    main()

