#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from animator import AbstractAnimator

plt.style.use('dark_background')

class BoxSizeAnimator(AbstractAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        self.size = args['size']
        self.val = 1
        self.toggle = args.get('toggle', False)
        self.factor = args['factor']
        self.coords = np.array([(-1, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)])

    def _update(self, i):
        coords = self.coords * self.size * self.val
        X, Y = zip(*coords)
        self.val += self.factor
        if self.toggle:
            if self.val < 0 or self.val > 1:
                self.factor *= -1
        # self.coords = self.coords * self.factor
        return X, Y

def main():
    animator = BoxSizeAnimator(interval=5, size=50, factor=-0.05, toggle=True)
    animator.animate(500)
    animator.save("out/box.mp4")

if __name__ == "__main__":
    main()

