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
        # self.fig.set_size_inches(13.66, 7.68, True)
        # self.fig.set_size_inches(8, 6, True)
        self.nlimit = args.get('nlimit', 50)
        n = self.nlimit
        self.ax = plt.axes(xlim=(-n, n), ylim=(-n, n))
        line_width = args.get('line_width', 1)
        self.img, = self.ax.plot([], [], lw=line_width)
        if 'title' in args:
            plt.title(args['title'])

    @abstractmethod
    def update(self, i):
        # Do something and return X, Y
        pass

    def _animate(self, i):
        print("Frame {}/{}".format(i, self.num_frames))
        X, Y = self.update(i)
        self.img.set_data(X, Y)
        return [self.img]

    def animate(self, num_frames=1000):
        self.num_frames = num_frames
        plt.axis('off')
        self.anim = animation.FuncAnimation(self.fig, self._animate,
                               frames=num_frames, interval=self.interval, blit=True,
                               repeat=False)

    def save(self, filename="out/animation.mp4", fps=30, dpi=100):
        writer = animation.writers['ffmpeg'](fps=fps)
        # self.anim.save(filename, writer='imagemagick')
        self.anim.save(filename, writer=writer, dpi=dpi)
        print("Saving {} to {}".format(self.__class__.__name__, filename))


def main():
    animator = AbstractAnimator() # we cannot initialize this

if __name__ == "__main__":
    main()

