from climate_health_simulations.simulator.temperature.RealisticTemperatureGenerator import RealisticTemperatureGenerator
from climate_health_simulations.simulator.temperature.SyntheticTemperatureDependentOnSeasonGenerator import \
    SyntheticTemperatureDependentOnSeasonGenerator
from climate_health_simulations.simulator.temperature.SyntheticTemperatureGenerator import SyntheticTemperatureGenerator
from climate_health_simulations.simulator.temperature.TemperatureGenerator import TemperatureGenerator


class TemperatureGeneratorFactory:
    def create_generator(self, is_realistic: bool, is_season_dependent: bool) -> TemperatureGenerator:
        if is_realistic:
            return RealisticTemperatureGenerator()
        elif is_season_dependent:
            return SyntheticTemperatureDependentOnSeasonGenerator()
        else:
            return SyntheticTemperatureGenerator()
