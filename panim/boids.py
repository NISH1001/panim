#!/usr/bin/env python3


import sys
from pathlib import Path
import random

path = str(Path().absolute())
print("Adding {} to system path...".format(path))
sys.path.insert(0, path)

import matplotlib.pyplot as plt
from matplotlib import animation

from abc import ABCMeta, ABC, abstractmethod
from abc import ABC, abstractmethod


import numpy as np

from loguru import logger

from panim.animator import AbstractAnimator, AbstractImageAnimator

from panim.spiral import SpiralAnimator

plt.style.use("dark_background")


class Circles(AbstractImageAnimator):
    def __init__(self, nballs=5, **kwargs):
        super().__init__(**kwargs)
        self.nballs = nballs
        self.balls = np.zeros(
            nballs,
            dtype=[
                ("center", float, 2),
                ("radius", float, 1),
                ("direction", float, 2),
            ],
        )

        # image_size = (w, h)
        # random x
        self.balls["center"][:, 0] = np.random.uniform(0, self.image_size[0], (nballs,))
        # random y
        self.balls["center"][:, 1] = np.random.uniform(0, self.image_size[1], (nballs,))

        # velocity
        # self.balls["direction"] = self._generate_direction_random(self.balls["center"])
        self.balls["direction"] = self._generate_direction_com(self.balls["center"])

        r = np.mean(self.image_size) // 13
        logger.info(f"Max radius = {r}")
        # self.balls["radius"] = np.random.randint(5, r, (nballs,))
        self.balls["radius"] = np.ones((nballs,)) * 2
        self.array = np.zeros((self.image_size[1], self.image_size[0]))

        # grid points
        self.grid = np.zeros((self.image_size[1], self.image_size[0], 2))
        for px in range(self.image_size[0]):
            for py in range(self.image_size[1]):
                self.grid[py][px] = px, py

        self.prev_com = self.compute_com(self.balls["center"])

    def _generate_direction_random(self, centers):
        nballs = len(centers)
        assert nballs == self.nballs
        vectors = np.random.choice([-1, 0.5, 1], (nballs, 2)) * 2.5
        return self.compute_unit_vectors(vectors)

    def compute_com(self, centers):
        return np.mean(centers, axis=0)

    def _generate_direction_com(self, centers):
        """
        Cohesive property
        Generate direction/velocity towards center of mass
        """
        nballs = len(centers)
        assert nballs == self.nballs
        # mean (x, y)
        com = np.mean(centers, axis=0)
        vectors = com - centers
        return self.compute_unit_vectors(vectors)
        return vectors

    def compute_unit_vectors(self, vectors):
        xs = vectors[:, 0] ** 2
        ys = vectors[:, 1] ** 2
        sqs = vectors ** 2
        mag = np.sum(sqs, 1) ** 0.5
        vectors[:, 0] /= mag
        vectors[:, 1] /= mag
        return vectors

    def _generate_circular_points(self, center, radius, npoints=10):
        """
        Generate npoints on the circle's circumference
        """
        theta = np.random.uniform(0, 2 * np.pi, npoints)
        x = (radius * np.cos(theta) + center[0]).astype(int)
        y = (radius * np.sin(theta) + center[1]).astype(int)
        return x, y

    def _generate_all_points_within(self, center, radius, npoints=10):
        """
        Generate points within + on the circle
        """
        radii = np.linspace(0.1, radius, 10)
        xs, ys = [], []
        for r in radii:
            _x, _y = self._generate_circular_points(center, r, npoints)
            xs.extend(_x)
            ys.extend(_y)
        return xs, ys

    def update(self, i):
        arr = np.zeros_like(self.array)
        nr, nc = arr.shape
        # xs = np.arange(0, nc, 1)
        # ys = np.arange(0, nr, 1)

        # # generate circle
        # TODO: Create separate animation element for simple circle
        # TODO: Detect collision between circl;
        for rad, cent in zip(self.balls["radius"], self.balls["center"]):
            # generate points
            x, y = self._generate_circular_points(cent, rad, npoints=20)
            # x, y = self._generate_all_points_within(cent, rad, npoints=15)
            x = np.clip(x, a_min=0, a_max=nc - 1)
            y = np.clip(y, a_min=0, a_max=nr - 1)
            arr[y, x] = 255

        # update position based on velocity
        self.balls["center"] += self.balls["direction"]

        # check for collision with edges
        for i, (center, radius, direction) in enumerate(
            zip(self.balls["center"], self.balls["radius"], self.balls["direction"])
        ):
            # x > width, reset direction to be -ve
            if center[0] > nc - radius:
                direction[0] *= np.random.uniform(-1, -0.5, (1,))
                center[0] = nc - radius

            # y > height, reset direction to be -ve
            if center[1] > nr - radius:
                direction[1] *= np.random.uniform(-1, -0.5, (1,))
                center[1] = nr - radius

            # x < 0, set direction +ve
            if center[0] - radius < 0:
                # direction[0] *= np.random.uniform(0.5, 1, (1,))
                direction[0] *= np.random.uniform(-1, -0.5, (1,))
                center[0] = radius

            # y < 0, set direction +ve
            if center[1] - radius < 0:
                # direction[1] *= np.random.uniform(0.5, 1, (1,))
                direction[1] *= np.random.uniform(-1, -0.5, (1,))
                center[1] = radius

            self.balls["direction"][i] = direction
            self.balls["center"][i] = center

        self.balls["direction"] = self._generate_direction_com(self.balls["center"])
        pcom = self.prev_com
        self.prev_com = self.compute_com(self.balls["center"])
        diff = self.prev_com - pcom
        tol = 0.05
        if np.sum(np.isclose(diff, [tol, tol], atol=tol)) == 2:
            # self.balls["direction"] *= -5
            self.balls["direction"] = (
                self._generate_direction_random(self.balls["center"]) * 10
            )
            self.balls["center"] += self.balls["direction"]

        return arr

    def __str__(self):
        return f"(nballs={self.nballs}), (image_size={self.image_size})"


def main():
    animator = Circles(nballs=20, width=200, height=200)
    logger.info(animator)
    animator.animate(500)
    animator.save(filename="out/", fps=16)


if __name__ == "__main__":
    main()
