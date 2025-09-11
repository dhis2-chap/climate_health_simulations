import numpy as np

from climate_health_simulations.simulator.rainfall.RainfallGenerator import RainfallGenerator
from chap_core.data.datasets import ISIMIP_dengue_harmonized

from climate_health_simulations.simulator.util import standardize_variable


class RealisticRainfallGenerator(RainfallGenerator):
    def generate(self, n_time_points_train: int, n_time_points_test: int):
        df = ISIMIP_dengue_harmonized['brazil'].to_pandas()
        total_time_points = n_time_points_train + n_time_points_test
        rainfall = df['rainfall'].values[:total_time_points]
        #rainfall = (rainfall/rainfall.max())*4 #not needed when standardize next line
        scaled_rainfall = standardize_variable(rainfall)
        desired_indices = np.arange(total_time_points) % len(scaled_rainfall)
        scaled_rainfall = scaled_rainfall[desired_indices]
        return scaled_rainfall.flatten()


