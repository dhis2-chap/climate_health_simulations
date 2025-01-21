from chap_core.data.datasets import ISIMIP_dengue_harmonized

from simulator.temperature.TemperatureGenerator import TemperatureGenerator


class RealisticTemperatureGenerator(TemperatureGenerator):
    def generate(self, n_time_points: int):
        df = ISIMIP_dengue_harmonized['brazil'].to_pandas()
        temperature = df['mean_temperature'].values[:n_time_points]
        temperature = (temperature / temperature.max()) * 4
        return temperature
