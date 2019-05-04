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

def binary_fractal_tree():
    angle = 45
    iteration = 7
    axiom = 'A'
    rule = {
        'A': 'F[+A]-A',
        'F': 'FF'
    }
    animator = BranchedLSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(0, -60)
    )
    animator.animate(len(animator.coords))
    animator.save("out/trees/binary-fractal-tree.mp4")

def wheat():
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
    animator.save("out/trees/wheat.mp4")

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

def tree1():
    angle = 25.7
    axiom = 'Y'
    rule = {
        'X': 'X[-FFF][+FFF]FX',
        'Y': 'YFX[+Y][-Y]'
    }
    iteration = 6
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
    animator.save("out/trees/tree1.mp4")

def tree2():
    angle = 22.5
    axiom = 'F'
    rule = {
        'F': ' FF+[+F-F-F]-[-F+F+F]'
    }
    iteration = 4
    animator = BranchedLSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(0, -30),
        nlimit=40
    )
    animator.animate(len(animator.coords))
    animator.save("out/trees/tree2.mp4")

def tree3():
    angle = 35
    axiom = 'F'
    rule = {
        'F': 'F[+FF][-FF]F[-F][+F]F'
    }
    iteration = 4
    animator = BranchedLSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(0, -40),
        nlimit=60
    )
    animator.animate(len(animator.coords))
    animator.save("out/trees/tree3.mp4")

def tree4():
    angle = 20
    axiom = 'VZFFF'
    rule = {
        'V': '[+++W][---W]YV',
        'W': '+X[-W]Z',
        'X': '-W[+X]Z',
        'Y': 'YZ',
        'Z': '[-FFF][+FFF]F'

    }
    iteration = 8
    animator = BranchedLSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(0, 0),
        nlimit=30
    )
    animator.animate(len(animator.coords))
    animator.save("out/trees/tree4.mp4")


def main():
    start = time.time()
    # wheat()
    # binary_fractal_tree()
    # tree1()
    # tree2()
    # tree3()
    tree4()
    end = time.time()
    print("Time Taken :: {} seconds".format(end-start))


if __name__ == "__main__":
    main()
