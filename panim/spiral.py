#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from panim.animator import AbstractAnimator

plt.style.use('dark_background')

class SpiralAnimator(AbstractAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        self.clockwise = self.args.get('clockwise', True)
        self.factor = self.args.get('factor', 0.1)
        self.rotation= 1 if self.clockwise else -1

    def update(self, i):
        t = self.factor * i * self.rotation

        # x, y values to be plotted
        x, y = t*np.sin(t), t*np.cos(t)
        # y = 0

        self.coords.append((x, y))
        X, Y = zip(*self.coords)
        return X, Y


def main():
    animator = SpiralAnimator(interval=1, clockwise=False, factor=0.1)
    animator.animate(500)
    animator.save("out/spiral.mp4")

if __name__ == "__main__":
    main()

