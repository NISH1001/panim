#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib import animation

import numpy as np


plt.style.use('dark_background')
plt.axis('off')

class BoxAnimator:
    def __init__(self, size=5, shrink_factor=0.9):
        self.shrink_factor = shrink_factor
        self.coords = np.array([(-1, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]) * size
        X, Y = zip(*self.coords)
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))

    def _animate(self, i):
        print("Frame number :: {}".format(i))
        X, Y = zip(*self.coords)
        self.img = self.ax.plot(X, Y, c='red')
        self.coords = self.coords * self.shrink_factor
        return []

    def animate(self, num_frames=1000):
        plt.axis('off')
        self.anim = animation.FuncAnimation(self.fig, self._animate,
                               frames=num_frames, interval=5, blit=True,
                               repeat=False)
        # plt.show()

    def save(self, filename="animation.mp4"):
        self.anim.save(filename, writer='imagemagick')


def main():
    animator = BoxAnimator(size=50, shrink_factor=0.95)
    animator.animate(75)
    animator.save("out/box.mp4")

if __name__ == "__main__":
    main()

