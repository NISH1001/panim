#!/usr/bin/env python3

import numpy as np
from scipy.ndimage.filters import gaussian_filter

import matplotlib.pyplot as plt
from matplotlib import animation
import random

from panim.animator import (
    AbstractImageAnimator,
    AbstractImageAnimator3,
    AbstractAnimator
)
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

class GenerativeArt2(AbstractImageAnimator):
    def __init__(self, **args):
        super().__init__(**args)

    def update(self, i):
        sigma = 1 if i<100 else i//100
        im = np.random.random((self.image_size[1], self.image_size[0]))
        im = gaussian_filter(im, sigma=sigma)
        im = self.ax.imshow(im, animated=True, cmap='gray')
        self.images.append([im])

class GenerativeArt3(AbstractImageAnimator3):
    def __init__(self, **args):
        super().__init__(**args)

    def update(self, i):
        return np.random.random((self.image_size[1], self.image_size[0]))

class GenerativeArt4(AbstractImageAnimator3):
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
        array = np.sin(self.a * self.p+ np.sin(self.lr * self.q) + self.lr*self.r)
        array = np.fmod((1 + array + self.lr), 1)
        array = get_image_array(array, normalize=False)
        return array


def main():
    animator = GenerativeArt(interval=1, clockwise=False, factor=0.1)
    animator.animate(2000)
    animator.save("out/spiral.mp4")

if __name__ == "__main__":
    main()

