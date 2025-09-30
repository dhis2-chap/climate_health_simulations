import numpy as np
from climate_health_simulations.simulator.rainfall.RainfallGenerator import RainfallGenerator
from climate_health_simulations.simulator.util import standardize_variable

#TODO alter so a flexible number of points are rainy, not hust 25%
class SyntheticRainfallGenerator(RainfallGenerator):
    def generate(self, n_time_points_train: int, n_time_points_test: int):
        total_time_points = n_time_points_train + n_time_points_test
        rainfall = np.zeros(total_time_points)

        # number of rainy days (train/test)
        rainy_days_train = max(1, n_time_points_train // 4)
        rainy_days_test = max(1, n_time_points_test // 4)

        # pick random indices
        train_indices = np.random.choice(n_time_points_train, rainy_days_train, replace=False)
        test_indices = np.random.choice(n_time_points_test, rainy_days_test, replace=False) + n_time_points_train

        # assign rainfall values (e.g., 1 unit)
        rainfall[train_indices] = 1
        rainfall[test_indices] = 1

        scaled_rainfall = standardize_variable(rainfall)

        return scaled_rainfall
