#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from panim.animator import AbstractImageAnimator
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


def main():
    animator = GenerativeArt(interval=1, clockwise=False, factor=0.1)
    animator.animate(2000)
    animator.save("out/spiral.mp4")

if __name__ == "__main__":
    main()

