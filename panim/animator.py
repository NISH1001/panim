#!/usr/bin/env python3

import os

import copy
import time

import matplotlib.pyplot as plt
from matplotlib import animation

from abc import ABCMeta, ABC, abstractmethod
from abc import ABC, abstractmethod

import numpy as np

from loguru import logger

from .utils import IAmTime, create_directory

plt.style.use("dark_background")


class AbstractAnimator(metaclass=ABCMeta):
    def __init__(self, **args):
        self.coords = []
        self.args = args
        self.interval = args.get("interval", 1)
        self.verbose = args.get("verbose", True)
        self.start_position = args.get("start_position", 0.0)
        self.color = args.get("color", (1, 1, 1))
        self.fig = plt.figure()
        # self.fig.set_size_inches(13.66, 7.68, True)
        w, h = args.get("width", 12.80), args.get("height", 7.68)
        self.fig.set_size_inches(w, h, True)
        self.nlimit = args.get("nlimit", 50)
        n = self.nlimit
        self.ax = plt.axes(xlim=(-n, n), ylim=(-n, n))
        # self.ax = plt.axes(xlim=(-w // 2, w // 2), ylim=(-h // 2, h // 2))
        self.line_width = args.get("line_width", 1)
        self.img = self.ax.plot([], [], lw=self.line_width, c=self.color)[0]
        if "title" in args:
            plt.title(args["title"])

    def setup(self, *args):
        pass

    def _f(self, x):
        pass

    @abstractmethod
    def update(self, i):
        """
        Do calculation and return either (X, Y) or a list of (X, Y)
        """
        pass

    def _animate(self, i):
        """
        Internal animation function that calls handles animation
        by calling update()

        If self.img is a single plot() object,
            then update() returns (X, Y) values to be used

        If self.img is a list of several plot(), update() returns a list
            of (X, Y) values
        """
        if self.verbose:
            print("Frame {i}/{self.num_frames}")
        res = self.update(i)
        if type(res) is list:
            for j, img in enumerate(self.img):
                X, Y = res[j]
                self.img[j].set_data(X, Y)
            return self.img
        else:
            (X, Y) = res
            self.img.set_data(X, Y)
            return [self.img]

    def animate(self, num_frames=1000):
        self.num_frames = num_frames
        plt.axis("off")
        self.anim = animation.FuncAnimation(
            self.fig,
            self._animate,
            frames=num_frames,
            interval=self.interval,
            blit=True,
            repeat=False,
        )

    def save(
        self, filename: str = None, prefix: str = "", fps: int = 30, dpi: int = 100
    ):
        start = time.time()
        cname = self.__class__.__name__ if not prefix else prefix

        iat = IAmTime()
        if not filename:
            outdir = self.autogenerate_path()
            filename = f"{cname}-{iat.year}-{iat.month}-{iat.day}--{iat.hour}.{iat.minute}.{iat.second}.mp4"
            if prefix:
                filename = f"{prefix}-{filename}"
            create_directory(outdir)
            filename = os.path.join(outdir, filename)
        else:
            basedir = os.path.dirname(filename)
            if not basedir or not basedir.startswith("out"):
                basedir = "out/"
            create_directory(basedir)

            _, ext = os.path.splitext(filename)
            if ext and ext != ".mp4":
                raise ValueError(f"(filename={filename}). Extension has to be mp4")

            if not ext:
                ext = ".mp4"

            basename, _ = os.path.splitext(os.path.basename(filename))
            fname = f"{cname}-{basename}{ext}"
            filename = os.path.join(basedir, fname)

        # self.anim.save(filename, writer='imagemagick')
        logger.info(f"Saving {cname} to {filename}")
        writer = animation.writers["ffmpeg"](fps=fps)
        self.anim.save(filename, writer=writer, dpi=dpi)
        logger.debug(f"Time Taken = {time.time() - start} seconds")

    def autogenerate_path(self):
        iat = IAmTime()
        basepath = "out/"
        cname = self.__class__.__name__
        timepath = f"{iat.year}--{iat.month}"
        return os.path.join(basepath, cname, timepath)

    def copy(self):
        return copy.copy(self)


class CombinedAnimator(AbstractAnimator):
    """
    A class to hold render multiple animator instances
    """

    def __init__(self, **args):
        super().__init__(**args)
        self.animators = []
        self.img = []
        self.total_coords = 0

    def add_animator(self, animator):
        self.total_coords += len(animator.coords)
        self.animators.append(animator)
        self.img.append(
            self.ax.plot([], [], lw=animator.line_width, c=animator.color)[0]
        )

    def add_animators(self, animators):
        for animator in animators:
            self.add_animator(animator)

    def update(self, i):
        res = []
        for j, animator in enumerate(self.animators):
            X, Y = animator.update(i)
            res.append((X, Y))
        return res


class AbstractImageAnimator(AbstractAnimator):
    def __init__(self, **args):
        self.interval = args.get("interval", 1)
        self.gray = args.get("gray", True)
        self.fig = plt.figure()

        # (w, h)
        self.image_size = (args.get("width", 800), args.get("height", 600))
        self.wres, self.hres = (args.get("wres", 12), args.get("hres", 9))
        w, h = self.image_size
        self.fig.set_size_inches(self.wres, self.hres, True)
        # self.ax = plt.axes(xlim=(0, w), ylim=(0, h))
        self.ax = plt.axes(xlim=(0, w), ylim=(0, h))

        # self.array = np.zeros((self.image_size[1], self.image_size[0]))
        self.array = np.random.random((self.image_size[1], self.image_size[0]))
        if self.gray:
            self.image = plt.imshow(self.array, animated=True, cmap="gray")
        else:
            self.image = plt.imshow(self.array, animated=True)

    def _animate(self, i):
        print(f"Frame {i}/{self.num_frames}")
        array = self.update(i)
        self.image.set_array(array)
        return (self.image,)


def main():
    # animator = AbstractAnimator() # we cannot initialize this
    animator = AbstractImageAnimator()  # we cannot initialize this
    animator.animate(500)
    animator.save("out/random2.mp4", fps=24)


if __name__ == "__main__":
    main()
