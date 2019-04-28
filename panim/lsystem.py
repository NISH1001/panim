#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from panim.animator import AbstractAnimator

plt.style.use('dark_background')

DEGREES_TO_RADIANS = np.pi / 180

class LSystem:
    """
        This is used to simulate Lindenmayer System.

        axiom:
            initial sequence (base)
        rule:
            transformation rule to apply to sequence
        turn_angle:
            anglye by which the turtle is rotated (+ve turn implies clockwise)
        iteration:
            total number of times the transfomration is applied successively to sequence


        The Symbols in the sequence after applying transformation are meant as:
            F : move 1 unit forward and also draw line while doing so
            f : move 1 unit forward without tracing a line
            + : rotate clockwise without moving forward
            - : rotate counter-clockwise without moving forward

    """
    def __init__(self, axiom, rule, turn_angle=45.0, start_position=(0.0, 0.0), iteration=5):
        self.axiom = axiom
        self.rule = rule
        self.turn_angle = turn_angle
        self.seq = self.transform_multiple(axiom, rule, iteration)
        self.start_position = start_position
        self.iteration = iteration

    def transform_sequence(self, sequence, rule):
        """
            Apply transformation to the sequence based on the rule.

            rule:
                a dictionary with mapping from a symbol to new symbol
        """
        return ''.join(rule.get(c, c) for c in sequence)

    def transform_multiple(self, sequence, rule, iteration):
        seq = sequence
        for _ in range(iteration):
            seq = self.transform_sequence(seq, rule)
        return seq

    def invoke(self):
        """
            A generator expression wrapper around simulate_turtle.
        """
        for c in self.simulate_turtle( self.seq, self.start_position, self.turn_angle):
            yield c

    def get_coordinates(self):
        """
            Return list of all the coordinates.
            This is an alternate to `invoke`.
        """
        return [
            c for c in self.simulate_turtle(
                self.seq,
                self.start_position,
                self.turn_angle
        )]

    def simulate_turtle(self, sequence, start_position, turn_angle):
        # (x, y, angle)
        state = (*start_position, 90)

        # starting point
        yield start_position

        # Loop over the every symbol
        for symbol in sequence:
            x, y, angle = state

            # Move turtle forward
            if symbol in 'Ff':
                state = (x - np.cos(angle * DEGREES_TO_RADIANS),
                        y + np.sin(angle * DEGREES_TO_RADIANS),
                        angle)

                if symbol == 'f':
                    # Insert a break in the path so that
                    # this line segment isn't drawn.
                    yield (float('nan'), float('nan'))

                yield (state[0], state[1])

            # turn clockwise without moving
            elif symbol == '+':
                state = (x, y, angle + turn_angle)
                # yield (x, y)

            # turn counter-clockwise without moving
            elif symbol == '-':
                state = (x, y, angle - turn_angle)
                # yield (x, y)

    def __str__(self):
        return "Axiom={}\nRule={}\nTurn Angle={}\nIterations={}\nFinal Sequence Length={}".format(
            self.axiom, self.rule, self.turn_angle, self.iteration, len(self.seq)
        )

class BranchedLSystem(LSystem):
    """
        A more complicated L-System in which we create discontinuity
        so that we can branch off at some parts, remembering the states.
        This is used to create complicated fractals like Tree Branches.

        This system has two more symbols: '[' and ']'
            F : move 1 unit forward and also draw line while doing so
            f : move 1 unit forward without tracing a line
            + : rotate clockwise without moving forward
            - : rotate counter-clockwise without moving forward
            [ : push (save) state (position and angle)
            ] : pop state (position and angle)

    """
    def simulate_turtle(self, sequence, start_position, turn_angle):
        saved_states = []
        state = (*start_position, 90)
        yield start_position

        for symbol in sequence:
            x, y, angle = state

            if symbol.lower() in 'abcdefghij':
            # if symbol in 'Ff':
                state = (x - np.cos(angle * DEGREES_TO_RADIANS),
                        y + np.sin(angle * DEGREES_TO_RADIANS),
                        angle)

                # Add a break in the line if symbol matches a-j
                # if symbol == 'f':
                if symbol.islower():
                    yield (float('nan'), float('nan'))

                yield (state[0], state[1])

            elif symbol == '+':
                state = (x, y, angle + turn_angle)

            elif symbol == '-':
                state = (x, y, angle - turn_angle)

            # Remember current state
            elif symbol == '[':
                saved_states.append(state)

            # Return to previous state
            elif symbol == ']':
                state = saved_states.pop()
                yield (float('nan'), float('nan'))
                x, y, _ = state
                yield (x, y)


class LSystemAnimator(AbstractAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        # self.program = args.get('program', 'FfF++FfF++FfF++FfF')
        axiom = args.get('axiom', 'F')
        rule = args.get('rule', {'F': 'FfF++'})
        turn_angle = args.get('turn_angle', 45.0)
        iteration = args.get('iteration', 15)
        self.lsystem = LSystem(axiom=axiom, rule=rule, turn_angle=turn_angle, iteration=iteration)
        self.coords = [ c for c in self.lsystem.invoke() ]
        print(self.lsystem)

    def update(self, i):
        return zip(*self.coords[:i+1])


class BranchedLSystemAnimator(AbstractAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        # self.program = args.get('program', 'FfF++FfF++FfF++FfF')
        axiom = args.get('axiom', 'F')
        rule = args.get('rule', {'F': 'FfF++'})
        turn_angle = args.get('turn_angle', 45.0)
        iteration = args.get('iteration', 15)
        self.lsystem = BranchedLSystem(axiom=axiom, rule=rule, turn_angle=turn_angle, iteration=iteration)
        self.coords = [ c for c in self.lsystem.invoke() ]
        print(self.lsystem)

    def update(self, i):
        return zip(*self.coords[:i+1])


def main():
    rule = {'F': '+F+F--F+F'}
    axiom = 'F'
    angle = 45

    # hilbert
    axiom = 'L'
    rule = {
        'L': '-RF+LFL+FR-',
        'R': '+LF-RFR-FL+'
    }
    angle = 90

    animator = LSystemAnimator(interval=50, iteration=5, rule=rule, axiom=axiom, turn_angle=angle)
    animator.animate(len(animator.coords))
    # animator.animate(500)
    animator.save("out/ls.mp4")

    # lsystem = LSystem(axiom=axiom, rule=rule, turn_angle=90, iteration=5)
    # coords = [ c for c in lsystem.invoke() ]
    # print(coords)

if __name__ == "__main__":
    main()

