import numpy as np

from climate_health_simulations.simulator.temperature.TemperatureGenerator import TemperatureGenerator


class SyntheticTemperatureGenerator(TemperatureGenerator):
    def generate(self, n_time_points: int):
        temperature = np.zeros(n_time_points)
        temperature[n_time_points // 2] = 4
        return temperature
