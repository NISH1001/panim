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

def hilbert():
    angle = 90
    axiom = 'L'
    rule = {
        'L': '-RF+LFL+FR-',
        'R': '+LF-RFR-FL+'
    }
    iteration = 6
    n = 50
    animator = LSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(n//2, -n//2),
        nlimit=n
    )
    animator.animate(len(animator.coords))
    animator.save("out/curves/hilbert.mp4")

def dragoncurve():
    angle = 90
    iteration = 12
    rule = {
        'X': 'X+YF+',
        'Y': '-FX-Y'
    }
    axiom = 'FX'
    n = 60
    animator = LSystemAnimator(
        interval=20,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(-20, 20),
        nlimit=n
    )
    animator.animate(len(animator.coords))
    animator.save("out/curves/dragoncurve.mp4")

def sierpinski():
    angle = 60
    iteration = 7
    rule = {
        'B' : 'F+B+F',
        'F' : 'B−F−B',
    }
    axiom = 'F'
    animator = LSystemAnimator(
        interval=20,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        # start_position=(-20, 0),
        nlimit=30
    )
    animator.animate(len(animator.coords))
    animator.save("out/curves/sierpinski.mp4")

def sierpinski_square():
    angle = 90
    iteration = 5
    rule = {
        'X': 'XF-F+F-XF+F+XF-F+F-X'
    }
    axiom = 'F+XF+F+XF'
    n = 80
    animator = LSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(-n+10, 0),
        nlimit=n
    )
    animator.animate(len(animator.coords))
    animator.save("out/curves/sierpinski-square.mp4")

def sierpinski_arrowhead():
    angle = 60
    iteration = 5
    rule = {
        'X': 'YF+XF+Y',
        'Y': 'XF-YF-X'
    }
    axiom = 'YF+XF+YF-XF-YF-XF-YF+XF+YF'
    n = 80
    animator = LSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(40, -n+10),
        nlimit=n
    )
    animator.animate(len(animator.coords))
    animator.save("out/curves/sierpinski-arrowhead.mp4")

def crystal():
    angle = 90
    iteration = 4
    rule = {
        'F': 'FF+F++F+F'
    }
    axiom = 'F+F+F+F'
    n = 60
    animator = LSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(-n+15, -n//2),
        nlimit=n
    )
    animator.animate(len(animator.coords))
    animator.save("out/curves/crystal.mp4")

def snowflake():
    angle = 90
    iteration = 4
    rule = {
        'F': 'F-F+F+F-F'
    }
    axiom = 'F'
    n = 60
    animator = LSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(0, -n//2),
        nlimit=n
    )
    animator.animate(len(animator.coords))
    animator.save("out/curves/snoflake.mp4")

def snowflake2():
    angle = 90
    iteration = 4
    rule = {
        'F': 'F+F-F-F+F'
    }
    axiom = 'FF+FF+FF+FF'
    n = 100
    animator = LSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(-n+10, -n+15),
        nlimit=n
    )
    animator.animate(len(animator.coords))
    animator.save("out/curves/snoflake2.mp4")

def board():
    angle = 90
    iteration = 4
    rule = {
        'F': 'FF+F+F+F+FF'
    }
    axiom = 'F+F+F+F'
    n = 60
    animator = LSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(-n+15, -n//2),
        nlimit=n
    )
    animator.animate(len(animator.coords))
    animator.save("out/curves/board.mp4")

def quadratic_koch():
    angle = 45
    iteration = 3
    rule = {
        'X': 'X+YF++YF-FX--FXFX-YF+X',
        'Y': '-FX+YFYF++YF+FX--FX-YF'
    }
    axiom = 'X+X+X+X+X+X+X+X'
    n = 150
    animator = LSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(-n+40, n//2+15),
        nlimit=n
    )
    animator.animate(len(animator.coords))
    animator.save("out/curves/koch-quadratic.mp4")



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

def pentaplexity():
    # http://paulbourke.net/fractals/lsys/
    angle = 35
    iteration = 3
    rule = {
        'F' : 'F[+FF][-FF]F[-F][+F]F'
    }
    axiom = 'F'

    rule = {
        'F' : 'F++F++F|F-F++F'
    }
    axiom = 'F++F++F++F++F'
    angle = 36
    iteration = 4
    n = 50

    animator = LSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(-n//2, -n//2),
        nlimit=n,
    )
    animator.animate(len(animator.coords))
    animator.save("out/curves/pentaplexity.mp4")

def tiles():
    rule = {
        'F': 'FF+F-F+F+FF'
    }
    axiom = 'F+F+F+F'
    angle = 90
    iteration = 4
    n = 50

    animator = LSystemAnimator(
        interval=5,
        iteration=iteration,
        rule=rule,
        axiom=axiom,
        turn_angle=angle,
        start_position=(-n//2+10, -10),
        nlimit=n,
    )
    animator.animate(len(animator.coords))
    animator.save("out/curves/tiles.mp4")

def spiral():
    """
        Generate spirals using L-System rules
    """
    rule = {
        'X': 'XF',
        'Y': 'Y+XF+XF'
    }
    axiom = '-Y'
    # change angle to generate non-square spirals
    # 90 -> Square
    angle = 90
    iteration = 75
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
    animator.animate(len(animator.coords))
    animator.save("out/curves/spiral.mp4", fps=60)

def main():
    start = time.time()
    # hilbert()
    # dragoncurve()
    # sierpinski()
    # sierpinski_square()
    # crystal()
    # snowflake()
    # snowflake2()
    # board()
    # quadratic_koch()
    # sierpinski_arrowhead()
    # pentaplexity()
    # tiles()
    spiral()
    end = time.time()
    print("Time Taken :: {} seconds".format(end-start))


if __name__ == "__main__":
    main()
