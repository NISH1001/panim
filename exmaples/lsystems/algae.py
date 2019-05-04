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


def algae1():
    angle = 12
    axiom = 'aF'
    rule = {
        "a": "FFFFFv[+++h][---q]fb",
        "b": "FFFFFv[+++h][---q]fc",
        "c": "FFFFFv[+++fa]fd",
        "d": "FFFFFv[+++h][---q]fe",
        "e": "FFFFFv[+++h][---q]fg",
        "g": "FFFFFv[---fa]fa",
        "h": "ifFF",
        "i": "fFFF[--m]j",
        "j": "fFFF[--n]k",
        "k": "fFFF[--o]l",
        "l": "fFFF[--p]",
        "m": "fFn",
        "n": "fFo",
        "o": "fFp",
        "p": "fF",
        "q": "rfF",
        "r": "fFFF[++m]s",
        "s": "fFFF[++n]t",
        "t": "fFFF[++o]u",
        "u": "fFFF[++p]",
        "v": "Fv"
    }
    iteration = 12
    animator = BranchedLSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(0, -70),
        nlimit=75
    )
    animator.animate(len(animator.coords))
    animator.save("out/algae/algae1.mp4")


def algae2():
    angle = 12
    axiom = 'aF'
    rule = {
        "a": "FFFFFy[++++n][----t]fb",
        "b": "+FFFFFy[++++n][----t]fc",
        "c": "FFFFFy[++++n][----t]fd",
        "d": "-FFFFFy[++++n][----t]fe",
        "e": "FFFFFy[++++n][----t]fg",
        "g": "FFFFFy[+++fa]fh",
        "h": "FFFFFy[++++n][----t]fi",
        "i": "+FFFFFy[++++n][----t]fj",
        "j": "FFFFFy[++++n][----t]fk",
        "k": "-FFFFFy[++++n][----t]fl",
        "l": "FFFFFy[++++n][----t]fm",
        "m": "FFFFFy[---fa]fa",
        "n": "ofFFF",
        "o": "fFFFp",
        "p": "fFFF[-s]q",
        "q": "fFFF[-s]r",
        "r": "fFFF[-s]",
        "s": "fFfF",
        "t": "ufFFF",
        "u": "fFFFv",
        "v": "fFFF[+s]w",
        "w": "fFFF[+s]x",
        "x": "fFFF[+s]",
        "y": "Fy"
    }
    iteration = 13
    animator = BranchedLSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(0, -75),
        nlimit=80
    )
    animator.animate(len(animator.coords))
    animator.save("out/algae/algae2.mp4")


def main():
    start = time.time()
    algae1()
    # algae2()
    end = time.time()
    print("Time Taken :: {} seconds".format(end-start))


if __name__ == "__main__":
    main()
