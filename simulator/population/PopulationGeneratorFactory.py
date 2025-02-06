from simulator.population.RealisticPopulationGenerator import RealisticPopulationGenerator

from simulator.population.SyntheticPopulationGenerator import SyntheticPopulationGenerator


class PopulationGeneratorFactory:
    def create_generator(self, is_realistic: bool) -> RealisticPopulationGenerator | SyntheticPopulationGenerator:
        if is_realistic:
            return RealisticPopulationGenerator()
        else:
            return SyntheticPopulationGenerator()
