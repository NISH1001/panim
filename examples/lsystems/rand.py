#!/usr/bin/env python3

import random
import numpy as np
import sys
import time
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

from panim.lsystem import LSystemAnimator, BranchedLSystemAnimator

"""
Some random systems generated from this experiment:

{'F': 'FFF-F'}
Axiom=F
Rule={'F': 'FFF-F'}
Turn Angle=70
Iterations=6
Final Sequence Length=5461
Start Position=(0.0, 0.0)


# monster?
{'F': 'fF[-FfFf]f++'}
Axiom=F
Rule={'F': 'fF[-FfFf]f++'}
Turn Angle=50
Iterations=5
Final Sequence Length=1332
Start Position=(0.0, 0.0)


# sphere?
{'F': 'FF-[+FFFf]-f'}
Axiom=F
Rule={'F': 'FF-[+FFFf]-f'}
Turn Angle=70
Iterations=5
Final Sequence Length=8592
Start Position=(0.0, 0.0)


# dance pose?
Axiom=F
Rule={'F': 'F+f[F-F++]Ff'}
Turn Angle=90
Iterations=5
Final Sequence Length=3752
Start Position=(0.0, 0.0)

# ring? (best so far)
Axiom=F
Rule={'F': 'Ff[FfFF+]fff'}
Turn Angle=35
Iterations=5
Final Sequence Length=3752
Start Position=(0.0, 0.0)

# random circular motion
Axiom=F
Rule={'F': '+F[+FFf]F-'}
Turn Angle=20
Iterations=5
Final Sequence Length=3070
Start Position=(0.0, 0.0)

# nice circular motions
{'F': 'FF[F-FF-]-F+'}
Axiom=F
Rule={'F': 'FF[F-FF-]-F+'}
Turn Angle=30
Iterations=5
N = 40
FPS = 25
DPI = 80
Final Sequence Length=17106
Start Position=(0.0, 0.0)
Want to generate?(y/n)y

"""


def generate_random(N):
    symbols = list("F+")
    # res = ['F']

    res = np.random.choice(symbols, N, p=[0.8, 0.2]).tolist()
    return {"F": "".join(res)}


def generate_branched(N):
    symbols = list("Ff+-")
    main = np.random.choice(symbols, N, p=[0.6, 0.2, 0.1, 0.1]).tolist()
    branch = (
        ["["]
        + np.random.choice(list("Ff++-"), N, p=[0.4, 0.3, 0.1, 0.1, 0.1]).tolist()
        + ["]"]
    )
    # indices = np.random.choice(range(N), size=2)
    # indices.sort()
    idx = np.random.choice(range(1, N - 2), size=1)
    # res = np.insert(res, indices+1, ['[', ']']).tolist()
    res = np.insert(main, idx + 1, branch).tolist()
    return {"F": "".join(res)}


def main():
    symbols = "Ff+-"
    axiom = "F"
    N = 5
    # rule = generate_random(N)
    rule = generate_branched(N)
    print(rule)
    # return
    angle = random.choice(range(10, 91, 5))
    # angle = 90
    iteration = 5
    n = 40

    animator = LSystemAnimator(
        interval=1,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        # start_position=(-n//2+10, -10),
        nlimit=n,
    )

    contd = bool(input("Want to generate?(y/n)").strip().lower() == "y")
    if not contd:
        print("See ya sucker...")
        sys.exit(0)

    animator.animate(len(animator.coords))
    animator.save("out/curves/random.mp4", fps=20, dpi=80)


if __name__ == "__main__":
    main()
