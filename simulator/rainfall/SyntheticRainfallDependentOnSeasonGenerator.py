import numpy as np

from simulator.rainfall.RainfallGenerator import RainfallGenerator
from simulator.util import generate_season_weights


class SyntheticRainfallDependentOnSeasonGenerator(RainfallGenerator):
    def generate(self, n_time_points: int):
        month_index = np.array(range(n_time_points)) % 12 + 1
        season_weights = generate_season_weights()
        rainfall = season_weights[month_index] * 100 + 150  # maybe have some noise later
        rainfall = (rainfall / rainfall.max()) * 4
        return rainfall
