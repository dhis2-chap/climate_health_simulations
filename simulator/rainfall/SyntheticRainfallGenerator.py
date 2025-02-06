import numpy as np
from simulator.rainfall.RainfallGenerator import RainfallGenerator


class SyntheticRainfallGenerator(RainfallGenerator):
    def generate(self, n_time_points: int):
        rainfall = np.zeros(n_time_points)
        rainfall[n_time_points // 2] = 4
        return rainfall
