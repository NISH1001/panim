#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

from panim.animator import AbstractAnimator

plt.style.use('dark_background')

class GravityAnimtor(AbstractAnimator):
    def __init__(self, **args):
        super().__init__(**args)
        self.gravity = args.get('gravity', 9.8)

        # pendulum 1
        self.l1 = args.get('l1', 1.0) # length
        self.m1 = args.get('m1', 1.0) # mass
        self.theta1 = args.get('theta1', 120.0) # initial angle
        self.omega1 = args.get('omega1', 0.0) # angular velocity

        # pendulum 2
        self.l2 = args.get('l2', 1.0)
        self.m2 = args.get('m2', 1.0)
        self.theta2 = args.get('theta2', -10.0)
        self.omega2 = args.get('omega2', 0.0)

        # timeline
        dt = args.get('dt', 0.05)
        time_length = args.get('time_length', 10)
        self.t = np.arange(0, 60, dt)
        self.setup()

    def setup(self):
        # initial state
        self.state = np.radians([self.theta1, self.omega1, self.theta2, self.omega2])
        y = integrate.odeint(self.derivatives, self.state, self.t)
        self.x1 = self.l1*np.sin(y[:, 0])
        self.y1 = -self.l1*np.cos(y[:, 0])

        self.x2 = self.l2*np.sin(y[:, 2]) + self.x1
        self.y2 = -self.l2*np.cos(y[:, 2]) + self.y1


    def derivatives(self, state, t):
        dydx = np.zeros_like(state)
        dydx[0] = state[1]

        M1, M2, L1, L2, G = self.m1, self.m2, self.l1, self.l2, self.gravity
        sin, cos = np.sin, np.cos
        delta = state[2] - state[0]
        den1 = (M1+M2) * L1 - M2 * L1 * cos(delta) * cos(delta)
        dydx[1] = ((M2 * L1 * state[1] * state[1] * sin(delta) * cos(delta)
                    + M2 * G * sin(state[2]) * cos(delta)
                    + M2 * L2 * state[3] * state[3] * sin(delta)
                    - (M1+M2) * G * sin(state[0]))
                / den1)

        dydx[2] = state[3]

        den2 = (L2/L1) * den1
        dydx[3] = ((- M2 * L2 * state[3] * state[3] * sin(delta) * cos(delta)
                    + (M1+M2) * G * sin(state[0]) * cos(delta)
                    - (M1+M2) * L1 * state[1] * state[1] * sin(delta)
                    - (M1+M2) * G * sin(state[2]))
                / den2)

        return dydx

    def update(self, i):
        x = [0, self.x1[i], self.x2[i]]
        y = [0, self.y1[i], self.y2[i]]
        return x, y


def main():
    pass

if __name__ == "__main__":
    main()

