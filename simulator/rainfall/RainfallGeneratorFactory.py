from simulator.rainfall.RainfallGenerator import RainfallGenerator
from simulator.rainfall.RealisticRainfallGenerator import RealisticRainfallGenerator
from simulator.rainfall.SyntheticRainfallDependentOnSeasonGenerator import SyntheticRainfallDependentOnSeasonGenerator
from simulator.rainfall.SyntheticRainfallGenerator import SyntheticRainfallGenerator


class RainfallGeneratorFactory:
    def create_generator(self, is_realistic: bool, is_season_dependent: bool) -> RainfallGenerator:
        if is_realistic:
            return RealisticRainfallGenerator()
        elif is_season_dependent:
            return SyntheticRainfallDependentOnSeasonGenerator()
        else:
            return SyntheticRainfallGenerator()
