#!/usr/bin/env python3

import copy

import numpy as np
import matplotlib.pyplot as plt

from panim.animator import AbstractAnimator
from panim.lsystem import LSystemAnimator

plt.style.use("dark_background")


class Transformer(AbstractAnimator):
    """
        The main transformation base that other will inherit.

        Every class has to implement `transform` method.
        This method takes in frame number and co-orindates (x,y)
        and perform the tnrasformation.

        Gets all the attribute of the provided animator dynamically.
    """

    def __init__(self, **kwargs):
        self.animobj = kwargs["animobj"]
        if "color" in kwargs:
            try:
                self.animobj.__dict__.pop("color")
                self.animobj.__dict__["args"].pop("color")
            except KeyError:
                pass
        kwargs.update(self.animobj.__dict__["args"])
        super().__init__(**kwargs)
        self.__dict__.update(self.animobj.__dict__)
        self.factor = kwargs.get("factor", 1.0)
        self.reset_frame = kwargs.get("reset_frame", 0)
        self.reset_interval = kwargs.get("reset_interval", None)
        # self.reset_interval = kwargs.get("reset_interval", 2500)

    def transform(self, i, X, Y):
        raise NotImplementedError


class ZoomTransformer(Transformer):
    """
        Performs zoom-in/zoom-out transformation by scaling the
        coordinates accorindlgy.
        Exponential scaler is used for smooth zoom.
        If direct single scalar is used, it will look too fast or too slow
        and will have glitches.
    """

    def update(self, i):
        X, Y = self.animobj.update(i)
        return self.transform(i, X, Y)

    def transform(self, i, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        # X = X * self.factor * i
        # Y = Y * self.factor * i

        scale = 1
        if self.reset_interval:
            if i % self.reset_interval == 0:
                self.reset_frame = i
            scale = np.exp((i - self.reset_frame + 300) / self.factor)
        else:
            scale = np.exp(i / self.factor)

        # if i < self.reset_frame:
        #     scale = np.exp(i / self.factor)
        # else:
        #     scale = np.exp((i - self.reset_frame + 200) / self.factor)

        X = X * scale
        Y = Y * scale
        return X.tolist(), Y.tolist()

    def __str__(self):
        return f"~ZoomTransformer~ Scale Factor={self.factor}\n" + str(self.animobj)


class RotationTransformer(Transformer):
    """
        Rotate the coordinates around the origin.
    """

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.rotation_angle = kwargs.get("rotation_angle", 0.0)
    #     theta = self.rotation_angle
    #     self.rot_matrix = self.__get_rot_matrix(theta)

    def __get_rot_matrix(self, theta):
        return np.array(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
        )

    def update(self, i):
        X, Y = self.animobj.update(i)
        return self.transform(i, X, Y)

    def transform(self, i, X, Y):
        X = np.array(X)
        Y = np.array(Y)

        theta = i * self.factor
        points = np.dot(self.__get_rot_matrix(theta), np.vstack([X, Y]))
        # X = X * self.factor * i
        # Y = Y * self.factor * i

        X = points[0, :]
        Y = points[1, :]
        return X.tolist(), Y.tolist()

    def __str__(self):
        return f"~RotationTransformer~ Rotation Angle ={self.factor}\n" + str(
            self.animobj
        )


class TransformerPipeline(Transformer):
    """
        Holds list of transformation objects.
        (x, y) -> T1 -> T2 -> .... (x', y')
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transformers = kwargs.get("transformers", [])

    def add_transformer(self, transformer):
        assert type(transformer) in [
            ZoomTransformer.__name__,
            RotationTransformer.__name__,
        ]
        assert transformer is not None
        self.transformers.append(transformer)

    def update(self, i):
        X, Y = self.transformers[0].update(i)
        for transformer in self.transformers[1:]:
            X, Y = transformer.transform(i, X, Y)
        return X, Y


def main():
    pass


if __name__ == "__main__":
    main()
