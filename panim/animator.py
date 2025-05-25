#!/usr/bin/env python3
"""
This module contains the base Animator class and related components for creating animations.
It provides the core functionality for managing animation loops, rendering frames, and saving animations.
"""

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
    """
    Base class for all animators in the panim library.

    This class is responsible for managing the animation loop, rendering frames,
    and saving animations. Key methods include `animate` for running the animation
    and `save` for saving the output. Subclasses should implement the `update`
    method to define the animation logic for each frame.
    """
    def __init__(self, **args):
        """
        Initializes the AbstractAnimator.

        Args:
            interval (int, optional): Interval between frames in milliseconds. Defaults to 1.
            verbose (bool, optional): Whether to print frame numbers during animation. Defaults to True.
            start_position (float, optional): Starting position for some coordinate calculations. Defaults to 0.0.
            color (tuple, optional): Default color for plotted lines. Defaults to (1, 1, 1) (white).
            width (float, optional): Width of the animation figure in inches. Defaults to 12.80.
            height (float, optional): Height of the animation figure in inches. Defaults to 7.68.
            nlimit (int, optional): Axis limit for x and y axes (e.g., -nlimit to nlimit). Defaults to 50.
            line_width (int, optional): Default line width for plots. Defaults to 1.
            title (str, optional): Title of the animation plot. Defaults to None.
        """
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
        """
        Optional setup method for subclasses to perform initial configurations.
        This method is called before the animation loop starts.
        """
        pass

    def _f(self, x):
        """Placeholder method, potentially for mathematical functions in subclasses."""
        pass

    @abstractmethod
    def update(self, i: int):
    def update(self, i: int):
        """
        Abstract method to be implemented by subclasses.

        This method should perform calculations for the current frame and return
        the data needed to draw the frame. The return type can be a tuple (X, Y)
        for a single plot or a list of (X, Y) tuples for multiple plots.

        Args:
            i (int): The current frame number.
        """
        pass

    def _animate(self, i: int):
        """
        Internal animation function that handles animation by calling update().

        This method is called by `matplotlib.animation.FuncAnimation` for each frame.
        It calls the `update()` method of the subclass and then sets the data
        for the plot(s).

        If self.img is a single plot() object, then update() returns (X, Y) values.
        If self.img is a list of several plot() objects, update() returns a list of (X, Y) values.

        Args:
            i (int): The current frame number.

        Returns:
            list: A list of artists to be redrawn for the current frame.
        """
        if self.verbose:
            print(f"Frame {i}/{self.num_frames}")
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

    def animate(self, num_frames: int = 1000, fps: int = None, timespan: int = None):
        """
        Runs the main animation loop.

        This method sets up and starts the animation using `matplotlib.animation.FuncAnimation`.
        It calls `_animate` for each frame.

        Args:
            num_frames (int, optional): The total number of frames to render if `fps` and `timespan` are not specified.
                                       Defaults to 1000.
            fps (int, optional): The desired frames per second for the animation. If specified along with `timespan`,
                                 `num_frames` will be calculated as `fps * timespan`. Defaults to None.
            timespan (int, optional): The desired total duration of the animation in seconds. If specified along
                                      with `fps`, `num_frames` will be calculated. Defaults to None.
        """
        self.fps = fps
        self.timespan = timespan
        if fps is not None and timespan is not None and timespan > 0 and fps > 0:
            self.num_frames = fps * timespan
            logger.info(f"Animating for {timespan} seconds")
        else:
            self.num_frames = num_frames
        plt.axis("off")
        self.anim = animation.FuncAnimation(
            self.fig,
            self._animate,
            frames=self.num_frames,
            interval=self.interval,
            blit=True,
            repeat=False,
        )

    def save(
        self, filename: str = None, prefix: str = "", fps: int = 30, dpi: int = 100
    ):
        """
        Saves the rendered animation to a file (e.g., MP4).

        The filename can be specified, or it will be auto-generated based on the
        animator class name, prefix, and current timestamp.

        Args:
            filename (str, optional): The desired output filename (including path).
                                      If None, a filename is auto-generated in the 'out/' directory.
                                      Defaults to None.
            prefix (str, optional): A prefix to be added to the auto-generated filename.
                                    Defaults to "".
            fps (int, optional): Frames per second for the output video.
                                 If `self.fps` was set during `animate()`, that value is used.
                                 Defaults to 30.
            dpi (int, optional): Dots per inch for the output video. Defaults to 100.

        Raises:
            ValueError: If the specified filename has an extension other than ".mp4".
        """
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
        if self.fps is not None and self.fps > 0:
            fps = self.fps
        writer = animation.writers["ffmpeg"](fps=fps)
        self.anim.save(filename, writer=writer, dpi=dpi)
        logger.debug(f"Time Taken = {time.time() - start} seconds")

    def autogenerate_path(self) -> str:
        """
        Generates a default output path for saving animations.

        The path is structured as 'out/<ClassName>/<Year>--<Month>/'.

        Returns:
            str: The auto-generated directory path.
        """
        iat = IAmTime()
        basepath = "out/"
        cname = self.__class__.__name__
        timepath = f"{iat.year}--{iat.month}"
        return os.path.join(basepath, cname, timepath)

    def copy(self):
        """
        Creates a shallow copy of the animator instance.

        Returns:
            AbstractAnimator: A shallow copy of the animator.
        """
        return copy.copy(self)


class CombinedAnimator(AbstractAnimator):
    """
    A class to hold and render multiple animator instances simultaneously.

    This animator takes other animator instances and plays them together in the
    same figure. It manages the updates for each individual animator.
    """

    def __init__(self, **args):
        """
        Initializes the CombinedAnimator.

        Args:
            **args: Arbitrary keyword arguments passed to the parent `AbstractAnimator`.
        """
        super().__init__(**args)
        self.animators = []
        self.img = []
        self.total_coords = 0

    def add_animator(self, animator: AbstractAnimator):
        """
        Adds an individual animator to this CombinedAnimator.

        Args:
            animator (AbstractAnimator): The animator instance to add.
        """
        self.total_coords += len(animator.coords)
        self.animators.append(animator)
        self.img.append(
            self.ax.plot([], [], lw=animator.line_width, c=animator.color)[0]
        )

    def add_animators(self, animators: list[AbstractAnimator]):
        """
        Adds a list of animator instances to this CombinedAnimator.

        Args:
            animators (list[AbstractAnimator]): A list of animator instances to add.
        """
        for animator in animators:
            self.add_animator(animator)

    def update(self, i: int) -> list[tuple]:
        """
        Updates all contained animators for the current frame.

        This method calls the `update` method of each animator added to this
        CombinedAnimator and collects their results.

        Args:
            i (int): The current frame number.

        Returns:
            list[tuple]: A list of (X, Y) data tuples, one for each animator.
        """
        res = []
        for j, animator in enumerate(self.animators):
            X, Y = animator.update(i)
            res.append((X, Y))
        return res


class AbstractImageAnimator(AbstractAnimator):
    """
    An animator class specialized for creating animations from image data (numpy arrays).

    This class manages the display and update of images, often used for
    visualizing simulations or cellular automata where the state is represented
    as a 2D array.
    """
    def __init__(self, **args):
        """
        Initializes the AbstractImageAnimator.

        Args:
            interval (int, optional): Interval between frames in milliseconds. Defaults to 1.
            gray (bool, optional): Whether to display the image in grayscale. Defaults to True.
            width (int, optional): Width of the image in pixels. Defaults to 800.
            height (int, optional): Height of the image in pixels. Defaults to 600.
            wres (int, optional): Width resolution for the figure display. Defaults to 12.
            hres (int, optional): Height resolution for the figure display. Defaults to 9.
            **args: Additional keyword arguments passed to `AbstractAnimator` (though AbstractAnimator.__init__ is not called directly here).
        """
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

    def _animate(self, i: int) -> tuple:
        """
        Internal animation function for image-based animations.

        This method is called by `matplotlib.animation.FuncAnimation` for each frame.
        It calls the `update()` method (which should be implemented by a subclass
        to return a numpy array) and then sets this array as the data for the image.

        Args:
            i (int): The current frame number.

        Returns:
            tuple: A tuple containing the image artist to be redrawn.
        """
        print(f"Frame {i}/{self.num_frames}")
        array = self.update(i) # Assumes update() is implemented by a subclass of AbstractImageAnimator
        self.image.set_array(array)
        return (self.image,)


def main():
    """
    Main function to demonstrate example usage of the animator classes.

    Note: This function currently attempts to instantiate abstract classes
    which will result in an error. It serves as a placeholder for example code.
    """
    # animator = AbstractAnimator() # we cannot initialize this
    animator = AbstractImageAnimator()  # we cannot initialize this
    animator.animate(500)
    animator.save("out/random2.mp4", fps=24)


if __name__ == "__main__":
    main()
