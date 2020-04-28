#!/usr/bin/env python3

import sys
from pathlib import Path

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

import numpy as np
import matplotlib.pyplot as plt

from panim.lsystem import LSystemAnimator, BranchedLSystemAnimator
from panim.transformers import ZoomTransformer, RotationTransformer, TransformerPipeline

plt.style.use("dark_background")
plt.axis("off")


def hilbert():
    angle = 90
    axiom = "L"
    rule = {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"}
    iteration = 5
    n = 40
    animator = LSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(n // 2, -n // 2),
        nlimit=n,
    )

    zoomer = ZoomTransformer(animobj=animator, factor=500)
    zoomer.animate(len(animator.coords))
    zoomer.save("out/hilbert.mp4")


def test():
    rule = {"F": "FF+F-F+F+FF"}
    axiom = "F+F+F+F"
    angle = 90
    iteration = 3
    n = 500

    angle = 22.5
    axiom = "F"
    rule = {"F": " FF+[+F-F-F]-[-F+F+F]"}
    iteration = 5

    # animator = LSystemAnimator(
    #     interval=5,
    #     iteration=iteration,
    #     rule=rule,
    #     axiom=axiom,
    #     turn_angle=angle,
    #     # start_position=(0, -10),
    #     # nlimit=n,
    # )
    animator = BranchedLSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(0, -20),
        nlimit=n,
        color=(1, 0, 0),
    )

    zoom_factor = 500
    zoomer = ZoomTransformer(animobj=animator, factor=zoom_factor, nlimit=n)
    rotator = RotationTransformer(animobj=animator, nlimit=n, rotation_angle=0.1)

    pipeline = TransformerPipeline(
        animobj=animator, color=(1, 1, 1), transformers=[zoomer, rotator]
    )
    obj = pipeline
    obj.animate(len(animator.coords))
    obj.save("out/zoom-test-tree.mp4")


def main():
    test()


if __name__ == "__main__":
    main()
