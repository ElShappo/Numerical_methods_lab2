import numpy as np
from constants import a


def pulse(x, t):
    if a * t <= x <= a * t + 1:
        return 1
    return 0


def bell(x, t):
    if a * t < x < a * t + 1:
        x0 = 0.5 + a * t
        return np.exp(-(x - x0) ** 2 / (0.25 - (x - x0) ** 2))
    return 0


def parabola(x, t):
    x0 = 1 + a * t
    if x0 - 1 <= x <= x0 + 1:
        return 1 - (x - x0) ** 2
    return 0


def sine(x, t):
    x0 = 1 + a * t
    if x0 - 1 <= x <= x0 + 1:
        return (np.cos(np.pi / 2 * np.abs(x - x0))) ** 3
    return 0
