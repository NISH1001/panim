#!/usr/bin/env python3

import sys
from pathlib import Path

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



def main():
    # animator = AbstractAnimator() # we cannot initialize this
    # animator = ImageAnimator() # we cannot initialize this
    # animator.animate(500)
    # animator.save("out/experiment.mp4", fps=24)

    animator = SineArt()
    animator.animate(500)
    animator.save("out/tangentsine.mp4", fps=24)

if __name__ == "__main__":
    main()

