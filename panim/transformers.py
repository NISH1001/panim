#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from panim.animator import AbstractAnimator
from panim.lsystem import LSystemAnimator

plt.style.use('dark_background')

class ZoomTransformer(AbstractAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        self.animobj = args['animobj']
        self.factor = args.get('factor', 1.0)

    def update(self, i):
        X, Y = self.animobj.update(i)
        X = np.array(X)
        Y = np.array(Y)
        # X = X * self.factor * i
        # Y = Y * self.factor * i
        X = X * np.exp(1/self.factor * i)
        Y = Y * np.exp(1/self.factor * i)
        return X.tolist(), Y.tolist()

def main():
    pass

if __name__ == "__main__":
    main()

