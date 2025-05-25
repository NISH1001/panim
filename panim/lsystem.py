#!/usr/bin/env python3
"""
This module provides classes for generating and animating L-systems (Lindenmayer systems).

It includes base classes for L-system string generation (`LSystem`, `BranchedLSystem`)
and animator classes (`LSystemAnimator`, `BranchedLSystemAnimator`) that extend
the core animator functionality to render these L-systems.
"""

import numpy as np
import matplotlib.pyplot as plt

from panim.animator import AbstractAnimator

plt.style.use("dark_background")
# plt.xkcd()

DEGREES_TO_RADIANS = np.pi / 180


class LSystem:
    """
    Generates and processes Lindenmayer System (L-system) strings.

    This class takes an initial axiom, a set of production rules, and a number of iterations
    to generate a final L-system string. It also provides methods to simulate a "turtle"
    graphics interpretation of the generated string, producing coordinates for drawing.

    Key Attributes:
        axiom (str): The starting string for the L-system.
        rule (dict): A dictionary defining the production rules (e.g., {"F": "F+F-"}).
        turn_angle (float): The angle (in degrees) for turtle turns (+ or - commands).
        iteration (int): The number of times the rules are applied to the axiom.
        seq (str): The final generated L-system string after all iterations.
        start_position (tuple): The (x, y) starting coordinates for turtle simulation.

    The recognized symbols for turtle interpretation are:
        'F': Move forward by 1 unit and draw a line.
        'f': Move forward by 1 unit without drawing a line.
        '+': Rotate clockwise by `turn_angle`.
        '-': Rotate counter-clockwise by `turn_angle`.
        '|': Rotate by 180 degrees.
    """

    def __init__(
        self, axiom: str, rule: dict, turn_angle: float = 45.0, start_position: tuple = (0.0, 0.0), iteration: int = 5
    ):
        """
        Initializes the LSystem.

        Args:
            axiom (str): The initial string (seed) of the L-system.
            rule (dict): A dictionary of rules for transforming symbols.
                         Example: `{"F": "F+F-", "X": "FX"}`.
            turn_angle (float, optional): The angle in degrees for turning commands ('+' or '-').
                                         Defaults to 45.0.
            start_position (tuple, optional): The (x, y) coordinate where the turtle starts.
                                              Defaults to (0.0, 0.0).
            iteration (int, optional): The number of times the transformation rule is applied.
                                       Defaults to 5.
        """
        self.axiom = axiom
        self.rule = rule
        self.turn_angle = turn_angle
        self.seq = self.transform_multiple(axiom, rule, iteration)
        self.start_position = start_position
        self.iteration = iteration

    def transform_sequence(self, sequence: str, rule: dict) -> str:
        """
        Applies the transformation rule to a sequence once.

        For each character in the input sequence, if the character is a key in the
        rule dictionary, it's replaced by its corresponding value. Otherwise,
        the character remains unchanged.

        Args:
            sequence (str): The input string sequence to transform.
            rule (dict): The dictionary of transformation rules.

        Returns:
            str: The transformed sequence.
        """
        return "".join(rule.get(c, c) for c in sequence)

    def transform_multiple(self, sequence: str, rule: dict, iteration: int) -> str:
        """
        Applies the transformation rule to a sequence multiple times.

        This method iteratively calls `transform_sequence` for the specified
        number of iterations.

        Args:
            sequence (str): The initial string sequence.
            rule (dict): The dictionary of transformation rules.
            iteration (int): The number of times to apply the transformation.

        Returns:
            str: The final sequence after all iterations.
        """
        seq = sequence
        for _ in range(iteration):
            seq = self.transform_sequence(seq, rule)
        return seq

    def invoke(self) -> iter:
        """
        Generates turtle coordinates by simulating the L-system string.

        This method is a generator that yields (x, y) coordinates produced by
        the `simulate_turtle` method based on the L-system's final sequence (`self.seq`),
        start position, and turn angle.

        Yields:
            iter: An iterator of (x, y) coordinate tuples.
        """
        for c in self.simulate_turtle(self.seq, self.start_position, self.turn_angle):
            yield c

    def get_coordinates(self) -> list[tuple]:
        """
        Returns a list of all turtle coordinates for the L-system string.

        This is an alternative to `invoke` that collects all generated coordinates
        into a list.

        Returns:
            list[tuple]: A list of (x, y) coordinate tuples.
        """
        return [
            c
            for c in self.simulate_turtle(
                self.seq, self.start_position, self.turn_angle
            )
        ]

    def simulate_turtle(self, sequence: str, start_position: tuple, turn_angle: float) -> iter:
        """
        Simulates a turtle interpreting the L-system sequence to generate coordinates.

        The turtle starts at `start_position` facing upwards (90 degrees).
        It processes each symbol in the sequence:
        - 'F', 'f': Moves forward. 'F' implies drawing, 'f' does not (though drawing
          is handled by yielding coordinates; 'f' yields a NaN break point).
        - '+': Turns clockwise.
        - '-': Turns counter-clockwise.
        - '|': Turns 180 degrees.

        Args:
            sequence (str): The L-system string to interpret.
            start_position (tuple): The (x, y) starting coordinates.
            turn_angle (float): The angle in degrees for turns.

        Yields:
            iter: An iterator of (x, y) coordinate tuples. A `(float('nan'), float('nan'))`
                  tuple is yielded to indicate a break in the path (e.g., for 'f' moves).
        """
        # (x, y, angle)
        state = (*start_position, 90)

        # starting point
        yield start_position

        # Loop over the every symbol
        for symbol in sequence:
            x, y, angle = state

            # Move turtle forward
            if symbol in "Ff":
                state = (
                    x - np.cos(angle * DEGREES_TO_RADIANS),
                    y + np.sin(angle * DEGREES_TO_RADIANS),
                    angle,
                )

                if symbol == "f":
                    # Insert a break in the path to not draw the line
                    yield (float("nan"), float("nan"))

                yield (state[0], state[1])

            # turn clockwise without moving
            elif symbol == "+":
                state = (x, y, angle + turn_angle)
                # yield (x, y)

            # turn counter-clockwise without moving
            elif symbol == "-":
                state = (x, y, angle - turn_angle)
                # yield (x, y)

            elif symbol == "|":
                state = (x, y, angle - 180)
                # yield (x, y)

    def __str__(self):
        return f"~{self.__class__.__name__}~\n" + "Axiom={}\nRule={}\nTurn Angle={}\nIterations={}\nFinal Sequence Length={}\nStart Position={}".format(
            self.axiom,
            self.rule,
            self.turn_angle,
            self.iteration,
            len(self.seq),
            self.start_position,
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
            (kind of: "remember 'this'")
        ] : pop state (position and angle)
            (kind of: "go back to that last remember state")

    """

    def simulate_turtle(self, sequence: str, start_position: tuple, turn_angle: float) -> iter:
        """
        Simulates a turtle for Branched L-systems, supporting state saving and restoring.

        In addition to the standard L-system symbols, this version supports:
        - '[': Pushes (saves) the current turtle state (position and angle) onto a stack.
        - ']': Pops (restores) a state from the stack, making the turtle jump to that
               saved position and orientation. A NaN coordinate pair is yielded before
               and after the jump to create a break in the drawn line.
        - Lowercase letters 'a'-'j': Behave like 'F' (move and draw) but also yield a NaN
          break point *before* drawing the segment if the symbol itself is lowercase,
          effectively treating them like 'f' for path breaking but 'F' for drawing.
          (Note: The original code's comment says "Add a break in the line if symbol matches a-j",
          and "if symbol.islower(): yield (float('nan'), float('nan'))". This means
          any lowercase letter used for drawing will first break the line.)


        Args:
            sequence (str): The L-system string to interpret.
            start_position (tuple): The (x, y) starting coordinates.
            turn_angle (float): The angle in degrees for turns.

        Yields:
            iter: An iterator of (x, y) coordinate tuples. NaN coordinates indicate path breaks.
        """
        saved_states = []
        state = (*start_position, 90)
        yield start_position

        for symbol in sequence:
            x, y, angle = state

            if symbol.lower() in "abcdefghij":
                # if symbol in 'Ff':
                state = (
                    x - np.cos(angle * DEGREES_TO_RADIANS),
                    y + np.sin(angle * DEGREES_TO_RADIANS),
                    angle,
                )

                # Add a break in the line if symbol matches a-j
                # if symbol == 'f':
                if symbol.islower():
                    yield (float("nan"), float("nan"))

                yield (state[0], state[1])

            elif symbol == "+":
                state = (x, y, angle + turn_angle)

            elif symbol == "-":
                state = (x, y, angle - turn_angle)

            # Remember current state
            elif symbol == "[":
                saved_states.append(state)

            # Return to previous state
            elif symbol == "]":
                state = saved_states.pop()
                yield (float("nan"), float("nan"))
                x, y, _ = state
                yield (x, y)


class LSystemAnimator(AbstractAnimator):
    """
    Animates L-systems generated by the `LSystem` class.

    This class extends `AbstractAnimator` to create visual animations from the
    coordinate sequences produced by an `LSystem` object. It takes L-system
    parameters (axiom, rule, etc.), generates the coordinates, and then animates
    the drawing of the L-system path frame by frame.
    """
    def __init__(self, **args):
        """
        Initializes the LSystemAnimator.

        Args:
            axiom (str, optional): The axiom for the L-system. Defaults to "F".
            rule (dict, optional): The production rules for the L-system.
                                   Defaults to `{"F": "FfF++"}`.
            turn_angle (float, optional): The angle for turtle turns in degrees.
                                          Defaults to 45.0.
            iteration (int, optional): The number of iterations for L-system generation.
                                       Defaults to 15.
            start_position (tuple, optional): The (x, y) starting position for drawing.
                                              Defaults to (0.0, 0.0).
            **args: Additional keyword arguments passed to the parent `AbstractAnimator`
                    (e.g., `interval`, `color`, `line_width`, `nlimit`).
        """
        super().__init__(**args)
        # self.program = args.get('program', 'FfF++FfF++FfF++FfF')
        axiom = args.get("axiom", "F")
        rule = args.get("rule", {"F": "FfF++"})
        turn_angle = args.get("turn_angle", 45.0)
        iteration = args.get("iteration", 15)
        start_position = args.get("start_position", (0.0, 0.0))
        self.lsystem = LSystem(
            axiom=axiom,
            rule=rule,
            turn_angle=turn_angle,
            iteration=iteration,
            start_position=start_position,
        )
        self.coords = [c for c in self.lsystem.invoke()]

    def update(self, i: int) -> tuple[list, list]:
        """
        Provides the data for the current animation frame.

        For frame `i`, this method returns the X and Y coordinates of the L-system's
        path up to the `i`-th point.

        Args:
            i (int): The current frame number.

        Returns:
            tuple[list, list]: A tuple containing two lists: the X coordinates and
                               the Y coordinates for the path to be drawn.
        """
        return zip(*self.coords[: i + 1])

    def __str__(self):
        return (
            f"coords-length={len(self.coords)}\n"
            + str(self.lsystem)
            + f"End-Position={self.coords[-1]}\n"
        )


class BranchedLSystemAnimator(LSystemAnimator):
    """
    Animates branched L-systems generated by the `BranchedLSystem` class.

    This class extends `LSystemAnimator` to specifically handle L-systems
    that use branching symbols ('[' and ']') by utilizing the `BranchedLSystem`
    for coordinate generation.
    """
    def __init__(self, **args):
        """
        Initializes the BranchedLSystemAnimator.

        The parameters are identical to `LSystemAnimator`, but this animator
        instantiates a `BranchedLSystem` internally to handle L-systems
        with branching rules.

        Args:
            axiom (str, optional): The axiom for the branched L-system. Defaults to "F".
            rule (dict, optional): The production rules. Defaults to `{"F": "FfF++"}`.
            turn_angle (float, optional): Angle for turtle turns. Defaults to 45.0.
            iteration (int, optional): Number of iterations. Defaults to 15.
            start_position (tuple, optional): Start (x,y) position. Defaults to (0.0, 0.0).
            **args: Additional keyword arguments passed to `LSystemAnimator` and
                    subsequently to `AbstractAnimator`.
        """
        super().__init__(**args)
        # self.program = args.get('program', 'FfF++FfF++FfF++FfF')
        axiom = args.get("axiom", "F")
        rule = args.get("rule", {"F": "FfF++"})
        turn_angle = args.get("turn_angle", 45.0)
        iteration = args.get("iteration", 15)
        start_position = args.get("start_position", (0.0, 0.0))
        self.lsystem = BranchedLSystem(
            axiom=axiom,
            rule=rule,
            turn_angle=turn_angle,
            iteration=iteration,
            start_position=start_position,
        )
        self.coords = [c for c in self.lsystem.invoke()]
        print(self.lsystem)


def main():
    """
    Example usage function for demonstrating LSystemAnimator.

    This function sets up parameters for a Hilbert curve L-system and
    animates it, then saves the animation to a file.
    """
    rule = {"F": "+F+F--F+F"}
    axiom = "F"
    angle = 45

    # hilbert
    axiom = "L"
    rule = {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"}
    angle = 90

    animator = LSystemAnimator(
        interval=50, iteration=5, rule=rule, axiom=axiom, turn_angle=angle
    )
    animator.animate(len(animator.coords))
    # animator.animate(500)
    animator.save("out/ls.mp4")

    # lsystem = LSystem(axiom=axiom, rule=rule, turn_angle=90, iteration=5)
    # coords = [ c for c in lsystem.invoke() ]
    # print(coords)


if __name__ == "__main__":
    main()
