#!/usr/bin/env python3

import sys
from pathlib import Path
import random

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

import matplotlib.pyplot as plt
from matplotlib import animation

from abc import ABCMeta, ABC, abstractmethod
from abc import ABC, abstractmethod

import numpy as np

from panim.animator import (
    AbstractAnimator,
    AbstractImageAnimator
)

from panim.spiral import (
    SpiralAnimator
)

plt.style.use('dark_background')


class ImageAnimator(AbstractAnimator):
    def __init__(self, **args):
        self.args = args
        self.interval = args.get('interval', 1)
        self.fig = plt.figure()
        self.image_size = (args.get('width', 800), args.get('height', 600))
        w, h = self.image_size
        # self.fig.set_size_inches(w/100, h/100, True)
        self.ax = plt.axes(xlim=(0, w), ylim=(0, h))

        self.x = np.linspace(0, 2 * np.pi, self.image_size[0])
        self.y = np.linspace(0, 2 * np.pi, self.image_size[1]).reshape(-1, 1)

        img = np.random.random((self.image_size[1], self.image_size[0]))
        self.img = np.sin(img) + np.cos(img)
        self.image = plt.imshow(img, animated=True)
        # self.image = plt.imshow(self.f(self.x, self.y), animated=True)

    def f(self, x, y):
        return np.sin(x) + np.cos(y)

    def update(self, i):
        print(i)
        # self.x += np.pi / 15.
        # self.y += np.pi / 20.
        self.img += 10
        # self.image.set_array(self.f(self.x, self.y))
        self.img = np.sin(self.img) + np.cos(self.img)
        # self.image = plt.imshow(self.img, animated=True)
        self.image.set_array(self.img)
        return self.image,

    def _animate(self, *args):
        return self.update(args)

class RandomGenerativeArt(AbstractImageAnimator):
    def __init__(self, **args):
        super().__init__(**args)

    def update(self, i):
        sigma = 1 if i<100 else i//100
        im = np.random.random((self.image_size[1], self.image_size[0]))
        return gaussian_filter(im, sigma=sigma)

class SineArt(SpiralAnimator):
    def __init__(self, **args):
        super().__init__(**args)

    def update(self, i):
        xs =  np.arange(-20, 20, 0.01) * i
        ys = np.sin(xs) * i%25
        X = xs
        # x0 = X[i]
        # yt = np.cos(x0) * (xs - x0) + np.sin(x0)
        # return xs, np.cos(x0) * (xs - x0) + np.sin(x0)
        return xs, ys

class RowArt(AbstractImageAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        self.array = np.zeros((self.image_size[1], self.image_size[0]))
        self.array2 = np.zeros((self.image_size[1], self.image_size[0]))

    def update(self, i):
        # for columns
        self.array[:, i] = 0
        self.array[:, i+1] = 255

        # for rows
        self.array[i+1, :] = 255
        self.array[i, :] = 0
        return self.array

class MetaBall(AbstractAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        self.x0, self.y0 = 0, 0
        self.xc = np.arange(0, 100, 0.01)
        self.yc = np.sin(self.xc) * 5

    def update(self, i):
        r = 1
        # a =  np.arange(-20, 20, 1)
        # self.x0 = self.xc[i] * 10
        # self.y0 = self.yc[i] * 1
        X =  np.arange(-1, 1, 0.1)
        Y =  np.arange(-1, 1, 0.1)
        # Y = (r**2 - (X-self.x0)**2)**0.5
        val = ((X - self.x0)**2 + (Y -self.y0) ** 2) / r**2

        # self.x0 += 0.2
        # self.y0 += 0.2
        # return np.hstack([X, X]), np.hstack([Y+self.y0, -Y+self.y0])
        bools = val>0.9
        print(bools.sum())
        return X[bools]*100, Y[bools]*100

class MetaBall2(AbstractImageAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        self.x0, self.y0 = 0, 0
        self.array = np.zeros((self.image_size[1], self.image_size[0]))
        self.direction = 1
        self.val = 0.4
        self.r = 0.1
        self.direction = 1

    def update(self, i):
        arr = np.zeros_like(self.array)
        # arr2 = np.zeros_like(self.array)
        if self. r < 0.1:
            self.x0, self.y0 = np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5)
        r = self.r
        nr, nc = arr.shape
        xs = np.linspace(-1, 1, nc)
        ys = np.linspace(-1, 1, nr)
        for col, x in enumerate(xs):
            for row, y in enumerate(ys):
                val = ((x - self.x0)**2 + (y -self.y0) ** 2) / r**2
                # val2 = ((x - self.x0-0.2)**2 + (y -self.y0-0.2) ** 2) / r**2
                if val > self.val:
                    arr[row][col] = 255
                # if val2 < 0.5:
                #     arr2[i][j] = 255


        if self.r >= 1:
            self.direction *= -1
        if self.r < 0.1:
            self.r = 0.1
            self.direction *= -1
        self.r += 0.05*self.direction
        return arr
        # return np.logical_or(arr, arr2)

class MetaBall3(AbstractImageAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        self.x0, self.y0 = 0, 0
        self.array = np.zeros((self.image_size[1], self.image_size[0]))
        self.n = args.get('n', 3)
        self.directions = [random.choice([-1, 1]) for i in range(self.n) ]
        self.thresholds = [random.choice([0.1, 0.2, 0.3, 0.4]) for i in range(self.n) ]
        self.deltas = [random.choice([0.01, 0.02, 0.03, 0.04, 0.05]) for i in range(self.n) ]
        self.radii = [random.choice([0.1, 0.2, 0.3, 0.4]) for i in range(self.n) ]
        self.centres = [(np.random.uniform(-0.9, 0.9), np.random.uniform(-0.9, 0.9)) for i in range(self.n) ]
        self.colors = [random.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1.0]) for i in range(self.n) ]

    def update(self, i):
        arr = np.zeros_like(self.array)
        nr, nc = arr.shape
        xs = np.linspace(-1, 1, nc)
        ys = np.linspace(-1, 1, nr)

        # go through every pixel and evaluate the function
        for col, x in enumerate(xs):
            for row, y in enumerate(ys):
                for radius, threshold, centre, color in zip(self.radii, self.thresholds, self.centres, self.colors):
                    x0, y0 = centre
                    val = ((x - x0)**2 + (y -y0) ** 2) / radius**2
                    if val < threshold:
                        arr[row][col] = color

        # update params
        for i, (r, d) in enumerate(zip(self.radii, self.directions)):
            if r >= 0.9:
                self.directions[i] *= -1
            if r < 0.1:
                self.radii[i] = 0.1
                self.directions[i] *= -1
                self.centres[i] = (np.random.uniform(-0.8, 0.8), np.random.uniform(-0.8, 0.8))
            self.radii[i] += self.deltas[i] * self.directions[i]
            self.colors[i] += self.deltas[i] * self.directions[i]
        return arr




def main():
    # animator = AbstractAnimator() # we cannot initialize this
    # animator = ImageAnimator() # we cannot initialize this
    # animator.animate(500)
    # animator.save("out/experiment.mp4", fps=24)

    # animator = SineArt()
    # animator.animate(500)
    # animator.save("out/tangentsine.mp4", fps=24)

    # animator = RowArt()
    # animator.animate(100)
    # animator.save("out/row.mp4", fps=24)

    animator = MetaBall3(
        width=400,
        height=400,
        n=11,
    )
    animator.animate(250)
    animator.save("out/metaball.mp4", fps=24)

if __name__ == "__main__":
    main()

