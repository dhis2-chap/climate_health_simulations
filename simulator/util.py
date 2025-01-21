import numpy as np


def generate_season_weights():  # maybe this has to be revisited at a later time point
    x = np.array(range(12))
    y = np.sin(x / 12 * 2 * np.pi)
    return y