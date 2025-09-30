from chap_core.data.datasets import ISIMIP_dengue_harmonized

from climate_health_simulations.simulator.temperature.TemperatureGenerator import TemperatureGenerator
from climate_health_simulations.simulator.util import standardize_variable


class RealisticTemperatureGenerator(TemperatureGenerator):
    def generate(self, n_time_points_train: int, n_time_points_test: int):
        df = ISIMIP_dengue_harmonized['brazil'].to_pandas()
        temperature = df['mean_temperature'].values[:(n_time_points_train + n_time_points_test)]
        scaled_temp = standardize_variable(temperature)
        return scaled_temp
