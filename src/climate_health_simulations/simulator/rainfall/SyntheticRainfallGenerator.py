import numpy as np
from climate_health_simulations.simulator.rainfall.RainfallGenerator import RainfallGenerator
from climate_health_simulations.simulator.util import standardize_variable

#TODO think about the hacky solution of not allowing rain in the last 3 time points

class SyntheticRainfallGenerator(RainfallGenerator):
    def generate(self, n_time_points_train: int, n_time_points_test: int, n_rainfall_train: int, n_rainfall_test: int) -> np.ndarray:
        total_time_points = n_time_points_train + n_time_points_test
        rainfall = np.zeros(total_time_points)

        # assert
        assert n_rainfall_train <= n_time_points_train-3, "Number of rainy train points cannot exceed total train points"
        assert n_rainfall_test <= n_time_points_test-3, "Number of rainy test points cannot exceed total test points"

        # pick random indices
        train_indices = np.random.choice(n_time_points_train-3, n_rainfall_train, replace=False)
        test_indices = np.random.choice(n_time_points_test-3, n_rainfall_test, replace=False) + n_time_points_train

        # assign rainfall values (e.g., 1 unit)
        rainfall[train_indices] = 1
        rainfall[test_indices] = 1

        scaled_rainfall = standardize_variable(rainfall)

        return scaled_rainfall
