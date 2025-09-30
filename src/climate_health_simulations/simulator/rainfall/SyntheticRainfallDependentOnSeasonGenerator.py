import numpy as np

from climate_health_simulations.simulator.rainfall.RainfallGenerator import RainfallGenerator
from climate_health_simulations.simulator.util import generate_season_weights
from climate_health_simulations.simulator.util import standardize_variable

class SyntheticRainfallDependentOnSeasonGenerator(RainfallGenerator):
    def generate(self, n_time_points_train: int, n_time_points_test: int):
        month_index = np.array(range(n_time_points_train + n_time_points_test)) % 12
        season_weights = generate_season_weights()
        rainfall = season_weights[month_index]  # maybe have some noise later
        scaled_rainfall = standardize_variable(rainfall)
        return scaled_rainfall
