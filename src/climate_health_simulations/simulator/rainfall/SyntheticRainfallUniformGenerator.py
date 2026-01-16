import numpy as np
from climate_health_simulations.simulator.rainfall.RainfallGenerator import RainfallGenerator
from climate_health_simulations.simulator.util import standardize_variable


#n_rainfall_train and n_rainfall_test now fall within a defined range
class SyntheticRainfallUniformGenerator(RainfallGenerator):
    def generate(self, n_time_points_train: int, n_time_points_test: int, n_rainfall_train: int,
                 n_rainfall_test: int) -> np.ndarray:

        assert n_rainfall_train <= n_time_points_train, "Number of rainy train points cannot exceed total train points"
        assert n_rainfall_test <= n_time_points_test, "Number of rainy test points cannot exceed total test points"


        n_train_baseline_points = n_time_points_train - n_rainfall_train
        n_test_baseline_points = n_time_points_test - n_rainfall_test
        train_baseline_rain = np.concatenate((np.random.uniform(0, 25, n_train_baseline_points // 2),
                                             np.random.uniform(75, 100,
                                                               n_train_baseline_points - n_train_baseline_points // 2),
                                             np.random.uniform(25,75, n_rainfall_train)), axis=None)
        test_baseline_rain = np.concatenate((np.random.uniform(0, 25, n_test_baseline_points // 2),
                                            np.random.uniform(75, 100,
                                                              n_test_baseline_points - n_test_baseline_points // 2),
                                             np.random.uniform(25,75, n_rainfall_test)), axis=None)
        # shuffle to randomize positions
        np.random.shuffle(train_baseline_rain)
        np.random.shuffle(test_baseline_rain)
        rainfall = np.concatenate((train_baseline_rain, test_baseline_rain), axis=None)
        # scaled_rainfall = standardize_variable(rainfall)
        return rainfall
