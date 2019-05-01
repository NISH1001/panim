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

def draw_binary_fractal_tree():
    angle = 45
    iteration = 6
    axiom = 'A'
    rule = {
        'A': 'F[+A]-A',
        'F': 'FF'
    }
    animator = BranchedLSystemAnimator(
        interval=20,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(0, -50)
    )
    animator.animate(len(animator.coords))
    animator.save("out/binary-fractal-tree.mp4")

def draw_wheat():
    angle = 22.5
    iteration = 5
    rule = {
        'F': 'FF',
        'A': 'F[+AF-[A]--A][---A]'
    }
    axiom = 'A'

    animator = BranchedLSystemAnimator(
        interval=20,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(0,-50)
    )
    animator.animate(len(animator.coords))
    animator.save("out/wheat.mp4")

def draw_simple_tree():
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

def draw_dragoncurve():
    angle = 90
    iteration = 11
    rule = {
        'X': 'X+YF+',
        'Y': '-FX-Y'
    }
    axiom = 'FX'
    animator = BranchedLSystemAnimator(
        interval=20,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(-20, 0)
    )
    animator.animate(len(animator.coords))
    animator.save("out/dragoncurve.mp4")

def draw_sierpinski():
    angle = 60
    iteration = 6
    rule = {
        'A' : 'B−A−B',
        'B' : 'A+B+A'
    }
    axiom = 'A'
    animator = BranchedLSystemAnimator(
        interval=20,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle
        # start_position=(-20, 0)
    )
    animator.animate(len(animator.coords))
    animator.save("out/sierpinski.mp4")


def test():
    angle = 30
    iteration = 4
    rule = {
        'F': 'F[-F][+F]'
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
    animator.save("out/test.mp4")

def test2():
    # http://www.motionesque.com/beautyoffractals/#!
    angle = 45
    iteration = 4

    rule = {
        'F' : 'F- – -F+F+F+F+F+F+F- – -F'
    }
    axiom = 'F-F-F-F-F-F-F-F'


    rule = {
        'F' : 'F+F- -F+F'
    }
    axiom = 'F++F++F'

    # 2
    angle = 40
    iteration = 2
    rule = {
        'F': 'F---F+F+F+F+F+F+F---F'
    }
    axiom = 'F+F+F+F+F+F+F+F+F'

    # 6
    angle = 72
    iteration = 3
    rule = {
        'F' : 'F-F+F+F+F--F'
    }
    axiom = 'F+F+F+F+F'

    animator = LSystemAnimator(
        interval=20,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(-25, 0)
    )
    animator.animate(len(animator.coords))
    animator.save("out/test.mp4")

def main():
    # draw_wheat()
    # draw_binary_fractal_tree()
    # draw_dragoncurve()
    # draw_sierpinski()
    test2()


if __name__ == "__main__":
    main()
