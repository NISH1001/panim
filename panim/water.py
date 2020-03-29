#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from panim.animator import AbstractAnimator


class WaterSimulator(AbstractAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        self.image_size = (args.get("width", 800), args.get("height", 600))
        self.drag = args.get("drag", 0.01)
        self.wres, self.hres = (args.get("wres", 12), args.get("hres", 9))

        w, h = self.image_size
        self.arr1 = np.random.random((h, w))
        self.arr2 = self.arr1.copy()

        self.ax = plt.axes(projection="3d")
        # self.ax.set_xlim3d([-10.0, 10.0])
        # self.ax.set_xlabel("X")

        # self.ax.set_ylim3d([-10.0, 10.0])
        # self.ax.set_ylabel("Y")

        # self.ax.set_zlim3d([0.0, 10.0])
        # self.ax.set_zlabel("Z")

        z = self.arr1
        x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))
        self.image = [self.ax.plot_surface(x, y, z)]

    def _animate(self, i):
        print("Frame {}/{}".format(i, self.num_frames))
        self.arr2 = self.arr1.copy()
        self.arr1 = self.update(i)
        z = self.arr1
        x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))
        self.image[0].remove()
        # self.image[0] = self.ax.plot_wireframe(x, y, z)
        self.image[0] = self.ax.plot_surface(x, y, z)
        return self.image

    def update(self, i):
        n = self.image_size[1]
        for x in range(1, n - 1):
            for y in range(1, n - 1):
                self.arr1[x][y] = (
                    (
                        self.arr2[x - 1][y]
                        + self.arr2[x + 1][y]
                        + self.arr2[x][y - 1]
                        + self.arr2[x][y + 1]
                    )
                    / 2
                ) - self.arr1[x][y]

                self.arr1[x][y] -= self.arr1[x][y] * self.drag
        return self.arr1


# def simulate_water(n):
#     arr1 = np.random.random((n, n))
#     arr2 = arr1.copy()
#     drag = 0.1
#     plt.imshow(arr1)
#     plt.show()
#     for x in range(1, n - 1):
#         for y in range(1, n - 1):
#             print(x, y)
#             arr1[x][y] = (
#                 (arr2[x - 1][y] + arr2[x + 1][y] + arr2[x][y - 1] + arr2[x][y + 1]) / 2
#             ) - arr1[x][y]

#             arr1[x][y] -= arr1[x][y] * drag
#     z = arr1
#     x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection="3d")
#     l = ax.plot_surface(x, y, z)
#     l.set_array(np.array([[1, 2], [1, 2]]))
#     print(l.get_array())
#     print(dir(l))
#     plt.title("z as 3d height map")
#     plt.show()


def main():
    # simulate_water(10)
    pass


if __name__ == "__main__":
    main()
