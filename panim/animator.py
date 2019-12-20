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
        self.start_position = args.get('start_position', 0.0)
        self.fig = plt.figure()
        # self.fig.set_size_inches(13.66, 7.68, True)
        w, h = args.get('width', 8), args.get('height', 6)
        self.fig.set_size_inches(w, h, True)
        self.nlimit = args.get('nlimit', 50)
        n = self.nlimit
        self.ax = plt.axes(xlim=(-n, n), ylim=(-n, n))
        line_width = args.get('line_width', 1)
        self.img, = self.ax.plot([], [], lw=line_width)
        if 'title' in args:
            plt.title(args['title'])

    def setup(self, *args):
        pass

    def _f(self, x):
        pass

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
        print("Saving {} to {}".format(self.__class__.__name__, filename))
        self.anim.save(filename, writer=writer, dpi=dpi)

class AbstractImageAnimator(AbstractAnimator):
    def __init__(self, **args):
        self.interval = args.get('interval', 1)
        self.gray = args.get('gray', True)
        self.fig = plt.figure()
        self.image_size = (args.get('width', 800), args.get('height', 600))
        self.wres, self.hres = (args.get('wres', 12), args.get('hres', 9))
        w, h = self.image_size
        self.fig.set_size_inches(self.wres, self.hres, True)
        # self.ax = plt.axes(xlim=(0, w), ylim=(0, h))
        self.ax = plt.axes(xlim=(0, w), ylim=(0, h))

        # self.array = np.zeros((self.image_size[1], self.image_size[0]))
        self.array = np.random.random((self.image_size[1], self.image_size[0]))
        if self.gray:
            self.image = plt.imshow(self.array, animated=True, cmap='gray')
        else:
            self.image = plt.imshow(self.array, animated=True)


    def _animate(self, i):
        print("Frame {}/{}".format(i, self.num_frames))
        array = self.update(i)
        self.image.set_array(array)
        return self.image,



def main():
    # animator = AbstractAnimator() # we cannot initialize this
    animator = AbstractImageAnimator() # we cannot initialize this
    animator.animate(500)
    animator.save("out/random2.mp4", fps=24)

if __name__ == "__main__":
    main()

