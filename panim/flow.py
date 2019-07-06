#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import random

from panim.animator import AbstractAnimator
plt.style.use('dark_background')

class FlowAnimator(AbstractAnimator):
    """
        This generates random hill-like stack of lines the height of which are animated.
        The result is more like a flowing hills.
    """
    def __init__(self, **args):
        super().__init__(**args)
        self.fig = plt.figure(figsize=(13.68, 7.2), facecolor='black')
        self.ax = plt.subplot(111, frameon=False)

        self.nlines = args.get('nlines', 70)
        self.npoints = args.get('npoints', 80)
        self.perspective = args.get('perspective', 150)
        self.setup()

    def setup(self, *args):
        # random Y points
        self.data = np.random.uniform(0, 1, (self.nlines, self.npoints))
        X = np.linspace(-1, 1, self.data.shape[-1])

        # gravity for the hills
        self.G = 2.5 * np.exp(-4 * X ** 2)
        self.val = 1

        self.lines = []
        for i in range(len(self.data)):
            # small reduction of the X extents to get a cheap perspective effect
            xscale = 1 - i / self.perspective
            # same for linewidth (thicker strokes on bottom)
            lw = 1.5 - i / 100.0
            line, = self.ax.plot(xscale * X, i + self.G * self.data[i], color="w", lw=lw)
            self.lines.append(line)

    def update(self, i):
        self.data[:, 1:] = self.data[:, :-1]
        # fill-in new values
        if i % 100 == 0:
            self.val = random.choices([0.1, 0.2, 1, 2, 3, 4], [0.1, 0.1, 0.6, 0.1, 0.1, 0.1])
        self.data[:, 0] = self.val*np.random.uniform(0, 1, len(self.data))

        # update data
        for j in range(len(self.data)):
            self.lines[j].set_ydata(j + self.G * self.data[j])
        return self.lines

    def _animate(self, i):
        print("Frame {}/{}".format(i, self.num_frames))
        self.lines = self.update(i)
        return self.lines


def main():
    pass

if __name__ == "__main__":
    main()

