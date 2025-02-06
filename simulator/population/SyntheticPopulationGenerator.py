import numpy as np

from simulator.population.PopulationGenerator import PopulationGenerator


class SyntheticPopulationGenerator(PopulationGenerator):
    def generate(self, n_time_points: int, population: int = None):
        return np.ones(n_time_points) * population
