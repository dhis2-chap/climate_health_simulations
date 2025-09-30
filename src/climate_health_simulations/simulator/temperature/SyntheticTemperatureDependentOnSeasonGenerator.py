import numpy as np
from gluonts.ev.stats import scaled_interval_score

from climate_health_simulations.simulator.temperature.TemperatureGenerator import TemperatureGenerator
from climate_health_simulations.simulator.util import generate_season_weights
from climate_health_simulations.simulator.util import standardize_variable

class SyntheticTemperatureDependentOnSeasonGenerator(TemperatureGenerator):
    def generate(self, n_time_points_train: int, n_time_points_test: int):
        month_index = np.array(range(n_time_points_train + n_time_points_train)) % 12
        season_weights = generate_season_weights()
        temperature = season_weights[month_index]
        scaled_temp = standardize_variable(temperature)
        return scaled_temp
