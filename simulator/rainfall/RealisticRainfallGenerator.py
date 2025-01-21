from simulator.rainfall.RainfallGenerator import RainfallGenerator
from chap_core.data.datasets import ISIMIP_dengue_harmonized


class RealisticRainfallGenerator(RainfallGenerator):
    def generate(self, n_time_points: int):
        df = ISIMIP_dengue_harmonized['brazil'].to_pandas()
        rainfall = df['rainfall'].values[:n_time_points]
        rainfall = (rainfall/rainfall.max())*4
        return rainfall


