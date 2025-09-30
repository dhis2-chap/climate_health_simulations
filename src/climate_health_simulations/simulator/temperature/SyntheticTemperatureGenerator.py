import numpy as np

from climate_health_simulations.simulator.temperature.TemperatureGenerator import TemperatureGenerator
from climate_health_simulations.simulator.util import standardize_variable

class SyntheticTemperatureGenerator(TemperatureGenerator):
    def generate(self, n_time_points_train: int, n_time_points_test: int):
        total_time_points = n_time_points_train + n_time_points_test
        temperature = np.zeros(total_time_points)

        # number of rainy days (train/test)
        warm_days_train = max(1, n_time_points_train // 4)
        warm_days_test = max(1, n_time_points_test // 4)

        # pick random indices
        train_indices = np.random.choice(n_time_points_train, warm_days_train, replace=False)
        test_indices = np.random.choice(n_time_points_test, warm_days_test, replace=False) + n_time_points_train

        # assign rainfall values (e.g., 1 unit)
        temperature[train_indices] = 1
        temperature[test_indices] = 1

        scaled_temp = standardize_variable(temperature)

        return scaled_temp
