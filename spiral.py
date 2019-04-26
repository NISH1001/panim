#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from animator import AbstractAnimator

plt.style.use('dark_background')

class SpiralAnimator(AbstractAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        self.clockwise = self.args.get('clockwise', True)
        self.factor = 1 if self.clockwise else -1

    def _update(self, i):
        t = 0.1 * i * self.factor

        # x, y values to be plotted
        x, y = t*np.sin(t), t*np.cos(t)

        self.coords.append((x, y))
        X, Y = zip(*self.coords)
        return X, Y


def main():
    animator = SpiralAnimator(interval=1, clockwise=False)
    animator.animate(500)
    animator.save("out/spiral.mp4")

if __name__ == "__main__":
    main()

