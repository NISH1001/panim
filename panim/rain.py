#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from panim.animator import AbstractAnimator

plt.style.use("dark_background")


class RainAnimator:
    """
    I directly copied (and modified this code from Matplotlib's official documentation).
    So yeah! I haven't been able to hook up AbstractAnimator here since that used plt.plot.
    Here, it requires scatter plot.
    """

    def __init__(self, **args):
        # super().__init__(**args)
        ndrops = args.get("ndrops", 50)
        self.interval = args.get("interval", 10)
        # Create new Figure and an Axes which fills it.
        self.fig = plt.figure(figsize=(13, 7))
        self.ax = self.fig.add_axes([0, 0, 1, 1], frameon=False)
        self.ax.set_xlim(0, 1), self.ax.set_xticks([])
        self.ax.set_ylim(0, 1), self.ax.set_yticks([])
        self.ndrops = ndrops
        self.drops = np.zeros(
            ndrops,
            dtype=[
                ("position", float, 2),
                ("size", float, 1),
                ("growth", float, 1),
                ("color", float, 4),
            ],
        )
        self.drops["position"] = np.random.uniform(0, 1, (ndrops, 2))
        self.drops["growth"] = np.random.uniform(1, 10, ndrops)
        self.img = self.ax.scatter(
            self.drops["position"][:, 0],
            self.drops["position"][:, 1],
            s=self.drops["size"],
            lw=0.5,
            edgecolors=self.drops["color"],
            facecolors="none",
        )

    def update(self, i):
        # Get an index which we can use to re-spawn the oldest raindrop.
        print(i)
        current_index = i % self.ndrops

        # Make all colors more transparent as time progresses.
        self.drops["color"][:, 3] -= 1.0 / len(self.drops)
        self.drops["color"][:, 3] = np.clip(self.drops["color"][:, 3], 0, 1)

        # Make all circles bigger.
        self.drops["size"] += self.drops["growth"]

        # Pick a new position for oldest rain drop, resetting its size,
        # color and growth factor.
        self.drops["position"][current_index] = np.random.uniform(0, 1, 2)
        self.drops["size"][current_index] = 5
        self.drops["color"][current_index] = (0, 1, 1, 1)
        self.drops["growth"][current_index] = np.random.uniform(50, 200)

        # Update the scatter collection, with the new colors, sizes and positions.
        self.img.set_edgecolors(self.drops["color"])
        self.img.set_sizes(self.drops["size"])
        self.img.set_offsets(self.drops["position"])

    def animate(self, num_frames=1000):
        self.num_frames = num_frames
        plt.axis("off")
        self.anim = animation.FuncAnimation(
            self.fig,
            self.update,
            frames=num_frames,
            interval=self.interval,
            blit=False,
            repeat=False,
        )

    def save(self, filename="out/animation.mp4", fps=30, dpi=100):
        writer = animation.writers["ffmpeg"](fps=fps)
        # self.anim.save(filename, writer='imagemagick')
        self.anim.save(filename, writer=writer, dpi=dpi)
        print("Saving {} to {}".format(self.__class__.__name__, filename))


def main():
    pass


if __name__ == "__main__":
    main()
