#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from panim.animator import AbstractAnimator
from panim.lsystem import LSystemAnimator

plt.style.use("dark_background")


class ZoomTransformer(AbstractAnimator):
    """
        Transform an animator object.
        Gets all the attribute of the provided animator dynamically
        and performs zoom-in/zoom-out transformation by scaling the
        coordinates
    """

    def __init__(self, **args):
        self.animobj = args["animobj"]
        if "color" in args:
            self.animobj.__dict__.pop("color")
            self.animobj.__dict__["args"].pop("color")
        args.update(self.animobj.__dict__["args"])
        super().__init__(**args)
        self.__dict__.update(self.animobj.__dict__)
        self.factor = args.get("factor", 1.0)
        self.reset_frame = args.get("reset_frame", 0)
        self.reset_interval = args.get("reset_interval", 2500)

    def update(self, i):
        X, Y = self.animobj.update(i)
        X = np.array(X)
        Y = np.array(Y)
        # X = X * self.factor * i
        # Y = Y * self.factor * i

        if i % self.reset_interval == 0:
            self.reset_frame = i

        scale = np.exp((i - self.reset_frame + 300) / self.factor)

        # if i < self.reset_frame:
        #     scale = np.exp(i / self.factor)
        # else:
        #     scale = np.exp((i - self.reset_frame + 200) / self.factor)

        X = X * scale
        Y = Y * scale
        return X.tolist(), Y.tolist()

    def __str__(self):
        return f"~ZoomTransformer~ Scale Factor={self.factor}\n" + str(self.animobj)


def main():
    pass


if __name__ == "__main__":
    main()
