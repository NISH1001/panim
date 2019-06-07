#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from panim.animator import AbstractAnimator

plt.style.use('dark_background')

class ExponentialDecay(AbstractAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        self.factor = 0.01

    def update(self, i):
        t = self.factor * i

        # x, y values to be plotted
        x, y = t-self.nlimit, 25*np.sin(2*np.pi*t) * np.exp(-t/20.)
        # y = 0

        self.coords.append((x, y))
        X, Y = zip(*self.coords)
        return X, Y



def main():
    pass

if __name__ == "__main__":
    main()

