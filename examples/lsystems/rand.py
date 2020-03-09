#!/usr/bin/env python3

import random
import numpy as np
import matplotlib.pyplot as plt
import sys
import time
from pathlib import Path

import time

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

from panim.lsystem import LSystemAnimator, BranchedLSystemAnimator
from panim.animator import CombinedAnimator
from panim.utils import generate_random_color

plt.style.use("dark_background")
plt.axis("off")

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


# beautiful?
{'F': 'F-F[F+f+F]-F'}
Axiom=F
Rule={'F': 'F-F[F+f+F]-F'}
Turn Angle=30
Iterations=5
Final Sequence Length=8592
Start Position=(0.0, 0.0)
Axiom=F
Rule={'F': 'F-F[F+f+F]-F'}
Turn Angle=30
Iterations=5
Final Sequence Length=8592
Start Position=(0.0, 0.0)

"""


def generate_branched(N):
    symbols = list("FF+-")
    main = np.random.choice(symbols, N, p=[0.6, 0.2, 0.1, 0.1]).tolist()
    branch = (
        ["["]
        + np.random.choice(list("FF++-"), N, p=[0.4, 0.3, 0.1, 0.1, 0.1]).tolist()
        + ["]"]
    )
    idx = np.random.choice(range(1, N - 2), size=1)
    res = np.insert(main, idx + 1, branch).tolist()
    return {"F": "".join(res)}


def generate_continuous(N):
    symbols = list("F+-|")
    main = np.random.choice(symbols, N, p=[0.4, 0.2, 0.1, 0.3]).tolist()
    return {"F": "".join(main)}


def combine(animators):
    res = animators[0]
    for anim in animators[1:]:
        res.coords += anim.coords
    return res


def multiple():
    axiom = "F"
    N = 5
    iteration = 5
    n = 10

    animators = []
    nanimators = 10
    for i in range(nanimators):
        print("-" * 10)
        print(f"Animator number = {i}/{nanimators}")
        rule = generate_continuous(N)
        angle = random.choice(range(0, 181, 1))
        start_pos = (0.0, 0.0) if not animators else animators[-1].coords[-1]
        if abs(start_pos[0]) > n:
            start_pos = (0, start_pos[-1])
        if abs(start_pos[1]) > n:
            start_pos = (start_pos[0], 0)

        color = generate_random_color()
        animator = LSystemAnimator(
            interval=60,
            iteration=iteration,
            rule=rule,
            axiom=axiom,
            turn_angle=angle,
            start_position=start_pos,
            nlimit=n,
            line_width=1,
            color=color,
            verbose=True,
        )
        print(animator)
        animators.append(animator)
        print("-" * 10)

    combined_animator = CombinedAnimator(
        interval=180, nlimit=n, line_width=1, color=(1, 1, 1), verbose=True,
    )
    combined_animator.add_animators(animators)

    animator = combine(animators)
    animator.verbose = True
    print(animator)
    # animator.animate(len(animator.coords))
    # animator.save(f"out/curves/random-{int(time.time())}.mp4", fps=25, dpi=150)
    # print(combined_animator.img_list[0].get_data())
    nframes = max([len(animator.coords) for animator in animators])
    combined_animator.animate(nframes)
    combined_animator.save(f"out/curves/random-{int(time.time())}.mp4", fps=25, dpi=150)


def main():
    symbols = "Ff+-"
    axiom = "F"
    N = 5
    # rule = generate_branched(N)
    rule = generate_continuous(N)
    print(rule)
    angle = random.choice(range(0, 181, 1))
    iteration = 8
    n = 50

    animator = LSystemAnimator(
        interval=1,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        # start_position=(-n//2+10, -10),
        nlimit=n,
        line_width=1,
    )

    contd = bool(input("Want to generate?(y/n)").strip().lower() == "y")
    if not contd:
        print("See ya sucker...")
        sys.exit(0)

    animator.animate(len(animator.coords))
    animator.save(f"out/curves/random-{int(time.time())}.mp4", fps=25, dpi=150)


if __name__ == "__main__":
    # main()
    multiple()
