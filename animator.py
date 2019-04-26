#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib import animation

from abc import ABCMeta, ABC, abstractmethod
from abc import ABC, abstractmethod

import numpy as np

plt.style.use('dark_background')

class AbstractAnimator(metaclass=ABCMeta):
    def __init__(self, **args):
        self.coords = []
        self.args = args
        self.interval = args.get('interval', 1)
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
        self.img, = self.ax.plot([], [], lw=2)

    @abstractmethod
    def _update(self, i):
        # Do something and return X, Y
        pass

    def _animate(self, i):
        print("Frame number :: {}".format(i))
        X, Y = self._update(i)
        self.img.set_data(X, Y)
        return [self.img]

    def animate(self, num_frames=1000):
        plt.axis('off')
        self.anim = animation.FuncAnimation(self.fig, self._animate,
                               frames=num_frames, interval=self.interval, blit=True,
                               repeat=False)

    def save(self, filename="out/animation.mp4"):
        self.anim.save(filename, writer='imagemagick')


def main():
    animator = AbstractAnimator() # we cannot initialize this

if __name__ == "__main__":
    main()

