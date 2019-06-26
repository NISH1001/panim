#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from panim.animator import AbstractImageAnimator, AbstractAnimator
from panim.utils import (
    meshgrid_polar,
    get_image_array
)

plt.style.use('dark_background')

class GenerativeArt(AbstractImageAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        self.r, self.a = meshgrid_polar(self.image_size)
        self.lr = np.log(1 + self.r)
        self.factor = -50
        self.p, self.q, self.r = -50, -40, 20

    def update(self, i):
        if -5 < self.p < 5:
            self.p += 0.01
        else:
            self.p += 0.2
        self.q += 0.1
        im = np.sin(self.a * self.p+ np.sin(self.lr * self.q) + self.lr*self.r)
        im = np.fmod((1 + im + self.lr), 1)
        im = get_image_array(im)
        im = self.ax.imshow(im, animated=True, cmap='gray')
        self.images.append([im])

class GenerativeArt2(AbstractAnimator):
    """
        This generate random hill-like stack of lines the height of which are animated.
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
        self.data[:, 0] = np.random.uniform(0, 1, len(self.data))

        # update data
        for j in range(len(self.data)):
            self.lines[j].set_ydata(j + self.G * self.data[j])
        return self.lines

    def _animate(self, i):
        print("Frame {}/{}".format(i, self.num_frames))
        self.lines = self.update(i)
        return self.lines


def main():
    animator = GenerativeArt(interval=1, clockwise=False, factor=0.1)
    animator.animate(2000)
    animator.save("out/spiral.mp4")

if __name__ == "__main__":
    main()

