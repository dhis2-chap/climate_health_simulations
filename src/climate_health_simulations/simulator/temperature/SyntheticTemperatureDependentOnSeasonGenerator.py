import numpy as np
from climate_health_simulations.simulator.temperature.TemperatureGenerator import TemperatureGenerator
from climate_health_simulations.simulator.util import generate_season_weights


class SyntheticTemperatureDependentOnSeasonGenerator(TemperatureGenerator):
    def generate(self, n_time_points_train: int, n_time_points_test: int):
        month_index = np.array(range(n_time_points_train + n_time_points_train)) % 12
        season_weights = generate_season_weights()
        temperature = season_weights[month_index] * 100 + 150  # maybe have some noise later
        return temperature
