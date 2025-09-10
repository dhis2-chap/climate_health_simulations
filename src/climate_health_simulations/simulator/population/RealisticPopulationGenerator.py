from chap_core.data.datasets import ISIMIP_dengue_harmonized


class RealisticPopulationGenerator:
    def generate(self, n_time_points: int, population: int = None):
        df = ISIMIP_dengue_harmonized['brazil'].to_pandas()
        population = df['population'].values[:n_time_points]
        return population
