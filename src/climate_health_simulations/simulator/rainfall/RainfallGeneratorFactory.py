from climate_health_simulations.simulator.rainfall.RainfallGenerator import RainfallGenerator
from climate_health_simulations.simulator.rainfall.RealisticRainfallGenerator import RealisticRainfallGenerator
from climate_health_simulations.simulator.rainfall.SyntheticRainfallDependentOnSeasonGenerator import SyntheticRainfallDependentOnSeasonGenerator
from climate_health_simulations.simulator.rainfall.SyntheticRainfallGenerator import SyntheticRainfallGenerator
from climate_health_simulations.simulator.rainfall.SyntheticRainfallUniformGenerator import \
    SyntheticRainfallUniformGenerator


class RainfallGeneratorFactory:
    def create_generator(self, is_realistic: bool, is_season_dependent: bool, is_uniform: bool) -> RainfallGenerator:
        if is_uniform:
            return SyntheticRainfallUniformGenerator()
        elif is_realistic:
            return RealisticRainfallGenerator()
        elif is_season_dependent:
            return SyntheticRainfallDependentOnSeasonGenerator()
        else:
            return SyntheticRainfallGenerator()
